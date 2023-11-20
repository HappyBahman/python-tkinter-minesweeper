from __future__ import annotations
from typing import List
from exceptions import EdgeAlreadyExists, EdgeDoesNotExist
from enum import Enum


class Value(Enum):
    Unknown = -1


class IDFactory:
    def __init__(self, digits=10) -> None:
        self.counter = 0
        self.digits = digits

    def get_new_id(self):
        return "{:0>{}}".format(self.counter, self.digits)


class Belief:
    def __init__(
        self, degree: int, observed: int, value: int, references: List[Node] = []
    ) -> None:
        self.degree = degree
        self.value = value
        self.observed = observed
        self.references = references

    def observe(self, reference=None) -> None:
        self.observed += 1
        if reference is not None:
            self.references.append(reference)


class BeliefSet:
    def __init__(self) -> None:
        self.table = {}

    def get_belief_subjects(self):
        return list(self.table.keys())

    def aquire_about(self, vertex) -> Belief:
        return self.table[vertex]

    def add_observation(self, observed_neighbour: Node, reference=None) -> None:
        if observed_neighbour in self.table:
            self.table[observed_neighbour].observe(reference)
        else:
            self.table[observed_neighbour] = Belief(
                degree=observed_neighbour.degree,
                value=observed_neighbour.value,
                observed=1,
                references=[reference],
            )


class Node:
    def __init__(
        self, id: int, value: int, neighbours: List[Node] = [], degree: int = 0
    ) -> None:
        self.id = id
        self.value = value
        self.neighbours = neighbours
        self.degree = degree
        self.beliefs = BeliefSet()

    def __eq__(self, other: Node) -> bool:
        assert isinstance(
            object, Node
        ), "can not compare Node to object type {}".format(type(other))
        return self.id == other.id

    def is_neighbours_with(self, potential_neighbour: Node) -> bool:
        return potential_neighbour in self.neighbours

    def find_neighbour_id_from_node(self, neighbour_to_find: Node) -> int | None:
        if self.is_neighbours_with(neighbour_to_find):
            return self.neighbours.index(neighbour_to_find)
        else:
            return None

    def add_neighbour(self, neighbour_to_add: Node) -> bool:
        if self.is_neighbours_with(neighbour_to_add):
            raise EdgeAlreadyExists
        self.neighbours.append(neighbour_to_add)
        self.degree += 1

    def remove_neighbour(self, neighbour_to_remove: Node) -> None:
        if not self.is_neighbours_with(neighbour_to_remove):
            raise EdgeDoesNotExist
        self.neighbours.pop(self.find_neighbour_id_from_node(neighbour_to_remove))
        self.degree -= 1
        return
    
    def get_known_neighbours(self) -> List[Node]:
        known_neighbours = []
        for neighbour in self.neighbours:
            if neighbour.value != Value.Unknown:
                known_neighbours.append(neighbour)
        return known_neighbours

    def get_unknown_neighbours(self) -> List[Node]:
        unknown_neighbours = []
        for neighbour in self.neighbours:
            if neighbour.value == Value.Unknown:
                unknown_neighbours.append(neighbour)
        return unknown_neighbours


    class Graph:
        def __init__(self) -> None:
            self.vertexes = []
            self.id_factory = IDFactory()

        def add_vertex(self, vertex: Node) -> None:
            self.vertexes.append(vertex)

        def add_edge(self, vertex_1: Node, vertex_2: Node) -> None:
            vertex_1.add_neighbour(vertex_2)
            vertex_2.add_neighbour(vertex_1)

        def get_known_vtxs(self) -> List[Node]:
            known_set = []
            for vtx in self.vertexes:
                if not vtx.value == Value.Unknown:
                    known_set.append[vtx]
            return known_set

        def get_unknown_vtxs(self) -> List[Node]:
            known_set = []
            for vtx in self.vertexes:
                if vtx.value == Value.Unknown:
                    known_set.append[vtx]
            return known_set

        def propagate_from_known_to_unkonwn_vtxs(self) -> None:
            known_vtxs = self.get_known_vtxs()
            for vtx in known_vtxs:
                vtx_neighbours = vtx.neighbours
                for neighbour in vtx_neighbours:
                    if neighbour.value == Value.Unknown:
                        neighbour.beliefs.add_observation(vtx)

        def propagate_from_unknown_to_known_vtxs(self) -> None:
            # although this method is similar to the propagate_from_known_to_unkonwn_vtxs
            # right now, there might be more substantial differences in the future,
            # Also they represented different phases of the algorithm,
            # hence they are implemented in two different methods.
            unknown_vtxs = self.get_unknown_vtxs()
            for vtx in unknown_vtxs:
                vtx_neighbours = vtx.neighbours
                belief_set = vtx.beliefs
                for neighbour in vtx_neighbours:
                    if neighbour.value != Value.Unknown:
                        for belief_subject in belief_set.get_belief_subjects():
                            if belief_subject == neighbour:
                                # do not propagate observation of a vertex to itself
                                continue
                            neighbour.beliefs.add_observation(observed_neighbour=belief_subject,
                                                              reference=vtx)

        def resolve_propagated_information(self) -> bool:
            known_vtxs = self.get_known_vtxs()
            for vtx in known_vtxs:
                unknown_neighbours = vtx.get_unknown_neighbours()
                belief_set = vtx.beliefs
                belief_subjects = belief_set.get_belief_subjects
                for belief_subject in belief_subjects:
                    belief_about_subject = belief_set.aquire_about(belief_subject)
                    if belief_about_subject.degree == belief_about_subject.observed:
                        # all the unknown neighbours of the belief subject subside under the
                        # set of unknown neighbours of current vtx, therefore, this vertex will
                        # definitely observe all that the belief subject will observe.
                        # TODO: check that the node beign added is not duplicate, e.g. does not 
                        # contain exactly the same info as the current node, 
                        # i.e. does not have the same value, degree and neighbours as current node.
                        unaffected_neighbours = []
                        for neighbour in unknown_neighbours:
                            if neighbour not in belief_about_subject.references:
                                unaffected_neighbours.append(neighbour)
                        new_node = Node(
                            id=self.id_factory.get_new_id(),
                            value=vtx.value - belief_about_subject.value,
                        )
                        self.add_vertex(new_node)
                        for un in unaffected_neighbours:
                            self.add_edge(new_node, un)



        