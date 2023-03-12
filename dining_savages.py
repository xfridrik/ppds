"""This module implements dinning savages problem.

This is dinning savages problem with multiple cooks solution using barriers, mutexes and events
 """

__author__ = "Martin Fridrik, Marián Šebeňa"
__email__ = "xfridrik@stuba.sk, mariansebena@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print, Semaphore, Event
from time import sleep

H: int = 4  # max pot capacity
D: int = 5  # number of savages
K: int = 3  # number of cooks


class Shared:
    """Represent shared data for all threads.
    """

    def __init__(self):
        """Shared class constructor."""


def eat_from_pot(i, shared):
    print(f"savage {i} eating")

def add_to_pot(i, shared):
    print(f"cook {i} adding")


def savage(i, shared):
    while True:
        print(f"savage {i}")


def cook(i, shared):
    while True:
        print(f"cook {i}")


def main():
    """Run main."""
    shared: Shared = Shared()

    savages: list[Thread] = [
        Thread(savage, i, shared) for i in range(D)
    ]
    cooks: list[Thread] = [
        Thread(cook, i, shared) for i in range(K)
    ]
    for p in savages + cooks:
        p.join()


if __name__ == "__main__":
    main()
