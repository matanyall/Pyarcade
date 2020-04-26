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
- [Contributions](#contributions)

## Overview
PyArcade is an arcade full of a variety of games. These games range from simple guessing games to strategical games. Currently,
PyArcade is only playable through command line. Online version coming soon.

## Setup
### Required Software
- Git
- Docker

### Steps
1. Clone the repository.  
```
git clone http://cmsc435.garrettvanhoy.com/cmsc435_group/pyarcade_extension.git
```
2. Navigate to the repository root and run the app.
```
cd pyarcade_extension
docker-compose run --rm app
```
##Running the login page
1. Start pyarcade with the pyarcade-deploy.yml
```
docker-compose -f pyarcade-deploy.yml up
```
2. Go to http://0.0.0.0/signup in your browser to make an account.
3. After signing up, go to http://0.0.0.0/login to sign into your account.
### Notes
- **DEVELOPERS:**  
If changes are made to the code base, `docker-compose run` does not pick up on
them. To bypass the Docker build cache and apply the changes correctly run
`docker-compose build --no-cache` before `docker-compose run --rm app`.
- The database container will be left running after exiting. In the current
absence of a mounted volume this allows for data persistence. To reset the
database in between runs use `docker-compose down`.

## Accounts
Luckily, this app runs locally. It probably could not be any less secure.

## Games
### Blackjack
In this game, the player will be originally dealt two cards and one card from the houses hand will be flipped up. The player has
the choice to either have another card dealt to them (hit) or if they want to stick with their cards (stand). If the players hand's sum
is closest to twenty-one then the player wins, if the sum is over twenty-one they lose (bust), or if the sum is exactly twenty-one they win (blackjack).
(User input should be in the form of either: Hit or Stand))

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
### Jill (%)
- 

### Anders (%)
- Fix the database integration
  - Implement `wait-for-it.sh` script by cloning it onto the Docker machine
  in the Dockerfile
  - Debug `docker-compose` to run the database in the background and the app in
  the foreground
  - Rewrite [Setup](#setup)
- Add user accounts
  - Add UI / input handling for create account, login, and logout
  - Query database to insert and select users' usernames and passwords

### Andy(%)
- 

### Matanya (%)
- 

