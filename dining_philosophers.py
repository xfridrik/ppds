"""This module implements dinning philosophers problem.
 To avoid deadlock it is used left/right-hand picking up forks.
 """

__author__ = "Martin Fridrik, Tomáš Vavro"
__email__ = "xfridrik@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from time import sleep, time, strftime, gmtime

NUM_PHILOSOPHERS: int = 5  # number of philosophers
NUM_RUNS: int = 10  # number of repetitions of think-eat cycle of philosophers


class Shared:
    """Represent shared data for all threads."""

    def __init__(self):
        """Initialize an instance of Shared."""
        self.forks = [Mutex() for _ in range(NUM_PHILOSOPHERS)]


def think(i: int):
    """Simulate thinking.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is thinking!")
    sleep(0.1)


def eat(i: int):
    """Simulate eating.
    Args:
        i -- philosopher's id
    """
    print(f"Philosopher {i} is eating!")
    sleep(0.1)


def right_handed_pick(i: int, shared: Shared):
    """Picking up forks, first right, then left
    Args:
        i -- philosopher's id
        shared -- shared data
    """

    shared.forks[i].lock()
    sleep(0.5)
    shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
    eat(i)
    shared.forks[i].unlock()
    shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()


def left_handed_pick(i: int, shared: Shared):
    """Picking up forks, first left, then right
    Args:
        i -- philosopher's id
        shared -- shared data
    """

    shared.forks[(i + 1) % NUM_PHILOSOPHERS].lock()
    sleep(0.5)
    shared.forks[i].lock()
    eat(i)
    shared.forks[(i + 1) % NUM_PHILOSOPHERS].unlock()
    shared.forks[i].unlock()


def philosopher(i: int, shared: Shared):
    """Run philosopher's code.
    Args:
        i -- philosopher's id
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        think(i)
        # get forks
        if i == 0:
            right_handed_pick(i, shared)
        else:
            left_handed_pick(i, shared)


def main():
    """Run main."""
    shared: Shared = Shared()
    philosophers: list[Thread] = [
        Thread(philosopher, i, shared) for i in range(NUM_PHILOSOPHERS)
    ]
    for p in philosophers:
        p.join()


if __name__ == "__main__":
    st = time()
    main()
    elapsed_time = time() - st
    print('Total time elapsed:', strftime("%H:%M:%S", gmtime(elapsed_time)))
