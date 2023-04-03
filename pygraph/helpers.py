from framework.graph import Graph, Edge
from framework.graph_io import load_graph


def load_graph_from(filename: str) -> Graph:
    """
    Loads a graph from a file.
    :param filename: The name of the file
    :return: The loaded graph
    """
    with open(filename) as f:
        loaded_graph = load_graph(f, read_list=True)
        graph = Graph(False, 0)
        i = 0
        for g in loaded_graph[0]:
            for v in g.vertices:
                v.g_num = i
            graph = graph + g
            i += 1
        return graph


def fast_copy(graph: Graph) -> Graph:
    """
    Makes a fast deepcopy of the graph.
    :param graph: A graph that should be copied
    :return: A copy of the graph
    """
    graph_copy = Graph(False, len(graph.vertices))
    for i in range(len(graph.vertices)):
        graph_copy.vertices[i].label = graph.vertices[i].label
        graph_copy.vertices[i].g_num = graph.vertices[i].g_num
        graph_copy.vertices[i].uid = graph.vertices[i].uid
    for j in range(len(graph.edges)):
        tail_index = graph.vertices.index(graph.edges[j].tail)
        head_index = graph.vertices.index(graph.edges[j].head)
        edge = Edge(graph_copy.vertices[tail_index], graph_copy.vertices[head_index])
        graph_copy.add_edge(edge)
    return graph_copy
