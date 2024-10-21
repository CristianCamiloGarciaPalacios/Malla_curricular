const iconMenu = document.querySelector('#icon-menu');
const mainMenu = document.querySelector('#main-menu');

iconMenu.addEventListener('click', () => {
    mainMenu.classList.toggle('menu-show');
});