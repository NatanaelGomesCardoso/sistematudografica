// Este script é executado assim que o conteúdo da página termina de carregar
document.addEventListener('DOMContentLoaded', function () {

    // --- 1. INTERATIVIDADE DA BARRA LATERAL (SIDEBAR) ---

    const sidebarToggle = document.getElementById('sidebar-toggle');
    const navModules = document.querySelectorAll('.nav-module');

    // Adiciona um "ouvinte" ao botão do menu (hamburger)
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function () {
            // Adiciona ou remove a classe 'sidebar-collapsed' do <body>
            // O CSS encarrega-se de fazer a animação de deslizar
            document.body.classList.toggle('sidebar-collapsed');
        });
    }

    // Adiciona um "ouvinte" a cada módulo que tem um submenu
    navModules.forEach(function (module) {
        const header = module.querySelector('.module-header');
        if (header) {
            header.addEventListener('click', function () {
                // Se a sidebar estiver fechada, primeiro abre-a para mostrar o submenu
                if (document.body.classList.contains('sidebar-collapsed')) {
                    document.body.classList.remove('sidebar-collapsed');
                    // Espera um pouco pela animação da sidebar antes de abrir o submenu
                    setTimeout(() => {
                        module.classList.toggle('active');
                    }, 150);
                } else {
                    // Adiciona ou remove a classe 'active' para mostrar/esconder o submenu
                    // O CSS encarrega-se da animação de deslizar para baixo
                    module.classList.toggle('active');
                }
            });
        }
    });

    // --- 2. INTERATIVIDADE DAS NOTIFICAÇÕES (FLASH MESSAGES) ---

    const flashMessages = document.querySelectorAll('.flash-message');
    // Se existir alguma notificação na tela...
    if (flashMessages.length > 0) {
        // Aguarda 4 segundos
        setTimeout(function () {
            flashMessages.forEach(function (message) {
                // Adiciona um estilo que aciona a animação de 'fadeOut' definida no CSS
                message.style.animation = 'fadeOut 0.5s forwards';
                // Remove o elemento da tela após a animação terminar, para não atrapalhar
                setTimeout(() => {
                    message.remove();
                }, 500);
            });
        }, 4000);
    }
});