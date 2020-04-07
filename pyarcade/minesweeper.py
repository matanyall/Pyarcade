import random
from typing import Optional, Dict, List


class Minesweeper:

    def __init__(self, width: Optional[int] = 9, height: Optional[int] = 9, mines: Optional[int] = 10):
        self.game_state = "New game."
        self.width = width
        self.height = height
        self.mines = mines
        self.grid = self.generate_hidden_grid()
        self.total_squares = width * height
        self.game_history = []

    def generate_hidden_grid(self):
        temp_grid = [['-'] * self.height for _ in range(self.width)]

        mines_placed: int = 0
        while mines_placed <= self.mines:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)

            if temp_grid[row][col] != '*':
                temp_grid[row][col] = '*'
                mines_placed += 1

        return temp_grid

    def set_hidden_grid(self, mine_locations: Dict[int, List[int]]):
        self.grid = [['-'] * self.height for _ in range(self.width)]

        for row in mine_locations:
            for col in mine_locations[row]:
                self.grid[row][col] = '*'

    def draw_board(self):
        board_string = ""

        for x in range(0, self.width):
            board_string += '  %s ' % x
        board_string += '\n' + '  ' + ('====' * self.width)

        for row in range(self.height):
            board_string += '\n' + '{idx}|'.format(idx=row)
            for col in range(self.width):
                if self.game_state != "Game over." and self.grid[row][col] == '*':
                    board_string += ' %s ' % '-' + '|'
                else:
                    board_string += ' %s ' % self.grid[row][col] + '|'
            if row != self.width - 1:
                board_string += '\n |' + ('---|' * self.width)
        board_string += '\n  ' + ('====' * self.width)

        return board_string

    def make_move(self, guess: List[int]) -> str:
        """ Reveals squares surrounding user's guess

        Returns:
            -1 if the square is a mine
            0 if the square is already empty
            1 if all squares without mines revealed

        """
        self.game_state = "Ongoing"
        row_guess = guess[0]
        col_guess = guess[1]

        if row_guess < 0 or row_guess > self.height or col_guess < 0 or col_guess > self.width:
            raise IndexError

        self.game_history.append(guess)

        if self.grid[row_guess][col_guess] == '*':
            self.game_state = "Game over."
            return Minesweeper.draw_board(self) + "\nBOOM! Game over."

        if self.grid[row_guess][col_guess] == ' ' or self.grid[row_guess][col_guess].isdigit():
            return Minesweeper.draw_board(self) + "\nLocation already uncovered"

        self.grid[row_guess][col_guess] = self.check_adjacent_mines(row_guess, col_guess)

        if self.total_squares == self.mines:
            self.game_state = "Game over."
            return Minesweeper.draw_board(self) + "\nCongratulations! You win!"

        return self.draw_board()

    def check_adjacent_mines(self, row: int, col: int) -> str:
        mine_count = 0
        mine_count += self.check_if_mine(row + 1, col)      # N
        mine_count += self.check_if_mine(row - 1, col)      # S
        mine_count += self.check_if_mine(row, col - 1)      # W
        mine_count += self.check_if_mine(row, col + 1)      # E
        mine_count += self.check_if_mine(row + 1, col + 1)  # NE
        mine_count += self.check_if_mine(row + 1, col - 1)  # NW
        mine_count += self.check_if_mine(row - 1, col - 1)  # SW
        mine_count += self.check_if_mine(row - 1, col + 1)  # SE
        if mine_count > 0:
            return str(mine_count)
        else:
            self.total_squares -= 1
            return ' '

    def check_if_mine(self, r: int, c: int) -> int:
        if 0 <= r < self.height and 0 <= c < self.width and self.grid[r][c] == '*':
            return 1
        else:
            return 0

    def reset_game(self) -> str:
        self.game_state = "New game."
        self.grid = self.generate_hidden_grid()
        self.total_squares = self.width * self.height
        self.game_history.clear()
        return "Game reset"

    def clear_game_history(self) -> str:
        self.game_history.clear()
        return "History Cleared"
