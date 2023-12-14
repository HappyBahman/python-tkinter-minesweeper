import numpy as np
import numpy.typing as npt
from graph import Graph, Node
from typing import List
from grid import MSGrid


class GraphSolver:
    def __init__(self, initial_grid_map) -> None:
        self.graphs = self.initiate_graphs(initial_grid_map)

    def make_graph_from_grid(self, grid: npt.ArrayLike) -> None:
        """This creates a full graph from all the cells in the grid,

        Args:
            grid (npt.ArrayLike): _description_
        """
        cols = grid.shape[0]
        rows = grid.shape[1]
        for col in cols:
            for row in rows:
                new_node = Node(
                    id=self.graph.id_factory.get_new_id(),
                    value=grid[row, col],
                    location=(row, col),
                )
                self.graph.add_vertex(new_node)
                if cols > 1:
                    left_neighbour_loc = (col - 1, row)
                    self.graph.add_edge(
                        new_node, self.graph.get_vtx_at(left_neighbour_loc)
                    )
                if row > 1:
                    top_neighbour_loc = (col, row - 1)
                    self.graph.add_edge(
                        new_node, self.graph.get_vtx_at(top_neighbour_loc)
                    )
                if row > 1 and col > 1:
                    corner_neighbour_loc = (col - 1, row - 1)
                    self.graph.add_edge(
                        new_node, self.graph.get_vtx_at(corner_neighbour_loc)
                    )
                if row > 1 and col < cols - 1:
                    corner_neighbour_loc = (col + 1, row - 1)
                    self.graph.add_edge(
                        new_node, self.graph.get_vtx_at(corner_neighbour_loc)
                    )

    def initiate_graphs(self, grid: MSGrid) -> List[Graph]:
        """
        This method will act similar to the Grid.get_connected_unknown_cells() method,
        the difference is that this method will create a graph out of each clique while finding 
        the cliques and will return a list of Graph objects
        """
        # This function is wrong because:
        # 1: it adds all the cells to the graph, not just the ones that are 
        # on the boundary,
        # 2: it adds some edges more than once
        visited = set()
        graphs = []
        for x in range(grid.size_x):
            for y in range(grid.size_y):
                if grid.boundary_flags[x, y]:
                    if (x, y) not in visited and grid.grid[x, y] == grid.unknown_constant:
                        graph = Graph()
                        stack = [(x, y)]
                        while stack:
                            cell = stack.pop()
                            if cell not in visited:
                                visited.add(cell)
                                if cell not in graph.location_hash:
                                    node = Node(id=graph.id_factory.get_new_id(), value=grid.grid[cell], location=cell)
                                    graph.add_vertex(node)
                                for neighbour_location in grid.get_cell_neighbours(cell):
                                    if grid.boundary_flags[neighbour_location]:
                                        if neighbour_location not in visited:
                                            stack.append(neighbour_location)
                                        if neighbour_location not in graph.location_hash:
                                            neighbour_node = Node(id=graph.id_factory.get_new_id(), value=grid.grid[neighbour_location], location=neighbour_location)
                                            graph.add_vertex(neighbour_node)
                                            graph.add_edge(node, neighbour_node)
                        graphs.append(graph)
        return graphs
                    

    def solve(self) -> None:
        to_clear = []
        to_flag = []
        for graph in self.graphs:
            # todo: it makes more sense to have the graph loop wrapped in an iteration loop, but I'm gonna leave 
            # it for now cause I'm lazy :)
            vtxs_to_clear, vtxs_to_flag = graph.solve_step()
            to_clear += [vtx.location for vtx in vtxs_to_clear]
            to_flag += [vtx.location for vtx in vtxs_to_flag]
        return to_flag, to_clear