from framework.basicpermutationgroup import Orbit, Stabilizer, FindNonTrivialOrbit
from framework.graph import *
from framework.graph_io import write_dot
from framework.permv2 import permutation


def refine(graph: Graph, reset: bool = False) -> list:
    """
    Refines the graph using Hopcroft's algorithm.
    :param graph: A graph that should be refined
    :param reset: If True, the refinement starts from the beginning
    :return: The refined graph
    """
    colours = dict()
    queue = set()  # Queue of colour classes to analyze
    graphs = dict()

    if reset:
        colours = _init_colours(graph)  # Dictionary of type: colour -> [vertices]
    else:
        for v in graph.vertices:
            colours.setdefault(v.label, set()).add(v)

    for colour in colours.keys():
        queue.add(colour)

    while len(queue) != 0:
        current_class = queue.pop()
        current_neighbours = _get_all_neighbours(colours, current_class)
        current_colours = _get_all_neighbour_colours(current_neighbours)
        for cc in current_colours:
            new_candidates = colours[cc].intersection(current_neighbours)
            new_colour = max(colours.keys()) + 1
            if new_candidates != colours[cc] and len(new_candidates) != 0:
                colours[new_colour] = new_candidates
                for c in new_candidates:
                    c.label = new_colour
                colours[cc] = colours[cc] - new_candidates
                if cc in queue:
                    queue.add(new_colour)
                else:
                    if len(colours[cc]) < len(new_candidates):
                        queue.add(cc)
                    else:
                        queue.add(new_colour)

    for v in graph.vertices:
        try:
            graphs[v.g_num].append(v.label)
        except KeyError:
            graphs[v.g_num] = [v.label]

    identical_graphs = _find_identical(graphs)
    if not identical_graphs:
        result = [graphs, 0, graph]
    else:
        if find_discrete(identical_graphs, graphs):
            result = [graphs, 1, graph]
        else:
            result = [graphs, 2, graph]

    return result


def _init_colours(graph: Graph) -> dict:
    """
    (Only for internal use).
    Initializes colours of the vertices of the graph according to their degree.
    :param graph: A graph that should be refined
    :return: The dictionary of the degrees of the vertices
    """
    degrees = dict()
    for v in graph.vertices:
        v.label = len(v.neighbours)
        degrees.setdefault(len(v.neighbours), set()).add(v)
    return degrees


def _get_all_neighbours(colours: dict, colour_class: int) -> set:
    """
    (Only for internal use).
    Returns all neighbours of all vertices of a current colour class.
    :param colours: Colours dictionary
    :param colour_class: Colour class to analyze
    :return: The list of neighbours
    """
    neighbours = set()
    for v in colours[colour_class]:
        for n in v.neighbours:
            neighbours.add(n)
    return neighbours


def _get_all_neighbour_colours(current_neighbours: set) -> set:
    """
    (Only for internal use).
    Returns all colours of neighbours of a current colour class.
    :param current_neighbours: Neighbours of a current colour class
    :return: The set of colours
    """
    neighbour_colours = set()
    for n in current_neighbours:
        neighbour_colours.add(n.label)
    return neighbour_colours


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


def choose_color_class(g: Graph) -> (str, List):
    color_classes = dict()
    max_color = None
    for v in g.vertices:
        try:
            color_classes[v.label].append(v)
        except KeyError:
            color_classes[v.label] = [v]
        if max_color is None and len(color_classes[v.label]) > 3:
            max_color = v.label
            continue
        if max_color is not None and len(color_classes[v.label]) > len(color_classes[max_color]):
            max_color = v.label

    return color_classes[max_color]


def create_mapping(vertices: List[Vertex]) -> List:
    mapping = list()
    mappings = dict()
    graph_length = int(len(vertices) / 2)
    starting_id = vertices[0].uid
    for i in range(1, graph_length + 1):
        for v1 in vertices[:graph_length]:
            if v1.label == i:
                for v2 in vertices[graph_length:]:
                    if v2.label == i:
                        mappings[v1.uid - starting_id] = v2.uid - starting_id - graph_length
    # for v1 in vertices[:graph_length]:
    #     for v2 in vertices[graph_length:]:
    #         if v1.label == v2.label:
    #             mappings[v1.uid - starting_index] = v2.uid - starting_index - graph_length
    #             mapping.append(v2.uid - starting_index - graph_length)
    #             break
    for i in range(graph_length):
        mapping.append(mappings[i])
    return mapping


X = list()


def compute_stabilizer_size(stabilizer: List) -> int:
    order = 1
    while True:
        if len(stabilizer) == 0:
            return order
        if len(stabilizer) == 1 and stabilizer[0].istrivial():
            return order
        vertex = FindNonTrivialOrbit(stabilizer)
        orbit = Orbit(stabilizer, vertex)
        stabilizer = Stabilizer(stabilizer, vertex)
        order *= len(orbit)


