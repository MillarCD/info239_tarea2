import socket
import time
import random

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
rangeSleep = range(2,5) # <-- cambiar al finalizar el trabajo
perdida = 0.3
timeout = 5
names = {}

# Quita los bits que añade CRC y retorna el mensaje en binario
# mas el bit para manejo de duplicidad
def CRC_decode( CRCMsg: str ) -> tuple:
    r = 3
    msg_bitMD = CRCMsg[:-r]
    return msg_bitMD[:-1], int(msg_bitMD[-1])

def decodeMsg( binMessage: str ) -> chr:
    return chr(int(binMessage,2)) 

def insertNewPort( diccPorts: dict, newPort: int ) -> dict:
    newDiccPorts = diccPorts.copy()

    newDiccPorts.update( {
        newPort: {
            'name': '',
            'bitMD': 1,
        }
    })

    return newDiccPorts

def updateData( data: dict, c: chr ) -> dict:
    newData = data.copy()

    newData['name'] += c
    newData['bitMD'] = data.get('bitMD') ^ 1 # XOR

    return newData 



# MAIN()

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.settimeout(timeout)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("Link Available")

# Listen for incoming datagrams
while(True):
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        [ message, address ] = bytesAddressPair
        _, clientPort = address
        
        print(f'clientPort: {clientPort}, msg: {message.decode()}')

        # validar si el cliente existe o crear uno
        if (names.get(clientPort)==None):
            names = insertNewPort( names, clientPort )
        

        print("Link bussy")


        # Probabilidad de perdida
        if (random.random()<=perdida):
            print('hubo perdida')
            bytesToSend = str.encode('NAK')

        else:
            # se decodifica el mensaje y se guarda en names
            binMsg, bitMD = CRC_decode(message.decode())
            msg = decodeMsg( binMsg )

            print(f'char: {msg}')

            clientData = names.get(clientPort)
            # comprueba si el mensaje ya ha sido procesado
            # con el bit de manejo de duplicidad
            lastBitMD = bitMD
            if ( bitMD != clientData.get('bitMD') ):
                names.update({ 
                    clientPort: updateData( clientData, msg )
                })
                lastBitMD = bitMD ^ 1
            bytesToSend = str.encode(f'{lastBitMD}-ACK') 
            
            print(f'name: {names.get(clientPort).get("name")}')


        # Tiempo de retardo
        sleep = random.choice(rangeSleep)
        print(f'sleep: {sleep}')
        time.sleep(sleep)
            
        # Sending a reply to client
        print(f'bytesTosend: {bytesToSend}')
        UDPServerSocket.sendto(bytesToSend, address)
        print()
        print("Link Available")

    except TimeoutError:
        print("Tiempo de espera agotado\nNombres:")
        for i, name in enumerate(names.values()):
            print(f'{i}. {name.get("name")}')
        break

print("fin del programa")


