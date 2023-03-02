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
The implementation consists of a shared object, functions for customer and barber threads, and auxiliary functions for activity simulation. 
The program contains global variables: `C` keeps count of all customers, `N` keeps maximum count of waiting customers in waiting room.
### Shared object
_Shared_ object is object shared by all threads with shared resources and has some attributes:
- _mutex_ - main Mutex for shared object for locking and unlocking when accessing and updating shared variables. 
- _waiting_room_ keeps count of actually waiting customers in waiting room
- _customer_ Semaphore for indication if customer is going to get new hairstyle
- _barber_ Semaphore for indication if barber is going to cut hair
- _customer_done_ Semaphore for indication if customer has done hairstyle and is leaving
- _barber_done_ Semaphore for indication if barber done cutting hair
 
### Customer
Function _Customer_ is simulation of customer actions in infinite loop.

Begin of this function simulates waiting room. When thread reaches this part, we must lock main mutex to avoid integrity confusion, when after value is read by one thread, another can rewrite it.
Then we check value stored in `shared.waiting_room` and if there is no free place for customer, we unlock mutex and customer leaves and waits (_bulk_ function).
Otherwise, it increments value in `shared.waiting_room` and then unlock mutex.
To ensure requirements, we use before and after function simulating cutting customer (_get_haircut_) rendezvous (described in _Rendezvous on entering_ and _Rendezvous on leaving_).
After hair cutting we must leave waiting room, so we lock main mutex again and decrements `shared.waiting_room`, then unlocking mutex.

### Barber
Function _Barber_ is simulation of barber actions in infinite loop.

In this function we ar calling _cut_hair_ function, which simulates cutting hair by barber.
To ensure requirements -  barber is sleeping and customer must wake him up and then wait for them both to be done, we use _rendezvouses_ described below (_Rendezvous on entering_ and _Rendezvous on leaving_)

### Rendezvous on entering
For reaching our requirements when entering inside critical section, we use _rendezvous_ to synchronize threads execution. 
We want to wake up sleeping barber when new customer arrives and then cut customer's hair.
#### Barber side
On enter we first signal for customer, that barber is free for cutting. Then barber waits (sleeps).
```Python
shared.customer.signal()
shared.barber.wait()
```
#### Customer side
When customer is going into critical section, he signal to barber, for waking him up and then waits for cutting his hair.
```Python
shared.barber.signal()
shared.customer.wait() 
```

### Rendezvous on leaving
Barber must finish work and then customer must leave hair cutting room, so they need to wait each other after finished hair cutting.
#### Barber side
When cutting is done, in _Barber_ function barber signalize, that he completed work, and we wait for customer to leave.    
```Python
shared.barber_done.signal()
shared.customer_done.wait()
```

#### Customer side
In _Customer_ function we are waiting for signal from barber, that he completed cutting and then send signal, that customer is completed and can leave hair cutting room.
```Python
shared.barber_done.wait()
shared.customer_done.signal()
```

### Main
In _main_ function we create shared object and threads: one for _Barber_ and `C` for _Customer_ threads.

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