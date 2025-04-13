document.addEventListener('DOMContentLoaded', function () {
    if (window.Crate) {
        const crate = new Crate({
            server: '1299162074609352787',
            channel: '1299162075041628292',
            color: '#7E56C2'
        });

        const AVATAR_URL = '/site/assets/img/avatar.jpg';

        function showNotificationWithSound(message) {
            const audio = new Audio('/site/assets/js/notif.mp3');
            audio.play().catch(e => console.log('Não foi possível reproduzir o som:', e));
        
            crate.notify({
                content: message,
                avatar: AVATAR_URL,
                timeout: 5000 // opcional, define duração da notificação (em ms)
            });
        }

        const messageConfig = {
            firstVisitGlobal: {
                messages: [
                    "🎉 Bem-vindo pela primeira vez ao nosso site! Temos um canal no Discord para ajudar com os Ultra Boss!",
                    "👋 Olá, novo visitante! Fique à vontade! Temos um canal no Discord para ajudar com os Ultra Boss!",
                    "🌟 Que bom te ver aqui pela primeira vez! Temos um canal no Discord para ajudar com os Ultra Boss!"
                ],
                probability: 1.0
            },
            pageSpecific: {
                "/site/sobre.html": {
                    messages: ["👋 Conheça nossa história!", "📖 Saiba mais sobre quem somos!"],
                    probability: 0.3
                },
                "/site/ajuda.html": {
                    messages: ["❓ Precisa de ajuda? Estamos aqui!", "🛠️ Problemas? Nos avise no chat!"],
                    probability: 0.3
                },
                "/site/index.html": {
                    messages: ["🌟 Bem-vindo à página inicial!", "🚀 Explore nosso conteúdo em Guias!"],
                    probability: 0.3
                },
                "/site/guias/ultra-bosses": {
                    messages: [
                        "Tá precisando de ajuda com ultra boss, meu chapa?",
                        "Ainda tá com problemas com ultras?",
                        "Quer saber como derrotar os ultras?"
                    ],
                    probability: 0.3
                }
            },
            generic: {
                messages: [
                    "Participe da conversa no nosso servidor!",
                    "Tá precisando de ajuda com algum boss?",
                    "Mulheres solteiras na sua região... mentira!",
                    "Voltou a jogar e não sabe pra onde ir?"
                ],
                probability: 0.2
            },
            settings: {
                firstVisitPageProbability: 1.0,
                cooldown: 30
            }
        };

        const isFirstVisitGlobal = !localStorage.getItem('visitedBefore');
        if (isFirstVisitGlobal) {
            localStorage.setItem('visitedBefore', 'true');
            const firstMessages = messageConfig.firstVisitGlobal.messages;
            const randomMessage = firstMessages[Math.floor(Math.random() * firstMessages.length)];
            showNotificationWithSound(randomMessage);
            return;
        }

        let currentPath = window.location.pathname;
        if (currentPath.endsWith('/')) currentPath = currentPath.slice(0, -1); // remove barra final

        const lastNotificationKey = `lastNotification_${currentPath}`;
        const lastNotificationTime = localStorage.getItem(lastNotificationKey);
        const now = new Date().getTime();

        if (lastNotificationTime && (now - lastNotificationTime < messageConfig.settings.cooldown * 60 * 1000)) {
            return;
        }

        let pageMessagesConfig = null;
        for (const path in messageConfig.pageSpecific) {
            const normalizedPath = path.endsWith('/') ? path.slice(0, -1) : path;
            if (currentPath.startsWith(normalizedPath)) {
                pageMessagesConfig = messageConfig.pageSpecific[path];
                break;
            }
        }

        const pageVisitKey = `visitedPage_${currentPath}`;
        const isFirstVisitPage = !localStorage.getItem(pageVisitKey);

        if (isFirstVisitPage) {
            localStorage.setItem(pageVisitKey, 'true');
            if (pageMessagesConfig) {
                const randomMessage = pageMessagesConfig.messages[Math.floor(Math.random() * pageMessagesConfig.messages.length)];
                showNotificationWithSound(randomMessage);
                localStorage.setItem(lastNotificationKey, now.toString());
                return;
            } else if (messageConfig.generic.messages.length > 0) {
                const randomMessage = messageConfig.generic.messages[Math.floor(Math.random() * messageConfig.generic.messages.length)];
                showNotificationWithSound(randomMessage);
                localStorage.setItem(lastNotificationKey, now.toString());
                return;
            }
        }

        if (pageMessagesConfig && Math.random() < pageMessagesConfig.probability) {
            const randomMessage = pageMessagesConfig.messages[Math.floor(Math.random() * pageMessagesConfig.messages.length)];
            showNotificationWithSound(randomMessage);
            localStorage.setItem(lastNotificationKey, now.toString());
        } else if (Math.random() < messageConfig.generic.probability) {
            const randomMessage = messageConfig.generic.messages[Math.floor(Math.random() * messageConfig.generic.messages.length)];
            showNotificationWithSound(randomMessage);
            localStorage.setItem(lastNotificationKey, now.toString());
        }
    }
});
