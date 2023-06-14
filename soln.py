import json
from sage.all import *
import time
import hashlib
from Crypto.Cipher import AES
import math
import random
import re
import multiprocessing
from Crypto.Util import Padding

error_ptrn = re.compile(r"Inverse of (\d+) ")
LOWER_BOUND = (1<<10)
GENERATOR = 2

def gen_curve(x: int, y: int, modulus: int):
    a = random.randint(0,modulus-1)
    b = y**2 - x**3 - a*x
    E = EllipticCurve(Zmod(modulus),[a,b])
    return E(x,y)


def small_factor(phi,curves=10, B = 100):
    for _ in range(curves):
        P = gen_curve(1,1,phi)
        for k in range(2,B):
            try:
                P *= k
            except ZeroDivisionError as e:
                v = int(re.search(error_ptrn,e.args[0]).group(1))
                return math.gcd(phi,v)
    return None

def get_factor(phi):
    f = 2
    tmp = phi
    while f < LOWER_BOUND:
        f = small_factor(tmp)
        if f == None:
            return None
        tmp //= f
    return f

def process_line(data: str):
    data = json.loads(data.strip())
    p = int(data['p'],16)
    A = int(data['A'],16)
    phi = p - 1
    return A, p, get_factor(phi)


with open("auth.log",'r') as f:
    data = json.loads(f.readline().strip())
    A0 = int(data['A'],16)
    p0  = int(data['p'],16)

with open("auth.log",'r') as f:
    start = time.time()
    secret = 0
    modulus = 1
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        for A, p, fac in pool.imap_unordered(process_line,f):          
            if fac != None:
                fac = Integer(fac)
                phi = p - 1
                Amodf = discrete_log(Mod(pow(A,phi//fac,p),p),Mod(pow(GENERATOR,phi//fac,p),p),ord=fac)
                secret = int(CRT(secret,Amodf,modulus,fac)) if secret != 0 else Amodf
                modulus = int(lcm(modulus,fac)) if modulus != 1 else fac
                if pow(GENERATOR,secret,p0) == A0:
                    break


print(secret)

with open("auth.log",'r') as f:
    data = json.loads(f.readline().strip())

B = int(data["B"],16)

ss: int = pow(B,secret,int(data["p"],16))

iv = bytes.fromhex(data["iv"])
ct = bytes.fromhex(data['ct'])

key = hashlib.sha256(ss.to_bytes(256,'big')).digest()[:16]

cipher = AES.new(key,AES.MODE_CBC,iv=iv)

print(Padding.unpad(cipher.decrypt(ct),16))

print(f"{time.time() - start} seconds elapsed.")