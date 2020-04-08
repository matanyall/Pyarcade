import random
import time
from typing import Optional, Dict, List


class Minesweeper:

    def __init__(self, width: Optional[int] = 9, height: Optional[int] = 9, mines: Optional[int] = 10):
        self.game_state = "New game."
        self.width = width
        self.height = height
        self.mines = mines
        self.hidden_grid = self.generate_hidden_grid()
        self.total_hidden_squares = width * height
        self.game_history = []
        self.score = 0
        self.threebv = 0
        self.start_time = time.time()
        self.end_time = time.time()

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
        self.hidden_grid = [['-'] * self.height for _ in range(self.width)]

        for row in mine_locations:
            for col in mine_locations[row]:
                self.hidden_grid[row][col] = '*'

    def draw_board(self):
        board_string = ""

        for x in range(0, self.width):
            board_string += '  %s ' % x
        board_string += '\n' + '  ' + ('====' * self.width)

        for row in range(self.height):
            board_string += '\n' + '{idx}|'.format(idx=row)
            for col in range(self.width):
                if self.game_state != "Game over." and self.hidden_grid[row][col] == '*':
                    board_string += ' %s ' % '-' + '|'
                else:
                    board_string += ' %s ' % self.hidden_grid[row][col] + '|'
            if row != self.width - 1:
                board_string += '\n |' + ('---|' * self.width)
        board_string += '\n  ' + ('====' * self.width)

        return board_string

    def count_threebv(self):
        solution = [row[:] for row in self.hidden_grid]
        row = 0
        col = 0
        while solution[row][col] == "*" and self.is_valid(row, col):
            col += 1
        self.bfs(solution, row, col, True)
        processed = [['.'] * self.height for _ in range(self.width)]
        for row_idx in range(len(solution)):
            for col_idx in range(len(solution[row_idx])):
                if solution[row_idx][col_idx] == " " and processed[row_idx][col_idx] != "*":
                    self.threebv += 1
                    self.flood_fill(row_idx, col_idx, solution, processed)

        for row_idx in range(len(processed)):
            for col_idx in range(len(processed[row_idx])):
                if processed[row_idx][col_idx] == "." and solution[row_idx][col_idx].isdigit():
                    self.threebv += 1

    def get_threebv(self):
        return self.threebv

    def flood_fill(self, row_idx, col_idx, sol, proc):
        queue = [(row_idx, col_idx)]
        proc[row_idx][col_idx] = "*"
        while queue:
            directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            row_idx, col_idx = queue.pop()
            for d in directions:
                nxt_row, nxt_col = row_idx + d[0], col_idx + d[1]
                if self.is_valid(nxt_row, nxt_col) and proc[nxt_row][nxt_col] != '*':
                    proc[nxt_row][nxt_col] = "*"
                    if sol[nxt_row][nxt_col] == " ":
                        queue.append((nxt_row, nxt_col))

    def set_score(self):
        time_elapsed = self.end_time - self.start_time
        self.count_threebv()
        self.score = int((self.threebv / time_elapsed) * 100)

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

        if self.hidden_grid[row_guess][col_guess] == '*':
            self.game_state = "Game over."
            return Minesweeper.draw_board(self) + "\nBOOM! Game over."

        if self.hidden_grid[row_guess][col_guess] == ' ' or self.hidden_grid[row_guess][col_guess].isdigit():
            return Minesweeper.draw_board(self) + "\nLocation already uncovered"

        self.bfs(self.hidden_grid, row_guess, col_guess, False)

        if self.total_hidden_squares == self.mines:
            self.game_state = "Game over."
            self.end_time = time.time()
            self.set_score()
            return Minesweeper.draw_board(self) + "\nCongratulations! You win!"

        return self.draw_board()

    def bfs(self, grid: [[str]], row_idx: int, col_idx: int, reveal_board: bool):
        queue = [(row_idx, col_idx)]
        grid[row_idx][col_idx] = self.check_adjacent_mines(row_idx, col_idx)
        if not reveal_board:
            self.total_hidden_squares -= 1
        while queue:
            directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            row_idx, col_idx = queue.pop()
            for d in directions:
                nxt_row, nxt_col = row_idx + d[0], col_idx + d[1]
                if self.is_valid(nxt_row, nxt_col) and grid[nxt_row][nxt_col] == '-':
                    grid[nxt_row][nxt_col] = self.check_adjacent_mines(nxt_row, nxt_col)
                    if not reveal_board:
                        self.total_hidden_squares -= 1
                        if grid[nxt_row][nxt_col] == " ":
                            queue.append((nxt_row, nxt_col))
                    else:
                        queue.append((nxt_row, nxt_col))

    def is_valid(self, row: int, col: int):
        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            return False
        return True

    def check_adjacent_mines(self, row: int, col: int) -> str:
        mine_count = 0
        mine_count += self.check_if_mine(row + 1, col)  # N
        mine_count += self.check_if_mine(row - 1, col)  # S
        mine_count += self.check_if_mine(row, col - 1)  # W
        mine_count += self.check_if_mine(row, col + 1)  # E
        mine_count += self.check_if_mine(row + 1, col + 1)  # NE
        mine_count += self.check_if_mine(row + 1, col - 1)  # NW
        mine_count += self.check_if_mine(row - 1, col - 1)  # SW
        mine_count += self.check_if_mine(row - 1, col + 1)  # SE
        if mine_count > 0:
            return str(mine_count)
        else:
            return ' '

    def check_if_mine(self, r: int, c: int) -> int:
        if self.is_valid(r, c) and self.hidden_grid[r][c] == '*':
            return 1
        else:
            return 0

    def reset_game(self) -> str:
        self.game_state = "New game."
        self.hidden_grid = self.generate_hidden_grid()
        self.total_hidden_squares = self.width * self.height
        self.game_history.clear()
        return "Game reset"

    def clear_game_history(self) -> str:
        self.game_history.clear()
        return "History Cleared"
