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

    Attributes:
    savage_mutex    -- Mutex for accessing pot while eating
    cook_mutex      -- Mutex for accessing pot while adding food
    pot             -- number of remaining portions in pot
    dining_room     -- number of savages in dining room
    turnstile1      -- turnstile for barrier when entering dining room
    turnstile2      -- turnstile for barrier when leaving dining room
    pot_empty       -- Event for empty pot signalisation
    pot_full        -- Event for full pot signalisation
    """

    def __init__(self):
        """Shared class constructor."""
        self.savage_mutex = Mutex()
        self.cook_mutex = Mutex()
        self.pot = 0

        self.dining_room = 0
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)

        self.pot_empty = Event()
        self.pot_full = Event()
        self.pot_empty.signal()  # pot is empty at begin


def eat_from_pot(i, shared):
    print(f"savage {i} eating")

def add_to_pot(i, shared):
    print(f"cook {i} adding")


def savage(i, shared):
    while True:
        shared.savage_mutex.lock()
        shared.dining_room += 1
        if shared.dining_room == D:
            print(f'savage {i} filled dining room and unlocked barrier')
            shared.turnstile1.signal(D)
        shared.savage_mutex.unlock()
        shared.turnstile1.wait()

        sleep(1 / 5)
        eat_from_pot(i, shared)

        shared.savage_mutex.lock()
        shared.dining_room -= 1
        if shared.dining_room == 0:
            shared.turnstile2.signal(D)
        shared.savage_mutex.unlock()
        shared.turnstile2.wait()


def cook(i, shared):
    while True:
        sleep(1/5)
        add_to_pot(i, shared)


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
