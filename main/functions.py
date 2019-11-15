import random
from datetime import datetime
from operator import itemgetter
import json
"""
Función que se encarga de crear las matrices de la maquina y del jugador
"""
def crearMatriz():
    matriz = []
    for i in range(10):
        matriz.append([])
        for j in range(10):
            #Se añaden "e"s que se refieren al estado "empty" de la casilla
            matriz[i].append("e")
    return matriz

"""
Funcion que se encarga de generar los barcos de la computadora
Entradas:
    -tamaño: se refiere al tamaño del barco a ubicar
    -lista: una lista con las coordenadas que ya poseen barcos para que no se 
    puedan superponer barcos
Retorno: una matriz con las coordenadas del barco y un 0 al final que se refiere al numero de
hits que le han dado al barco, empieza en 0 porque cuando esta función se llama la fase de batalla
todavía no ha empezado
"""
def posicionarComputadora(tamaño, lista):
    error = True
    barco = []
    coordenadas = []
    while error:
        direccion = random.randint(1, 2)
        x1 = random.randint(0, 9)   
        y1= random.randint(0, 9)
        
        if direccion == 2:
            y2 = 0
            lastY1 = y1

            while True:
                orientacion = random.randint(1, 2)
                if orientacion == 1:
                    y2 = y1 + tamaño - 1
                elif orientacion == 2:
                    y1 = y1 - tamaño + 1
                    y2 = y1 + tamaño - 1
                if y1 < 0 or y2 > 9:
                    y1 = lastY1
                else:
                    break

            for pos in range(y1, y2 + 1):
                if not([x1, pos] in lista):
                    coordenadas.append([x1, pos])
                else:
                    break
                if len(coordenadas) == tamaño:
                    barco.append(coordenadas)
                    barco.append(0)  
                    error = False          
            
        elif direccion == 1:
            x2 = 0
            lastX1 = x1
            while True:
                orientacion = random.randint(1, 2) 
                if orientacion == 1:
                    x2 = x1 + tamaño - 1
                elif orientacion == 2:
                    x1 = x1 - tamaño + 1
                    x2 = x1 + tamaño - 1
                if x1 < 0 or x2 > 9:
                    x1 = lastX1
                else:
                    break

            for pos in range(x1, x2 + 1):
                if not([pos, y1] in lista):
                    coordenadas.append([pos, y1])
                else:
                    break
                if len(coordenadas) == tamaño:
                    barco.append(coordenadas)
                    barco.append(0)
                    error = False

        if error:
            barco = []
            coordenadas = []
    return barco


"""
Función que se encarga de ubicar los barcos en la matriz
Entradas:
    -matriz: se refiere a la matriz que se va a actualizar
    -barco: el barco que se va a ubicar
    -flota: un diccionario que posee la información de todos los barcos, se usa porque
    esta contiene las coordenadas del barco a ubicar
Retorno: la matriz ya actualizada
"""
def ubicarBarco(matriz, barco, flota):
    for coordenada in flota[barco][0]:
        x = coordenada[0]
        y = coordenada[1]
        """
        Se coloca una "s", que se refiere al estado "ship" de la casilla, es decir que en ella
        hay un barco
        """
        matriz[x][y] = "s"
    return matriz


"""
Función que se encarga de añadir las posiciones de un barco a una lista, es usada para
que no se superpongan los barcos de la computadora
Entradas:
    -barco: es el barco que recibe el diccionario "flota" para saber que coordenadas 
    se van a añadir
    -listaPosiciones: es la lista a la que se le van a añadir las coordenadas
    -flota: es el diccionario que almacena las coordenadas de los barcos
Retorno: la lista con las coordenadas ya añadidas
"""
def appendLista(barco, listaPosiciones, flota):
    for coord in flota[barco][0]:
        listaPosiciones.append(coord)
    return listaPosiciones


"""
Función que se encarga de revisar que el disparo que haya hecho el jugador haya sido a 
una casilla vacia, de manera que no pueda disparar dos veces al mismo lugar
Entradas:
    -x: la coordenada en x del disparo
    -y: la coordenada en y del disparo
    -matriz: la matriz en la que se va a revisar que se dispare a una casilla vacia
Retorno: una variable de tipo booleana, True si el disparo le dio a una casilla repetida,
False en el caso contrario
"""
def checkCoordenada(x, y, matriz):
    error = False
    if not(matriz[x][y] == "e"):
        error = True
    return error


