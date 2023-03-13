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
    """
    Simulation of getting one food portion from the pot by one savage

    Arguments:
    i       -- Identifier of the cook.
    shared  -- Object shared by threads
    """

    sleep(0.2)
    shared.pot -= 1
    print(f"savage [{i}] is eating (remaining portions: {shared.pot})")


def add_to_pot(i, shared):
    """
    Simulation of adding one food portion into the pot by one cook

    Arguments:
    i       -- Identifier of the cook.
    shared  -- Object shared by threads
    """

    sleep(0.1)
    shared.pot += 1
    print(f"cook [{i}] added portion (remaining portions: {shared.pot})")


def cook_portion():
    """
    Simulation of cooking food portion by cook
    """

    sleep(0.2)


def savage(i, shared):
    """
    Function for threads - "savage" with simulation of waiting for each other and eating from pot

    Arguments:
    i       -- Identifier of the savage.
    shared  -- Object shared by threads
    """

    while True:
        shared.savage_mutex.lock()
        shared.dining_room += 1
        if shared.dining_room == D:  # check if everyone is in dining room
            print(f'savage [{i}] filled dining room. Every savage can go eat!')
            shared.turnstile1.signal(D)  # signal to every savage that they can go eat
        shared.savage_mutex.unlock()
        shared.turnstile1.wait()

        shared.savage_mutex.lock()
        shared.pot_full.wait()  # wait until pot is filled

        eat_from_pot(i, shared)

        if shared.pot == 0:
            print(f"savage [{i}] There is no portion in pot!")
            shared.pot_full.clear()  # reset pot - cannot eat
            shared.pot_empty.signal()  # signal to cooks that pot is empty
        shared.savage_mutex.unlock()

        shared.savage_mutex.lock()
        shared.dining_room -= 1
        if shared.dining_room == 0:  # wait while every savage is fed - nobody is in dining room
            shared.turnstile2.signal(D)  # signal that savages can go into dining room again
        shared.savage_mutex.unlock()
        shared.turnstile2.wait()


def cook(i, shared):
    """
    Function for threads - "cooks" with simulation of adding food into pot

    Arguments:
    i       -- Identifier of the cook.
    shared  -- Object shared by threads
    """

    while True:
        cook_portion()

        shared.cook_mutex.lock()
        shared.pot_empty.wait()  # wait until pot empty

        add_to_pot(i, shared)

        if shared.pot >= H:
            print(f"cook [{i}] Pot is filled!")
            shared.pot_empty.clear()  # reset empty - don't need to cook
            shared.pot_full.signal()  # signal full - savages can eat
        shared.cook_mutex.unlock()


def main():
    """Create threads for savages and cooks with one Shared object."""
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
