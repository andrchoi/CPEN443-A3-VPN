'''
A = g**secret_value % p
public_key1 is g
private_key is secret_value
public_key2 is p
partial_key is A
'''
class DH_Endpoint(object):
    def __init__(self, public_key1, public_key2):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = #
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
            encrypted_message += chr(ord(c)+key) #simple encryption by adding key to ASCII value of character
        return encrypted_message
    
    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c)-key)
        return decrypted_message

if __name__ == "__main__":
    zach = DH_Endpoint(1294,79,54)
    alex = DH_Endpoint(1294,79,31)
    zach_pk = zach.generate_partial_key()
    alex_pk = alex.generate_partial_key()
    full_key = zach.generate_full_key(alex_pk)
    full_key = alex.generate_full_key(zach_pk)
    zach_em = zach.encrypt_message("hello alex i am doing good help me do my 432 writeen adssignment")
    alex_dm = alex.decrypt_message(zach_em)
    print(alex_dm)
