# PPDS assignment 4 - Dining savages
At this assignment we deal dining savages problem.


## Dining savages problem
_Dining savages_ problem is analogy based on savages who share one pot. The pot contains a certain number of portions of food and savages can take from it as long as it is not empty.
When the pot is empty, the savage must tell the cook(s) to fill it up again so that the savages can eat again until there is food.[^1]

## Our implementation requirements
- The savages begin to dine all together. They start eating when the last one arrives.
- Savage always get one portion at a time, until the pot is empty.
- When the savage discovers that the pot is empty, he calls the cooks to cook.
- Savages are waiting for the whole pot to be filled.
- The cook always cooks and puts to pot one portion at a time.
- When the pot is full, savages continue to eat.
- The process is repeated endlessly.

## Implementation
The implementation consists of a Shared object, functions for savages and cooks and auxiliary functions for _eating from pot_ and _putting food into pot_ simulations.

The program contains global variables: `D` keeps count of all savages, `K` keeps count of all cooks, `H` keeps maximum count of portions in pot.

### Shared object
Shared object is object shared by all threads (savages and cooks) with shared resources and has some attributes:

* _savage_mutex_ - Mutex for accessing pot by savages while eating
* _cook_mutex_ - Mutex for accessing pot by cooks while adding food into it
* _barrier_mutex_ - Mutex for accessing variable in barrier
* _pot_ - actual number of remaining portions in pot
* _dining_room_ - actual number of savages in dining room
* _turnstile1_ - turnstile for barrier when entering dining room
* _turnstile2_ - turnstile for barrier when leaving dining room
* _pot_empty_ - Event for empty pot signalisation to cook new food (this event is signalised in initialisation, because pot is empty first)
* _pot_full_ - Event for full pot signalisation to start eating

### Function _savage_
Function _savage_ is simulation of savage, eating in infinite loop.

We have requirement, that the savages begin to dine all together and must wait to last one before going to eat. To ensure this we use **barrier** at begin:
```
shared.barrier_mutex.lock()
shared.dining_room += 1
if shared.dining_room == D:
    shared.turnstile1.signal(D)
shared.barrier_mutex.unlock()
shared.turnstile1.wait()
```
To ensure integrity, before incrementing value in dining room to simulate that savage is ready to eat we first lock `barrier_mutex`. Then value can be safely incremented and checked, if current savage is last one. If it is, he signal to all savages, that they can go eat and unlock Mutex. Otherwise, the savage is after unlocking mutex waiting for this signal from another savage (last line in snippet).

Then we lock `savage_mutex` and check pot value. When the pot is empty (0), savage clear **Event** `pot_full` for savages, so they can't eat and must wait and signalize `pot_empty` to cook new food:
```
shared.pot_full.clear()
shared.pot_empty.signal()
```

Then we check and wait, when cooks are currently cooking meal  - `shared.pot_full.wait()`. If they are not cooking, function `get_from_pot` is called, where is decremented value in `pot` and simulated getting portion by sleeping for 0.1 seconds. Then can be mutex unlocked and savage can eat - function `eat_portion` with sleep for 0.2 seconds is called.

After this we use another **barrier** to wait all savages after eating and leaving _together_. In this way we get a **reusable barrier** for savage threads.

### Function _cook_
Function _cook_ is simulation of cook, cooking food in infinite loop.

In function cook we call `cook_portion` function at begin, which contains only _sleep_ to simulate food cooking. We want to modify `pot` value, so we are using mutex to ensure integrity.

After locking mutex, we check, if pot is full. When it is full, thread clear `pot_empty` event - cooks are no more adding food into pot. Then send `pot_full` signal to savages, that pot is full and they can eat again.
```
shared.pot_empty.clear()
shared.pot_full.signal()
```


Then function is waiting for `pot_empty` signal, which indicate that pot is empty and cooks can add food into it - by calling function `add_to_pot` which is incrementing pot value and simulating adding portion by sleeping for 0.1 seconds.



## Implementation review
We have also added prints for the important thread activities and simulated by running our implementation with parameters: 5 savages (`D`), 3 cooks (`K`) and maximum pot capacity 4 (`H`). Result is displayed below.

### Sample console output
![img.png](img.png)

First line indicate, that all savages are ready to eat, but pot is empty first, so they must wait until cooks fill pot. Cooks are then filling pot one by one and last cook signalize to cooks that pot is already full, and they can stop adding food and to savages signalizes, that they can get portion and eat. The 4 savages get and eat all the portions and the next savage signals that pot is empty. Cooks add portions and fill pot again and then can get portion last one savage while others are waiting. When every savage is done eating, they can go to the next round.

[^1]: https://www.eiffel.org/doc/solutions/Dining_savages