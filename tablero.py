import numpy as np
import pygame
import sys
import math
import random

FILAS = 6
COLUMNAS = 7
COLOR = 0, 0, 255
BG = 0, 0, 0
COLORJUGADOR = 255, 191, 0
COLORIA = 255, 0, 0

# Constantes para mejor legibilidad
VACIO = 0
JUGADOR = 1
IA = 2
VENTANA_LONGITUD = 4

def crear_tabla():
    tabla = np.zeros((FILAS, COLUMNAS))
    return tabla

def decidir_turno():
    while(True):
        turno_seleccionado = int(input("Ingresa el turno que jugara el contrincante 1ro o 2do (1-2): "))
        if turno_seleccionado == 1 or turno_seleccionado == 2:
            break
        else:
            print("Ingresa una decision aceptable")
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
    # Chequeo horizontal
    for c in range(COLUMNAS - 3):
        for f in range(FILAS):
            if tabla[f][c] == pieza and tabla[f][c+1] == pieza and tabla[f][c+2] == pieza and tabla[f][c+3] == pieza:
                return True
    # Chequeo vertical
    for c in range(COLUMNAS):
        for f in range(FILAS - 3):
            if tabla[f][c] == pieza and tabla[f+1][c] == pieza and tabla[f+2][c] == pieza and tabla[f+3][c] == pieza:
                return True
    # Chequeo diagonal positivo
    for c in range(COLUMNAS - 3):
        for f in range(FILAS - 3):
            if tabla[f][c] == pieza and tabla[f+1][c+1] == pieza and tabla[f+2][c+2] == pieza and tabla[f+3][c+3] == pieza:
                return True
    # Chequeo diagonal negativo
    for c in range(COLUMNAS - 3):
        for f in range(3, FILAS):
            if tabla[f][c] == pieza and tabla[f-1][c+1] == pieza and tabla[f-2][c+2] == pieza and tabla[f-3][c+3] == pieza:
                return True 

def dibujar_tabla(tabla):
    for c in range(COLUMNAS):
        for f in range(FILAS):
            pygame.draw.rect(pantalla, COLOR, (c*TAMANO, f*TAMANO+TAMANO, TAMANO, TAMANO))
            pygame.draw.circle(pantalla, BG, (int(c*TAMANO+TAMANO/2), int(f*TAMANO+TAMANO+TAMANO/2)), RADIO)
    for c in range(COLUMNAS):
        for f in range(FILAS):
            if tabla[f][c] == 1:
                pygame.draw.circle(pantalla, COLORJUGADOR, (int(c*TAMANO+TAMANO/2), altura - int(f*TAMANO+TAMANO/2)), RADIO)
            elif tabla[f][c] == 2:
                pygame.draw.circle(pantalla, COLORIA, (int(c*TAMANO+TAMANO/2), altura - int(f*TAMANO+TAMANO/2)), RADIO)
    pygame.display.update()


#Algoritmo Minimax

def evaluar_ventana(ventana, pieza):
    score = 0
    pieza_rival = JUGADOR if pieza == IA else IA

    # Evaluación ofensiva
    if ventana.count(pieza) == 4:
        score += 100
    elif ventana.count(pieza) == 3 and ventana.count(VACIO) == 1:
        score += 5
    elif ventana.count(pieza) == 2 and ventana.count(VACIO) == 2:
        score += 2

    # Evaluación defensiva (bloquear al rival)
    if ventana.count(pieza_rival) == 3 and ventana.count(VACIO) == 1:
        score -= 4

    return score

