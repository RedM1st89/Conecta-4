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
    return turno_seleccionado == 1

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

def checar_victoria(tabla, pieza):
    #Chequeo horizontal
    for c in range(COLUMNAS - 3):
        for f in range(FILAS):
            if tabla[f][c] == pieza and tabla[f][c+1] == pieza and tabla[f][c+2] == pieza and tabla[f][c+3] == pieza:
                return True
    #Chequeo vertical
    for c in range(COLUMNAS):
        for f in range(FILAS - 3):
            if tabla[f][c] == pieza and tabla[f+1][c] == pieza and tabla[f+2][c] == pieza and tabla[f+3][c] == pieza:
                return True
    #Chequeo diagonal positivo
    for c in range(COLUMNAS - 3):
        for f in range(FILAS - 3):
            if tabla[f][c] == pieza and tabla[f+1][c+1] == pieza and tabla[f+2][c+2] == pieza and tabla[f+3][c+3] == pieza:
                return True
    #Chequeo diagonal negativo
    for c in range(COLUMNAS - 3):
        for f in range(3, FILAS):
            if tabla[f][c] == pieza and tabla[f-1][c-1] == pieza and tabla[f-2][c-2] == pieza and tabla[f-3][c-3] == pieza:
                return True 


def turno_IA():
    pass

        
fin = False
tabla = crear_tabla()
turno_jugador = decidir_turno()
jugador = 1
bot = 2

while not fin:
    if turno_jugador == True:
            columna = int(input("\nJugador ingresa en que casilla quieres meter la ficha (0-6)"))
            if columna < 6 and columna >= 0:
                if checar_jugada(tabla, columna):
                    fila = caida_pieza(tabla, columna)
                    poner_pieza(tabla, fila, columna, jugador)
                    imprimir_tabla(tabla)
                    if checar_victoria(tabla, 1):
                        print("\n\nGanador Jugador humano!!")
                        fin = True
                    turno_jugador = False
                else:
                    print("\nJugador ingresa un movimiento apropiado")
            else:
                print("\n Ingresa un numero correcto ")
    else:
        columna = int(input("\nIA ingresa en que casilla quieres meter la ficha (0-6)"))
        if checar_jugada(tabla, columna) == True:
            fila = caida_pieza(tabla, columna)
            poner_pieza(tabla, fila, columna, bot)
            imprimir_tabla(tabla)
            if checar_victoria(tabla, 2):
                    print("\n\nGanador IA!!")
                    fin = True
            turno_jugador = True
            
        else:
            print("\nUh oh")