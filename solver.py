import numpy as np 

UNKNOWN = -2
MINE = -1
EMPTY = 0


def check_neighborhood(field, x, y):
    left = x-1 if x > 0 else None
    right = x + 1 if x < field.shape[1] - 1 else None
    down = y + 1 if y < field.shape[1] - 1 else None 
    up = y - 1 if y > 0 else None 
    mines = 0
    unsolved = False 
    unknown_neighbors= []
    total = 0
    for xx in [left, x, right]:
        if xx is None:
            continue
        for yy in [up, y, down]:
            if yy is None:
                continue
            total += 1
            if field[xx, yy] == MINE:
                mines += 1
            if field[xx, yy] == UNKNOWN:
                unsolved = True
                unknown_neighbors.append((xx, yy))
    return mines, unsolved, unknown_neighbors, total




def relax(field):
    to_clear = []
    to_flag = []
    # relaxed_field = np.copy(field)
    for i in range(field.shape[0]):
        for j in range(field.shape[1]):
            if field[i, j] != UNKNOWN:
                if field[i, j] != EMPTY:
                    if field[i, j] != MINE:
                        mines, unsolved, unknown_neighbours, _ = check_neighborhood(field, i, j)
                        if not unsolved:
                            continue
                        # relaxed_field[i, j] = field[i, j] - mines 
                        if mines == field[i, j]:
                            to_clear += unknown_neighbours
                        if len(unknown_neighbours) == field[i, j] - mines:
                            to_flag += unknown_neighbours
                        print('i: {} | j: {} | mines: {} | unsolved: {}| val: {}'.format(
                            i, j, mines ,len(unknown_neighbours), field[i, j]))
    return None, to_clear, to_flag



def solve(field):
    print(field)
    field, to_clear, to_flag = relax(field)
    if to_clear or to_flag:
        return to_clear, to_flag
    return None, None 


