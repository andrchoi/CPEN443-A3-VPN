import socket
import json
import dh_algo
import sympy

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
        print(partial_key)
        s = self.s
        s.connect((HOST, PORT)) #HOST, PORT of client
        s.send(bytes([partial_key]))
        while True:
            data = s.recv(1024) # Limit message size to 1024 bytes?
            if not data: # At end of message break
                # s.close()
                break
            try:
                partial_key_server = int.from_bytes(data, byteorder='little') 
                self.generate_full_key(partial_key_server)
                self.flag_generated_key = True
                print("client has created key")
                break
            except:
                print("error")
                # s.close()
                # print(self.decrypt_message(data.decode('utf-8')))
    
    def communicate(self):
        message = input("Enter message:")
        self.send_encrypted(message)
        s = self.s
        while True:
            data = s.recv(1024) # Limit message size to 1024 bytes?
            if not data: # At end of message break
                # s.close()
                break # at s.close on the connection it closes
            else:
                print(self.decrypt_message(data.decode('utf-8')))
                # s.close()
                break
            
    def send_encrypted(self, message):
        if self.encrypt_message:
            encrypted_message = self.encrypt_message(message)
            self.s.sendall(encrypted_message.encode('utf-8'))
            # self.s.close()
        else:
            print("Enter Shared Value first")

shared_secret_value = input("Enter Shared Secret Value:") #p
client = Client(shared_secret_value)
client.authenticate()
while True:
    client.communicate()
