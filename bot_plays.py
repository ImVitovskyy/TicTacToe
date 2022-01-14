from random import choice

groups = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [7, 4, 1], [8, 5, 2], [9, 6, 3], [7, 5, 3], [9, 5, 1]]
corners = [1, 3, 7, 9]
r_corners = [9, 7, 3, 1]
middles = [2, 4, 6, 8]
opposites = {
    2: [7, 9],
    4: [3, 9],
    6: [1, 7],
    8: [1, 3]
}
plays = 1
bot_last_move = 0
strategy = 0

# groups -> Possible marks to win

# This variables above will be used just in the level 3 bot
# ↳ corners -> The board corners
# ↳ r_corners -> The corners, but reversed
# ↳ middles -> The middles of the board
# ↳ plays -> The number of times that the bot played
# ↳ bot_last_move -> The last move that the bot did
# ↳ strategy -> The strategy that the bot will use, actualy, this will only be usend on the level 3 bot

# This functions bellow will always return the board given, but with the modification of the bot's move

def bot_turn_1(board: dict):
    # Level 1 of difficulty
    # This level will make totally random moves everytime
    options = []
    
    # For every house in the board, if it's empty, append it on options
    for option in board.items():
        if option[1] == ' ':
            options.append(option[0])
    move = choice(options)

    board[move] = 'X'
    return board

def bot_turn_2(board: dict):
    # Level 2 of difficulty
    # This level will draw if make a random play or a kinda smart play
    smart = choice([1, 2]) # 1 -> smart move / 2 -> not smart move

    if smart == 1:
        # Check if someone is near to a win
        for possibility in groups:
            group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
            if group.count('X') == 2 and group.count(' ') == 1: # Means that the bot is near to a win
                move = group.index(' ') # Finding where to move to win
                board[possibility[move]] = 'X'
                return board
        
        # If arrived here, it means that the bot isn't near to a win, so the bot is going to check if the player is near to a win
        for possibility in groups:
            group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
            if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                move = group.index(' ') # Finding where to block the player
                board[possibility[move]] = 'X'
                return board

    # If arrived here, it means that anyone is near to a win or that the draw resulted in 2 so the bot does a random play
    board = bot_turn_1(board)
    return board

