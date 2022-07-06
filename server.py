import socket
import time
import random
from utils import CRC_decode, decodeMsg

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
rangeSleep = range(500,3000) # tiempo en mseg 
perdida = 0.3
timeout = 5
names = {}

def insertNewClient( diccPorts: dict, newPort: int ) -> dict:
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
        

        # validar si el cliente existe o crear uno
        if (names.get(clientPort)==None):
            names = insertNewClient( names, clientPort )
        
        print(f"Link bussy, client: {clientPort}")

        # Probabilidad de perdida
        if (random.random()<=perdida):
            print(f'hubo perdida')
            bytesToSend = str.encode('NAK')

        else:
            # se decodifica el mensaje y se guarda en names
            binMsg, bitMD = CRC_decode(message.decode())
            if( binMsg == None ):
                bytesToSend = str.encode('NAK')
            else:
                msg = decodeMsg( binMsg )

                print(f'char: {msg} ', end=' ')

                clientData = names.get(clientPort)
                # comprueba si el mensaje ya ha sido procesado
                # con el bit de manejo de duplicidad
                lastBitMD = bitMD
                if ( bitMD != clientData.get('bitMD') ):
                    names.update({ 
                        clientPort: updateData( clientData, msg )
                    })

                bytesToSend = str.encode(f'{lastBitMD}-ACK') 
            
                print(f'name: {names.get(clientPort).get("name")}')


        # Tiempo de retardo
        sleep = (random.choice(rangeSleep)) / 1000
        print(f'sleep: {sleep}')
        time.sleep(sleep)
            
        # Sending a reply to client
        print(f'bytesTosend: {bytesToSend}')
        UDPServerSocket.sendto(bytesToSend, address)
        print()

    except TimeoutError:
        print("Tiempo de espera agotado\nNombres:")
        for i, name in enumerate(names.values()):
            print(f'{i}. {name.get("name")}')
        break

print("fin del programa")


