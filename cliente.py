import socket
import numpy as np

print("Inserta la direccion ip del servidor")
HOST = input()  # The server's hostname or IP address
PORT = 54321  # The port used by the server
buffer_size = 1024
#print("Introduce la Ip del servidor")
#HOST = input()

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    data = client_socket.recv(buffer_size).decode('utf-8') # Resive bienveidida
    print(data)

    
    #------------------------------Inicio del juego-------------
    while True:

        #------Selecciona dificultad-------------
        dificultad = input()
        client_socket.sendall(dificultad.encode('utf-8'))

        # Recive si la opcion no es valida
        data = client_socket.recv(buffer_size).decode('utf-8')  # Resive dificultad
        # Mientras el mensaje no sea una opcion no valida
        while data == 'Opcion no valida, inserta "F" para facil y "D" para dificil' or not (dificultad == "end" or dificultad == "") :
            print(data, end = "\n\n")
            dificultad = input()
            client_socket.sendall(dificultad.encode('utf-8'))
            data = client_socket.recv(buffer_size).decode('utf-8')

        if dificultad == "end" or dificultad == "":
            print("Desconectandose del servidor...")
            break

        if dificultad == "F" :
            matriz = np.zeros((9,9))
        else :
            matriz = np.zeros((16,16))

        print(data)
        

        while not (data == "Perdiste" or data == "Ganaste") :
            casilla = input(); 
            client_socket.sendall(casilla.encode('utf-8'))
            data = client_socket.recv(buffer_size).decode('utf-8')
            if data == "Perdiste" or data == "Ganaste" :
                posicion = casilla.split(",")
                matriz[int(posicion[0])-1][int(posicion[1])-1] = 8
                imprimir_matriz(matriz)
                print("\n" + data + '. Inserta "F" para facil y "D" para dificil, para salir pon "end"')
            else : 
                posicion = casilla.split(",")
                matriz[int(posicion[0])-1][int(posicion[1])-1] = 1
                imprimir_matriz(matriz)