import socket
import json
import dh_algo
import sympy
# import aes_algo
from threading import Thread


sharedSecret = ''

def setSecret(value):
    global sharedSecret
    sharedSecret = value

HOST = 'localhost'
PORT = 2003

class Client(dh_algo.DH_Endpoint):
    def __init__(self, shared_secret_value):
        public_key1 = sympy.nextprime(shared_secret_value)
        public_key2 = sympy.nextprime(public_key1//2)
        super().__init__(public_key1, public_key2)
        self.flag_generated_key = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def authenticate(self): # sends the partial key
        partial_key = self.generate_partial_key()
        s = self.s
        s.connect((HOST, PORT)) #HOST, PORT of client
        s.send(bytes([partial_key]))
        while True:
            data = s.recv(1024) # Limit message size to 1024 bytes?
            if not data: # At end of message break
                break
            try:
                partial_key_server = int.from_bytes(data, byteorder='little') 
                full_key = self.generate_full_key(partial_key_server)
                print("Full key is {}".format(full_key))
                self.flag_generated_key = True
                print("client has created key")
                break
            except:
                print("error")
    
    def communicate(self):
        # message = input("Enter message:")
        # self.send_encrypted(message)
        s = self.s
        while True:
            data = s.recv(1024) # Limit message size to 1024 bytes?
            if not data: # At end of message break
                pass
                # break # at s.close on the connection it closes
            else:
                decrypted_msg = self.decrypt_message(data.decode('utf-8'))
                print(decrypted_msg)
                # if(decrypted_msg == "goodbye"):
                #     exit()
                # break
            
    def send_encrypted(self, message):
        if self.encrypt_message:
            encrypted_message = self.encrypt_message(message)
            self.s.send(encrypted_message.encode('utf-8'))
        else:
            print("Enter Shared Value first")


shared_secret_value = input("Enter Shared Secret Value:") #p
client = Client(shared_secret_value)
client.authenticate()
# while True:
communicate_thread = Thread(target=client.communicate)
communicate_thread.start()
# client.communicate()
# client.s.close()
while True:
    message = input("Enter message:")
    client.send_encrypted(message)

def connectClient(sharedSecret, host, isIPaddr, port):
    global client
    client = Client(sharedSecret)
    partial_key = client.generate_partial_key()
    client.send(host, port, partial_key)

def encryptAndSend(server, message):
    global client
    client.send_encrypted(message)
