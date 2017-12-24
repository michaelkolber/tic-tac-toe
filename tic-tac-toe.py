import random

board = [
    ['-', '-', '-'],
    ['-', '-', '-'],
    ['-', '-', '-']
]

# print the board
def printBoard():
    print()
    print('  1 2 3')
    for item in range(3):
        print(item + 1, *board[item], sep=' ')
    print('\n')

# check if cell is empty
def isEmpty(r, c):
    return board[r][c] == '-'

# set a position to a certain piece
def setPos(row, col):
    global currentPlayer # make sure we can change the player after the turn

    # set the position with the correct player marker ('x' or 'o')
    if currentPlayer == 'user':
        board[row - 1][col - 1] = 'x' # -1 to adjust for 0-based indexes and normal user input
        currentPlayer = 'computer' # turn is over, switch players
        return
    else:
        board[row][col] = 'o'
        currentPlayer = 'user' # turn is over, switch players
        return

# make a move as the user
def userGo():
    while True:
        col = int(input("Choose a column: "))
        # input checking for column
        while col not in (1, 2, 3):
            col = int(input("Invald column, choose 1-3: "))

        row = int(input("Choose a row: "))
        # input checking for row
        while row not in (1, 2, 3):
            row = int(input("Invald row, choose 1-3: "))

        if isEmpty(row - 1, col - 1): # break only if the position isn't taken
            break
        else:
            print("Position is taken, try another.\n")
            # reset values to avoid old inputs being recycled
            row = -1
            col = -1

    setPos(row, col)

# check if someone won
def gameIsWon():
    # check if any row or column wins
    for i in range(3):
        if isEmpty(i, i): # quit if the character is the default '-'
            break
        elif (board[i][0] == board[i][1] == board[i][2]
              or board[0][i] == board[1][i] == board[2][i]):
            return True

    #check diagonals
    if isEmpty(1, 1): # quit if the character is the default '-'
        return False
    elif (board[0][0] == board[1][1] == board[2][2]
          or board[2][0] == board[1][1] == board[0][2]):
        return True

    # return false if no winning moves
    return False

# check for a tie
def boardFull():
    for r in range(3):
        for c in range(3):
            if isEmpty(r, c):
                return False
    return True

# check for rows containing 2 of the same token -- vulnerabilities (for the AI)
def check2():
    for i in range(3):
        # check if any row contains 2 of the same token
        if not isEmpty(i, 0) and isEmpty(i, 2) and board[i][0] == board[i][1]:
            return [i, 2]
        elif not isEmpty(i, 1) and isEmpty(i, 0) and board[i][1] == board[i][2]:
            return [i, 0]
        elif not isEmpty(i, 2) and isEmpty(i, 1) and board[i][2] == board[i][0]:
            return [i, 1]
        # check columns
        elif not isEmpty(0, i) and isEmpty(2, i) and board[0][i] == board[1][i]:
            return [2, i]
        elif not isEmpty(1, i) and isEmpty(0, i) and board[1][i] == board[2][i]:
            return [0, i]
        elif not isEmpty(2, i) and isEmpty(1, i) and board[2][i] == board[0][i]:
            return [1, i]
    # check diagonals
    if not isEmpty(0, 0) and isEmpty(2, 2) and board[0][0] == board[1][1]:
        return [2, 2]
    elif not isEmpty(1, 1) and isEmpty(0, 0) and board[1][1] == board[2][2]:
        return [0, 0]
    elif not isEmpty(2, 2) and isEmpty(1, 1) and board[2][2] == board[0][0]:
        return [1, 1]
    elif not isEmpty(0, 2) and isEmpty(2, 0) and board[0][2] == board[1][1]:
        return [2, 0]
    elif not isEmpty(1, 1) and isEmpty(0, 2) and board[1][1] == board[2][0]:
        return [0, 2]
    elif not isEmpty(2, 0) and isEmpty(1, 1) and board[2][0] == board[0][2]:
        return [1, 1]
    # if there are no obviously good moves,
    return [-1, -1]

# concise version of go() for the AI, without printing and input checking
def aiGo():
    coordinates = check2()
    if coordinates[0] == -1: # if there were no vulnerabilities found
        coordinates = [0, 0] # to avoid out of bounds errors
        # try random spots until one works
        while not isEmpty(coordinates[0], coordinates[1]):
            coordinates = [random.randint(0, 2), random.randint(0, 2)]
    setPos(coordinates[0], coordinates[1])


# main program
random.seed()
currentPlayer = 'computer'
print('Welcome to tic tac toe!')
print('You\'ll be x. The computer goes first.\n')

while True: # until someone wins
    if currentPlayer == 'user':
        print('Computer\'s turn.')
        aiGo()
    else:
        print('Your turn.\n')
        userGo()

    printBoard()
    if gameIsWon():
        # switch the conditions, since aiGo() and userGo() switch the user at the end
        if currentPlayer == 'computer':
            print('You win! To be fair, though, it\'s not a very smart program.\n')
            break
        else:
            print('The computer wins! You\'re literally a two-bit loser.\n')
            break
    elif boardFull():
        print('It\'s a tie!\n')
        break
