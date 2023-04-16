from collections import Counter

from framework.graph import *
from framework.graph_analyzer import colourize
from framework.permv2 import *

X = Set[permutation]

def generate_mapping(G: Graph, D: List, I: List):


def generate_automorphism(G: Graph, D: List, I: List):
    """
    Counts the number of isomorphisms between two graphs
    :param G: Graph (coloured)
    :param D: List of vertices in the left graph that have previously been selected for branching
    :param I: List of vertices in the right graph that have previously been selected for branching
    """
    if len(D) == 0:  # If this is the first iteration, perform colour refinement with default colouring
        result = colourize(G)
    else:  # If this is a branch, perform colour refinement with the assigned colouring of G
        result = colourize(G, reset=False)
    if 0 in result:  # Result is 0 if the colouring of the graphs do not match
        return
    if 1 in result:  # Result is 1 if the colouring of the graphs are bijective
        if
        return 1
    if 2 in result:  # Result is 2 if the colouring of the graphs are equal but not bijective. Start of Branching
        coloured_graph = result[2]
        colouring = list(result[0].values())[0]
        colour_classes = Counter(colouring)
        dup_coloured_nodes = []
        for colour_class in colour_classes:
            if colour_classes[colour_class] >= 2:  # choose a colour that have instances in both left and right graph
                for v in coloured_graph.vertices:
                    if v.label == colour_class:
                        dup_coloured_nodes.append(v)
                for x in dup_coloured_nodes[:int(len(
                        dup_coloured_nodes) / 2)]:  # choose a vertex x in the left graph to be used for branching
                    if x.uid not in D:
                        for y in dup_coloured_nodes[
                                 int(len(
                                     dup_coloured_nodes) / 2):]:  # choose a vertex y in the right graph to be used for branching
                            if y.uid not in I:
                                for vertex in coloured_graph.vertices:
                                    vertex.label = "1"
                                    for i in range(len(D)):
                                        if vertex.uid == D[i] or vertex.uid == I[i]:
                                            vertex.label = str(i + 2)  # assign previous chosen x's and y's a new colour
                                x.label = str(len(D) + 2)  # assign x and y with a unique colour
                                y.label = str(len(I) + 2)
                                generate_automorphism(coloured_graph, D + [x.uid], I + [y.uid])  # explore the branch by recursion
                                if D != I:
                                    return
                                y.label = "1"
                        break
                break
    return 0