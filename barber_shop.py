"""
This module contains a sleeping barber problem implementation.

This is the implementation of a sleeping barber problem and simulation with possible customer overrun.
"""


__authors__ = "Marián Šebeňa, Martin Fridrik"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xfridrik@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Thread, Semaphore
from time import sleep
from random import randint

C = 5  # number of customers
N = 3  # size of waiting room


class Shared(object):
    """"Object Shared for multiple customers (threads)"""

    def __init__(self):
        """"Shared class constructor"""

        self.mutex = Mutex()  # main mutex for shared object
        self.waiting_room = 0  # waiting customers
        self.customer = Semaphore(0)  # indication for going to get new hairstyle
        self.barber = Semaphore(0)  # indication for going to cut hair
        self.customer_done = Semaphore(0)  # indication for done hairstyle and leaving
        self.barber_done = Semaphore(0)  # indication for done cutting and leaving


def get_haircut(i):
    # TODO: Simulate time and print info when customer gets haircut
    print(f"Customer[{i}]: I'm getting a new haircut!")
    sleep(2)


def cut_hair():
    # TODO: Simulate time and print info when barber cuts customer's hair
    print(f"Barber is cutting hair...")
    sleep(2)


def balk(i):
    # TODO: Represents situation when waiting room is full and print info
    print(f"Customer[{i}]: There is no space in waiting room, I'm leaving!")


def growing_hair(i):
    # TODO: Represents situation when customer wait after getting haircut. So hair is growing and customer is
    #  sleeping for some time
    print(f"Customer[{i}]: I don't need a new haircut, so I wait.")


def customer(i, shared):
    # TODO: Function represents customers behaviour. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again

    while True:
        # TODO: Access to waiting room. Could customer enter or must wait? Be careful about counter integrity :)

        # TODO: Rendezvous 1
        get_haircut(i)
        # TODO: Rendezvous 2

        # TODO: Leave waiting room. Integrity again
        growing_hair(i)


def barber(shared):
    # TODO: Function barber represents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.

    while True:
        # TODO: Rendezvous 1
        cut_hair()
        # TODO: Rendezvous 2


def main():
    shared = Shared()
    customers = []

    for i in range(C):
        customers.append(Thread(customer, i, shared))
    hair_stylist = Thread(barber, shared)

    for t in customers + [hair_stylist]:
        t.join()


if __name__ == "__main__":
    main()