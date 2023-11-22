import numpy as np 
import numpy.typing as npt
from graph import Graph, Node
from typing import List


class GraphSolver:
    def __init__(self, initial_grid_map) -> None:
        self.graph = Graph()
        self.make_graph_from_grid(initial_grid_map)

    def make_graph_from_grid(self, grid: npt.ArrayLike) -> None:
        """This creates a full graph from all the cells in the grid,

        Args:
            grid (npt.ArrayLike): _description_
        """
        cols = grid.shape[0]
        rows = grid.shape[1]
        for col in cols:
            for row in rows:
                new_node = Node(id=self.graph.id_factory.get_new_id(), 
                                value=grid[row, col], location=(row, col))
                self.graph.add_vertex(new_node)
                if cols > 1:
                    left_neighbour_loc = (col-1, row)
                    self.graph.add_edge(new_node, self.graph.get_vtx_at(left_neighbour_loc))
                if row > 1:
                    top_neighbour_loc = (col, row-1)
                    self.graph.add_edge(new_node, self.graph.get_vtx_at(top_neighbour_loc))
                if row > 1 and col >1:
                    corner_neighbour_loc = (col-1, row-1)
                    self.graph.add_edge(new_node, self.graph.get_vtx_at(corner_neighbour_loc))
                if row > 1 and col < cols-1:
                    corner_neighbour_loc = (col+1, row-1)
                    self.graph.add_edge(new_node, self.graph.get_vtx_at(corner_neighbour_loc))

    def make_graph_from_edges(self, grid:npt.ArrayLike) -> List[Graph]:
        pass 

    def solve(self) -> None:
        self.graph