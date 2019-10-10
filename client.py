import socket

sharedSecret = ''

def setSecret(value):
    global sharedSecret
    sharedSecret = value

# input: 
# 1. symmetric key
# 2. ip of other computer

def encrypt(message):
    message = message%5
    return message

def get_hostname():
    hostname = input("Enter Host name:")
    return hostname
def get_portnum():
    portnum = input("Enter port number:")
    return portnum
def get_symmetrickey():
    sym_key = input("Enter symmetric key:")
    return sym_key

def clientSend(hostInfo, isIP, port):
    # HOST = '127.0.0.1'  # The server's hostname or IP address
    # PORT = 65432        # The port used by the server
    HOST = get_hostname()
    PORT = get_portnum()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

    print('Received', repr(data)) #repr returns string of data
