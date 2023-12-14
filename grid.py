import numpy as np 
from typing import List, Tuple
from itertools import product 

class MSGrid:
    """MineSweeper Grid as a class 
    """
    UKNOWN_CONSTANT = -1
    MINE = -2
    EMPTY = 0
    def __init__(self, grid=None, size_x=None, size_y=None) -> None:
        assert grid is not None or (size_x is not None and size_y is not None), 'either an initial grid or the grid size should be given!'
        # TODO makes more sense to just use class constant everywhere, 
        # should be refactored later
        self.unknown_constant = MSGrid.UKNOWN_CONSTANT
        if grid is not None:
            self.grid = grid
            self.size_x = grid.shape[0]
            self.size_y = grid.shape[1]
            self.boundary_flags = np.zeros((self.size_x, self.size_y))
            self.mark_boundary_flags()
        else:
            self.size_x = size_x
            self.size_y = size_y
            self.grid = np.zeros((size_x, size_y)) + self.unknown_constant
            self.boundary_flags = np.zeros((self.size_x, self.size_y))

    def mark_boundary_flags(self) -> None:
        """
        boundary cells are same as non_trivial cells, basically either an unkonwn cell that has at least one known
        neighbour or a known cell that has at least one unknown neighbour. 
        These are the only important cells in solving the problem. 
        This method will iterate the grid, and whereever there is a non_trivial cell, mark that location in the 
        self.boundary_flags map to True
        """
        # for each cell we will check the four cells to the right, left bottom, bottom and right bottom
        # the other foru will have been checked when we were at the left, top right, etc.. cells.
        neighbour_offsets = [
            (1, 0), (-1, 1), (0, 1), (1, 1)
        ]
        for i in range(self.size_x):
            for j in range(self.size_y):
                for neighbour_offset in neighbour_offsets:
                    neighbour_index = (i + neighbour_offset[0], j + neighbour_offset[1])
                    if -1 < neighbour_index[0] < self.size_x and -1 < neighbour_index[1] < self.size_y:
                        if (self.grid[i, j] == self.unknown_constant) != (self.grid[neighbour_index] == self.unknown_constant):
                            self.boundary_flags[i, j] = 1
                            self.boundary_flags[neighbour_index] = 1 



    def get_known_cells(self):
        known_cells = []
        for col in self.size_x:
            for row in self.size_y:
                if self.grid[col, row] != self.unknown_constant:
                    known_cells.append((col, row))
        return known_cells
    
    def cell_is_edge(self, cell_location: Tuple[int, int]):
        is_known = self.grid[cell_location] != self.unknown_constant
        x_offsets = [-1, 0, 1]
        y_offsets = [-1, 0, 1]
        neighbouring_offsets = product(x_offsets, y_offsets)
        for neighbouring_offset in neighbouring_offsets:
            if neighbouring_offset != (0, 0):
                neighbour = (cell_location[0] + neighbouring_offset[0], cell_location[1] + neighbouring_offset[1])
                neighbour_is_known = self.grid[neighbour] != self.unknown_constant
                if is_known == neighbour_is_known:
                    # if found a neighbour of opposite status (known vs. unkonwn)
                    return True
        return False


    def get_cell_neighbours(self, cell_location:Tuple[int, int], radius:int=1, radius_x:int=None, radius_y:int=None) -> List[Tuple[int, int]]:
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
        x_offsets = [r for r in range(radius_x + 1)] + [0] + [r for r in range(radius_x + 1)]
        y_offsets = [r for r in range(radius_y + 1)] + [0] + [r for r in range(radius_y + 1)]

        list_of_neighbours = []
        neighbouring_offsets = product(x_offsets, y_offsets)
        for neighbouring_offset in neighbouring_offsets:
            if neighbouring_offset != (0, 0):
                neighbour = (cell_location[0] + neighbouring_offset[0], cell_location[1] + neighbouring_offset[1])
                list_of_neighbours.append(neighbour)
        return list_of_neighbours


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
        """in a minesweeper game there might be a number of unconnected islands 
        for which the solution is independent (if the margin of distance between them is larger than 1 and 
        until they remain unconnected). 

        Returns:
            List[List[Tuple[int, int]]]: A list of connected unknown cells, each unknown cell is in itself another 
            list of tuples of form (x, y)
        """
        # This will run a dfs on the edges of the islands to find the cliques of unknown cells 
        # A non_trivial known cell is a cell that is known and adjacent to at least one unknown cell
        # Similarly, a non_trivial unknown cell is one that is adjacent to at least one known cell

        def dfs(cell):
            if cell not in visited:
                visited.add(cell)
                if self.grid[cell] == self.unknown_constant:
                    clique.append(cell)
                    for neighbour in self.get_cell_neighbours(cell):
                        if neighbour not in visited:
                            dfs(neighbour)

        cliques = []
        visited = set()
        for x in range(self.size_x):
            for y in range(self.size_y):
                if (x, y) not in visited and self.grid[x, y] == self.unknown_constant:
                    clique = []
                    dfs((x, y))
                    cliques.append(clique)
        return cliques