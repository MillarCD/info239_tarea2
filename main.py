import socket
from utils import binaryTranslate, CRC
import sys

msgFromClient       = sys.argv[1]
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
timeout             = 2 # segundos

# envia el mensaje al servidor mediante conexion UDP
# retorna ACK si la comunicacion fue exitosa y NAK si hubo perdida
def sendMsg( msg: str ) -> str:
    bytesToSend = str.encode(msg)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    try:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        res = msgFromServer[0].decode()
    except TimeoutError:
        res = 'TimeoutError'
    return res

# MAIN()

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(timeout)

# Send to server using created UDP socket
print("Intentando enviar")
index = 0;
while index<len(msgFromClient):
    binaryMsg = binaryTranslate(msgFromClient[index])
    # se le agrega un bit para manejo de duplicado
    crcMsg = CRC(f'{binaryMsg}{index%2}') 
    res = sendMsg(crcMsg)

    print(f"character: {msgFromClient[index]}, bitMD: {index%2}. Message from Server {res}")
    print()
    # asegura que la respuesta sea exitosa y para el msg correspondiente
    if (res[2:] == 'ACK' and int(res[0])==index%2):
        index += 1
