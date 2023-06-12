import alice
import multiprocessing

def main():
    with open("strong_primes",'r') as f:
        primes = set(map(lambda x: int(x.strip(),16),f.readlines()))
    alice.main(primes)

repetitions = 256

with multiprocessing.Pool(multiprocessing.cpu_count()//2) as pool:
    pool.starmap(main,[() for _ in range(repetitions)])