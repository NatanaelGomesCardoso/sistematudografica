/**
 * Script Principal para Interatividade do Sistema Tudo Gráfica Online
 * Este ficheiro controla:
 * 1. A expansão e o recolhimento da barra lateral (sidebar).
 * 2. O comportamento de clique dos módulos de menu para expandir (dropdown)
 * ou mostrar um menu flutuante (fly-out).
 * 3. O desaparecimento automático das notificações (flash messages).
 */

// Executa o script apenas quando o HTML da página estiver totalmente carregado.
document.addEventListener('DOMContentLoaded', function () {

    const sidebarToggle = document.getElementById('sidebar-toggle');
    const navModules = document.querySelectorAll('.nav-module');

    // ========================================================================
    // 1. LÓGICA PARA RECOLHER/EXPANDIR A BARRA LATERAL (SIDEBAR)
    // ========================================================================
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function () {
            document.body.classList.toggle('sidebar-collapsed');

            // Garante que todos os submenus 'fly-out' fechem ao expandir a barra
            if (!document.body.classList.contains('sidebar-collapsed')) {
                navModules.forEach(module => module.classList.remove('active'));
            }
        });
    }

    // ========================================================================
    // 2. LÓGICA PARA ABRIR SUBMENUS (MODO NORMAL E FLY-OUT)
    // ========================================================================
    navModules.forEach(function (module) {
        const header = module.querySelector('.module-header');
        if (header) {
            header.addEventListener('click', function (e) {
                // Impede que o clique se propague para outros elementos,
                // como o listener que fecha o menu ao clicar fora.
                e.stopPropagation();

                const isActive = module.classList.contains('active');

                // Fecha todos os outros módulos abertos para criar o efeito "acordeão".
                navModules.forEach(otherModule => {
                    otherModule.classList.remove('active');
                });

                // Se o módulo clicado não estava ativo, ele é ativado.
                // Se já estava, o passo anterior já o fechou, resultando num efeito de "toggle".
                if (!isActive) {
                    module.classList.add('active');
                }
            });
        }
    });

    // ========================================================================
    // 3. LÓGICA PARA FECHAR O MENU FLY-OUT AO CLICAR FORA
    // ========================================================================
    document.addEventListener('click', function () {
        // Esta função só precisa de fechar os módulos se a sidebar estiver recolhida.
        if (document.body.classList.contains('sidebar-collapsed')) {
            navModules.forEach(module => {
                module.classList.remove('active');
            });
        }
    });

    // ========================================================================
    // 4. LÓGICA PARA AS NOTIFICAÇÕES (FLASH MESSAGES)
    // ========================================================================
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        setTimeout(function () {
            flashMessages.forEach(function (message) {
                // Adiciona a classe que dispara a animação de saída
                message.classList.add('fade-out');

                // Remove o elemento da página após a animação
                setTimeout(() => {
                    message.remove();
                }, 500); // Tempo igual à duração da animação no CSS
            });
        }, 4500); // A notificação começa a desaparecer após 4.5 segundos
    }
});