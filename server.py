'''
This server waits for conenction from client and displays clients address
TODO: 
1. Encrypt data sent
2. Link to GUI

The program you must create can be toggled between “client mode” and “server mode”. 
When set in server mode, the program waits for a TCP connection on a port that can be specified on the user interface (UI). 
When set in client mode, the program can initiate a TCP connection to a given host name (or IP address), on a given port; 
both the target host name (IP address) and the TCP port are specified on the UI.
The TA will choose two machines (computer A and computer B), and install one instance of your program on A and another instance on B; both 
instances will then be run, one in client mode and one in server mode, with the client connecting to the server. 
The TA will input shared secret value into “Shared Secret Value” window on both, client and server.
On A, the TA will type some text into a “Data to be Sent” window and then click a “Send” button. On B, the received text will be 
displayed in a “Data as Received” window. Similarly, it should be possible to type data at B and receive/display it at A.
By the time that the TA is ready to type into the “Data to be Sent” window, the two machines must be certain that they
 are talking to each other (i.e., no other machine is impersonating one of them) and must share a fresh symmetric key that no one else knows.
You may choose whichever mutual authentication protocol and whichever key establishment protocol (or whichever combined protocol), stream or 
block ciphers and modes of operation you wish. However, you must be able to defend why you chose it and why you feel it is suitable (i.e., sufficiently
 secure) for implementing a VPN. To keep things simple, appropriate cryptographic algorithms include AES, DES, MD5, SHA (various versions), RSA, D-H, 
 HMAC-MD5; when using these, ignore all padding rules (i.e., when padding is required, pad with zeros) and use the smallest moduli that will work.
Your UI must allow the TA to see what data is actually sent and received over the wire at each point in the setup and communication processes. The TA should be able 
to step through these processes using a “Continue” button.
'''
import socket
import json
import dh_algo
import sympy
#import updateGUI

class Server(dh_algo.DH_Endpoint):
    def __init__(self, shared_secret_value):
        public_key1 = sympy.nextprime(shared_secret_value)
        public_key2 = sympy.nextprime(public_key1//2)
        super().__init__(public_key1, public_key2)
        self.flag_generated_key = False
        self.conn = None


    def run(self, port): # listen and print out messages
        # with is constructor and at end of with it is a destructor
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('',port))
            s.listen()
            conn, addr = s.accept() # Only if client is run
            self.conn = conn
            with conn:
                print('Connected by', addr)
                partial_key = self.generate_partial_key()
                self.send(partial_key)
                while True:
                    data = conn.recv(1024) # Limit message size to 1024 bytes?
                    if not data: # At end of message break
                        break
                    try:
                        data_loaded = json.loads(data.decode('utf-8')) #data loaded
                        partial_key = data_loaded.get('p')
                        self.generate_full_key(partial_key)
                        self.flag_generated_key = True
                        print("server has created key")
                    except:
                        #TODO:
                        import updateGUI
                        updateGUI.showRecData(self.decrypt_message(data))
                        print(self.decrypt_message(data))
    
    def send(self, partial_key): # sends the partial key
            flagged_partial_key = {'p':partial_key}
            data_string = json.dumps(flagged_partial_key).encode('utf-8') #data serialized
            self.conn.sendall(data_string)
    
    def send_encrypted(self, message):
        if self.flag_generated_key:
            encrypted_message = self.encrypt_message(message)
            self.conn.sendall(encrypted_message.encode('utf-8'))
        else:
            print("Enter Shared Value first")


def openServer(sharedSecret, port):
    global server
    server = Server(sharedSecret)
    server.run(port)
    partial_key = server.generate_partial_key()
    server.send(partial_key)

def encryptAndSend(message):
    global server
    server.send_encrypted(message)

server = None
    
# server = Server(shared_secret_value)
# server.run()
# partial_key = server.generate_partial_key()
# server.send(partial_key)
# message = input("Enter message:")
# server.send_encrypted(message)