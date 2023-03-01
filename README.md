# PPDS assigment 2 - Barber shop
In this assigment we deal _sleeping barber_ problem with possible customer overrun.
## Sleeping barber problem
_Sleeping barber_ problem is analogy based on barbershop with one barber who cuts only one customer's hair at a time and waiting room with N seats.
The barber sleeps if he has no customers and the next customer has to wake him up. When she starts cutting, other customers have to wait in the waiting room and if it fills up, they have to leave.[^1]
## Implementation requirements

- There is barber shop with waiting room with capacity N and hair cutting room.
- If there is no customer, barber is sleeping.
- If customer arrives:
  - And barber is sleeping, he wakes him up, sits down and waits.
  - And barber is working, he sits down and waits if there is space in waiting room.
  - And waiting room is full, he leaves.
## Barber shop implementation
### Shared object
### Barber
### Customer
### Main
## Verification
### Console output

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