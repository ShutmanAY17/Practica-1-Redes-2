import socket
import random
import numpy as np

print("Incerta la ip del servidor")
HOST = input() # El hostname o IP del servidor
PORT = 54321  # El puerto que usa el servidor
buffer_size = 1024
msg = 'Bienvenido al buscaminas, inserta "F" para facil y "D" para dificil\nPara salir inserta "end"'
msg_in_btyes = msg.encode('utf-8')  # Transforma de stringa a bytes

# --------------------Funciones para eñl Busca minas--------------------------------

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

# -------------------------------------------------------------------------------------------------------

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:   # El segundo parametro dice que es udp el socket
    #--------------------------------Conexion con el cliente-----------------------------------
    server_socket.bind((HOST, PORT)) 
    server_socket.listen()
    print("Servidor de Buscaminas activo, esperando peticiones\n")
    client_conn, client_addr = server_socket.accept()           
    
    #-------------------------Usa el socket del cliente para enviar mensajes--------------------------------
    with client_conn:
        
        print("Conectado al cliente con la ip", client_addr)
        client_conn.sendall(msg_in_btyes) # Bienvenida y dificultad

    #-----------------------------------------Inicio del juego--------------------------------------------------
        while True:                   
            data = client_conn.recv(buffer_size).decode('utf-8')  #Mensaje con la dificultad
            
            matriz = crear_matriz(data)
            
            while not matriz[1] and not (data == "end" or data == ""):                # Si la opcion es invalida se mantiene en un ciclo hasta que sea valida
                client_conn.sendall(matriz[0].encode('utf-8'))
                data = client_conn.recv(buffer_size).decode('utf-8')
                matriz = crear_matriz(data)

            if data == "end" or data == "":       # Si el jugador manda end o no manda nada termina el programa
                print("\nDesconectandose del cliente...")
                break
            
            if data == "F" :         # Si es facil el numero de casillas sin mina es 72
                num_casillas = 71
            else :
                num_casillas = 216

            client_conn.sendall(b'Mapa creado\nPara seleccionar una casilla inserta Fila,Columna\n Ejemplo: 6,9')
            casillas_abiertas = 0
            perder = False

            #------------------Tiradas del cliente hasta que pierda o abra todas las casillas----------------------
            while True: 
                data = client_conn.recv(buffer_size).decode('utf-8')      # Coordenada
                perder = jugar(matriz[0], data)   
                casillas_abiertas = casillas_abiertas + 1
                if perder : 
                    client_conn.sendall(b'Perdiste')
                    break
                else :
                    client_conn.sendall(b'Bien')
                if casillas_abiertas == num_casillas:
                    client_conn.sendall(b'Ganaste')
                    print(data)
                    break

            


