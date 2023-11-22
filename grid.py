import numpy as np 
from typing import List, Tuple
from itertools import product 

class MSGrid:
    """MineSweeper Grid as a class 
    """
    def __init__(self, size_x, size_y) -> None:
        self.unknown_constant = -1
        self.size_x = size_x
        self.size_y = size_y
        self.grid = np.zeros((size_x, size_y)) + self.unknown_constant

    def get_known_cells(self):
        known_cells = []
        for col in self.size_x:
            for row in self.size_y:
                if self.grid[col, row] != self.unknown_constant:
                    known_cells.append((col, row))
        return known_cells


    def get_cell_neighbours(self, cell_location, radius=1, radius_x=None, radius_y=None) -> List[Tuple[int, int]]:
        """_summary_

        Args:
            radius (int, optional): raduis of neighbours in both dirs, ignored if radius_x and raduis_y are given. Defaults to 1.
            radius_x (_type_, optional): raduis in direction of cols, also needs to have radius_y. Defaults to None.
            radius_y (_type_, optional): raduis in direction of cols. Defaults to None.

        Returns:
            List[Tuple[int, int]]: _description_
        """
        assert type(radius_x) == type(radius_y), 'radiux_x and raduis_y should both be ints or both be None!'
        if radius_x is None:
            radius_x = radius
            radius_y = radius 

        list_of_neighbours = []
        neighbouring_offsets = product(radius_x, radius_y)
        for neighbouring_offset in neighbouring_offsets:
            if neighbouring_offset != (0, 0):
                neighbour = (cell_location[0] + neighbouring_offset[0], cell_location[1] + neighbouring_offset[1])
                list_of_neighbours.append(neighbour)
        return neighbouring_offset


    def get_unknown_cells(self) -> List[Tuple[int, int]]:
        """in this context, unkown cells are cells that 
        are not known but also are adjacent to at least one known cell
        """
        unknown_cells = {}
        known_cells = self.get_known_cells()
        for known_cell in known_cells:
            for neighbour_location in self.get_cell_neighbours(known_cell):
                if self.grid[neighbour_location[0], neighbour_location[1]] == self.unknown_constant:
                    unknown_cells.add(neighbour_location)
        return list(unknown_cells)
    

    def get_connected_unknown_cells(self) -> List[List[Tuple[int, int]]]:
        """in a minesweper game there might be a number of unconnected islands 
        for which the solution is independent (if the margin of distance between them is larger than 1 and 
        until they remain unconnected). 

        Returns:
            List[List[Tuple[int, int]]]: A list of connected unknown cells, each unknown cell is in itself another 
            list of tuples of form (x, y)
        """
        # This will run a dfs on the edges of the islands to find the cliques of unknown cells 
        # A nont_trivial known cell is a cell that is known and adjacent to at least one unknown cell
        # Similarly, an non_trivial unkonwn cell is one that is adjacent to at least one known cell
        observed_known_cells = {}
        observed_unknown_cells = {}
        cliques = []
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.grid[x, y] != self.unknown_constant:
                    pass 
                # TODO recursivey look at below and right of the cell, if this is a non-trivial cell 
                # and both below and right cells are also non_trivial, get the 
