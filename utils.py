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


# Quita los bits que añade CRC y retorna el mensaje en binario
# mas el bit para manejo de duplicidad
def CRC_decode( CRCMsg: str ) -> tuple:
    gx = '1011' # <- polinimio generador x^3 + x + 1
    r = len(gx)-1

    if (binaryDiv( CRCMsg, gx ) != '000'): # El mensaje llego corrompido
        print('\n hola \n')
        return None, None

    msg_bitMD = CRCMsg[:-r]
    return msg_bitMD[:-1], int(msg_bitMD[-1])
    

def binaryDiv( msg: str, gx: str ) -> str:
    if ( len(msg) < len(gx) ):
        return msg
    
    elif ( msg[0] == '0' ):
        return binaryDiv( msg[1:], gx )

    resto = ''
    for msg_i, gx_i in zip(msg, gx):
        resto += str( int(msg_i) ^ int(gx_i) )

    return binaryDiv( f'{resto}{msg[len(gx):]}', gx )


def decodeMsg( binMessage: str ) -> chr:
    return chr(int(binMessage,2)) 
