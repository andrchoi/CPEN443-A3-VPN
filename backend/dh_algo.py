g = 31
p = 47
secret_value = 11
def dh_algo(g,p, secret_value, result):
    A = g**secret_value % p
    socket.send(A) # placeholder
    key = result**secret_value % p
    return key
