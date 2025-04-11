import json
from datetime import datetime, timedelta

# Nome dos arquivos
arquivo_entrada = 'raw-aqw.json'
arquivo_saida = 'aqw.json'

# Boosts principais (48h ou 72h)
boost_keys = [
    "Double Rep", "Double Class Point", "Double EXP", "Double Gold", "Double ALL"
]

# Boosts de recursos (1 semana = 8 dias)
resource_keys = [
    "Essences + Totems", "Blood Gems", "Dark Spirt Orbs",
    "Spirit Orbs + Metals Boost", "Void Aura Boost", "Celestial Dungeon Boost",
    "Legion Token + Rib Boost", "Unidentified 34 & 35 Boost"
]

# Todas as keywords válidas
keywords = boost_keys + resource_keys

# Descrições padrão (48h)
descriptions_48h = {
    "Double EXP": "Experiência (EXP) EM DOBRO por 48 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com.",
    "Double Gold": "Ouro (gold) EM DOBRO por 48 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com.",
    "Double Class Point": "Pontos de Classe (class point) EM DOBRO por 48 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com.",
    "Double Rep": "Reputação (reputation) EM DOBRO por 48 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com.",
    "Double ALL": "Ouro (gold), Reputação (rep), Experiência (exp) e Pontos de Classe (class point) EM DOBRO por 48 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com."
}

# Descrições para sextas-feiras (72h)
descriptions_72h = {
    "Double EXP": "Experiência (EXP) EM DOBRO por 72 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com.",
    "Double Gold": "Ouro (gold) EM DOBRO por 72 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com.",
    "Double Class Point": "Pontos de Classe (class point) EM DOBRO por 72 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com.",
    "Double Rep": "Reputação (reputation) EM DOBRO por 72 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com.",
    "Double ALL": "Ouro (gold), Reputação (rep), Experiência (exp) e Pontos de Classe (class point) EM DOBRO por 72 horas em todos os servidores do AQWorlds!\nLogue todos os dias para receber uma nova recompensa, aumento ou outro bônus em AQ.com."
}

# Lê o arquivo JSON externo
with open(arquivo_entrada, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Processa apenas os eventos com título que contenha alguma keyword
for item in data:
    title = item["title"]

    if not any(keyword in title for keyword in keywords):
        continue  # pula o item se não tiver nenhuma das palavras-chave

    start_date = datetime.strptime(item["start"], "%Y-%m-%d")
    is_friday = start_date.weekday() == 4

    # Define a duração com base no tipo
    if "end" not in item:
        for key in boost_keys:
            if key in title:
                days = 3 if is_friday else 2
                break
        else:
            # Se não for boost, assume que é recurso (1 semana)
            days = 7
        end_date = start_date + timedelta(days=days)
        item["end"] = end_date.strftime("%Y-%m-%d")

    # Define a description (se aplicável e ainda não existir)
    if "description" not in item:
        for key in descriptions_48h:
            if key in title:
                item["description"] = descriptions_72h[key] if is_friday else descriptions_48h[key]
                break

# Salva o resultado em um novo arquivo
with open(arquivo_saida, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Arquivo '{arquivo_saida}' salvo com sucesso.")
