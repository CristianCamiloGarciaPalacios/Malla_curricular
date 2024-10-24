import { Materia } from "/app/Materia.js";

const contenedorSemestres = document.querySelector('.contenedor-semestres');
const contenedorCreditos = document.querySelector('.contenedor-creditos');
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
        const semestre = document.createElement('p')
        semestre.classList.add('semestre');
        if (i < 9) {
            semestre.textContent = `semestre 0${i+1}`;
        } else {
            semestre.textContent = `semestre ${i+1}`;
        }
        contenedorSemestres.appendChild(semestre);
        
        const credito = document.createElement('p')
        if (i < 9) {
            credito.innerHTML = `<p id="credito-0${i+1}" class="credito">0 creditos</p>`;
        } else {
            credito.innerHTML = `<p id="credito-${i+1}" class="credito">0 creditos</p>`;
        }
        contenedorCreditos.appendChild(credito);
        
    }
    
    for (let i = 1; i <= numSemestres; i++) {
        arrayMaterias[i-1] = []
        for (let j = 1; j <= numFilas; j++) {
            arrayMaterias[i-1][j-1] = new Materia({ semestre: i, fila: j });
        }
    }
}
