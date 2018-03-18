import os
import random
import datetime
from copy import deepcopy, copy

# constants
START_BLUE = "\u001b[34m"
END_BLUE = "\u001b[0m"
START_PINK = "\u001b[35m"
END_PINK = "\u001b[0m"
START_RED = "\u001b[31m"
END_RED = "\u001b[0m"
START_GREEN = "\u001b[32m"
END_GREEN = "\u001b[0m"
START_BOLD = "\033[1m"
END_BOLD = "\033[0m"

class GameData: 
    level_dict = {"1": "easy_sudoku2.csv", "2": "medium_sudoku.csv", "3": "hard_sudoku.csv"}
    choosen_level = []
    user_name = ""
    original = []
    quit = False
    restart = False
    best_times_dict = dict()
    choosen_row = ""
    choosen_column = ""
    input_matrix = [["row", "column"], [choosen_row, choosen_column]]
    filled_board = False

game_data = GameData()

# waits for an input before continue
def wait():
    input()

# imports sudoku board from files on a choosen level - randomly from three different games on each level
def import_sudoku(sudoku, filename="easy_sudoku.csv", skip=0):
    line_read = 0
    with open(filename, "r") as input_stream:
        for i in range((skip*8)+skip):
            next(input_stream)
        for line in input_stream:
            if line_read == 9:
                break
            line = line.strip("\n")
            current_line = line.split(",")
            sudoku.append(current_line)
            line_read += 1
    return sudoku

# draws the Sudoku title
def title():
    os.system('clear')
    print("   _____           _       _          \n" +
          "  / ____|         | |     | |         \n" +
          " | (___  _   _  __| | ___ | | ___   _ \n" +
          "  \___ \| | | |/ _` |/ _ \| |/ / | | |\n" +
          "  ____) | |_| | (_| | (_) |   <| |_| |\n" +
          " |_____/ \__,_|\__,_|\___/|_|\_\\\\__,_|\n" +
          "                                      \n")

def menu():
    game_data.user_name = game_data.user_name  
    while True:  # amig igaz 
        if exit:
            game_data.choosen_level = deepcopy(game_data.original)   
        os.system('clear') 
        title() 
        if not game_data.user_name:
            game_data.user_name = input("Please enter your name: \n")
        print("\nFor row, column and number you can type in numbers from", START_BLUE+"1 to 9"+END_BLUE+".")
        print("If you want to delete a number, press", START_BLUE+"enter"+END_BLUE+" or type", START_BLUE+"\"0\""+END_BLUE+".")
        print("If you want to quit the game or the chosen level, type", START_BLUE, "\"exit\""+END_BLUE+".")
        print("If you want to restart the game, type", START_BLUE+"\"restart\""+END_BLUE+"!\n")
        print("For easy level, press", START_BLUE, "\"1\""+END_BLUE+"!\nFor medium level, press",
              START_BLUE+"\"2\""+END_BLUE+"!\nFor hard level, press", START_BLUE+"\"3\""+END_BLUE+"!")
        print()
        level = input("Please choose level: ")

        start_time = datetime.datetime.now()
        if level in game_data.level_dict.keys():
            num = random.randint(0, 2)
            game_data.choosen_level = import_sudoku(game_data.choosen_level, game_data.level_dict[level], num)
            break
        elif is_exit(level):
            game_data.quit = True
            break
        else:
            print("Invalid input, press enter to continue!")
            wait()

# continually checking if the board is full
def check_if_board_full():
    game_data.filled_board = True
    for row in range(9):
        for column in range(9):
            if game_data.choosen_level[row][column] == " ":
                return False
    return True

# checks if the fully filled board is correct (1-9 in each row, column and block)
def check_if_board_correct(sudoku_board):
    for row in sudoku_board:
        for number in row:
            if row.count(number) > 1:
                return False
    value = len(sudoku_board)
    each_row = []
    while value > 0:
        for row in sudoku_board:
            each_row.append(row[value - 1])
        for number in each_row:
            if each_row.count(number) > 1:
                return False
            each_row = []
            value -= 1
        return True
    shift_column = 0
    while shift_column <= 6:
        shift_row = 0
        while shift_row <= 6:
            box = []
            for row in range(3):
                for column in range(3):
                    box.append(sudoku_board[shift_row + row][shift_column + column])
                    for number in box:
                        if each_row.count(number) > 1:
                            return False
                        box = []
            shift_row += 3
        shift_column += 3
    return True

# displays the result when board is full 
def display_result(filled_board):
    if game_data.filled_board:
        for row in range(len(game_data.choosen_level)):
            for item in range(len(game_data.choosen_level)):
                game_data.choosen_level[row][item] = int(game_data.choosen_level[row][item])
        if check_if_board_correct(game_data.choosen_level):
            draw_board()
            print(START_PINK+"\nCORRECT answer, congratulations!!!\n"+END_PINK)
            user_time = datetime.datetime.now() - start_time
            print("Dear %s, your time is: %s." % (game_data.user_name, user_time))
            time_export(game_data.best_times_dict, "results.csv")
            game_data.quit = True
        else:
            draw_board()
            print(START_PINK+"\nWRONG answer, press enter to continue!\n"+END_PINK)
            game_data.filled_board = False
            wait()
            os.system('clear')

