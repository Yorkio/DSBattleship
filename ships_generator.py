import random

def generate_ships(board_size):
    board = [[0]*board_size for i in range(board_size)]
    available_positions = [[i, j] for i in xrange(board_size) for j in xrange(board_size)]
    ship_types = [5, 4, 3, 3, 2]
    ships = []
    while ship_types:
        ship_length = ship_types[0]
        horizontal = random.getrandbits(1)
        if bool(horizontal):
            position_x = random.randint(0, board_size-1)
            position_y = random.randint(0, board_size-ship_length-1)
            pairs = []
            for s in range(position_y-1, position_y+ship_length+1):
                for p in range(position_x-1, position_x+2):
                    if 0 <= s < board_size and 0 <= p < board_size:
                        pairs.append([p, s])
            if all(pairs[i] in available_positions for i in range(len(pairs))):
                for i in range(ship_length):
                    board[position_x][position_y+i] = 1
                    i += 1
                print horizontal
                [available_positions.remove(pairs[i]) for i in range(len(pairs))]
                ship_types.remove(ship_types[0])
                ships.append(tuple(map(str, (position_x, position_y, ship_length, int(horizontal)))))
        else:
            position_x = random.randint(0, board_size-ship_length-1)
            position_y = random.randint(0, board_size-1)
            pairs = []
            for s in range(position_x-1, position_x+ship_length+1):
                for p in range(position_y-1, position_y+2):
                    if 0 <= s < board_size and 0 <= p < board_size:
                        pairs.append([s, p])
            if all(pairs[i] in available_positions for i in range(len(pairs))):
                for i in range(ship_length):
                    board[position_x+i][position_y] = 1
                    i += 1
                print horizontal
                [available_positions.remove(pairs[i]) for i in range(len(pairs))]
                ship_types.remove(ship_types[0])
                ships.append(tuple(map(str, (position_x, position_y, ship_length, int(horizontal)))))
    return ships

