"""This module contains a bakery algorithm implementation.

This is the implementation of a mutual exclusion - bakery algorithm.
"""

__author__ = "Tomáš Vavro, Martin Fridrik"
__email__ = "xfridrik@stuba.sk"
__license__ = "MIT"

from time import sleep
from fei.ppds import Thread

N_THREADS: int = 10  # count of threads

num: list[int] = [0] * N_THREADS  # num[tid] - "ticket" number for thread with tid
inside: list[int] = [0] * N_THREADS  # inside[tid] is 1 - thread with tid is in process of assigning new number


def bakery(tid: int):
    """Bakery algorithm implementation with simulation of critical section in thread.
    Arguments:
        tid -- thread identifier number
    """

    global num, inside

    # thread wants to go in critical section - inside process of assigning new ticket number
    inside[tid] = 1
    num[tid] = 1 + max(num)
    inside[tid] = 0

    # thread with assigned ticket number check for all threads
    for i in range(N_THREADS):
        # thread is waiting while is checking thread inside process of assigning new ticket number
        while inside[i]:
            pass
        # wait while checking thread with assigned number has lower number
        # or equal number, and it is thread with lower identifier
        while num[i] != 0 and (num[i] < num[tid] or (num[i] == num[tid] and i < tid)):
            pass

    # Begin of the critical section
    print(tid)
    sleep(1)
    print("Hello world, I'm only one alive now: "+str(tid))
    # End of the critical section

    # invalidation of current ticket number
    num[tid] = 0


if __name__ == '__main__':
    threads = [Thread(bakery, i) for i in range(1, N_THREADS)]
    [t.join() for t in threads]
