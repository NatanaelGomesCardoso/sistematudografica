document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const navModules = document.querySelectorAll('.nav-module');

    // 1. Controla o clique no botão de menu (hamburger)
    sidebarToggle.addEventListener('click', function () {
        document.body.classList.toggle('sidebar-collapsed');
    });

    // 2. Controla o clique nos módulos para abrir/fechar o sub-menu
    navModules.forEach(function (module) {
        const header = module.querySelector('.module-header');
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
    });
});

// Em static/js/main.js, adicione ao final:

// 3. Controla o desaparecimento das mensagens flash
document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.flash-message');
    setTimeout(function () {
        flashMessages.forEach(function (message) {
            message.style.display = 'none';
        });
    }, 4500); // Tempo um pouco maior que a animação de fade-out
});

