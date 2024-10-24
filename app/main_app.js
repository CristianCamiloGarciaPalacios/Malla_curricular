import { Materia } from "/app/Materia.js";

const mainPanel = document.querySelector('.main-panel');
const iconMenu = document.querySelector('#icon-menu');
const mainMenu = document.querySelector('#main-menu');

let arrayMaterias = [] // (semestre, fila)
let numSemestres = 15
let numFilas = 5

iconMenu.addEventListener('click', () => {
    mainMenu.classList.toggle('menu-show');
});

window.onload = function() {
    for (let i = 0; i < numSemestres; i++) {
        const contenedorSemestre = document.createElement('div')
        contenedorSemestre.setAttribute("id", `contenedor-semestre-0${i+1}`);
        contenedorSemestre.classList.add('contenedor-semestre');
        const semestre = document.createElement('p')
        semestre.classList.add('semestre');
        const credito = document.createElement('p')
        credito.classList.add('credito');
        credito.textContent = '0 creditos';
        if (i < 9) {
            semestre.textContent = `semestre 0${i+1}`;
        } else {
            semestre.textContent = `semestre ${i+1}`;
        }
        contenedorSemestre.appendChild(semestre);
        contenedorSemestre.appendChild(credito);
        mainPanel.appendChild(contenedorSemestre);

        arrayMaterias[i-1] = []
        for (let j = 1; j <= numFilas; j++) {
            arrayMaterias[i-1][j-1] = new Materia({ semestre: i, fila: j });
            contenedorSemestre.appendChild(arrayMaterias[i-1][j-1].etiqueta);
        }
    }
}
