import random

def generate_random_fleet(board_size):
    ships = [5, 4, 3, 3, 2]
    placed_ships = []
    board = []
    for i in range(board_size):
        board_row = []
        for j in range(board_size):
            board_row.append(0)
        board.append(board_row)

    for ship in ships:
        valid = False
        while (not valid):

            x = random.randint(1, board_size)-1
            y = random.randint(1, board_size)-1
            o = random.randint(0, 1)

            if o == 0:
                ori = "v"
            else:
                ori = "h"
            valid = validate(board, ship, x, y, ori)

        board = place_ship(board, ship, ori, x, y)
        if ori == "v":
            placed_ships.append(tuple(map(str, (x, y, ship, 0))))
        elif ori == "h":
            placed_ships.append(tuple(map(str, (x, y, ship, 1))))

    return placed_ships


def place_ship(board, ship, ori, x, y):

    if ori == "v":
        for i in range(ship):
            board[x + i][y] = 1

        for i in range(-1, ship+1):
            for j in [-1, 0, 1]:
                if 0 <= x+i < len(board) and 0 <= y+j < len(board):
                    board[x+i][y+j] = 1

    elif ori == "h":
        for i in range(ship):
            board[x][y + i] = 1

        for i in range(-1, ship+1):
            for j in [-1, 0, 1]:
                if 0 <= x+j < len(board) and 0 <= y+i < len(board):
                    board[x+j][y+i] = 1
    return board


def validate(board, ship, x, y, ori):

    if ori == "v" and x + ship > len(board):
        return False
    elif ori == "h" and y + ship > len(board):
        return False
    else:
        if ori == "v":
            try:
                for i in range(-1, ship+1):
                    for j in [-1, 0, 1]:
                        if 0 <= x + i < len(board) and 0 <= y + j < len(board):
                            if board[x+i][y+j] != 0:
                                return False
            except IndexError:
                pass
        elif ori == "h":
            try:
                for i in range(-1, ship+1):
                    for j in [-1, 0, 1]:
                        if 0 <= x + j < len(board) and 0 <= y + i < len(board):
                            if board[x+j][y+i] != 0:
                                return False
            except IndexError:
                pass
    return True
