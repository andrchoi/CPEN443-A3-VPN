import socket
import json
import dh_algo
import sympy
import aes_algo


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
        self.aesfunc = None

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

    def send(self, host, port, partial_key): # sends the partial key
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.s = s
            s.connect((host, port)) #HOST, PORT of client
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
                    self.aesfunc = aes_algo.Rijndael(self.full_key)
                    break
                except:
                    print(data)
    
    def communicate(self):
        message = input("Enter message:")
        zeroes_req = 15 - len(message) % 16
        padded_message = "0" * zeroes_req + "1" + message
        iterations_num = len(padded_message) // 16
        ciphertext_message = ""
        for i in range(iterations_num):
            partial_plainmessage = padded_message[i * 16:i * 16 + 16]
            encrypted_partial = self.aesfunc.encrypt(partial_plainmessage)
            ciphertext_message += encrypted_partial
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
def connectClient(sharedSecret, host, isIPaddr, port):
    global client
    client = Client(sharedSecret)
    partial_key = client.generate_partial_key()
    client.send(host, port, partial_key)

def encryptAndSend(server, message):
    global client
    client.send_encrypted(message)

# client = Client(shared_secret_value)
# partial_key = client.generate_partial_key()
# client.send(partial_key)
# message = input("Enter message:")
# client.send_encrypted(message)

