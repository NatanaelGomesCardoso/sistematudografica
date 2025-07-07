document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const navModules = document.querySelectorAll('.nav-module');

    // 1. Controla o clique no botão de menu (hamburger)
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function () {
            document.body.classList.toggle('sidebar-collapsed');
        });
    }

    // 2. Controla o clique nos módulos para abrir/fechar o sub-menu
    navModules.forEach(function (module) {
        const header = module.querySelector('.module-header');
        if (header) {
            header.addEventListener('click', function () {
                // Se a sidebar estiver recolhida, primeiro expanda
                if (document.body.classList.contains('sidebar-collapsed')) {
                    document.body.classList.remove('sidebar-collapsed');
                    setTimeout(() => {
                        module.classList.toggle('active');
                    }, 150);
                } else {
                    module.classList.toggle('active');
                }
            });
        }
    });

    // 3. Controla o desaparecimento das mensagens flash
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        setTimeout(function () {
            flashMessages.forEach(function (message) {
                // Adiciona uma classe para iniciar a animação de saída
                message.style.animation = 'fadeOut 0.5s forwards';
            });
        }, 4000); // Começa a desaparecer após 4 segundos
    }
});