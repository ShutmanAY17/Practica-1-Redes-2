import random
import numpy as np

# --------------------Codigo para el servidor------------------------------

def crear_matriz(dificultad: str):

    if dificultad == "F" :
        size = 9
        minas = 10
    elif dificultad == "D" :
        size = 16
        minas = 40
    else:
        return 'Opcion no valida, inserta "F" para facil y "D" para dificil\nPara salir pon "end"', False

    matriz = np.zeros((size,size))
    count = 1
    while count <= minas :
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        
        if matriz[x][y] == 0 :
            matriz[x][y] = 1
            count = count + 1

    return matriz, True


def jugar(matriz: np.ndarray, casilla:str):     #Ejemplo de casilla: 16,16
    posicion = casilla.split(",")
    if matriz[int(posicion[0])-1][int(posicion[1])-1] == 0:
        print("Bien")
        return False
    else:
        print("Perdiste")
        return True

# --------------------Codigo para el cliente------------------------------

def imprimir_matriz(matriz: np.ndarray) :
    cadena: str = "   "

    for j in range(0, matriz.shape[0]+1): # Vertical
        
        for i in range(0, matriz.shape[0]+1) : # Lateral
            if j == 0:
                if i == 0:
                    print(cadena, end="")
                else:
                    cadena = cadena[:1] + str(i) + cadena[len(str(i))+1:]
                    if i == matriz.shape[0]:
                        print(cadena)
                    else:
                        print(cadena, end="")
                    cadena = "   "
            else:
                if i == 0:
                    cadena = cadena[:0] + str(j) + cadena[len(str(j)):]
                    print(cadena, end="")
                    cadena = "   "
                else:
                    cadena = cadena[:1] + str(int(matriz[j-1][i-1])) + cadena[2:]
                    if i == matriz.shape[0]:
                        print(cadena)
                    else:
                        print(cadena, end="")
                    cadena = "   "

a = crear_matriz("D")
imprimir_matriz(a[0])