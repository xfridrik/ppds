# PPDS assigment 1 - Bakery algorithm
In this assigment we deal mutual exclusion problem, so the multiple threads can not access critical section at the same time, using Bakery Algorithm.
### Bakery algorithm
We use the Bakery algorithm to obtain the correct mutual exclusion for the processes.
The Bakery algorithm assures us that processes cannot execute a critical section at the same time, so they can, for example, access shared resources without causing concurrent execution problems.

Bakery algorithm is based on the analogy of people waiting in line at a bakery, where each customer receive ticket with number, which increases for every customer and when one customer is served, other must wait in a line until this customer leaves and customer with the following number is served.[^1] 
### Algorithm implementation
At the beginning, we need to create global variables that all processes will have access to.
We are creating algorithm for N processes and number of them is saved in variable `N_THREADS`. We also need 2 lists with `N_THREADS` length - `num` for saving thread "ticket" numbers, and `inside` for tracking, if thread is inside the critical section. At the beginning there is no thread in "line" or critical section, so both lists are initialized to zero values.  


In `__main__` we are creating `N_THREADS` threads of function `bakery`.
This function is implementation of Bakery algorithm with simulation of the critical section, which is indicated by comments (`# Begin of the critical section` and `# End of the critical section`).
Function gets identifier of thread as an argument (`tid`). 

First step is setting value 1 into the `inside` list for current thread to indicate, that thread wants to go in critical section and is inside the process of assigning new number. Then is receiving "ticket" number with the number following the maximum, which is saved into `num[tid]`. After this is thread ready for going into the critical section and process of assigning new number is done - `inside[tid]` is changed back to 0.

Next step is iterate all threads and wait, if there is thread with intention to go into the critical section and is inside process of assigning "ticket" number (`inside[i] is 1`), this helps to read new "ticket" numbers, because we wait while assigning new one. 
Then we check if this thread has assigned "ticket" number (`num[i]` is not 0) and wait, if this thread with assigned number has lower "ticket" number value (`num[i] < num[tid]`) or same value, and it is thread with lower identifier as actual thread (`num[i] == num[tid] and i < tid`).

When we checked all the threads and there is no one satisfying requirements to wait, actual thread is going into the critical section.
In the critical section we are printing `tid` of actual thread on enter, then we froze thread for 1 second to simulate computations of thread and then print string with the same `tid` before leaving critical section. After thread left critical section, "ticket" number is no longer valid and is set to 0.

---
Martin Fridrik, PPDS FEI STUBA
2023
---

[^1]: https://www.codingninjas.com/codestudio/library/bakery-algorithm
