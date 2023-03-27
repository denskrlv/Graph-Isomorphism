import hashlib
from copy import deepcopy
from collections import Counter
from framework.graph_io import *


def colorize(graph: Graph, colours: dict = None) -> Graph:
    """
    Colorizes the graph using Weisfeiler Lehman algorithm.
    :param graph: A graph that should be (re-)colorized
    :param colours: A dictionary with the colours to use as a starting point.
    If None, colorization will start from the beginning
    :return: The colorized graph
    """

    colored_graph = deepcopy(graph)

    if colours is None:
        colours = {}
        for v in colored_graph.vertices:
            v.label = "1"
        colours["1"] = colored_graph.vertices
    else:
        for key, value in colours.items():
            for v in value:
                v.label = key

    converged = False
    number_of_partitions = _check_partitions(colours)
    for i in range(1000):
        _step(colours)
        _update_dict(colours)
        new_number_of_partitions = _check_partitions(colours)
        if new_number_of_partitions == number_of_partitions:
            print("Colorized successfully! Iterations:", i)
            converged = True
            break
        else:
            number_of_partitions = new_number_of_partitions
    if not converged:
        raise TimeoutError("Limit 1000 iterations exceeded! Colorization failed.")

    return colored_graph

    # graphs = {}
    # for _, value in colours.items():
    #     for v in value:
    #         graphs.setdefault(v.g_num, []).append(v.label)
    # identical_graphs = compare_graphs(graphs)
    # return [graphs, identical_graphs]

    # for ig in identical_graphs:
    #     if len(set(graphs[ig[0]])) == len(graphs[ig[0]]):
    #         ig.append(1)
    #     else:
    #         ig.append(0)
    #
    # return identical_graphs


def check_discreteness(colours: dict):
    graphs = {}
    for _, value in colours.items():
        for v in value:
            graphs.setdefault(v.g_num, []).append(v.label)
    identical_graphs = _find_identical(graphs)
    for ig in identical_graphs:
        if len(set(graphs[ig[0]])) == len(graphs[ig[0]]):
            ig.append(1)
        else:
            ig.append(0)
    return identical_graphs


def _find_identical(graphs):
    identical = {}
    for key, value in graphs.items():
        value_key = tuple(value)
        if value_key in identical:
            identical[value_key].append(key)
        else:
            identical[value_key] = [key]
    output = [group for group in identical.values() if len(group) > 1]
    return output


def _map_values_with_colours(labels, curr_key, colours):
    for lb in labels:
        lb[0].label = lb[1]
        colours.setdefault(lb[1], []).append(lb[0])
        colours[curr_key].remove(lb[0])


def _check_partitions(colours):
    return len(colours.keys())


def _update_dict(colours):
    colours_copy = colours.copy()
    for key, value in colours_copy.items():
        if value == []:
            del colours[key]


def _get_compressed_label(V):
    cl = V.label
    neighbours = []
    for n in V.neighbours:
        neighbours.append(n.label)
    neighbours = sorted(neighbours)
    str_neighbours = cl.join(str(n) for n in neighbours)
    hash_cl = hashlib.sha256(str_neighbours.encode())
    hash_label = hash_cl.hexdigest()
    hash_label = hash_label[:8]
    return (V, hash_label)


def _step(colours):
    colours_copy = colours.copy()
    for key, value in colours_copy.items():
        if value:
            compressed_labels = []
            for v in value:
                cl = _get_compressed_label(v)
                compressed_labels.append(cl)
            _map_values_with_colours(compressed_labels, key, colours)


def compare_graphs(graphs):
    colourings = set()
    identical = {}
    for key, value in graphs.items():
        value_key = tuple(sorted(value))
        colourings.add(value_key)
        if value_key in identical:
            identical[value_key].append(key)
        else:
            identical[value_key] = [key]
    # output = [group for group in identical.values() if len(group) > 1]
    if len(colourings) == 2:
        return 0
    if len(colourings) == 1:
        for colouring in colourings:
            if len(colouring) == len(tuple(set(colouring))):
                print("bijection")
                return 1
            else:
                return 2
    return 0


def count_isomorphism(G: Graph, D: List, I: List) -> int:
    colours = {"1": [v for v in G.vertices if v.label == "1"]}
    for v1 in D:
        colours.setdefault(v1.label, []).append(v1)
    for v2 in I:
        colours.setdefault(v2.label, []).append(v2)

    print("Before: " + str(G))
    result = colorize(G, colours)
    print("After: " + str(result))
    if 0 in result:
        print("hello0")
        return 0
    if 1 in result:
        print("hello1")
        return 1
    if 2 in result:
        colouring = list(result[0].values())[0]
        colour_classes = Counter(colouring)
        print("colours" + str(colour_classes))
        graph_numbers = list(result[0].keys())
        g_num_left = graph_numbers[0]
        g_num_right = graph_numbers[1]
        # with open('graph' + str(g_num_left) + 'x' + str(g_num_right) + '.dot', 'w') as gg:
        #     write_dot(G, gg)
        num = 0
        for colour_class in colour_classes:
            if colour_classes[colour_class] >= 2:
                print("color class chosen: " + colour_class)
                for x in G.vertices:
                    if x.g_num == g_num_left and x.label == colour_class and x not in D:
                        print("x selected: " + str(x.label))
                        for y in G.vertices:
                            if y.g_num == g_num_right and y.label == colour_class and y not in I:
                                print("Currently running y: " + str(y))
                                for vertex in G.vertices:
                                    vertex.label = "1"
                                for i in range(len(D)):
                                    D[i].label = str(i + 2)
                                    I[i].label = str(i + 2)
                                x.label = str(len(D) + 2)
                                y.label = str(len(I) + 2)
                                # with open('graph' + str(g_num_left) + 'x' + str(g_num_right) + '.dot', 'w') as gg:
                                #     write_dot(G, gg)
                                num = num + count_isomorphism(G, D + [x], I + [y])
                                print(num)
                        break
                break
        return num
    return 0
