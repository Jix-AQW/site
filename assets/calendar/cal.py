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

# Cores para os boosts principais
boost_colors = {
    "Double EXP": "#800080",        # Roxo
    "Double Rep": "#008000",        # Verde
    "Double Gold": "#FFD700",       # Dourado
    "Double Class Point": "#800000",# Bordô
    "Double ALL": "#0000FF"         # Azul (padrão para Double ALL)
}

# Cor padrão para recursos (personalizável)
resource_color = "#964B00"          # Marrom (exemplo)

# Descrições para recursos
resource_descriptions = {
    "Celestial Dungeon Boost": """<strong>Boost de Farming: Drops em Dungeons em Dobro</strong><br><br>
Receba recompensas em dobro enquanto batalha para forjar sua <strong>Greatblade of the Entwined Eclipse</strong>.<br><br>
<strong>Dungeons com Boost Ativo:</strong><br>
<ul>
<li><strong>Temple of the Midnight Sun</strong>:<ul>
<li>2x <strong>Sliver of Sunlight</strong></li>
<li>2x <strong>Hallowed Remains</strong></li>
</ul></li>
<li><strong>Temple of the Solstice Moon</strong>:<ul>
<li>2x <strong>Sliver of Moonlight</strong></li>
<li>2x <strong>Hallowed Remains</strong></li>
</ul></li>
<li><strong>Ascension of the Eclipse</strong>:<ul>
<li>2x <strong>Ecliptic Offering</strong></li>
<li>2x <strong>Hallowed Remains</strong></li>
</ul></li>
</ul>
Faça login diariamente em AQ.com para receber novas recompensas, bônus ou boosts de recursos.""",

    "Essences + Totems Boost": """<strong>Boost de Farming: Essences & Totems em Dobro</strong><br><br>
Receba recompensas em dobro enquanto completa quests para coletar <strong>Essences</strong> e <strong>Totems of Nulgath</strong>.<br><br>
<strong>Essences of Nulgath</strong><br>
Usadas para criar a <strong>Void HighLord Class</strong> + armor set e completar algumas <strong>Quests of Nulgath</strong>.<br><br>
<strong>Totems of Nulgath</strong><br>
Usados na <strong>Diamond Shop</strong> de Nulgath, para criar o set <strong>ArchFiend Warlord</strong> e completar quests específicas de Nulgath.<br><br>
Faça login diariamente em AQ.com para ganhar novas recompensas, bônus ou boosts de recursos.""",

    "Blood Gems Boost": """<strong>Boost de Farming: Blood Gems em Dobro</strong><br><br>
Receba recompensas em dobro enquanto completa quests para coletar <strong>Blood Gems of the Archfiend</strong>.<br><br>
Esses recursos são usados para criar a <strong>Void Highlord Class</strong>, o set <strong>Ancient Shogun</strong>, <strong>Archfiend Warlord</strong> e muitos outros itens.<br><br>
<strong>2x Blood Gems nas seguintes quests:</strong><br>
<ul>
<li>The Perfect Pet</li>
<li>Kiss the Void</li>
<li>Crimson Hanzo Orb Quest</li>
<li>Astral Hanzo Orb Quest</li>
<li>Forge Blood Gems for Nulgath</li>
<li>Carve the Unidentified Gemstone</li>
<li>Eternal Rest</li>
<li>Void Knight Sword Quest</li>
<li>Assisting Oblivion Blade</li>
<li>New Worlds, New Opportunities</li>
<li>Time is Money</li>
<li>Contract Exchange</li>
<li>Drudgen the Salesman</li>
<li>Nulgath's Roulette of Misfortune</li>
<li>Swindle's Return Policy</li>
<li>Bloody Chaos</li>
<li>Dirt-y Deeds Done Dirt Cheap</li>
<li>Swindle's Bonus Deal</li>
</ul>
Faça login diariamente em AQ.com para receber novas recompensas, bônus ou boosts de recursos.""",

    "Spirit Orbs + Metals Boost": """<strong>Boost de Farming: Spirit Orbs + Metals em Dobro</strong><br><br>
Receba recompensas em dobro enquanto batalha para forjar sua <strong>Blinding Light of Destiny Axe</strong>.<br><br>
<strong>Spirit Orb Quests:</strong><br>
<ul>
<li>Essential Essences</li>
<li>Bust Some Dust</li>
</ul>
Recompensas: x10, x20, x30 ou x40 Spirit Orbs (normalmente x5, x10, x15 ou x20)<br><br>
<strong>MineCrafting Metal Quest:</strong><br>
Receba 2x os metais na quest, podendo escolher <strong>x2 Metals</strong> ao invés de x1:<br>
<ul>
<li>Aluminium</li>
<li>Barium</li>
<li>Iron</li>
<li>Gold</li>
<li>Silver</li>
<li>Copper</li>
<li>Platinum</li>
</ul>
Faça login diariamente em AQ.com para receber novas recompensas, bônus ou boosts de recursos.""",

    "Dark Spirit Orbs Boost": """<strong>Boost de Farming: Dark Spirit Orbs em Dobro</strong><br><br>
Ganhe recompensas em dobro enquanto batalha para forjar a <strong>DoomKnight Armor de Sepulchure</strong>.<br><br>
<strong>Dark Spirit Orb Quests:</strong><br>
<ul>
<li>Penny For Your Foughts</li>
<li>Dark Spirit Orbs</li>
</ul>
Recompensas: x10, x20, x30 ou x40 Dark Spirit Orbs (normalmente x5, x10, x15 ou x20)<br><br>
Dark Spirit Orbs são usados para criar a DoomKnight Armor do Sepulchure e outros itens sombrios da Necropolis.<br><br>
Acesse AQ.com todos os dias para receber novas recompensas, bônus ou boosts de farm!""",

    "Void Aura Boost": """<strong>Boost de Farming: Void Auras em Dobro</strong><br><br>
Ganhe recompensas em dobro enquanto batalha para criar a <strong>Necrotic Sword of Doom</strong> até <strong>17 de julho</strong>!<br><br>
<strong>Void Aura Quests:</strong><br>
<ul>
<li>Retrieve Void Auras</li>
<li>Gathering Unstable Essences</li>
<li>Commanding Shadow Essences</li>
</ul>
Recompensas: x10, x12 ou x14 Void Auras (normalmente x5, x6 ou x7)<br><br>
Void Auras são necessárias para forjar partes da Necrotic Sword of Doom e da Necrotic Blade of Doom.<br><br>
Entre diariamente em AQ.com para novas recompensas, bônus ou boosts de recursos!""",

    "Unidentified 34 & 35 Boost": """<strong>Boost de Farming: Unidentified 34 e 35 em Dobro</strong><br><br>
Ganhe recompensas em dobro enquanto coleta recursos para forjar o set <strong>ArchFiend DOOMLord</strong> até o fim do boost!<br><br>
<strong>2x Unidentified 34:</strong><br>
<ul>
<li>Willpower Extraction</li>
<li>Enough DOOM for an ArchFiend</li>
</ul>
Recompensas: x2, x4, x6 ou x8 (normalmente x1, x2, x3 ou x4)<br><br>
<strong>2x Unidentified 35:</strong><br>
<ul>
<li>Nulgath Demands Work</li>
<li>Enough DOOM for an ArchFiend</li>
</ul>
Recompensa: x2 com taxa de drop de 30% (normalmente x1 com 15%)<br><br>
Unidentified 34 e 35 são usados para forjar as armaduras <strong>ArchFiend DOOMLord</strong> e <strong>Warlord</strong>.<br><br>
Entre diariamente em AQ.com para novas recompensas, bônus ou boosts de recursos!""",

    "Legion Token + Rib Boost": """<strong>Boost Duplo: Legion Tokens + Dark Unicorn Rib</strong><br><br>
Ganhe Legion Tokens em dobro em quests selecionadas e 2x Dark Unicorn Ribs ao derrotar o Binky até <strong>25 de dezembro</strong>!<br><br>
<strong>Quests com Boost de Legion Token:</strong><br>
<ul>
<li>Spring Cleaning</li>
<li>First Class Entertainment</li>
<li>Legion Quest: Light vs Dark</li>
<li>Coal for the Legion</li>
<li>Hearts and Souls</li>
<li>Hearts and Souls (Membro)</li>
<li>Legion Castle Quest</li>
<li>Research Materials</li>
<li>Suffering is Magic</li>
</ul>
<strong>Boost de Drop: Dark Unicorn Rib</strong><br>
Derrote o Binky nos mapas /binky ou /doomvault para receber 2x Dark Unicorn Ribs (antes era apenas 1).<br><br>
Entre todos os dias em AQ.com para recompensas, bônus e boosts diários!"""
}


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
# Lê o JSON de entrada
with open(arquivo_entrada, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Processa cada item
for item in data:
    title = item["title"]
    has_keyword = any(keyword in title for keyword in keywords)

    if not has_keyword:
        item["description"] = "Sem detalhes."
        continue  # Pula o restante do processamento

    start_date = datetime.strptime(item["start"], "%Y-%m-%d")
    is_friday = start_date.weekday() == 4

    # Define data de fim
    if "end" not in item:
        for key in boost_keys:
            if key in title:
                days = 3 if is_friday else 2
                break
        else:
            days = 7  # Recursos duram 7 dias
        end_date = start_date + timedelta(days=days)
        item["end"] = end_date.strftime("%Y-%m-%d")

    # Define descrição
    if "description" not in item:
        for key in boost_keys:
            if key in title:
                item["description"] = descriptions_72h[key] if is_friday else descriptions_48h[key]
                break
        else:
            for key in resource_descriptions:
                if key in title:
                    item["description"] = resource_descriptions[key]
                    break

    # Define a cor
    for key in boost_keys:
        if key in title:
            item["color"] = boost_colors.get(key, resource_color)
            break
    else:
        item["color"] = resource_color

# Salva o JSON final
with open(arquivo_saida, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Arquivo '{arquivo_saida}' salvo com sucesso.")