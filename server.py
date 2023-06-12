import random
from Crypto.Util import number, Padding
from Crypto.Cipher import AES
import flag
import logging
import hashlib

GENERATOR = 2
KEY_BYTES = 16
PRIME_BITS = 1024
logging.basicConfig(filename="auth.log",level=logging.INFO,format="%(message)s")

def authenticate():
    RAND = random.SystemRandom()
    p = number.getStrongPrime(PRIME_BITS)
    b = RAND.randint(2,p-2)
    print(hex(p)[2:])
    A = int.from_bytes(bytes.fromhex(input()),'big')
    B = pow(GENERATOR,b,p)
    print(hex(B)[2:])
    ss = hashlib.sha256(pow(A,b,p).to_bytes(PRIME_BITS//8,'big')).digest()[:KEY_BYTES]
    iv = RAND.getrandbits(AES.block_size*8)
    iv = iv.to_bytes(AES.block_size,'big')
    cipher = AES.new(ss,AES.MODE_CBC,iv=iv)
    ct = cipher.encrypt(Padding.pad(flag.FLAG,AES.block_size))
    print(iv.hex() + ct.hex())
    logging.info({
        "ct": ct.hex(),
        'iv': iv.hex(),
        "B": hex(B)[2:],
        "A": hex(A)[2:],
        "p": hex(p)[2:]
    })

authenticate()