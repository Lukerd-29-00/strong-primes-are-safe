import json
from sage.all import *
import multiprocessing
LOWER_BOUND = (1<<10)
GENERATOR = 2

def get_factor(phi, queue, found):
    tmp = phi
    f = trial_division(phi)
    while f < LOWER_BOUND or f in found:
        tmp //= f
        f = trial_division(tmp)
    queue.put(f)


with open("auth.log",'r') as f:
    found = set()
    moduli = []
    outputs = []
    for line in f:
        data = json.loads(line.strip())
        p = int(data['p'],16)
        A = int(data["A"],16)
        phi = p-1
        queue = multiprocessing.Queue()
        P = multiprocessing.Process(target=get_factor,args=(phi,queue,found))
        P.start()
        P.join(3)
        if not P.is_alive():
            f = queue.get()
            if f != None:
                found.add(f)
                Amodf = discrete_log(Mod(pow(A,phi//f,p),p),Mod(pow(GENERATOR,phi//f,p),p),ord=f)
                outputs.append(Amodf)
                moduli.append(f)
        else:
            P.kill()

secret = CRT_list(outputs,moduli)
print(secret)
print(pow(GENERATOR,secret,p) == A)
