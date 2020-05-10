# PyArcade
- [Overview](#overview)
- [Setup](#setup)
  - [Required Software](#required-software)
  - [Steps](#steps)
  - [Notes](#notes)
- [Accounts](#accounts)
- [Games](#games)
  - [Blackjack](#blackjack)
  - [Crazy Eights](#crazy-eights)
  - [Mastermind](#mastermind)
  - [Minesweeper](#minesweeper)
- [Contributors](#contributors)

## Overview
PyArcade is an arcade full of a variety of games. These games range from simple guessing games to strategical games. 


## Setup
Visit [pyarcade.tk](http://pyarcade.tk) to
access PyArcade over the internet or download it using the following steps to
run it locally.

### Local Installation
#### Required Software
- Git
- Docker

#### Steps
1. Clone the repository and navigate to the repository root.  
```
git clone http://cmsc435.garrettvanhoy.com/cmsc435_group/pyarcade_extension.git
cd pyarcade_extension
```
2. Run the app.
   - Browser UI
     1. Start the app.
     ```
     docker-compose up
     ```
     2. Go to http://0.0.0.0:5000 in your browser
   - Command Line UI [deprecated]
     1. Start the app.
     ```
     docker-compose -f pyarcade-cmdline.yml run --rm app
     ```

### Notes
#### Website

#### Local Installation
- By design, `docker-compose up` does not check for changes when it builds the
containers. To check for changes that are different from the build cache use
`docker-compose up --build`.
- Database data will persist in the Docker database container after exiting. To
reset the database use `docker-compose down`.

## Accounts
On the website **DO NOT** use secure username / password information for any accounts.

## Games
### Blackjack
In this game, the player will be originally dealt two cards and one card from the houses hand will be flipped up. The player has
the choice to either have another card dealt to them (hit) or if they want to stick with their cards (stand). If the players hand's sum
is closest to twenty-one then the player wins, if the sum is over twenty-one they lose (bust), or if the sum is exactly twenty-one they win (blackjack). (User input should be in the form of either: Hit or Stand))

### Crazy Eights
In this game, the player will be originally dealt five cards and one card from the top the deck will be up. If the player has a 
card whose rank is eight or if they have a card that matches either the rank or the suit he can play the card. 
Otherwise, the player must draw a card from the deck. (User input should be in the form of: Rank,Suit))

### Mastermind
The goal of this game is for the player to correctly guess a hidden sequence of four numbers. The only hints the player will receive during the game is how many of the numbers they guessed 
are in the right location (bulls) and how many are located somewhere else in the sequence (cows). 
(User input should be in the form of: ####)

### Minesweeper
The goal of this game is for the player to uncover all of the cells of a hidden grid that do not contain a mine. As the player
uncovers cells, all of the adjacent cells that do not contain mines will be revealed and the number of mines near certain cells will appear.
(User input should be in the form of: #,#)

## Contributors
### Jill (25%)
- Created all of the game pages and added implemented gameplay functionality
- Created api for saves
- Created page that lists all of users saves and implemented the load functionality
- Set up the cloud instance and deployed our project to it

### Anders (25%)
- Refactor Blackjack and Crazy Eights to use uniform Card, Deck, and Player classes
- Refactor Flask routing and all templates to use Flask variable routing and
template inheritance to eliminate duplicate code
- Add game menus
- Add high scores database, REST API, and template
- Fix login bugs and update templates

### Andy(25%)
- Implemented documention using sphinx 
- documented and reviewed code 
- Format the documentation to be visually appealing 

### Matanya (25%)
- Implemented DevOps through Gitlab CI/CD
  - Automatic Testing with pytest, as well as coverage
- Added Favorite and Friends functionality through the rest API
- Did general bug fixes and improvements
- Updated documentation
- Managed Zoom Meetings

### Andy(0%)

