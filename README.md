# Inkspired
 
Mutiplayer game made for the french contest "Trophées NSI". This is a drawing contest game playable online.

![scène1](https://github.com/user-attachments/assets/9b400039-7dda-481e-af24-80e917349d20)

## Challenges

This game has been created with some challenges requested by the contest. For exemples the game must be written only in python and SQL and in the context of the french NSI's Program. This was a real challenge for a game online because there is no real place for a server.

## Installation

You can download a .exe file on the releases tab and execute it ! ([here](https://github.com/xmanu91/Trophees-NSI/releases))

Or you can clone this repository.

Then, you can install the required packages by using this command:

```BASH
pip install -r requirements.txt
```

Finnaly, run the game by running the main.py file:
```BASH
py main.py
```
## Rules

The game is played by a minimum of three people. New players can be added by joining with a private code. Choice of number of rounds and length of rounds. Players can choose the general theme of the game. New players can be added by joining with private code. Choice of number and duration of rounds.

### First phase 

A word is drawn at random from the theme list.

### Second phase

Players must draw a picture around the word they have chosen.

Players have access to the following tools:

- Brush
- Eraser
- Pot

They also have access to the following parameters:

- Brush size
- Backspace
- Color change

### Third phase

Players vote for the best design. Then return to phase 1 for x rounds (variable).

Players may not vote for themselves

### Fourth phase

End of game, player ranking.