def score_posicion(tabla, pieza):
    score = 0
    
    # 1. Priorizar el centro (Heurística clave)
    centro_array = [int(i) for i in list(tabla[:, COLUMNAS//2])]
    centro_count = centro_array.count(pieza)
    score += centro_count * 3

    # 2. Horizontal
    for f in range(FILAS):
        fila_array = [int(i) for i in list(tabla[f,:])]
        for c in range(COLUMNAS - 3):
            ventana = fila_array[c:c+VENTANA_LONGITUD]
            score += evaluar_ventana(ventana, pieza)

    # 3. Vertical
    for c in range(COLUMNAS):
        col_array = [int(i) for i in list(tabla[:,c])]
        for f in range(FILAS - 3):
            ventana = col_array[f:f+VENTANA_LONGITUD]
            score += evaluar_ventana(ventana, pieza)

    # 4. Diagonal Positiva
    for f in range(FILAS - 3):
        for c in range(COLUMNAS - 3):
            ventana = [tabla[f+i][c+i] for i in range(VENTANA_LONGITUD)]
            score += evaluar_ventana(ventana, pieza)

    # 5. Diagonal Negativa
    for f in range(FILAS - 3):
        for c in range(COLUMNAS - 3):
            ventana = [tabla[f+3-i][c+i] for i in range(VENTANA_LONGITUD)]
            score += evaluar_ventana(ventana, pieza)

    return score

def obtener_posiciones_validas(tabla):
    posiciones_validas = []
    for col in range(COLUMNAS):
        if checar_jugada(tabla, col):
            posiciones_validas.append(col)
    return posiciones_validas

def es_nodo_terminal(tabla):
    return checar_victoria(tabla, JUGADOR) or checar_victoria(tabla, IA) or len(obtener_posiciones_validas(tabla)) == 0

def minimax(tabla, profundidad, alpha, beta, maximizandoJugador):
    posiciones_validas = obtener_posiciones_validas(tabla)
    es_terminal = es_nodo_terminal(tabla)
    
    # Condición de salida de la recursividad
    if profundidad == 0 or es_terminal:
        if es_terminal:
            if checar_victoria(tabla, IA):
                return (None, 10000000000000) # Gana la IA
            elif checar_victoria(tabla, JUGADOR):
                return (None, -10000000000000) # Gana el contrincante
            else: # Empate
                return (None, 0)
        else: # Profundidad 0
            return (None, score_posicion(tabla, IA))
            
    if maximizandoJugador:
        value = -math.inf
        columna_elegida = random.choice(posiciones_validas)
        for col in posiciones_validas:
            fila = caida_pieza(tabla, col)
            copia_tabla = tabla.copy()
            poner_pieza(copia_tabla, fila, col, IA)
            nuevo_score = minimax(copia_tabla, profundidad - 1, alpha, beta, False)[1]
            if nuevo_score > value:
                value = nuevo_score
                columna_elegida = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break # Poda Alfa-Beta
        return columna_elegida, value
        
    else: # Minimizando al jugador
        value = math.inf
        columna_elegida = random.choice(posiciones_validas)
        for col in posiciones_validas:
            fila = caida_pieza(tabla, col)
            copia_tabla = tabla.copy()
            poner_pieza(copia_tabla, fila, col, JUGADOR)
            nuevo_score = minimax(copia_tabla, profundidad - 1, alpha, beta, True)[1]
            if nuevo_score < value:
                value = nuevo_score
                columna_elegida = col
            beta = min(beta, value)
            if alpha >= beta:
                break # Poda Alfa-Beta
        return columna_elegida, value

fin = False
tabla = crear_tabla()
turno_jugador = decidir_turno() # Determina de quién es el primer turno

pygame.init()

TAMANO = 100
RADIO = int(TAMANO/2-5)
longitud = COLUMNAS * TAMANO
altura = (FILAS+1) * TAMANO
total = (longitud, altura)

pantalla = pygame.display.set_mode(total)
dibujar_tabla(tabla)
pygame.display.update()

# Bucle principal
while not fin:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
            
        if evento.type == pygame.MOUSEMOTION:
            pygame.draw.rect(pantalla, BG, (0,0, longitud, TAMANO))
            posx = evento.pos[0]
            if turno_jugador:
                pygame.draw.circle(pantalla, COLORJUGADOR, (posx, int(TAMANO/2)), RADIO)
            pygame.display.update()
            
        # Cuando el contrincante hace click
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(pantalla, BG, (0,0, longitud, TAMANO))
            
            if turno_jugador:
                posx = evento.pos[0]
                columna = int(math.floor(posx/TAMANO))
                
                if columna <= 6 and columna >= 0:
                    if checar_jugada(tabla, columna):
                        fila = caida_pieza(tabla, columna)
                        poner_pieza(tabla, fila, columna, JUGADOR)
                        
                        if checar_victoria(tabla, JUGADOR):
                            print("\n\n¡Ganador Jugador Humano!")
                            fin = True
                            
                        turno_jugador = False # Cede el turno al Bot
                        imprimir_tabla(tabla)
                        dibujar_tabla(tabla)
                    else:
                        print("\nMovimiento inválido: Columna llena.")
                else:
                    print("\nNúmero fuera de rango.")

    # Cuando es el turno de la IA 
    if not turno_jugador and not fin:
        # Llamamos al algoritmo con una profundidad de 5
        columna, minimax_score = minimax(tabla, 5, -math.inf, math.inf, True)
        
        # Validar jugada y colocar pieza
        if checar_jugada(tabla, columna):
            fila = caida_pieza(tabla, columna)
            poner_pieza(tabla, fila, columna, IA)
            
            if checar_victoria(tabla, IA):
                print("\n\n¡Ganador la Inteligencia Artificial!")
                fin = True
                
            imprimir_tabla(tabla)
            dibujar_tabla(tabla)
            
            turno_jugador = True # Cede el turno

    if fin:
        pygame.time.wait(3000) # Esperar 3 segundos para que el usuario vea el resultado