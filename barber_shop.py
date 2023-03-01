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
    print(f"\x1b[1;{31+i};40m Customer[{i}] \x1b[0m: I'm getting a new haircut!")
    sleep(0.15)


def cut_hair():
    print(f"\x1b[6;30;43m    Barber   \x1b[0m: is cutting hair...")
    sleep(0.1)


def balk(i):
    print(f"\x1b[1;{31+i};40m Customer[{i}] \x1b[0m: There is no space in waiting room, I'm leaving!")
    sleep(0.2)


def growing_hair(i):
    print(f"\x1b[1;{31+i};40m Customer[{i}] \x1b[0m: I've got new haircut, so I wait.")
    sleep(1)


def customer(i, shared):
    """"Function for threads - "customers" """

    while True:
        shared.mutex.lock()
        if shared.waiting_room == N:  # waiting room is full - leaving and wait for another try
            shared.mutex.unlock()
            balk(i)
        else:
            shared.waiting_room += 1
            print(f"\x1b[5;30;42m WaitingRoom \x1b[0m: "
                  f"arrived \x1b[1;{31 + i};40m Customer[{i}] \x1b[0m ({shared.waiting_room})")
            shared.mutex.unlock()

            shared.barber.signal()  # trying to wake up the barber
            shared.customer.wait()  # waiting for barber to cut me

            get_haircut(i)

            shared.barber_done.wait()  # waiting for barber getting work done
            shared.customer_done.signal()  # customer is done, barber is free for another one

            #  leaving waiting room
            shared.mutex.lock()
            shared.waiting_room -= 1
            print(f"\x1b[5;30;42m WaitingRoom \x1b[0m: "
                  f"left \x1b[1;{31 + i};40m Customer[{i}] \x1b[0m ({shared.waiting_room})")
            shared.mutex.unlock()

            growing_hair(i)


def barber(shared):
    """"Function for thread - "barber" """

    while True:
        shared.customer.signal()  # barber is free
        shared.barber.wait()  # barber is sleeping

        cut_hair()

        shared.barber_done.signal()  # barber completed work
        shared.customer_done.wait()  # waiting for customer to leave


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
