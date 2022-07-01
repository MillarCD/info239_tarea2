import socket

msgFromClient       = "qwert"
serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024
timeout             = 3 # segundos

# transforma el caracter en una string de 0s y 1s
def binaryTranslate( char: chr ) -> str:
    asciiChar = ord(char)
    binChar = bin(asciiChar)
    # añade los ceros restantes para tener largo 8
    return f'{"0"*( 8%len(binChar[2:]) )}{binChar[2:]}' 

# aplica mecanismo CRC al mensaje
def CRC( msg: str ) -> str:
    gx = '1011' # <- polinimio generador x^3 + x + 1
    r = '000'
    
    crcMsg = f'{msg}{r}'
    
    # DIVISION
    index = len(r)+1
    resto = crcMsg[:len(r)+1]
    while ( index <= len(crcMsg) ):        
        if resto[0]=='0':
            if index<len(crcMsg):
                resto = resto[1:]+crcMsg[index]
            index +=1
            pass
        else:
            newResto = ''
            for resto_i, gx_i in zip(resto, gx):
                newResto += str( int(resto_i) ^ int(gx_i) )

            resto = newResto
            
    return f'{msg}{resto[1:]}'

# envia el mensaje al servidor mediante conexion UDP
# retorna ACK si la comunicacion fue exitosa y NAK si hubo perdida
def sendMsg( msg: str ) -> str:
    bytesToSend         = str.encode(msg)
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

    print(f"Message from Server {res}, character: {msgFromClient[index]}")
    print()
    # asegura que la respuesta sea exitosa y para el msg correspondiente
    if (res[2:] == 'ACK' and int(res[0])!={index%2}):
        index += 1
