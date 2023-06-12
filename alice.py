import alice_secret
from pwn import *
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Padding

GENERATOR = 2
KEY_BYTES = 16
PRIME_BITS = 1024

def main():
    prc = process(['python3', 'server.py'])

    p = int(prc.recvline().decode('utf-8'),16)

    A = pow(GENERATOR,alice_secret.a,p)

    prc.sendline(hex(A)[2:].encode('utf-8'))

    B = int(prc.recvline().decode('utf-8'),16)

    ct = bytes.fromhex(prc.recvline().decode('utf-8'))

    ss = pow(B,alice_secret.a,p)

    key = hashlib.sha256(ss.to_bytes(PRIME_BITS//8,'big')).digest()[:KEY_BYTES]

    cipher = AES.new(key,AES.MODE_CBC,iv=ct[:AES.block_size])

    print(Padding.unpad(cipher.decrypt(ct[AES.block_size:]),AES.block_size))

if __name__ == "__main__":
    main()