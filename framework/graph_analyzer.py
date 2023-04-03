import hashlib
from copy import deepcopy
from collections import Counter
from framework.graph_io import *
from utils.utils import fast_copy


def colourize(graph: Graph, reset: bool = True) -> List:
    """
    Colorizes the graph using Weisfeiler Lehman algorithm.
    :param graph: A graph that should be (re-)colorized
    :param reset: If True, the colours of the graph will be reset before colorization
    :return: The colorized graph
    """
    coloured_graph = fast_copy(graph)
    colours = {}
    graphs = {}
    if reset:
        for v in coloured_graph.vertices:
            v.label = "1"
        colours["1"] = coloured_graph.vertices
    else:
        for v in coloured_graph.vertices:
            colours.setdefault(str(v.label), []).append(v)

    converged = False
    number_of_partitions = _check_partitions(colours)
    for i in range(1000):
        _step(colours)
        _update_dict(colours)
        new_number_of_partitions = _check_partitions(colours)
        if new_number_of_partitions == number_of_partitions:
            converged = True
            break
        else:
            number_of_partitions = new_number_of_partitions
    if not converged:
        raise TimeoutError("Limit 1000 iterations exceeded! Colorization failed.")

    for v in coloured_graph.vertices:
        try:
            graphs[v.g_num].append(v.label)
        except KeyError:
            graphs[v.g_num] = [v.label]

    identical_graphs = _find_identical(graphs)
    if not identical_graphs:
        result = [graphs, 0, coloured_graph]
    else:
        if find_discrete(identical_graphs, graphs):
            result = [graphs, 1, coloured_graph]
        else:
            result = [graphs, 2, coloured_graph]
    return result


def find_discrete(identical_graphs: List, graphs: dict) -> bool:
    """
    Check which graphs are discrete.
    :param graphs: A graph (disjoint union of graphs) that should be checked
    :return: A list of lists of graphs that are discrete
    """
    for ig in identical_graphs:
        if len(set(graphs[ig[0]])) == len(graphs[ig[0]]):
            return True
        else:
            return False
    return False


def _find_identical(graphs: dict) -> List:
    """
    Find identical graphs in a dictionary of graphs.
    :param graphs: A dictionary of graphs
    :return: A list of lists of graphs that are identical
    """
    identical = {}
    for key, value in graphs.items():
        value_key = tuple(sorted(value))
        if value_key in identical:
            identical[value_key].append(key)
        else:
            identical[value_key] = [key]
    identical_graphs = [group for group in identical.values() if len(group) > 1]
    return identical_graphs


def _map_values_with_colours(labels, colours):
    for lb in labels:
        lb[0].label = lb[1]
        colours.setdefault(lb[1], []).append(lb[0])


def _check_partitions(colours):
    return len(colours.keys())


def _update_dict(colours):
    """
    Remove empty lists of colours from dictionary.
    :param colours: A dictionary of colours
    """
    colours_copy = colours.copy()
    for key, value in colours_copy.items():
        if not value:
            del colours[key]


def _get_compressed_label(vertex):
    """
    Compress the label of a vertex using hash function.
    :param vertex: A vertex with the label to be compressed
    :return: A tuple of the vertex and the compressed label
    """
    cl = vertex.label
    neighbours = []
    for n in vertex.neighbours:
        neighbours.append(n.label)
    neighbours = sorted(neighbours)
    str_neighbours = "".join(str(n) for n in neighbours)
    not_hashed_label = cl + str_neighbours
    hash_cl = hashlib.sha256(not_hashed_label.encode())
    hash_label = hash_cl.hexdigest()
    hash_label = hash_label[:16]
    return vertex, hash_label


def _step(colours):
    """
    Perform one step of the Weisfeiler Lehman algorithm.
    :param colours: A dictionary of colours
    """
    colours_copy = colours.copy()
    colours.clear()
    compressed_labels = []
    for key, value in colours_copy.items():
        for v in value:
            cl = _get_compressed_label(v)
            compressed_labels.append(cl)
    _map_values_with_colours(compressed_labels, colours)


def count_isomorphism(G: Graph, D: List, I: List, count=True) -> int:
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
        return 0
    if 1 in result:  # Result is 1 if the colouring of the graphs are bijective
        return 1
    if 2 in result:  # Result is 2 if the colouring of the graphs are equal but not bijective. Start of Branching
        coloured_graph = result[2]
        colouring = list(result[0].values())[0]
        colour_classes = Counter(colouring)
        num = 0
        dup_coloured_nodes = []
        for colour_class in colour_classes:
            if colour_classes[colour_class] >= 2:  # choose a colour that have instances in both left and right graph
                for v in coloured_graph.vertices:
                    if v.label == colour_class:
                        dup_coloured_nodes.append(v)
                for x in dup_coloured_nodes[:int(len(dup_coloured_nodes)/2)]:  # choose a vertex x in the left graph to be used for branching
                    if x.uid not in D:
                        for y in dup_coloured_nodes[int(len(dup_coloured_nodes)/2):]:  # choose a vertex y in the right graph to be used for branching
                            if y.uid not in I:
                                for vertex in coloured_graph.vertices:
                                    vertex.label = "1"
                                    for i in range(len(D)):
                                        if vertex.uid == D[i] or vertex.uid == I[i]:
                                            vertex.label = str(i + 2)  # assign previous chosen x's and y's a new colour
                                x.label = str(len(D) + 2)  # assign x and y with a unique colour
                                y.label = str(len(I) + 2)
                                num = num + count_isomorphism(coloured_graph, D + [x.uid], I + [y.uid], count=count)  # explore the branch by recursion
                                if not count and num != 0:
                                    return -1
                                y.label = "1"
                        break
                break
        return num
    return 0
