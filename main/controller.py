from flask import render_template, Blueprint, request
import json
from operator import itemgetter
from .forms import FormularioNombre
from .forms import FormularioUbicar
from .forms import FormularioDisparo
from .functions import *
import random
from datetime import datetime

bp = Blueprint('batalla', __name__, url_prefix='/')

matrizAliada = []
flotaAliada = {}
matrizEnemiga = []
flotaEnemiga = {}
listaPosiciones = []
nombre = ""
ganador = ""
disparosJugador = 0
disparosEnemigo = 0

# Función que muestra la pantalla inicial
@bp.route("/")
def inicio():
        return render_template("inicio.html")


# Funcion que muestra el ranking, en caso de que el ranking esté vacío pasa una lista vacía
@bp.route("/ranking/")
def ranking():
    try:
        with open("ranking.json", "r") as archivo1:
            ranking = json.load(archivo1)
        items = list(ranking.items())
        '''
        La linea de abajo se encarga de organizar el ranking de mayor a menor cantidad de victorias.
        La función itemgetter(1) se encarga de devolver la lista con la información del jugador
        para que la sorted lo organize en base a ella
        '''
        items2 = sorted(items, key=itemgetter(1))
        keysOrdenadas = items2[::-1]
        return render_template("ranking.html", jugadores = keysOrdenadas)
    except:
        return render_template("ranking.html", jugadores = [])

# Función que crea la flota enemiga y recibe el nombre del jugador
# Adicionalmente esta función reinicia todo el juego para que no ocurran errores
@bp.route("/nombre/", methods = ["POST", "GET"])
def nombre():
    """
    Se definen las variables como globales para que los cambios hechos a estas dentro 
    de la función se mantengan en todo el programa
    """
    global matrizAliada
    global flotaAliada
    global matrizEnemiga
    global flotaEnemiga
    global nombre
    global ganador
    global disparosJugador
    global disparosEnemigo
    matrizAliada = crearMatriz()
    flotaAliada = {}
    matrizEnemiga = crearMatriz()
    flotaEnemiga = {}
    # La variable listaPosiciones guarda las posiciones de los barcos enemigos para que no se
    # superpongan
    listaPosiciones = []
    nombre = ""
    ganador = ""
    disparosEnemigo = 0
    disparosJugador = 0

    # Se crea la flota enemiga
    flotaEnemiga["carrier"] = posicionarComputadora(5, listaPosiciones)
    listaPosiciones = appendLista("carrier", listaPosiciones, flotaEnemiga)

    flotaEnemiga["battleship"] = posicionarComputadora(4, listaPosiciones)
    listaPosiciones = appendLista("battleship", listaPosiciones, flotaEnemiga)

    flotaEnemiga["cruiser"] = posicionarComputadora(3, listaPosiciones)
    listaPosiciones = appendLista("cruiser", listaPosiciones, flotaEnemiga)

    flotaEnemiga["submarine"] = posicionarComputadora(3, listaPosiciones)
    listaPosiciones = appendLista("submarine", listaPosiciones, flotaEnemiga)

    flotaEnemiga["destroyer"] = posicionarComputadora(2, listaPosiciones)
    listaPosiciones = appendLista("destroyer", listaPosiciones, flotaEnemiga)

    form = FormularioNombre()
    if request.method == "POST" and form.validate_on_submit():
        nombre = form.nombre.data
        return render_template("confirmacion.html")
    else:
        return render_template("nombre.html", form = form)

#Función que se crear la flota del jugador en caso de que el jugador la quiera hacer
#manualmente
@bp.route("/faseColocacion/", methods = ["POST", "GET"])
def colocacion():

    # Se definen las variables como globales para que los cambios hechos a estas dentro 
    # de la función se mantengan en todo el programa

    global matrizAliada
    global flotaAliada
    global nombre
    form = FormularioUbicar()
    barco = []
    error = 0
    tamaño = 0
    tipoBarco = ""
    if len(flotaAliada) == 0:
        tipoBarco = "carrier"
        tamaño = 5
    elif len(flotaAliada) == 1:
        tipoBarco = "battleship"
        tamaño = 4
    elif len(flotaAliada) == 2:
        tipoBarco = "cruiser"
        tamaño = 3
    elif len(flotaAliada) == 3:
        tipoBarco = "submarine"
        tamaño = 3
    elif len(flotaAliada) == 4:
        tipoBarco = "destroyer"
        tamaño = 2
    if request.method == "POST" and form.validate_on_submit():
        x = int(form.x.data)
        y = int(form.y.data)
        direccion = int(form.direccion.data)
        checkVacio = checkCoordenada(x, y, matrizAliada)
        if checkVacio:
            error = 1
        else:   
            barco = generarBarco(x, y, direccion, tamaño, matrizAliada)
            if len(barco) != 0:
                if len(barco[0]) == tamaño:
                    flotaAliada[tipoBarco] = barco  
                    matrizAliada = ubicarBarco(matrizAliada, tipoBarco, flotaAliada)
            else:
                error = 1

        return render_template("faseColocacion.html", matriz = matrizAliada, flota = flotaAliada, 
                            form = form, barco = tipoBarco, error = error, nombre = nombre)
    else:
        return render_template("faseColocacion.html", matriz = matrizAliada, flota = flotaAliada, 
                                form = form, barco = tipoBarco, error = error, nombre = nombre)

