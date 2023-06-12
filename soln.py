import json
from sage.all import *
import multiprocessing
import hashlib
from Crypto.Cipher import AES
import math
LOWER_BOUND = (1<<10)
GENERATOR = 2

def get_factor(phi, queue):
    tmp = phi
    f = trial_division(phi)
    while f < LOWER_BOUND:
        tmp //= f
        f = trial_division(tmp)
    queue.put(f)


with open("auth.log",'r') as f:
    secret = 0
    modulus = 1
    for line in f:
        data = json.loads(line.strip())
        p = int(data['p'],16)
        A = int(data["A"],16)
        phi = p-1
        queue = multiprocessing.Queue()
        P = multiprocessing.Process(target=get_factor,args=(phi,queue))
        P.start()
        P.join(3)
        if not P.is_alive():
            f = queue.get()
            if f != None:
                Amodf = discrete_log(Mod(pow(A,phi//f,p),p),Mod(pow(GENERATOR,phi//f,p),p),ord=f)
                secret = int(CRT(secret,Amodf,modulus,f)) if secret != 0 else Amodf
                modulus = int(lcm(modulus,f)) if modulus != 1 else f
                if pow(GENERATOR,secret,p) == A:
                    break
        else:
            P.kill()

print(secret)

with open("auth.log",'r') as f:
    data = json.loads(f.readline().strip())

B = int(data["B"],16)

ss: int = pow(B,secret,int(data["p"],16))

iv = bytes.fromhex(data["iv"])
ct = bytes.fromhex(data['ct'])

key = hashlib.sha256(ss.to_bytes(256,'big')).digest()[:16]

cipher = AES.new(key,AES.MODE_CBC,iv=iv)

print(cipher.decrypt(ct))

