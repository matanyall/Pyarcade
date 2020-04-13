# PyArcade
- [Overview](#overview)
- [Setup](#setup)
- [Games](#games)
- [Contributions](#contributions)

## Overview
PyArcade is an arcade full of a variety of games. These games range from simple guessing games to strategical games. Currently,
PyArcade is only playable through command line. Online version coming soon.

## Setup
To play pyarcade, download the pyarcade_extension and navigate to the directory using your terminal. Run the command `python setup.py install` 
to install the package. To run pyarcade all you need to do is type the command `pyarcade`. Enjoy!

## Games
### Mastermind
The goal of this game is for the player to correctly guess a hidden sequence of four numbers. The only hints the player will receive during the game is how many of the numbers they guessed 
are in the right location (bulls) and how many are located somewhere else in the sequence (cows). 
(User input should be in the form of: ####)

### Minesweeper
The goal of this game is for the player to uncover all of the cells of a hidden grid that do not contain a mine. As the player
uncovers cells, all of the adjacent cells that do not contain mines will be revealed and the number of mines near certain cells will appear.
(User input should be in the form of: #,#)

### Crazy Eights
In this game, the player will be originally dealt five cards and one card from the top the deck will be up. If the player has a 
card whose rank is eight or if they have a card that matches either the rank or the suit he can play the card. 
Otherwise, the player must draw a card from the deck. (User input should be in the form of: Rank,Suit))

### Black Jack
In this game, the player will be originally dealt two cards and one card from the houses hand will be flipped up. The player has
the choice to either have another card dealt to them (hit) or if they want to stick with their cards (stand). If the players hand's sum
is closest to twenty-one then the player wins, if the sum is over twenty-one they lose (bust), or if the sum is exactly twenty-one they win (blackjack).
(User input should be in the form of either: Hit or Stand))

## Contributions
### Jill (40%)
*  Added Mastermind, Minesweeper, and Crazy Eight games to PyArcade along with their tests
*  Created an input system to handle input for all of the games
*  Updated each game so that they integrate with the input system
*  Created a basic command line ui to manual test interactions between the input system and the games
*  Created tests for input system
*  Updated README (Overview, Setup, Games, Contributions)

### Anders

### Andy(15%)
* Added Blackjack to pyarcade 
* formatted input system 
* updated blackjack to fit input system and remove coupling with curses

