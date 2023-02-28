"""
This module contains a sleeping barber problem implementation.

This is the implementation of a sleeping barber problem and simulation with possible customer overrun.
"""


__authors__ = "Marián Šebeňa, Martin Fridrik"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk, xfridrik@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Thread, Semaphore, print
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
    print(f"\x1b[1;{31+i};40m Customer[{i}] \x1b[0m: I'm getting a new haircut!")
    sleep(0.1)


def cut_hair():
    # TODO: Simulate time and print info when barber cuts customer's hair
    print(f"\x1b[6;30;43m    Barber   \x1b[0m: is cutting hair...")
    sleep(0.1)


def balk(i):
    # TODO: Represents situation when waiting room is full and print info
    print(f"\x1b[1;{31+i};40m Customer[{i}] \x1b[0m: There is no space in waiting room, I'm leaving!")
    sleep(0.3)


def growing_hair(i):
    # TODO: Represents situation when customer wait after getting haircut. So hair is growing and customer is
    #  sleeping for some time
    print(f"\x1b[1;{31+i};40m Customer[{i}] \x1b[0m: I've got new haircut, so I wait.")
    sleep(1)


def customer(i, shared):
    # TODO: Function represents customers behaviour. Customer come to waiting if room is full sleep.
    # TODO: Wake up barber and waits for invitation from barber. Then gets new haircut.
    # TODO: After it both wait to complete their work. At the end waits to hair grow again

    while True:
        # TODO: Access to waiting room. Could customer enter or must wait? Be careful about counter integrity :)
        shared.mutex.lock()
        if shared.waiting_room == N:
            shared.mutex.unlock()
            balk(i)
        else:
            shared.waiting_room += 1
            shared.mutex.unlock()
            print(f"\x1b[5;30;42m WaitingRoom \x1b[0m: arrived \x1b[1;{31 + i};40m Customer[{i}] \x1b[0m")

            shared.barber.signal()
            shared.customer.wait()

            get_haircut(i)

            shared.customer_done.signal()
            shared.barber_done.wait()

            print(f"\x1b[5;30;42m WaitingRoom \x1b[0m: left \x1b[1;{31 + i};40m Customer[{i}] \x1b[0m")
            #  leaving waiting room
            shared.mutex.lock()
            shared.waiting_room -= 1
            shared.mutex.unlock()

            growing_hair(i)


def barber(shared):
    # TODO: Function barber represents barber. Barber is sleeping.
    # TODO: When customer come to get new hair wakes up barber.
    # TODO: Barber cuts customer hair and both wait to complete their work.

    while True:
        shared.customer.signal()
        shared.barber.wait()

        cut_hair()

        shared.barber_done.signal()
        shared.customer_done.wait()


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
