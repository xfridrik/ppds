"""
This module contains a sleeping barber problem implementation.

This is the implementation of a sleeping barber problem and simulation with possible customer overrun.
"""


__authors__ = "Marián Šebeňa, Martin Fridrik"
__email__ = "mariansebena@stuba.sk, xfridrik@stuba.sk"
__license__ = "MIT"


from fei.ppds import Mutex, Thread, Semaphore, print
from time import sleep
from random import randint

C = 5  # number of customers
N = 3  # size of waiting room
COL = False  # colourful prints


class Shared(object):
    """
    Object Shared for multiple customers (threads)

    Attributes:
    mutex           -- main Mutex for shared object
    waiting_room    -- count of waiting customers
    customer        -- Semaphore for indication of going to get new hairstyle
    barber          -- Semaphore for indication of going to cut hair
    customer_done   -- Semaphore for indication of done hairstyle and leaving
    barber_done     -- Semaphore for indication of done cutting
    """

    def __init__(self):
        """"
        Shared class constructor
        """

        self.mutex = Mutex()
        self.waiting_room = 0
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def get_haircut(i):
    """
    Simulates a customer getting a haircut.

    Arguments:
    i -- Identifier of the customer.
    """

    if COL:
        print(f"\x1b[1;{31 + i};40m Customer[{i}] \x1b[0m: I'm getting a new haircut!")
    else:
        print(f"Customer[{i}]: I'm getting a new haircut!")
    sleep(0.15)


def cut_hair():
    """
    Simulates a barber cutting hair.
    """

    if COL:
        print(f"\x1b[6;30;43m    Barber   \x1b[0m: is cutting hair...")
    else:
        print(f"Barber: is cutting hair...")

    sleep(0.1)


def balk(i):
    """
    Simulates a customer leaving and waiting due to full waiting room.

    Arguments:
    i -- Identifier of the customer.
    """

    if COL:
        print(f"\x1b[1;{31 + i};40m Customer[{i}] \x1b[0m: There is no space in waiting room, I'm leaving!")
    else:
        print(f"Customer[{i}]: There is no space in waiting room, I'm leaving!")
    sleep(0.2)


def growing_hair(i):
    """
    Simulates a customer growing hair after getting a haircut.

    Arguments:
    i -- Identifier of the customer.
    """

    if COL:
        print(f"\x1b[1;{31 + i};40m Customer[{i}] \x1b[0m: I've got new haircut, so I wait.")
    else:
        print(f"Customer[{i}]: I've got new haircut, so I wait.")
    sleep(1)


def waiting_room_update(i, count, action):
    """
    Prints action and status of waiting room.

    Arguments:
    i       -- Identifier of the customer.
    count   -- Count of customers in waiting room.
    action  -- Customer's action ("arrived"/"left")
    """

    if COL:
        print(f"\x1b[5;30;42m WaitingRoom \x1b[0m: "
              f"{action} \x1b[1;{31 + i};40m Customer[{i}] \x1b[0m ({count})")
    else:
        print(f"WaitingRoom: {action} Customer[{i}] ({count})")


def customer(i, shared):
    """
    Function for threads - "customers" with simulation of waiting room and getting haircut

    Arguments:
    i       -- Identifier of the customer.
    shared  -- Object shared by threads
    """

    while True:
        shared.mutex.lock()
        if shared.waiting_room == N:  # waiting room is full - leaving and wait for another try
            shared.mutex.unlock()
            balk(i)
        else:
            # enter waiting room
            shared.waiting_room += 1
            waiting_room_update(i, shared.waiting_room, "arrived")
            shared.mutex.unlock()

            # rendezvous enter
            shared.barber.signal()  # trying to wake up the barber
            shared.customer.wait()  # waiting for barber to cut me

            get_haircut(i)

            # rendezvous leave
            shared.barber_done.wait()  # waiting for barber getting work done
            shared.customer_done.signal()  # customer is done, barber is free for another one

            # leaving waiting room
            shared.mutex.lock()
            shared.waiting_room -= 1
            waiting_room_update(i, shared.waiting_room, "left")
            shared.mutex.unlock()

            growing_hair(i)


def barber(shared):
    """
    Function for thread - "barber" with calling simulation of cutting hair

    Arguments:
    shared -- Object shared by threads
    """

    while True:
        # rendezvous enter
        shared.customer.signal()  # barber is free
        shared.barber.wait()  # barber is sleeping

        cut_hair()

        # rendezvous leave
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