# draws the sudoku board
def draw_board():
    title()
    shift_column = 0
    shift_row = 0
    row_number = 1
    print(START_BOLD+START_RED+"      1 2 3   4 5 6   7 8 9"+END_BOLD+END_RED)
    print()
    while shift_column <= 6:
        print("    + - - - + - - - + - - - +", end="\n")
        for row in range(3):
            print(START_BOLD+START_RED, row_number, END_BOLD+END_RED, "|", end=" ")
            row_number += 1
            shift_row = 0
            while shift_row <= 6:
                for column in range(3):
                    if game_data.original[row + shift_column][column + shift_row] == " ":
                        print(game_data.choosen_level[row + shift_column][column + shift_row], end=" ")
                    else:
                        print(START_GREEN+str(game_data.choosen_level[row + shift_column][column + shift_row]) +
                              END_GREEN, end=" ")
                print("|", end=" ")
                shift_row += 3
            print()
        shift_column += 3
    print("    + - - - + - - - + - - - +", end="\n")
    print()

# restart the choosen board if called by the user
def restart(choosen_level):
    game_data.restart = True
    game_data.choosen_level = deepcopy(game_data.original)
    return game_data.choosen_level

# exports the time of the game to an external file with the player's name
def time_export(best_times_dict, filename="times.csv"):
    try:
        with open(filename, "a") as output_stream:
            for name, time in game_data.best_times_dict.items():
                output_stream.write("%s- %s" % (name, time))
            output_stream.write("%s- %s\n" % (game_data.user_name, user_time))
    except FileNotFoundError:
        with open(filename, "w") as output_stream:
            output_stream.write("%s- %s" % (game_data.user_name, user_time))

def is_exit(choice):
    return str.upper(choice) == "EXIT"  # true vagy false?

def is_restart(choice):
    return str.upper(choice) == "RESTART"  # true vagy false?

def row_column_validation(value, input_matrix, i):
    while not (str.isdigit(value)) or (int(value) > 9 or int(value) < 1):  # szám ellenőrzése  
        if is_exit(value):
            exit = True
            break
        value = input("Enter 222 the %s: " % game_data.input_matrix[i])
        if is_restart(value):
            game_data.choosen_level = restart(game_data.choosen_level)
            break
    return value 

# a row, colum bekérése utáni tényleges szám ellenőrzése
def input_validation(choosen_number):
    while not str.isdigit(choosen_number) or (int(choosen_number) > 9 or int(choosen_number) < 1):
        choosen_number = input("Enter the number222: ")
        if (choosen_number == "" or choosen_number == "0") and game_data.original[int(game_data.choosen_row) - 1] \
            [int(game_data.choosen_column) - 1] == " ":
            choosen_number = " "
            break
        if is_exit(choosen_number):
            exit = True
            break
        if is_restart(choosen_number):
            game_data.choosen_level = restart(game_data.choosen_level)
            game_data.restart = True
            break
    return choosen_number

def change_cell(choosen_number):
    int_choosen_row = int(game_data.choosen_row) - 1
    int_choosen_column = int(game_data.choosen_column) - 1
    if game_data.original[int_choosen_row][int_choosen_column] == " ":
        if choosen_number == " ":
            game_data.choosen_level[int_choosen_row][int_choosen_column] = choosen_number
        else:
            game_data.choosen_level[int_choosen_row][int_choosen_column] = int(choosen_number)
    else:
        if choosen_number != " ":
            print("You cannot change the given numbers, press enter to continue!")
            wait()
        else:
            print("You cannot delete the given numbers, press enter to continue!")
            wait()

    os.system('clear')
    game_data.filled_board = check_if_board_full()  # nyerés ellenőrzése
    display_result(game_data.filled_board)

def game_cycle(filled_board, original, exit):
    while not game_data.filled_board and not exit: # amig ezek false-ok
        draw_board()
        exit = False

        game_data.input_matrix = ["row", "column"]
        game_data.restart = False
        for i in range(2):  # ez lenne a main input???
            value = input("Enter the %s: " % game_data.input_matrix[i])
            if is_exit(value):
                exit = True
                break
            if is_restart(value):
                game_data.choosen_level = restart(game_data.choosen_level)
                game_data.restart = True
                break
            value = row_column_validation(value, game_data.input_matrix, i)
            if exit or game_data.restart:
                break
            if game_data.input_matrix[i] == "row":
                game_data.choosen_row = value
            else:
                game_data.choosen_column = value
        if exit:
            break

        if not game_data.restart:
            choosen_number = input("Enter the number: ")
            if is_exit(choosen_number):
                exit = True
                break
            if is_restart(choosen_number):
                game_data.choosen_level = restart(game_data.choosen_level)
                continue
            if (choosen_number == "" or choosen_number == "0"):
                choosen_number = " "
            else:
                choosen_number = input_validation(choosen_number)
            if exit:
                break
            if game_data.restart:
                continue
            change_cell(choosen_number)

def main():
    menu()
    if not game_data.quit:
        game_data.original = deepcopy(game_data.choosen_level)
        game_data.filled_board = check_if_board_full()
        exit = False
        game_cycle(game_data.filled_board, game_data.original, exit) 
        main()  

main()