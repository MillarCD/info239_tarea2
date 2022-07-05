import socket

msgFromClient       ="name"
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
timeout             = 2 # segundos

# transforma el caracter en una string de 0s y 1s
def binaryTranslate( char: chr ) -> str:
    asciiChar = ord(char)
    binChar = bin(asciiChar)
    # añade los ceros restantes para tener largo 8
    return f'{"0"*( 8%len(binChar[2:]) )}{binChar[2:]}' 


# aplica mecanismo CRC al mensaje
def CRC( msg: str ) -> str:
    gx = '1011' # <- polinimio generador x^3 + x + 1
    r = '0'*(len(gx)-1)
    crcMsg = f'{msg}{r}'
    crcMsg = f'{msg}{binaryDiv( crcMsg, gx )}'

    return crcMsg

def binaryDiv( msg: str, gx: str ) -> str:
    if ( len(msg) < len(gx) ):
        return msg
    
    elif ( msg[0] == '0' ):
        return binaryDiv( msg[1:], gx )

    resto = ''
    for msg_i, gx_i in zip(msg, gx):
        resto += str( int(msg_i) ^ int(gx_i) )

    return binaryDiv( f'{resto}{msg[len(gx):]}', gx )


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

    print(f"Message from Server {res}, character: {msgFromClient[index]}, bitMD: {index%2}")
    print()
    # asegura que la respuesta sea exitosa y para el msg correspondiente
    if (res[2:] == 'ACK' and int(res[0])==index%2):
        index += 1
