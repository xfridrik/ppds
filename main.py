"""This module contains a bakery algorithm implementation.

This is the implementation of a mutual exclusion - bakery algorithm.
"""

__author__ = "Martin Fridrik"
__email__ = "xfridrik@stuba.sk"
__license__ = "MIT"

from time import sleep
from fei.ppds import Thread

N_THREADS: int = 10

num: list[int] = [0] * N_THREADS
inside: list[int] = [0] * N_THREADS


# Bakery algorithm implementation
def bakery(tid: int):

    global num, inside

    inside[tid] = 1
    num[tid] = 1 + max(num)
    inside[tid] = 0
    for i in range(N_THREADS):
        while inside[i]:
            pass
        while num[i] != 0 and (num[i] < num[tid] or (num[i] == num[tid] and i < tid)):
            pass
    # Begin of the critical section
    print(tid)
    sleep(1)
    print("Hello world, I'm only one alive now: "+str(tid))
    # End of the critical section
    num[tid] = 0


if __name__ == '__main__':
    threads = [Thread(bakery, i) for i in range(1, N_THREADS)]
    [t.join() for t in threads]
