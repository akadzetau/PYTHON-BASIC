import os
from random import randint
import multiprocessing as mp
import time
import csv

OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'
CPUS = mp.cpu_count()


def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    return f1


def save(f):
    with open(f"{OUTPUT_DIR}/{f[0]}.txt", 'w') as file:
        file.write(str(f[1]))


def func1(array: list):
    start = time.time()
    print(f"{len(array)} items to process")
    print(f"{len(set(array))} unique items to process")

    with mp.Pool(CPUS) as p:
        res = [(a, res) for a, res in zip(array, p.map(fib, array))]
        p.map(save, res)

    print(f"Done with func1 in {time.time() - start}")


def read(f):
    with open(f"{OUTPUT_DIR}/{f}", 'r') as file:
        return int(f.split(".")[0]), int(file.readline())


def func2(result_file: str):
    start = time.time()

    files = [f for f in os.listdir(OUTPUT_DIR) if not f.endswith(result_file.split("/")[2])]
    with mp.Pool(CPUS) as p:
        res = p.map(read, files)
    with open(result_file, 'w') as file:
        csv.writer(file).writerows(res)

    print(f"Done with func2 in {time.time() - start}")


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Using {CPUS} CPUs")
    func1(array=[randint(1000, 100000) for _ in range(1000)])
    func2(result_file=RESULT_FILE)
