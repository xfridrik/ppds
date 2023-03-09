# PPDS assignment 3 - Dining philosophers
At this assignment we deal _dining philosophers_ problem using right/left-handed philosophers.
## Dining philosophers problem
Dining philosophers problem is synchronization problem based on the analogy of K dining philosophers having a meal at a round table. They have only K forks between them and if someone wants to eat, they have to pick up both the right and left fork, but one fork can pick up only one philosopher.
Philosopher can eat or think and if there is no available fork for eating, he is thinking again.[^1]

<img src="img/img1.png"  width="300">

We want to make sure that philosophers don't starve to death and that we don't get a deadlock (each philosopher takes one fork on the same side)

<img src="img/img2.png"  width="300">


---
Martin Fridrik, PPDS FEI STUBA
2023
---

[^1]: https://www.geeksforgeeks.org/sleeping-barber-problem-in-process-synchronization/