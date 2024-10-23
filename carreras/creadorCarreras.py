import json
import pandas as pd
from bs4 import BeautifulSoup
import re

nombreCarrera = "Ingeniería de Sistemas y Computación" 
codigoCarrera = "2A74"

carrera = {"F":{}, "D":{}, "L":{}, "N":{}}
nTabla = 0
nFundamentacion = 12
nDisiplinar = 17
nLibre = 1

dicMaterias = {}

materiasExtra = {
    'Introducción a las ciencias de la computación':'4200887',
    'haber aprobado 40 creditos del componente de formacion disciplinar o profesional':'ZZZZZZZ',
    'diseño, gestion y evaluacion de proyecto':'2016028',
    'haber aprobado 60 creditos del componente de formacion disciplinar o profesional':'ZZZZZZY',
    'electronica analoga i':'2016495',
    'lineas y antenas':'2016503',
    }

def quitarTildes(s):
    replacements = [
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    ]
    for a, b in replacements:
        s = s.replace(a, b)
    return s

def hallarAgrupacionesPorTabla():
    agrupacion = []
    with open('/workspaces/Malla_curricular/carreras/Normativa_ing_sistemas_y_computacion.html', 'r', encoding='utf-8') as file:
        contenido = file.read()
    soup = BeautifulSoup(contenido, 'html.parser')

    tablas = soup.find_all('table')

    for tabla in tablas:
        etiqueta_anterior = tabla.find_previous()
        texto_anterior = etiqueta_anterior.get_text(strip=True)
        while (texto_anterior == ""):
            etiqueta_anterior = etiqueta_anterior.find_previous()
            texto_anterior = etiqueta_anterior.get_text(strip=True)
        agrupacion.append(texto_anterior.split(": ")[1])
    return agrupacion

agrupaciones = hallarAgrupacionesPorTabla()

def conCodigo(diccionario, nFilas):
    for i in range(nFilas):
        codigo = str(diccionario[('CÓDIGO DE LA ASIGNATURA', 'CÓDIGO DE LA ASIGNATURA')][i])
        nombre = diccionario[('NOMBRE DE LA ASIGNATURA', 'NOMBRE DE LA ASIGNATURA')][i]
        dicMaterias[quitarTildes(nombre.lower())] = codigo
        creditos = diccionario[('CRÉDITOS', 'CRÉDITOS')][i]
        tipo = ""
        if nTabla < nFundamentacion:
            tipo = "F"
        elif nTabla < nDisiplinar + nFundamentacion:
            tipo = "D"
        else:
            tipo = "L"
        optativa = ""
        if diccionario[('OBLIGATORIA', 'OBLIGATORIA')][i] == "NO" and nTabla < nDisiplinar + nFundamentacion:
            optativa = agrupaciones[nTabla]
        prerrequisitos = diccionario[('ASIGNATURA PRERREQUISITO / CORREQUISITO', 'NOMBRE DE LA ASIGNATURA')][i]
        if str(prerrequisitos) == 'nan':
            prerrequisitos = ""
        prerrequisitos = quitarTildes(prerrequisitos.lower())
        carrera[tipo][codigo] = {"nombre": nombre, "creditos":creditos, "optativa":optativa, "prerrequisitos":prerrequisitos}

def sinCodigo(diccionario):
    for i in range(2, len(diccionario[0])):
        codigo = diccionario[0][i]
        nombre = diccionario[1][i]
        dicMaterias[quitarTildes(nombre.lower())] = codigo
        creditos = diccionario[2][i]
        tipo = ""
        if nTabla < nFundamentacion:
            tipo = "F"
        elif nTabla < nDisiplinar + nFundamentacion:
            tipo = "D"
        else:
            tipo = "L"
        optativa = ""
        if diccionario[3][i] == "NO" and nTabla < nDisiplinar + nFundamentacion:
            optativa = agrupaciones[nTabla]
        prerrequisitos = diccionario[4][i]
        if str(prerrequisitos) == 'nan':
            prerrequisitos = ""
        prerrequisitos = quitarTildes(prerrequisitos.lower())
        carrera[tipo][codigo] = {"nombre": nombre, "creditos":creditos, "optativa":optativa, "prerrequisitos":prerrequisitos}

def arrayPrerrequisitos(s:str):
    if(s == "-" or s == ""):
        return [[]]
    
    arreglo = []
    s = s.replace(";", "")
    s = s.replace(",", "")
    s = s.replace(".", "")
    for i in re.split('[ye]', s):
        arreglo.append([])
        for j in i.split("o"):
            arreglo[len(arreglo)-1].append(j.strip())
    return arreglo


df = pd.read_html("/workspaces/Malla_curricular/carreras/Normativa_ing_sistemas_y_computacion.html")
for tabla in df:
    diccionario = tabla.to_dict(orient='dict')
    if 'CÓDIGO DE LA ASIGNATURA' in tabla:
        conCodigo(diccionario=diccionario, nFilas=tabla.shape[0])
    else:
        sinCodigo(diccionario=diccionario)
    nTabla += 1

carrera["N"]["1000001-B"] = {"nombre": "Matemáticas Básicas", "creditos":4, "optativa":"", "prerrequisitos":""}
carrera["N"]["1000002-B"] = {"nombre": "Lecto-Escritura", "creditos":4, "optativa":"", "prerrequisitos":""}
carrera["N"]["1000044-B"] = {"nombre": "Inglés I- Semestral", "creditos":3, "optativa":"Inglés I", "prerrequisitos":""}
carrera["N"]["1000045-B"] = {"nombre": "Inglés II- Semestral", "creditos":3, "optativa":"Inglés II", "prerrequisitos":"Inglés I- Semestral"}
carrera["N"]["1000046-B"] = {"nombre": "Inglés III- Semestral", "creditos":3, "optativa":"Inglés III", "prerrequisitos":"Inglés II- Semestral"}
carrera["N"]["1000047-B"] = {"nombre": "Inglés IV- Semestral", "creditos":3, "optativa":"Inglés IV", "prerrequisitos":"Inglés III- Semestral"}

for materia in carrera['N']:
    dicMaterias[quitarTildes(carrera['N'][materia]['nombre'].lower())] = materia
    carrera['N'][materia]['prerrequisitos'] = quitarTildes(carrera['N'][materia]['prerrequisitos'].lower())

for materia in materiasExtra:
    dicMaterias[quitarTildes(materia.lower())] = materiasExtra[materia]

dicMaterias = dict(sorted(dicMaterias.items(), key=lambda item: len(item[0]), reverse=True))

for tipo in carrera:
    for materiaCarrera in carrera[tipo]:
        for materiDic in dicMaterias:
            if materiDic in carrera[tipo][materiaCarrera]['prerrequisitos']:
                carrera[tipo][materiaCarrera]['prerrequisitos'] = carrera[tipo][materiaCarrera]['prerrequisitos'].replace(materiDic, f' {dicMaterias[materiDic]} ')
        carrera[tipo][materiaCarrera]['prerrequisitos'] = arrayPrerrequisitos(carrera[tipo][materiaCarrera]['prerrequisitos'])
        print(carrera[tipo][materiaCarrera]['prerrequisitos'])

nuevoNombre = ""
for i in nombreCarrera.split(" "):
    nuevoNombre += i.capitalize()

with open(f'/workspaces/Malla_curricular/carreras/{codigoCarrera}_{nuevoNombre}.json', 'w', encoding='utf-8') as file:
    json.dump(carrera, file, ensure_ascii=False, indent=4)