# Bibliotecas
import requests
import json
from random import choice
from random import randint
#Descargar la extension tabulate
#from tabulate import tabulate

#Constantes del programa
N_VUELO = 3421
PASAJE = 22000
DESCUENTO = 0.1
VENDER = 1
CERRAR = 2
SALIR = 3
FILAS = ["  ", "A","B","C","D","E","F"]
LETRAS = ["A","B","C","D","E","F"]

#Estructuras

# printea las opciones y comandos para usar el programa.
def display_menu():
    print(" 1 - VENDER PASAJE")
    print(" 2 - CERRAR VUELO")
    print(" 3 - FINALIZAR ")

# devuelve un esquema printeable del avion.
def esquema_avion():
    avion = []
    avion.append(FILAS)
    for i in range(1,25):
        avion.append([])

        for j in range(7):
            if j == 0:
                fila =  i
                if i < 10:
                    avion[fila].append(str(fila) + " ")
                else:
                    avion[fila].append(str(fila))
            else:
                avion[i].append("-")
    return avion

# agrega un pasajero a la lista de pasajeros
def agregar_pasajero(lista, fila, columna, asiento):
    
    nombre = input("Ingrese su nombre: ")
    posicion = asiento
    domicilio = input("Ingrese su domicilio: ")
    domic_normalizado = normalizar_direccion(domicilio)
    domic = domic_normalizado[0]
    costo =  domic_normalizado[1]
    persona = {"nombre": nombre, "asiento": posicion, "domicilio_normalizado": domic, "costo": costo}
    lista.append(persona)
    return lista
    
    
# vender pasaje
def vender(avion, lista):
    print("-------------------")
    for i in range(0,25):
        print(avion[i])
    print("--------------------")
    print("Elija el asiento: ")
    elegir = int(input("Ingrese 1 para elegir o 0 para que se le asigne al azar: "))

    libre = False
    while libre == False:
        
        if elegir == 1:
            asiento = [int(input("Ingrese la fila: ")), input("Ingrese la letra: ")]
        else:
            print ("seleccionando ubicacion aleatoria disponible")
            asiento = [randint(1,24), choice(LETRAS)]
        fila = asiento[0]

        #Usaria asiento[1] in ("Aa") o un asiento[1].upper() == A
        #Lo mismo para los elifs
        if asiento[1] in ("Aa"):
            columna = 1
        elif asiento[1] in ("Bb"):
            columna = 2
        elif asiento[1] in ("Cc"):
            columna = 3
        elif asiento[1] in ("Dd"):
            columna = 4
        elif asiento[1] in ("Ee"):
            columna = 5
        elif asiento[1] in ("Ff"):
            columna = 6
        libre = esta_libre(avion, fila, columna)
        if libre == False:
            print("el asiento esta ocupado")
        else: 
            print("asiento disponible")

    avion[fila][columna] = "×" 
    
    lista = agregar_pasajero(lista,fila,columna,asiento)
    
    return [avion, lista]

# devuelve en un booleano si el asiento dado esta ocupado
def esta_libre(avion, fila, columna): 
    if avion[fila][columna] == "×":
        return False
    else:
        return True

# devuelve la direccion normalizada de gba en un string y un precio
def normalizar_direccion(direccion):
    url = "http://servicios.usig.buenosaires.gob.ar/normalizar/?direccion="
    response = requests.get(url + direccion)
    jsonobj = json.loads(response.content)
    dom = jsonobj["direccionesNormalizadas"][0]

    precio = PASAJE
    partido = dom["cod_partido"]

    if partido == "caba":
        precio = PASAJE - (PASAJE * DESCUENTO)

    res = [str(dom), precio]
    return res

# devuelve un string con el porcentaje de ocupacion
def porcentaje_ocupacion(avion):
    cant = 0
    for i in range(24):
        for j in range(7):
            if esta_libre(avion,i,j) == False:
                cant += 1
    porcentaje = float((cant / 120) * 100)
    imprimir = "El porcentaje de ocupación es: "+ str(porcentaje)+"%"
    return imprimir

def __main__():
    avion = esquema_avion()
    pasajeros = []

    display_menu()
    opcion = int(input("Ingrese su opcion: "))

    while opcion != 1 and opcion != 2 and opcion != 3:
        opcion = int(input("No es valida la opcion, indique devuelta :"))
    
    while opcion != SALIR:
        
        if opcion == VENDER:
            venta = vender(avion, pasajeros)
            avion = venta[0]
            pasajeros = venta[1]
           
        if opcion == CERRAR:
            cant = 1
            nombre_archivo = "vuelo{}.txt".format(N_VUELO)
            f = open(nombre_archivo, "w")
            for i in pasajeros:
                imprimir = "{}) {}, {}, {}. Precio: {}".format(cant, i["nombre"], i["asiento"], i["domicilio_normalizado"], i["costo"])
                print(imprimir)
                f.write(imprimir)
                cant += 1
            imprimir = "La cantidad de pasajeros es {}".format(len(pasajeros))
            f.write(imprimir)
            imprimir = "Porcentaje de ocupacion: {}".format(porcentaje_ocupacion(avion))
            f.write(imprimir)

            f.close()

        display_menu()
        opcion = int(input("Ingrese otra opcion: "))

        while opcion != 1 and opcion != 2 and opcion != 3:
            opcion = int(input("No es valida la opcion, indique devuelta: "))

__main__()
