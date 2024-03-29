import socket

# input: 
# 1. symmetric key
# 2. ip of other computer


class DH_Endpoint(object):
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.full_key = None
        
    def generate_partial_key(self):
        partial_key = self.public_key1**self.private_key
        partial_key = partial_key%self.public_key2
        return partial_key
    
    def generate_full_key(self, partial_key_r):
        full_key = partial_key_r**self.private_key
        full_key = full_key%self.public_key2
        self.full_key = full_key
        return full_key
    
    def encrypt_message(self, message):
        encrypted_message = "" #in form of a string 
        key = self.full_key
        for c in message:
            encrypted_message += chr(ord(c)+key) #simple encryption by adding ket to ASCII value of character
        return encrypted_message
    
    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c)-key)
        return decrypted_message

def get_hostname():
    hostname = input("Enter Host name:")
    return hostname
def get_portnum():
    portnum = input("Enter port number:")
    return portnum
def get_symmetrickey():
    sym_key = input("Enter symmetric key:")
    return sym_key


# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 65432        # The port used by the server
HOST = get_hostname()
PORT = get_portnum()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data)) #repr returns string of data
# if __name__ == "__main__":
#     zach = DH_Endpoint(1294,79,54)
#     alex = DH_Endpoint(1294,79,31)
#     zach_pk = zach.generate_partial_key()
#     alex_pk = alex.generate_partial_key()
#     full_key = zach.generate_full_key(alex_pk)
#     full_key = alex.generate_full_key(zach_pk)
#     zach_em = zach.encrypt_message("hello alex i am doing good help me do my 432 writeen adssignment")
#     alex_dm = alex.decrypt_message(zach_em)
#     print(alex_dm)