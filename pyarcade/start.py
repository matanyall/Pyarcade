from pyarcade.input_system import InputSystem

def run_pyarcade():
    input_sys = InputSystem()

    while True:
        print("Welcome to PyArcade (Enter number)")
        print("(1) Mastermind      (2) Minesweeper      (3) Crazy Eights     (4) Exit")
        game_input = str(input())

        if game_input == "4":
            break

        game_in_play = ""
        if game_input == "1":
            game_in_play = "Mastermind"
        elif game_input == "2":
            game_in_play = "Minesweeper"
        elif game_input == "3":
            game_in_play = "Crazy Eights"

        print(input_sys.handle_game_input(game_in_play, "New Game"))
        while True:
            print("Game Options:    "
                  "(1) New Game      "
                  "(2) Reset Game     "
                  "(3) Clear Game History      "
                  "(4) Quit")
            if game_input == "1":
                print("Please enter your guess (\"####\") or enter quit to leave game")
                user_move = str(input())
                if user_move == "quit":
                    break
                print(input_sys.handle_game_input(game_in_play, user_move))
                if input_sys.mastermind_game.game_state == "Game over.":
                    print("Game over. Play again? y/n")
                    if str(input()) != "y":
                        break
                    else:
                        print(input_sys.handle_game_input(game_in_play, "Reset"))
            elif game_input == "2":
                print("Please enter x, y coordinate (\"#,#\")")
                user_move = str(input())
                if user_move == "quit":
                    break
                print(input_sys.handle_game_input(game_in_play, user_move))
                if input_sys.minesweeper_game.game_state == "Game over.":
                    print("Game over. Play again? y/n")
                    if str(input()) != "y":
                        break
                    else:
                        print(input_sys.handle_game_input(game_in_play, "Reset"))
            elif game_input == "3":
                print("Please type draw or enter card you wish to play (Ex: Eight,Spades).")
                print("Or enter quit to leave game")
                user_move = str(input())
                if user_move == "quit":
                    break
                print(input_sys.handle_game_input(game_in_play, user_move))
                if input_sys.crazy_eights_game.game_state == "Game over.":
                    print("Game over. Play again? y/n")
                    if str(input()) != "y":
                        break
                    else:
                        print(input_sys.handle_game_input(game_in_play, "Reset"))
            else:
                break


if __name__ == "__main__":
    run_pyarcade()