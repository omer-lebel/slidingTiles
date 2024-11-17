from searchAI import Node, bfs



def liner_conflict(node):
    return manhattan_distance(node) + 2*( row_conflict(node) + col_conflict(node) )

def manhattan_distance(node):
    """
    The Manhattan distance is the sum of the distance of the tile from their goal position
    """
    distance = 0
    size = int(len(node.state) ** 0.5)

    for idx, num in enumerate(node.state):
        if num != 0:  # skip the blank tile
            current_row, current_col = divmod(idx, size)
            target_row, target_col = divmod(num, size)
            distance += abs(current_row - target_row) + abs(current_col - target_col)

    return distance

def row_conflict(node):
    """
    row conflict is when 2 tile are in their goal row, but are reversed relative to their goal position
    for example: in the row [5, 3, 4] there are 2 row conflicts: (5,3), (5,4)
    """
    conflict = 0
    size = int(len(node.state) ** 0.5)

    for row in range(size):
        # iterating over the tiles in the current row
        for i in range(size):
            current_tile = node.state[row*size + i]
            target_row = current_tile // size

            # skip blank tile or tiles that not belong to this row
            if current_tile == 0 or target_row != row:
                continue

            # look at the tiles down to the current tile
            for j in range(i + 1, size):
                other_tile = node.state[row * size + j]
                target_row_other_tile = other_tile // size

                # skip blank tile or tiles that not belong to this row
                if other_tile == 0 or target_row_other_tile != row:
                    continue

                if current_tile > other_tile: # found conflict
                    conflict += 1

    return conflict


def col_conflict(node):
    """
    col conflict is when 2 tile are in their goal col, but are reversed relative to their goal position
    for example: in the col [8, 5, 2]^t there are 3 col conflicts: (8,5), (8,2), (5,2)
    """
    conflict = 0
    size = int(len(node.state) ** 0.5)

    for col in range(size):
        # iterating over the tiles in the current col
        for i in range(size):
            current_tile = node.state[col + i*size]
            target_col = current_tile % size

            # skip blank tile or tiles that not belong to this col
            if current_tile == 0 or target_col != col:
                continue

            # look at the tiles to the right of the current tile
            for j in range(i + 1, size):
                other_tile = node.state[col + j*size]
                target_col_other_tile = other_tile % size

                # skip blank tile or tiles that not belong to this col
                if other_tile == 0 or target_col_other_tile != col:
                    continue

                # found conflict
                if current_tile > other_tile:
                    conflict += 1

    return conflict

