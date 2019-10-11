import socket
import json
import dh_algo
import sympy

sharedSecret = ''

def setSecret(value):
    global sharedSecret
    sharedSecret = value

# def get_hostname():
#     hostname = input("Enter Host name:")
#     return hostname
# def get_portnum():
#     portnum = input("Enter port number:")
#     return portnum

HOST = 'localhost'
PORT = 2000

class Client(dh_algo.DH_Endpoint):
    def __init__(self, shared_secret_value):
        public_key1 = sympy.nextprime(shared_secret_value)
        public_key2 = sympy.nextprime(public_key1//2)
        super().__init__(public_key1, public_key2)
        self.flag_generated_key = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, partial_key): # sends the partial key
        s = self.s
        s.connect((HOST, PORT)) #HOST, PORT of client
        flagged_partial_key = {"p":partial_key}
        flagged_partial_key = json.dumps(flagged_partial_key).encode('utf-8') #data serialized
        s.send(flagged_partial_key)
        while True:
            data = s.recv(1024) # Limit message size to 1024 bytes?
            if not data: # At end of message break
                break
            try:
                data_loaded = json.loads(data.decode('utf-8')) #data loaded
                partial_key = data_loaded.get('p')
                self.generate_full_key(partial_key)
                self.flag_generated_key = True
                print("client has created key")
                break
            except:
                print(self.decrypt_message(data.decode('utf-8')))
    
    def send_encrypted(self, message):
        if self.encrypt_message:
            encrypted_message = self.encrypt_message(message)
            self.s.sendall(encrypted_message.encode('utf-8'))
            self.s.close()
        else:
            print("Enter Shared Value first")

shared_secret_value = input("Enter Shared Secret Value:") #p

client = Client(shared_secret_value)
partial_key = client.generate_partial_key()
client.send(partial_key)
while True:
    message = input("Enter message:")
    client.send_encrypted(message)

