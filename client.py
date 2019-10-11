import socket
import json
import dh_algo
import sympy
import aes_algo
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
        self.aesfunc = None


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
                if len(full_key) == 16:
                    pass
                elif len(full_key) > 16:
                    full_key = full_key[:16]
                else:
                    padded_zeroes_req = 16 - len(full_key)
                    full_key = "0" * padded_zeroes_req + full_key
                # print("Full key is {}".format(full_key))
                self.flag_generated_key = True
                print("client has created key")
                self.aesfunc = aes_algo.Rijndael(full_key)
                break
            except:
                print("error")
                # s.close()
                # print(self.decrypt_message(data.decode('utf-8')))
    
    def communicate(self):

        s = self.s
        while True:
            data = s.recv(1024) # Limit message size to 1024 bytes?
            if not data: # At end of message break
                # break # at s.close on the connection it closes
                pass
            else:
                decoded_data = data.decode('utf-8')
                iterations_decrypt = len(decoded_data) // 16
                padded_plaintext_message = ""
                for i in range(iterations_decrypt):
                    partial_ciphermessage = decoded_data[i * 16:i * 16 + 16]
                    decrypted_partial = self.aesfunc.decrypt(partial_ciphermessage)
                    padded_plaintext_message += decrypted_partial
                padding_stops = padded_plaintext_message.index("1")
                # print(decoded_data)
                print(padded_plaintext_message[padding_stops + 1:])
            
    def send_encrypted(self, message):
        if self.flag_generated_key:
            zeroes_req = 15 - len(message) % 16
            padded_message = "0" * zeroes_req + "1" + message
            iterations_encrypt = len(padded_message) // 16
            ciphertext_message = ""
            for i in range(iterations_encrypt):
                partial_plainmessage = padded_message[i * 16:i * 16 + 16]
                encrypted_partial = self.aesfunc.encrypt(partial_plainmessage)
                ciphertext_message += encrypted_partial
            self.s.send(ciphertext_message.encode('utf-8'))
        else:
            print("Enter Shared Value first")


shared_secret_value = input("Enter Shared Secret Value:")
client = Client(shared_secret_value)
client.authenticate()
communicate_thread = Thread(target=client.communicate)
communicate_thread.start()
while True:
    # client.communicate()
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

# client = Client(shared_secret_value)
# partial_key = client.generate_partial_key()
# client.send(partial_key)
# message = input("Enter message:")
# client.send_encrypted(message)

