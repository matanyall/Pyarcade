# PyArcade
- [Overview](#overview)
- [Setup](#setup)
- [Games](#games)
- [Contributions](#contributions)

## Overview
PyArcade is an arcade full of a variety of games. These games range from simple guessing games to strategical games. Currently,
PyArcade is only playable through command line. Online version coming soon.

## Setup
### Docker (recommended)
1. Build the PyArcade image.  
`docker build -t pyarcade https://cmsc435.garrettvanhoy.com/cmsc435_group/pyarcade_extension`
2. Run the app.  
`docker run -it --rm pyarcade`

### Git
1. Clone the repository.  
`git clone https://cmsc435.garrettvanhoy.com/cmsc435_group/pyarcade_extension`
2. Navigate to the repository root and install the project dependencies.  
`pip install -r requirements.txt`
3. Run the app manually.  
`python pyarcade/start.py`

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

## Contributors
### Jill (50%)
*  Added Mastermind, Minesweeper, and Crazy Eight games to PyArcade along with their tests
*  Created an input system to handle input for all of the games
*  Updated each game so that they integrate with the input system
*  Created a basic command line ui to manual test interactions between the input system and the games
*  Created tests for input system
*  Updated README (Overview, Setup, Games, Contributions)

### Anders (35%)
*Note: login functionality not currently supported*
- Create Dockerfile to build app in stages
- Add `requirements.txt` to manage project dependencies
- Create Docker Compose YAML configuration
  - Specify MySQL database
  - Build app
- Add `controller.py` to query the database using SQLAlchemy with PyMySQL
- Add SQLAlchemy ORM User class for the database Users table
- `.dockerignore`, `db.env`, README format and [Setup](#setup)

### Andy(15%)
* Added Blackjack to pyarcade 
* formatted input system 
* updated blackjack to fit input system and remove coupling with curses
* added feature to display help menu for each game

