import socket
import json
import dh_algo
import sympy
import aes_algo
from threading import Thread
import hashlib
import pickle
import ipaddress
import struct
import time

HOST = 'localhost'
PORT = 2008

class Client(dh_algo.DH_Endpoint):
    def __init__(self, shared_secret_value):
        public_key1 = sympy.nextprime(shared_secret_value)
        public_key2 = 255
        super().__init__(public_key1, public_key2)
        self.flag_generated_key = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.aesfunc = None


    def authenticate(self, host, port): # sends the partial key
        partial_key = self.generate_partial_key()
        s = self.s
        s.connect((host, port)) #HOST, PORT of client
        s.send(bytes([partial_key]))
        stepThrough(partial_key, 'Send Partial Key')
        while True:
            data = s.recv(1024) # Limit message size to 1024 bytes?
            stepThrough(data, 'Recieved partial key')
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
                print("(System) Client symmetric key (" + full_key + ") has been created.\n")
                stepThrough(full_key, 'Generated Symmetric Key')
                self.aesfunc = aes_algo.Rijndael(full_key)
                break
            except:
                print("Error.")
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

                # update UI
                recText.set(padded_plaintext_message[padding_stops + 1:])
                stepThrough(padded_plaintext_message[padding_stops + 1:], 'Received')

                # print(decoded_data)
                print(padded_plaintext_message[padding_stops + 1:])
                hashed_aes = hashlib.sha3_256(padded_plaintext_message[padding_stops + 1:].encode('utf-8'))
                # print('hash is {}'.format(hash_msg))
                # print('aes is {}'.format(hashed_aes))
                if hashed_aes.hexdigest() == hash_msg:
                    print("(System) Message integrity has been confirmed.\n")
                else:
                    print("(System) Message integrity has been compromised.\n")

    def send_encrypted(self, message):
        if self.flag_generated_key:
            hash_msg = hashlib.sha3_256(message.encode('utf-8'))
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
            self.s.send(json_msg)
            stepThrough(json_msg, 'Send encrypted')
            print("(System) Encrypted message has been sent.\n")

        else:
            print("Please enter Shared Secret Value first.")

    def closeConn(self):
        print('closing client')
        self.s.close()

client = None
recText = None
status = None
comm = None
willStep = False
inputWait = False

def connectClient(sharedSecret, host, isIPaddr, port, isStepping):
    global client
    global willStep
    willStep = isStepping

    stepThrough('Start Connecting', 'Stepping')

    hostInfo = host
    if isIPaddr == 1:
        # host is an IP address
        packedIP = socket.inet_aton(host)
        numIP = struct.unpack("!L", packedIP)[0]
        hostInfo = str(ipaddress.ip_address(numIP))

    client = Client(sharedSecret)
    client.authenticate(hostInfo, port)
    communicate_thread = Thread(target=client.communicate)
    communicate_thread.start()

    global comm 
    comm = communicate_thread

def encryptAndSend(message):
    global willStep
    willStep = False    
    client.send_encrypted(message)

def getUIFields(recieved, state, ui):
    global recText
    global status
    global window
    window = ui
    recText = recieved
    status = state

def closeConnection():
    global client
    client.closeConn

def stepThrough(message, line):
    global status
    global window
    res = line + ': ' + str(message)
    status.set(res)

    window.update()
    # TODO:
    global willStep
    if willStep:
        global inputWait
        inputWait = True
        print('need to wait for input', line)
        window.after(5000)