from pyarcade.controller import Controller
from pyarcade.input_system import InputSystem
from os import system, name


def run_pyarcade():
    input_sys = InputSystem()
    controller = Controller()
    username_logged_in = None

    while True:
        clear()
        print('Welcome to PyArcade (Enter number)')
        menu = '(1) Mastermind  (2) Minesweeper  (3) Crazy Eights  (4) Blackjack  (5) Create Account  (6) Login  (7) Exit'
        if username_logged_in:
            menu = '(1) Mastermind  (2) Minesweeper  (3) Crazy Eights  (4) Blackjack  (5) Logout  (6) Exit'
        print(menu)
        game_input = input()

        if game_input == '5' and username_logged_in:
            username_logged_in = None
            continue
        if game_input == '5' and not username_logged_in:
            print('Username:')
            username = input()
            print('Password:')
            passwd = input()
            print('Confirm password:')
            confirm = input()
            register_status = controller.register(username, passwd, confirm)

            clear()
            if not register_status:
                print('Failed to create account.')
            else:
                print('Account created.')
                controller.authenticate(username, passwd)
                username_logged_in = username
            continue
        if game_input == '6' and username_logged_in:
            break
        if game_input == '6' and not username_logged_in:
            print('Username:')
            username = input()
            print('Password:')
            passwd = input()
            auth_status = controller.authenticate(username, passwd)

            clear()

            if not auth_status:
                print('Login failed.')
            else:
                print('Login success.')
                username_logged_in = username
            continue
        if game_input == '7' and not username_logged_in:
            break

        game_in_play = ""
        if game_input == "1":
            game_in_play = "Mastermind"
        elif game_input == "2":
            game_in_play = "Minesweeper"
        elif game_input == "3":
            game_in_play = "Crazy Eights"
        elif game_input == "4":
            game_in_play = "BlackJack"

        clear()
        print(input_sys.handle_game_input(game_in_play, "New Game"))
        while game_in_play:
            print("Game Options: \n"
                  "New Game (Start new game)\n"
                  "Reset    (Reset game)\n"
                  "Clear    (Clear game history)\n"
                  "Help     (Game Instructions)\n"
                  "Quit     (Leave game)\n"
                  "* The options above can be entered at any time during game play *\n")
            if game_input == "1":
                print("Please enter your guess (\"####\")")
            elif game_input == "2":
                print("Please enter x, y coordinate (\"#,#\")")
            elif game_input == "3":
                print("Please type draw or enter card you wish to play (Ex: Eight,Spades).")
            elif game_input == "4":
                print("Please enter your move (hit or stand)")
            else:
                print("Invalid selection")
                break
            user_move = str(input())
            clear()
            if user_move.lower() == "quit":
                break
            print(input_sys.handle_game_input(game_in_play, user_move) + "\n")
            if input_sys.handle_game_input(game_in_play, "state") == "Game over.":
                print("Game over. Play again? y/n")
                if str(input()) != "y":
                    break
                else:
                    print(input_sys.handle_game_input(game_in_play, "reset"))

# define our clear function
def clear():

    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


if __name__ == "__main__":
    run_pyarcade()
