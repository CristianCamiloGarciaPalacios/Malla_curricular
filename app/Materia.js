const main_panel = document.querySelector('.main-panel');

export class Materia {
    constructor({codigo = "", nombre = "", tipo = "", creditos = 0, optativa = "", prerrequisitos = [[]], semestre = 1, fila = 1 } = {}) {
        this.codigo = codigo;
        this.nombre = nombre;
        this.tipo = tipo;
        this.creditos = creditos;
        this.optativa = optativa;
        this.prerrequisitos = prerrequisitos;
        this.etiqueta = document.createElement('div');
        main_panel.appendChild(this.etiqueta);
        this.etiqueta.classList.add('materia');
        this.semestre = semestre;
        this.fila = fila;
    }
}