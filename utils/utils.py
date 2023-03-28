from framework.graph import *
from framework.graph_io import load_graph


def load_graph_from(filename: str) -> Graph:
    with open(filename) as f:
        L = load_graph(f, read_list=True)
        graph = Graph(False, 0)
        i = 0
        for g in L[0]:
            for v in g.vertices:
                v.g_num = i
            graph = graph + g
            i += 1
        return graph


def make_copy(graph: Graph) -> Graph:
    graph_copy = Graph(False, 0)
    return graph_copy