"""
Función que se encarga de generar las coordenadas en las que se va a ubicar el barco de un
jugador
Entradas:
    -x1: coordenadas en x donde se va a empezar a ubicar el barco
    -y1: coordenadas en y donde se va a empezar a ubicar el barco
    -direccion: la direccion en la que se va a poner el barco, 1 para vertical, 2 para horizontal
    -tamaño: el tamaño del barco que se va a ubicar
    -matriz: la matriz del jugador que se usa para checkear que el jugador no ponga un barco
    encima de otro barco
Retorno: una matriz con las coordenadas del barco y un 0 al final que se refiere al numero de
hits que le han dado al barco, empieza en 0 porque cuando esta función se llama la fase de batalla
todavía no ha empezado. En caso de que se produzca un error, devuelve una lista vacia
"""
def generarBarco(x1, y1, direccion, tamaño, matriz):
    barco = []
    coordenadas = []
    if direccion == 2:
        y2 = 0
        lastY1 = y1
        y2 = y1 + tamaño - 1
        if y2 <= 9:
            for pos in range(y1, y2 + 1):
                if matriz[x1][pos] == "e":
                    coordenadas.append([x1, pos])
                else:
                    break
                if len(coordenadas) == tamaño:
                    barco.append(coordenadas)
                    barco.append(0)
    
    elif direccion == 1:
        x2 = 0
        lastX1 = x1
        x2 = x1 + tamaño - 1
        if x2 <= 9:
            for pos in range(x1, x2 + 1):
                if matriz[pos][y1] == "e":
                    coordenadas.append([pos, y1])
                else:
                    break
                if len(coordenadas) == tamaño:
                    barco.append(coordenadas)
                    barco.append(0)
                        
    return barco


"""
Función que genera el disparo de la computadora
Entradas:
    -matriz: la matriz del jugador que se usa para revisar que no se dispare 2 veces 
    al mismo lugar
Retorno: una lista con las coordenadas del disparo
"""
def disparoComputadora(matriz):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if matriz[x][y] == "e" or matriz[x][y] == "s":
            break
    return [x, y]


"""
Función que revisa si el disparo acierta a algún barco y a cual le dio
Entradas:
    -x: coordenada en x del disparo
    -y: coordenada en y del disparo
    -flota: diccionario que contiene la información de los barcos
Retorno: el nombre del barco al que se le dio, en caso de fallar devuelve un string vacio
"""
def checkDisparo(x, y, flota):
    hit = ""
    for barco in flota:
        for coordenada in flota[barco][0]:
            xBarco = coordenada[0]
            yBarco = coordenada[1]
            if x == xBarco and y == yBarco:
                hit = barco
                break
        if hit != "":
            break
    return hit


"""
Función que revisa si el jugador o la maquina ha ganado
Entradas:
    -flota: diccionario con la información de los barcos, se usa ya que este contiene el numero
    de hits que se le ha hecho ha cada barco.
Retorno: en caso de que los hits sumen 17, es decir que se han hundido todos los barcos, entonces
ese jugador habra ganado
"""
def checkGanador(flota, nombre):
    totalHits = 0
    ganador = ""
    for barco in flota:
        totalHits += flota[barco][1]
    if totalHits == 17:
        ganador = nombre
    return ganador


"""
Función que actualiza el número de hits hecho a una flota
Entradas:
    -checkBarco: un string que contiene el barco al que se le hizo un hit, si esta vacío quiere
    decir que no se le dio a algún barco
    -flota: diccionario con la información de los barcos
Retorno: el diccionario de la flota ya actualizado
"""
def actualizarFlota(checkBarco, flota):
    if checkBarco != "":
        barco = checkBarco
        flota[barco][1] += 1
    return flota


"""
Función que comprueba si se hundió algún barco
Entradas:
    -barco: un string que contiene el barco al que se le hizo un hit, si esta vacío quiere
    decir que no se le dio a algún barco
    -flota: diccionario con la información de los barcos
Retorno: si el número de hits hecho al barco es igual a su tamaño, entonces la función devuelve
el nombre del barco que se hundió, si no se hundió ninguno devuelve un string vacío
"""
def checkHundido(barco, flota):
    hundido = ""
    if barco != "":
        if flota[barco][1] == len(flota[barco][0]):
            hundido = barco
    return hundido

"""
Función que se encarga de actualizar la matriz durante la fase de disparos
Entradas:
    -x: coordenada en x del disparo
    -y: coordenada en y del disparo
    -checkBarco: un string que contiene el barco al que se le hizo un hit, si esta vacío quiere
    decir que no se le dio a algún barco
    -matriz: matriz que se va a actualizar
Retorno: la matriz ya actualizada
"""
def actualizarMatriz(x, y, checkBarco, matriz):
    letra = ""
    if checkBarco != "":
        # La "h" se refiere al estado de la casilla "hit", 
        # es decir que se le dio a un barco en esa posición
        letra = "h"
    else:
        # La "m" se refiere al estado de la casilla "miss", 
        # es decir que no se le dio a algo en esa posición
        letra = "m"
    matriz[x][y] = letra
    return matriz


