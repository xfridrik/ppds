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
shared.savage_mutex.lock()
shared.dining_room += 1
if shared.dining_room == D:
    shared.turnstile1.signal(D)
shared.savage_mutex.unlock()
shared.turnstile1.wait()
```
To ensure integrity, before incrementing value in dining rook to simulate that savage is ready to eat we first lock `savage_mutex`. Then value can be safely incremented and checked, if current savage is last one. If it is, he signal to all savages, that they can go eat and unlock Mutex. Otherwise, the savage is after unlocking mutex waiting for this signal from another savage (last line in snippet).

Savages are now in kitchen and can access pot where we are changing value, so we need to lock `savage_mutex` again to keep integrity. Then we check and wait, when cooks are currently cooking meal  - `shared.pot_full.wait()`. If they are not cooking, function `eat_from_pot` is called, where is decremented value in `pot`. When this was last portion and pot is empty, before unlocking Mutex, savage clear **Event** `pot_full` for all savages, so they can't eat and must wait and signalize `pot_empty` to cook new food:
```
shared.pot_full.clear()
shared.pot_empty.signal()
```

After this we use another **barrier** to wait all savages after eating and leaving _together_. In this way we get a **reusable barrier** for savage threads.

### Function _cook_
Function _cook_ is simulation of cook, cooking food in infinite loop.

## Important fragments in implementation

## Implementation verification


[^1]: https://www.eiffel.org/doc/solutions/Dining_savages