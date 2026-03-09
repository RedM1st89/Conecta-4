import numpy as np

FILAS = 6
COLUMNAS = 7
ULTIMA_FILA = 0

def crear_tabla():
    tabla = np.zeros((FILAS, COLUMNAS))
    return tabla

def decidir_turno():
    while(True):
        turno_seleccionado = int(input("Ingresa el turno que jugaras tu 1ro o 2do (1-2)"))
        if turno_seleccionado == 1 or turno_seleccionado == 2:
            break
        else:
            print("Ingresa una decision aceptable")
    #Aqui estamos haciendo que para el resto del juego, si le toca a la IA primero siempre sera cuando turno palanca sea 1 entonces si el jugador eligio ser 2, el primer turno
    #sera 1, mientras que si eligen jugar primero el 1er turno sera 0 osea no de la IA
    turnoIA = turno_seleccionado - 1
    return turnoIA

def poner_pieza(tabla, fila, col, pieza):
    tabla[fila][col] = pieza

def checar_jugada(tabla, col):
    return tabla[FILAS-1][col] == 0

def caida_pieza(tabla, col):
    for fila in range(FILAS):
        if tabla[fila][col] == 0:
            return fila

def imprimir_tabla(tabla):
    print(np.flip(tabla, 0))

def turno_IA():
    pass

        
fin = False
tabla = crear_tabla()
turno_palanca = decidir_turno()

while not fin:
    if turno_palanca == 0:
            columna = int(input("Jugador ingresa en que casilla quieres meter la ficha (0-6)"))
            if checar_jugada(tabla, columna):
                fila = caida_pieza(tabla, columna)
                poner_pieza(tabla, fila, columna, 1)
                imprimir_tabla(tabla)
                turno_palanca = 1
            else:
                print("Jugador ingresa un movimiento apropiado")
    else:
        columna = int(input("IA ingresa en que casilla quieres meter la ficha (0-6)"))
        if checar_jugada(tabla, columna) == True:
            fila = caida_pieza(tabla, columna)
            poner_pieza(tabla, fila, columna, 2)
            imprimir_tabla(tabla)
            turno_palanca = 0
        else:
            print("Uh oh")