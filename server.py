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
import aes_algo
from threading import Thread
import hashlib
import pickle

sharedSecret = ''

def setSecret(value):
    global sharedSecret
    sharedSecret = value

def get_portnum():
    portnum = input("Please enter Port Number: ")
    portnum = int(portnum)
    return portnum

PORT = 2008

class Server(dh_algo.DH_Endpoint):
    def __init__(self, shared_secret_value, port):
        public_key1 = sympy.nextprime(shared_secret_value)
        public_key2 = 255
        super().__init__(public_key1, public_key2)
        self.flag_generated_key = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('',port))
        self.s.listen()
        self.conn, addr = self.s.accept()
        self.aesfunc = None
        print('(System) Connected by: ', addr)
        msg = '(System) Connected by: ', addr
        stepThrough(msg)

    def authenticate(self): # listen and print out messages
        partial_key = self.generate_partial_key()
        self.conn.send(bytes([partial_key]))
        while True:
            data = self.conn.recv(1024) # Limit message size to 1024 bytes?
            if not data: # At end of message break
                break # at s.close on the connection it closes
            try:
                partial_key_client = int.from_bytes(data, byteorder='little') 
                full_key = self.generate_full_key(partial_key_client)
                if len(full_key) == 16:
                    pass
                elif len(full_key) > 16:
                    full_key = full_key[:16]
                else:
                    padded_zeroes_req = 16 - len(full_key)
                    full_key = "0" * padded_zeroes_req + full_key
                # print("Full key is {}".format(full_key))
                self.flag_generated_key = True
                print("(System) Server symmetric key (" + full_key + ") has been created.\n")
                msg = "(System) Server symmetric key (" + full_key + ") has been created.\n"
                stepThrough(msg)
                self.aesfunc = aes_algo.Rijndael(full_key)
                break
            except:
                print("Error.")
                stepThrough("Error.")
    
    def communicate(self):
        while True:
            data = self.conn.recv(1024) # Limit message size to 1024 bytes?
            if not data: # At end of message break
                print('no data')
                stepThrough('no data')

                # break # at s.close on the connection it closes
            else:
                dict_msg = pickle.loads(data)
                decoded_data = dict_msg.get('e')
                hash_msg = dict_msg.get('h')
                iterations_decrypt = len(decoded_data) // 16
                padded_plaintext_message = ""
                for i in range(iterations_decrypt):
                    partial_ciphermessage = decoded_data[i * 16:i * 16 + 16]
                    decrypted_partial = self.aesfunc.decrypt(partial_ciphermessage)
                    padded_plaintext_message += decrypted_partial
                padding_stops = padded_plaintext_message.index("1")

                #update UI
                recText.set(padded_plaintext_message[padding_stops + 1:])

                print(padded_plaintext_message[padding_stops + 1:])
                hashed_aes = hashlib.md5(padded_plaintext_message[padding_stops + 1:].encode('utf-8'))
                # print('hash is {}'.format(hash_msg))
                # print('aes is {}'.format(hashed_aes))
                if hashed_aes.hexdigest() == hash_msg:
                    print("(System) Message integrity has been confirmed.\n")
                    stepThrough("(System) Message integrity has been confirmed.\n")
                else:
                    print("(System) Message integrity has been compromised.\n")
                    stepThrough("(System) Message integrity has been compromised.\n")

    
    def send_encrypted(self, message):
        if self.flag_generated_key:
            hash_msg = hashlib.md5(message.encode('utf-8'))
            zeroes_req = 15 - len(message) % 16
            padded_message = "0" * zeroes_req + "1" + message
            iterations_encrypt = len(padded_message) // 16
            ciphertext_message = ""
            for i in range(iterations_encrypt):
                partial_plainmessage = padded_message[i * 16:i * 16 + 16]
                encrypted_partial = self.aesfunc.encrypt(partial_plainmessage)
                ciphertext_message += encrypted_partial
            dict_msg = {'e':ciphertext_message,'h':hash_msg.hexdigest()}
            json_msg = pickle.dumps(dict_msg)
            # self.s.send(ciphertext_message.encode('utf-8'))
            self.conn.send(json_msg)
            print("(System) Encrypted message has been sent.\n")
            stepThrough("(System) Encrypted message has been sent.\n")

#shared_secret_value = input("Please enter 3-digit Shared Secret Value: ") #p
# server = Server(shared_secret_value)
# server.authenticate()
# communicate_thread = Thread(target=server.communicate)
# communicate_thread.start()
# while True:
#     message = input()
#     server.send_encrypted(message)

def openServer(sharedSecret, port):
    global server
    server = Server(sharedSecret, port)
    server.authenticate()
    communicate_thread = Thread(target=server.communicate)
    communicate_thread.start()

def encryptAndSend(message):
    global server
    server.send_encrypted(message)

def getUIFields(recieved, state):
    global recText
    global status
    recText = recieved
    status = state

def stepThrough(message):
    global status
    status.set(message)

    # TODO:
    willStep = True
    if willStep:
        print('need to wait for input')
    

server = None
recText = None
status = None