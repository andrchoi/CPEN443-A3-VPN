import socket

'''
This server waits for conenction from client and displays clients address
TODO: 
1. Encrypt data sent
2. Link to GUI
'''

sharedSecret = ''

def setSecret(value):
    global sharedSecret
    sharedSecret = value
    print('server',sharedSecret)

def openServer(port):
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    # with is constructor and at end of with it is a destructor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) #listening at localhost
        s.listen()
        conn, addr = s.accept() # Only if client is run
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024) # Limit message size to 1024 bytes?
                if not data: # At end of message break
                    break
                conn.sendall(data) # echos the data TODO change this to a reply