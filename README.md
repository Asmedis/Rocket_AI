# Rocket AI 
This is a simple project attempting an unusual neural network with a undefined structure. (Currently not very succesful of efficient)
The aim for the ai running the rocket is to succesfully land on the landing pad as fast, accurately, softly as possible, reward system in `scoring.py`

# Usage
## To run
```
python game.py
```
or
```
python3 mage.py
```
## Required packages
Arcade
```
pip install arcade
```

## Internal setting
### game.py
ROCKET_AMOUNT - defiens amount of players ni the game, how many rocket compete and mutate

### brain.py
DEFAULT_NEURON_LINKS - how many random links can a neuron create

MAX_THINKING_STEPS - how many steps (times) the neurons send each other signals before the output neuron is read.

RADIATION - multiplier for mutating the weight values

# Preview
<img width="1950" height="1111" alt="image" src="https://github.com/user-attachments/assets/45b6e330-cd5c-45b1-a19d-6b6f29276e0c" />