"""
Función que se encarga de actualizar el ranking
Entradas:
    -nombre1: nombre del jugador1
    -nombre2: nombre del jugador2
    -ganador: nombre del ganador
    -disparos1: cantidad de disparos hechos por el jugador1
    -disparos2: cantidad de disparos hechos por el jugador2
Actualiza el JSON con la nueva información
"""
def actualizarRanking(nombre1, nombre2, ganador, disparos1, disparos2):
    try:
        with open("ranking.json", "r") as archivo1:
            ranking = json.load(archivo1)
    except:
        ranking = {}
    jugadores = [nombre1, nombre2]
    listaDisparos = [disparos1, disparos2]
    for i in range(2):
        nombre = jugadores[i]
        disparos = listaDisparos[i]
        if nombre in ranking:
            antDisparos = ranking[nombre][2]
            if antDisparos == "-":
                antDisparos = 0
            if nombre == ganador:
                ranking[nombre][0] += 1
                if disparos < antDisparos:
                    ranking[nombre][2] = disparos
            else:
                ranking[nombre][1] += 1
        else:
            if nombre == ganador:
                ranking[nombre] = [1, 0, disparos]
            else:
                ranking[nombre] = [0, 1, "-"]

    with open("ranking.json", "w") as archivo2:
        json.dump(ranking, archivo2, indent=4)


"""
Función que se encarga de guardar un JSON con las posiciones del jugador
Entradas:
    -nombreJugador: el nombre del jugador
    -flota: diccionario con la información de los barcos a guardar
"""
def guardarUbicaciones(nombreJugador, flota):
    fecha = str(datetime.now())
    fechaMod = fecha.replace(":", "_")
    fechaMod2 = fechaMod[:-7]
    nombreArchivo = nombreJugador + fechaMod2 + ".json"
    nombreCompleto = "./main/Ubicaciones Guardadas/" + nombreArchivo
    with open(nombreCompleto, "w") as archivo:
        json.dump(flota, archivo, indent=4)

"""
Función que se encarga de cargar las posiciones de los barcos
Entradas:
    -nombreArchivo: es el nombre del archivo a cargar
Retorno: devuelve un diccionario con la información de los barcos, si da un error devuelve un
diccionario vacio
"""
def cargarUbicaciones(nombreArchivo):
    flotaAliada = {}
    if nombreArchivo[-5:] == ".json":
        try:
            with open(nombreArchivo, "r") as files:
                flotaAliada = json.load(files)
        except:
            flotaAliada = {}
    return flotaAliada

"""
Función que se encarga de comprobar que las posiciones de la flota sean correctas
Entradas:
    -flota: diccionario con la información de los barcos
Retorno: una variable de tipo booleana, si es True quiere decir que la matriz esta correcta,
False si es lo contrario
"""
def checkearUbicaciones(flota):
    check = True
    try:
        checkLongitud = False
        if len(flota) == 5:
            barcos = list(flota.keys())
            if barcos[0] == "carrier" and len(flota[barcos[0]][0]) == 5:  
                if barcos[1] == "battleship" and len(flota[barcos[1]][0]) == 4: 
                    if barcos[2] == "cruiser" and len(flota[barcos[2]][0]) == 3:
                        if barcos[3] == "submarine" and len(flota[barcos[3]][0]) == 3:  
                            if barcos[4] == "destroyer" and len(flota[barcos[4]][0]) == 2:
                                checkLongitud = True
        if not(checkLongitud):
            check = False

        for barco in flota:
            if flota[barco][1] != 0:
                check = False

            direccion = ""
            coord1 = flota[barco][0][0]
            coord2 = flota[barco][0][1]
            if coord1[0] == coord2[0]:
                direccion = "horizontal"
            elif  coord1[1] == coord2[1]:
                direccion = "vertical"
            else:
                    check = False
            if check:
                coordenadas = flota[barco][0]
                for i in range(len(coordenadas)):
                    if i == 0:
                        lastX = coordenadas[0][0]
                        lastY = coordenadas[0][1]

                    elif direccion == "horizontal":
                        if coordenadas[i][0] == lastX:
                            if coordenadas[i][1] == lastY + 1:
                                lastY = coordenadas[i][1]
                            else:
                                check = False
                        else:
                            check = False

                    elif direccion == "vertical":
                        if coordenadas[i][1] == lastY:
                            if coordenadas[i][0] == lastX + 1:
                                lastX = coordenadas[i][0]
                            else:
                                check = False
                        else:
                            check = False
                    
                    if not(check):
                        break
            else:
                break

        if check:
            for barco in flota:
                if not(check):
                    break
                coordenadas = flota[barco][0]
                for coord in coordenadas:
                    veces = 0
                    if not(check):
                        break
                    for barco2 in flota:
                        if coord in flota[barco2][0]:
                            veces += 1
                            if veces > 1:
                                check = False
                                break
    except:
        check = False
                
    return check

