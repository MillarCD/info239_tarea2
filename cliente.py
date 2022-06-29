import socket

msgFromClient       ="name_1"
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
timeout             = 3

# transforma el caracter en una string de 0s y 1s
def binaryTransformation(caracter):
    return caracter

# aplica mecanismo CRC al mensaje
def CRC(msg):
    return msg

# envia el mensaje al servidor mediante conexion UDP
# retorna ACK si la comunicacion fue exitosa y NAK si hubo perdida
def sendMsg(msg):
    bytesToSend         = str.encode(msg)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    try:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)
        res = msgFromServer[0].decode()
    except TimeoutError:
        print('TimeoutError')
        res = 'NAK'
    return res

# MAIN()

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(timeout)

# Send to server using created UDP socket
print("Intentando enviar")
index = 0;
while index<len(msgFromClient):
    binaryMsg = binaryTransformation(msgFromClient[index])
    # se le agrega un bit para manejo de duplicado
    crcMsg = CRC(f'{binaryMsg}{index%2}') 
    res = sendMsg(crcMsg)
    print(f"Message from Server {res}, character: {msgFromClient[index]}")
    if (res == 'ACK'):
        index += 1
 