# Función que se encarga de cargar las posiciones de un archivo JSON
@bp.route("/cargarUbicaciones/", methods = ["POST", "GET"])
def archivo():
    """
    Se definen las variables como globales para que los cambios hechos a estas dentro 
    de la función se mantengan en todo el programa
    """
    global matrizAliada
    global flotaAliada
    error = False
    check = False
    if request.method == "POST":
        archivo = request.form["file"]
        path = "./main/Ubicaciones Guardadas/" + archivo
        flotaAliada = cargarUbicaciones(path)
        check = checkearUbicaciones(flotaAliada)
        if check:
            matrizAliada = ubicarBarco(matrizAliada, "carrier", flotaAliada)
            matrizAliada = ubicarBarco(matrizAliada, "battleship", flotaAliada)
            matrizAliada = ubicarBarco(matrizAliada, "cruiser", flotaAliada)
            matrizAliada = ubicarBarco(matrizAliada, "submarine", flotaAliada)
            matrizAliada = ubicarBarco(matrizAliada, "destroyer", flotaAliada)
        return render_template("cargarArchivo.html", check = check , Primero = False)
    else:
        return render_template("cargarArchivo.html", check = check, primero = True)

#Función que se encarga de guardar las ubicaciones del usuario
@bp.route("/guardar/", methods = ["POST", "GET"])
def guardar():

    #Se define la variable como global para que se pueda guardar la flota 
    global flotaAliada
    guardar = False
    if request.method == "POST":
        guardarUbicaciones(nombre, flotaAliada)
        guardar = True
        return render_template("guardar.html", guardar = guardar)
    else:
        return render_template("guardar.html", guardar = guardar)
        

#Función que se encarga de toda la fase de batalla del juego
@bp.route("/faseDisparos/", methods = ["POST", "GET"])
def disparos():
    """
    Se definen las variables como globales para que los cambios hechos a estas dentro 
    de la función se mantengan en todo el programa
    """
    global matrizAliada
    global flotaAliada
    global nombre
    global matrizEnemiga
    global flotaEnemiga
    global disparosEnemigo
    global disparosJugador
    global ganador
    error = 0
    hitEnemigo = ""
    hitAliado = ""
    hundidoEnemigo = ""
    hundidoAliado = ""
    form = FormularioDisparo()
    if request.method == "POST" and form.validate_on_submit():
        x1 = int(form.x.data)
        y1 = int(form.y.data)
        checkVacio = checkCoordenada(x1, y1, matrizEnemiga)
        if checkVacio:
            error = 1
        else:
            hitEnemigo = checkDisparo(x1, y1, flotaEnemiga)
            flotaEnemiga = actualizarFlota(hitEnemigo, flotaEnemiga)
            matrizEnemiga = actualizarMatriz(x1, y1, hitEnemigo, matrizEnemiga)
            ganador = checkGanador(flotaEnemiga, nombre)
            hundidoEnemigo = checkHundido(hitEnemigo, flotaEnemiga)
            disparosJugador += 1


            if ganador == "":
                coordsDisparoEnemigo = disparoComputadora(matrizAliada)
                x2 = coordsDisparoEnemigo[0]
                y2 = coordsDisparoEnemigo[1]
                hitAliado = checkDisparo(x2, y2, flotaAliada)
                flotaAliada = actualizarFlota(hitAliado, flotaAliada)
                matrizAliada = actualizarMatriz(x2, y2, hitAliado, matrizAliada)
                ganador = checkGanador(flotaAliada, "maquina")
                hundidoAliado = checkHundido(hitAliado, flotaAliada)
                disparosEnemigo += 1
        if ganador != "":
            actualizarRanking(nombre, "maquina", ganador, disparosJugador, disparosEnemigo)
                
        return render_template("faseDisparos.html", matrizAliada = matrizAliada, 
        matrizEnemiga = matrizEnemiga, form = form, hitEnemigo = hitEnemigo, hitAliado = hitAliado,
        error = error, hundidoEnemigo = hundidoEnemigo, hundidoAliado = hundidoAliado, 
        ganador = ganador, nombre = nombre, primero = 0)
    else:
        return render_template("faseDisparos.html", matrizAliada = matrizAliada, 
        matrizEnemiga = matrizEnemiga, form = form, hitEnemigo = hitEnemigo, hitAliado = hitAliado,
        error = error, hundidoEnemigo = hundidoEnemigo, hundidoAliado = hundidoAliado, 
        ganador = ganador, nombre = nombre, primero = 1)

