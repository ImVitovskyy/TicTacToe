from random import randint, choice
from json import load
from time import sleep
import bot_plays

score = [0, 0]
# groups -> All the combinations of the board to win
groups = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [7, 4, 1], [8, 5, 2], [9, 6, 3], [7, 5, 3], [9, 5, 1]]

with open('phrases.json', 'r') as file:
    # Loading some phrases that the bot will print during the game

    phrases = load(file)

def verify_win():
    # Checking if the game has a winner
    # 1 means that the player won
    # 2 means that the bot won
    for possibility in groups:
        if (board[possibility[0]], board[possibility[1]], board[possibility[2]]) == ('O', 'O', 'O'):
            return 1 
        elif (board[possibility[0]], board[possibility[1]], board[possibility[2]]) == ('X', 'X', 'X'):
            return 2
    
    # Checking if the game has a draw 
    # draw receives True, and if just one of the values of the board is empty, it receives False, "canceling" the draw
    draw = True
    for value in board.values():
        if value == ' ':
            draw = False
    if draw is True:
        return 3

    # If the game doesn't have a draw or a winner, return False, continuing the game
    return False

def board_status():
    # This function just shows the game state in a nice way

    print('|=====||=====||=====|\n'
          f'|  {board[7]}  ||  {board[8]}  ||  {board[9]}  |\n'
          '|=====||=====||=====|\n'
          f'|  {board[4]}  ||  {board[5]}  ||  {board[6]}  |\n'
          '|=====||=====||=====|\n'
          f'|  {board[1]}  ||  {board[2]}  ||  {board[3]}  |\n'
          '|=====||=====||=====|')

def game_level():
    # This function will print the game difficulty levels and get the player's choice

    chosen_mode = input("[1] Easy\n[2] Medium\n[3] This level is like impossible, bro, don't pick this one\n")

    if chosen_mode not in ('1', '2', '3'):
        print('Choose a valid game mode!')
        return game_level()

    print("Nice choice, I'll draw who starts...")
    sleep(1)
    who_starts = randint(1, 1) # 1 means player, and 2 means bot

    if who_starts == 1:
        print("I'm X and you're O\nYou start")
        board_status()
        continue_game(1, int(chosen_mode))
    else:
        print("I'm X and you're O\nI was the one drawn, so I'll start, let me think...")
        sleep(1)
        continue_game(2, int(chosen_mode))

def continue_game(turn, level):
    # turn -> Who starts the game
    # level -> The bot's level of difficulty
    global board

    def player_turn():
        # Everytime that the player will play, I'll call this function
        global board

        move = input()

        # Verifying if the inputted value is valid, if yes, modifying the board
        if move.isnumeric():
            if board[int(move)] == ' ':
                board[int(move)] = 'O'
            else:
                print('Type a valid move!!')
                board_status()
                return player_turn()
        else:
            print('Type a valid move!!')
            board_status()
            return player_turn()
        
        board_status()

        if verify_win() == 1: # Means that the player won
            score[0] += 1
            print(f'You won!\n{choice(phrases["lost"])}')
        
        elif verify_win() == 2: # Means that the bot won
            score[1] += 1
            print(f'I won!\n{choice(phrases["won"])}')
        
        elif verify_win() == 3: # Means thet the game ended in a draw
            print('This game ended in a draw, you had luck...')
        
        else:
            # Bot turn
            print('My turn')
            sleep(1)
            print(choice(phrases['loosing']))
            sleep(1)
            bot_turn(level, move)
            
    def bot_turn(level: int, last_move: int):
        # level -> The bot's level of difficulty
        # starts -> The bot will start the game
        global board

        if level == 1:
            board = bot_plays.bot_turn_1(board)
        elif level == 2:
            board = bot_plays.bot_turn_2(board)
        else:
            board = bot_plays.bot_turn_3(board, int(last_move))

        board_status()

        if verify_win() == 1: # Means that the player won
            score[0] += 1
            print(f'You won!\n{choice(phrases["lost"])}')
        
        elif verify_win() == 2: # Means that the bot won
            score[1] += 1
            print(f'I won!\n{choice(phrases["won"])}')
        
        elif verify_win() == 3: # Means thet the game ended in a draw
            print('This game ended in a draw, you had luck...')
        
        else:
            # Player turn
            print(choice(phrases['winning']))
            print('Your turn')
            player_turn()
    
    if turn == 1:
        player_turn()
    
    else:
        bot_turn(level, 0)

while True:
    board = {1: ' ', 2: ' ', 3: ' ', 4: ' ', 5: ' ', 6: ' ', 7: ' ', 8: ' ', 9: ' '}
    print('\nWellcome to Tic Tac Toe, made by Phant - https://github.com/ImPhant')
    print('Choose your game mode')
    game_level()
    print(f'The score is: {score[0]} / {score[1]}')
    input('If you whant to to play again, press Enter\n')
    bot_plays.reset()