def compute_order(generators: List):
    vertex = FindNonTrivialOrbit(generators)
    orbit = Orbit(generators, vertex)
    stabilizers = Stabilizer(generators, vertex)
    size_of_stabilizer = compute_stabilizer_size(stabilizers)
    order = len(orbit) * size_of_stabilizer
    X.clear()
    return order


def is_member(perm: permutation, generators: List) -> bool:
    vertex = FindNonTrivialOrbit(generators)
    if vertex is None:
        return False
    orbit = Orbit(generators, vertex)
    cycles = perm.cycles()
    self_mapping = True
    f = -1
    for sublist in cycles:
        if vertex in sublist:
            self_mapping = False
            for i in range(len(sublist)):
                if sublist[i] == vertex:
                    try:
                        f = sublist[i + 1]
                    except IndexError:
                        f = sublist[0]
                    break
            break
    member_of = f in orbit
    return not self_mapping and member_of


def generate_automorphism(G: Graph, D: List, I: List):
    """
    Counts the number of isomorphisms between two graphs
    :param G: Graph (coloured)
    :param D: List of vertices in the left graph that have previously been selected for branching
    :param I: List of vertices in the right graph that have previously been selected for branching
    """
    with open('test_before.dot', 'w') as f:
        write_dot(G, f)
    if len(D) == 0:  # If this is the first iteration, perform colour refinement with default colouring
        result = refine(G)
    else:  # If this is a branch, perform colour refinement with the assigned colouring of G
        result = refine(G, reset=False)
    if 0 in result:  # Result is 0 if the colouring of the graphs do not match
        return 0
    if 1 in result:  # Result is 1 if the colouring of the graphs are bijective
        with open('test.dot', 'w') as f:
            write_dot(result[2], f)
        mapping = create_mapping(result[2].vertices)
        perm = permutation(len(mapping), mapping=mapping)
        if not is_member(perm, X):
            if len(perm.cycles()) > 0:
                X.append(permutation(len(mapping), mapping=mapping))
        return 1
    if 2 in result:  # Result is 2 if the colouring of the graphs are equal but not bijective. Start of Branching
        coloured_graph = result[2]
        colour_class = choose_color_class(coloured_graph)
        for x in colour_class[:int(len(
                colour_class) / 2)]:  # choose a vertex x in the left graph to be used for branching
            if x.uid not in D:
                for y in colour_class[
                         int(len(
                             colour_class) / 2):]:  # choose a vertex y in the right graph to be used for branching
                    if y.uid not in I:
                        for vertex in coloured_graph.vertices:
                            vertex.label = 1
                            for i in range(len(D)):
                                if vertex.uid == D[i] or vertex.uid == I[i]:
                                    vertex.label = i + 2  # assign previous chosen x's and y's a new colour
                        x.label = len(D) + 2  # assign x and y with a unique colour
                        y.label = len(I) + 2
                        status = generate_automorphism(coloured_graph, D + [x.uid],
                                                       I + [y.uid])  # explore the branch by recursion
                        y.label = 1
                        if status == 1:
                            length = int(len(coloured_graph.vertices) / 2)
                            for i in range(len(D)):
                                if D[i] != I[i] - length:
                                    return 1
                break
            break
        return 0


def check_isomorphism(G: Graph, D: List, I: List, count=True) -> int:
    """
    Counts the number of isomorphisms between two graphs
    :param G: Graph (coloured)
    :param D: List of vertices in the left graph that have previously been selected for branching
    :param I: List of vertices in the right graph that have previously been selected for branching
    """
    if len(D) == 0:  # If this is the first iteration, perform colour refinement with default colouring
        result = refine(G)
    else:  # If this is a branch, perform colour refinement with the assigned colouring of G
        result = refine(G, reset=False)
    if 0 in result:  # Result is 0 if the colouring of the graphs do not match
        return 0
    if 1 in result:  # Result is 1 if the colouring of the graphs are bijective
        return 1
    if 2 in result:  # Result is 2 if the colouring of the graphs are equal but not bijective. Start of Branching
        coloured_graph = result[2]
        colour_class = choose_color_class(coloured_graph)
        num = 0
        for x in colour_class[:int(len(
                colour_class) / 2)]:  # choose a vertex x in the left graph to be used for branching
            if x.uid not in D:
                for y in colour_class[
                         int(len(
                             colour_class) / 2):]:  # choose a vertex y in the right graph to be used for branching
                    if y.uid not in I:
                        for vertex in coloured_graph.vertices:
                            vertex.label = 1
                            for i in range(len(D)):
                                if vertex.uid == D[i] or vertex.uid == I[i]:
                                    vertex.label = i + 2  # assign previous chosen x's and y's a new colour
                        x.label = len(D) + 2  # assign x and y with a unique colour
                        y.label = len(I) + 2
                        num = num + check_isomorphism(coloured_graph, D + [x.uid], I + [y.uid],
                                                      count=count)  # explore the branch by recursion
                        if not count and num != 0:
                            return -1
                        y.label = 1
                break
            break
        return num
    return 0
