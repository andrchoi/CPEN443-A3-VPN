import socket
import json
import dh_algo
import sympy

sharedSecret = ''

def setSecret(value):
    global sharedSecret
    sharedSecret = value

def get_hostname():
    hostname = input("Enter Host name:")
    return hostname
def get_portnum():
    portnum = input("Enter port number:")
    return portnum

HOST = get_hostname()
PORT = get_portnum()

class Client(dh_algo.DH_Endpoint):
    def __init__(self, shared_secret_value):
        public_key1 = sympy.nextprime(shared_secret_value)
        public_key2 = sympy.nextprime(public_key1//2)
        super.__init__(public_key1, public_key2)
        self.flag_generated_key = False

    def send(self, partial_key): # sends the partial key
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT)) #HOST, PORT of client
            flagged_partial_key = {'p':'partial_key'}
            data_string = json.dumps(flagged_partial_key) #data serialized
            s.sendall(data_string)
            while True:
                data = s.recv(1024) # Limit message size to 1024 bytes?
                if not data: # At end of message break
                    break
                try:
                    data_loaded = json.loads(data) #data loaded
                    partial_key = data_loaded.get('p')
                    self.generate_full_key(partial_key)
                    self.flag_generated_key = True
                except:
                    print(data)
    
    def send_encrypted(self, message):
        if self.encrypt_message:
            encrypted_message = self.encrypt_message(message)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(encrypted_message)
                data = s.recv(1024)
            print('Received', repr(data)) #repr returns string of data
        else:
            print("Enter Shared Value first")

shared_secret_value = input("Enter Shared Secret Value:") #p
private_key = input("Enter Private Value:")

client = Client(shared_secret_value)
partial_key = client.generate_partial_key()
client.send(partial_key)
message = input("Enter message:")
client.send_encrypted(message)

