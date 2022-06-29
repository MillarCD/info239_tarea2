import socket
import time
import random

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
rangeSleep = range(500,5000) # <-- cambiar al finalizar el trabajo
perdida = 0.3
names = {}

def CRC( CRCMsg ):
    # primero que nada se le aplica decode()
    # se le quitan los bit crc y se retorna el mensaje en binario
    # y el bit para manejo de duplicado
    return CRCMsg, 0

def decodeMsg( binMessage ):
    return binMessage 

def insertNewPort( diccPorts, newPort );
    newDiccPorts = diccPorts.copy()

    newDiccPorts.update( {
        newPort: {
            'name': '',
            'bitMD': 1,
        }
    })

    return newDiccPorts

def updateData( data, c ):
    newData = data.copy()

    newData['bitMD'] = data.get('bitMD') ^ 1 # XOR
    newData['name'] += c

    return newData



# MAIN()

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("Link Available")

# Listen for incoming datagrams
while(True):
    
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    [ message, address ] = bytesAddressPair
    _, clientPort = address
    print(message.decode())

    # validar si el cliente existe o crear uno
    if (names.get(address)==None):
        names = insertNewPort( names, address )

    print("Link bussy")


    if (random.random()<=perdida):
        bytesToSend = str.encode('NAK')
    else:
        bytesToSend = str.encode('ACK') 
        # <-- aqui se decodifica el mensaje y se guarda en names
        binMsg, bitMD = CRC(message.decode())
        msg = decodeMsg( binMsg )

        clientData = names.get(clientPort)
        if ( bitMD != clientData.get('bitMD') ):
            # añadirlo al diccionario
            names.update( updateData( clientData ), msg )

    sleep = random.choice(rangeSleep)
    print(f'sleep: {sleep}')
    time.sleep(sleep)
        
    # Sending a reply to client
    UDPServerSocket.sendto(bytesToSend, address)
    print("Link Available")


