# PPDS assignment 3 - Dining philosophers
At this assignment we deal _dining philosophers_ problem using right/left-handed philosophers.
## Dining philosophers problem
Dining philosophers problem is synchronization problem based on the analogy of K dining philosophers having a meal at a round table. They have only K forks between them and if someone wants to eat, they have to pick up both the right and left fork, but one fork can pick up only one philosopher.
Philosopher can eat or think and if there is no available fork for eating, he is thinking again.[^1]

<img src="img/img1.png"  width="300">

We want to make sure that philosophers don't starve to death and that we don't get a deadlock (each philosopher takes one fork on the same side)

<img src="img/img2.png"  width="300">

## Left/right-handed philosophers
To avoid deadlock we use implementation, where one philosopher picks up fork with another hand first.

<img src="img/img3.png"  width="300">

If left-handed has no fork, philosopher on the right can pick up both forks (or next philosopher is already eating etc...).
When left-handed philosopher takes left fork, there are 2 possible scenarios:
- next fork (right) is free and philosopher can take it and eat,
- next fork isn't free because it has philosopher on the right. This means, next philosopher is eating, and he will release this fork later. 

There is always situation in all scenarios, where one can eat and then release both forks, so there is no possible deadlock.

## Implementation
In this program there are 2 global variables - `NUM_PHILOSOPHERS` to keep number of philosophers and `NUM_RUNS` to keep number of think-eat cycles.

### Shared object
Shared object is object shared by all threads with shared resources and has attribute `forks`, which is array containing Mutex for every fork (total `NUM_PHILOSOPHERS` forks).

### Function _philosopher_ 
Function for philosopher cycle takes as an argument `i` - philosopher's id and `shared` - Shared object.
This function repeats `NUM_RUNS` think-eat process. At first the function _think_, which simulates thinking, is called. Then we check philosopher's id - when it is first philosopher (id is 0), this philosopher is marked as _left-handed_ and there is called function _left_handed_pick_, where is first locked fork on the right and then fork on the left. Otherwise the philosopher takes the forks in reverse order (_right_handed_pick_ function is called).

After the philosopher picks up both forks, function _eat_ is called, to simulate eating process for philosopher. Then both forks are unlocked.

## Comparison
We are now comparing 2 _dining philosophers_ problem solutions - using waiter and using right/left-handed philosophers (our implementation).

In _Waiter_ solution there is used Semaphore (with lower value as number of philosophers), this ensures that all philosophers can't take up fork at the same time and last philosopher must wait before picking up process.
### Blocking
Since the case where the philosophers are more blocked while eating increases the overall running time of the program, we checked this value for both solutions and the same parameters - 5 philosophers and 10 cycles of eating and thinking.
With **Right/left-handed** solution we get **13 seconds** total time elapsed and with **Waiter** solution it was only **8 seconds**.

### Starvation
To check whether the philosopher ate often enough and is not blocked for too long, we again use an experiment in which we measure how long it took one thread to execute one eat-think process.
Getting forks takes 0.5s, eating 0.1s and thinking 0.1s, we added some time (0.3s) and check, if philosophers can access resource (eat) always under this time.

#### Waiter solution
When running code with waiter solution with 5 philosophers and 10 cycles for every philosopher thread (total 50 eat-think runs), there were two runs crossing the selected one-second threshold. One with value 1.06s , which is just above our threshold and second with higher value - 1.36s.

#### Right/left-handed solution
We also run this test with same parameters for our implementation. We got a worse result, with up to 20 runs exceeding our 1-second limit. The worst result was 1.48s, which is worse than the worst result from the first test. Often repeated values were about 1.25 or 1.44 seconds.

### Comparison table

| Solution              | Possible deadlock | Starvation                 | Elapsed time (s)      |
|-----------------------|-------------------|----------------------------|-----------------------|
| **No solution**       | Yes               | No / Fatal (when deadlock) | 7 / ∞ (when deadlock) |
| **Left/right-handed** | No                | Higher                     | 13                    |
| **Waiter**            | No                | Lower                      | 8                     |

## How to run script
1. Clone repository
   ```sh
   git clone repository_url
   ```
2. Install package `fei.ppds` using pip:
   ```sh
   py -3 -m pip install --upgrade fei.ppds
   ```
   or for Linux:
   ```sh
   pip3 install --upgrade fei.ppds
   ```
3. Run script using Python interpreter (ver. 3.10)

---
Martin Fridrik, PPDS FEI STUBA
2023
---

[^1]: https://www.geeksforgeeks.org/sleeping-barber-problem-in-process-synchronization/