def bot_turn_3(board: dict, last_move: int):
    global plays, groups, bot_last_move, corners, r_corners, strategy, opposites
    # Strategy 1 and 2 is when the bot is startin the game
    # ↳ Strategy 1 -> Start from the cernter of the board
    # ↳ Strategy 2 -> Start from the corner of the board

    if last_move == 0: # It means that the bot is starting the game
        strategy = choice([1, 2])
    
    elif last_move != 0 and plays == 1: # It means that the player has already started the game
        # So we have to check if the player moved to 5, if yes, we have a problem, so, strategy 3
        if last_move == 5:
            strategy = 3

        # If the player didn't moved to 5, we had luck, so, strategy 4
        else:
            strategy = 4

    if strategy == 1: # The bot is starting, and the strategy is start from center
        if plays == 1: # If it's the first move
            board[5] = 'X'
            plays += 1
            bot_last_move = 5
            return board
    
        elif plays == 2: # If this is the second bot's move
            if last_move in corners: # If the player's first move was in the corners
                move = r_corners[corners.index(last_move)] # The bot will find the oposite side of the player's move
                board[move] = 'X'
                plays += 1
                bot_last_move = move
                return board
                
            else: # If the player's first move was in the middles, the bot will win
                move = choice(opposites[last_move])
                board[move] = 'X'
                plays += 1
                bot_last_move = move
                return board

        elif plays == 3: # If this is the third bot's move
            # Check if someone is near to a win
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('X') == 2 and group.count(' ') == 1: # Means that the bot is near to a win
                    move = group.index(' ') # Finding where to move to win
                    board[possibility[move]] = 'X'
                    return board
            
            # If arrived here, it means that the bot isn't near to a win, so the bot is going to check if the player is near to a win
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                    move = group.index(' ') # Finding where to block the player
                    board[possibility[move]] = 'X'
                    return board
            
            # If arrived here, so nobody is near to a win
            # The bot will move to the opposite side of the player's play
            for a in choice([[0, 1], [1, 0]]):
                if board[opposites[last_move][a]] == ' ':
                    board[opposites[last_move][a]] = 'X'
                    plays += 1
                    bot_last_move = opposites[last_move][a]
                    return board
        
        else: # If arrived here, it means that the game will end in a draw
            # Check if someone is near to a win
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('X') == 2 and group.count(' ') == 1: # Means that the bot is near to a win
                    move = group.index(' ') # Finding where to move to win
                    board[possibility[move]] = 'X'
                    return board
            
            # If arrived here, it means that the bot isn't near to a win, so the bot is going to check if the player is near to a win
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                    move = group.index(' ') # Finding where to block the player
                    board[possibility[move]] = 'X'
                    return board

        # If arrived here, the bot will make a random play, because the game will end in a draw
        return bot_turn_1(board)

    elif strategy == 2: # The bot is starting, and the strategy is start from the corners
        if plays == 1: # The first move will be any of the corners
            move = choice(corners)
            board[move] = 'X'
            plays += 1
            bot_last_move = move
            return board
        
        elif plays == 2: # The seconde move is kinda complicated
            # First, find the lines of the bot_last_move
            bot_lines = []
            for line in groups:
                if bot_last_move in line and line not in ([7, 5, 3], [9, 5, 1]):
                    bot_lines.append(line)

            if last_move in middles: # If the player moved in a middle, the bot won
                opposites_options = opposites[last_move]
                for option in opposites_options:
                    if option in bot_lines[0] or option in bot_lines[1]:
                        if board[option] == ' ':
                            move = option
                            board[move] = 'X'
                            plays += 1
                            bot_last_move = move
                            return board
            
            elif last_move in corners: # If the player moved in a corner, the bot will try to move to the opposite side
                opposite_player_move = r_corners[corners.index(last_move)]
                if board[opposite_player_move] == ' ':
                    move = opposite_player_move
                    board[move] = 'X'
                    plays += 1
                    bot_last_move = move
                    return board
                
                # If we can't move to an opposite side, we will go to some of the other corners last
                else:
                    if last_move in (1, 9):
                        move = choice([3, 7])
                        board[move] = 'X'
                        plays += 1
                        bot_last_move = move
                        return board
                    else:
                        move = choice([1, 9])
                        board[move] = 'X'
                        plays += 1
                        bot_last_move = move
                        return board
            
            if last_move == 5: # If the player moved to the center, the bot have to go to the opposite side of his first move
                opposite_bot_move = r_corners[corners.index(bot_last_move)]
                move = opposite_bot_move
                board[move] = 'X'
                plays += 1
                bot_last_move = move
                return board

        elif plays == 3:# If arrived here, probably, this game will end in a draw
            # Check if someone is near to a win
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('X') == 2 and group.count(' ') == 1: # Means that the bot is near to a win
                    move = group.index(' ') # Finding where to move to win
                    board[possibility[move]] = 'X'
                    return board
            
            # If arrived here, it means that the bot isn't near to a win, so the bot is going to check if the player is near to a win
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                    move = group.index(' ') # Finding where to block the player
                    board[possibility[move]] = 'X'
                    return board

            move = choice([a for a in corners if board[a] == ' '])
            board[move] = 'X'
            plays += 1
            bot_last_move = move
            return board

        else:
            # Check if someone is near to a win
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('X') == 2 and group.count(' ') == 1: # Means that the bot is near to a win
                    move = group.index(' ') # Finding where to move to win
                    board[possibility[move]] = 'X'
                    return board
            
            # If arrived here, it means that the bot isn't near to a win, so the bot is going to check if the player is near to a win
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                    move = group.index(' ') # Finding where to block the player
                    board[possibility[move]] = 'X'
                    return board
        
        return bot_turn_1(board)

    elif strategy == 3: # The player is starting from the center
        if plays == 1:
            # As the player moved to 5, we have to move to one of the corners
            move = choice(corners)
            board[move] = 'X'
            plays += 1
            bot_last_move = move
            return board
        
        elif plays == 2:
            # Checking if someone is near to a win
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('X') == 2 and group.count(' ') == 1: # Means that the bot is near to a win
                    move = group.index(' ') # Finding where to move to win
                    board[possibility[move]] = 'X'
                    plays += 1
                    bot_last_move = move
                    return board
            
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                    move = group.index(' ') # Finding where to block the player
                    board[possibility[move]] = 'X'
                    plays += 1
                    bot_last_move = move
                    return board
            
            if last_move in corners: # The player isn't near to a win
                # If the player moved to the opposite corner of the first play of the bot
                # The bot will move to a random empty corner
                for move in [a for a in corners if board[a] == ' ' and r_corners[corners.index(bot_last_move)] != a]:
                    board[move] = 'X'
                    plays += 1
                    bot_last_move = move
                    return board

        else:
            # If arrived here, it means that the game will probably end in a draw
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('X') == 2 and group.count(' ') == 1: # Means that the bot is near to a win
                    move = group.index(' ') # Finding where to move to win
                    board[possibility[move]] = 'X'
                    plays += 1
                    bot_last_move = move
                    return board
            
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                    move = group.index(' ') # Finding where to block the player
                    board[possibility[move]] = 'X'
                    plays += 1
                    bot_last_move = move
                    return board

        return bot_turn_1(board)

    elif strategy == 4: # The player is starting from the corners
        if plays == 1:
            # As the player started from the corners, the bot has to go to the mid
            board[5] = 'X'
            plays += 1
            bot_last_move = 5
            return board
        
        elif plays == 2:

            if last_move in corners:
                # First, check if the player is near to a win
                for possibility in groups:
                    group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                    if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                        move = group.index(' ') # Finding where to block the player
                        board[possibility[move]] = 'X'
                        plays += 1
                        bot_last_move = move
                        return board

                # If the player isn't near to a win, so he is making a trap
                # Move to any of the middles will block his trap
                move = choice(middles)
                board[move] = 'X'
                plays += 1
                bot_last_move = move
                return board
            
            else:
                # If the player moved to a mid, so he is probably near to a win
                for possibility in groups:
                    group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                    if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                        move = group.index(' ') # Finding where to block the player
                        board[possibility[move]] = 'X'
                        plays += 1
                        bot_last_move = move
                        return board
                
                # If the player isn't near to a win, the bot will make a random play in "return bot_turn_1(board)"

        else:
            # If arrived here, the game will probably end in a draw
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('X') == 2 and group.count(' ') == 1: # Means that the bot is near to a win
                    move = group.index(' ') # Finding where to move to win
                    board[possibility[move]] = 'X'
                    plays += 1
                    bot_last_move = move
                    return board
            
            for possibility in groups:
                group = (board[possibility[0]], board[possibility[1]], board[possibility[2]])
                if group.count('O') == 2 and group.count(' ') == 1: # Means that the player is near to a win
                    move = group.index(' ') # Finding where to block the player
                    board[possibility[move]] = 'X'
                    plays += 1
                    bot_last_move = move
                    return board

        return bot_turn_1(board)

def reset():
    # Everytime that the game restarts, this function will reset the variables that has been changed
    global plays, bot_last_move, strategy
    strategy = 0
    plays = 1
    bot_last_move = 0
