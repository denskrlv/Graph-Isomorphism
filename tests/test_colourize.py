from framework.graph import *
from pygraph.graph_analyzer import colourize
import unittest

from framework.graph_io import load_graph, write_dot


class TestColourize(unittest.TestCase):

    def setUp(self) -> None:
        with open("/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/custom/trees11.grl") as f:
            L = load_graph(f, read_list=True)
            graph1 = L[0][2]
            graph2 = L[0][5]
            self.graph = Graph(False, 0)
            self.graph = self.graph + graph1
            self.graph = self.graph + graph2
        # self.graph = Graph(False, 0)
        # a = Vertex(self.graph)
        # b = Vertex(self.graph)
        # c = Vertex(self.graph)
        # d = Vertex(self.graph)
        # e = Vertex(self.graph)
        # self.graph.add_edge(Edge(a, b))
        # self.graph.add_edge(Edge(a, c))
        # self.graph.add_edge(Edge(b, c))
        # self.graph.add_edge(Edge(a, d))
        # self.graph.add_edge(Edge(d, e))
        # self.graph.add_edge(Edge(c, e))
        for i in range(len(self.graph.vertices)):
            self.graph.vertices[i].label = "1"

    def test_colourize_deepcopy(self):
        """
        Tests if the colourize function returns a new graph object and if the vertices and edges are new objects.
        """
        coloured_graph = colourize(self.graph)
        assert coloured_graph is not self.graph
        assert coloured_graph.vertices is not self.graph.vertices
        assert coloured_graph.edges is not self.graph.edges
        for i in range(len(coloured_graph.vertices)):
            assert coloured_graph.vertices[i] is not self.graph.vertices[i]
        for i in range(len(coloured_graph.edges)):
            assert coloured_graph.edges[i] is not self.graph.edges[i]

    def test_colourize_empty(self):
        """
        Tests if the colourize function returns a correctly coloured graph.
        """
        coloured_graph = colourize(self.graph)
        assert len(coloured_graph.vertices) == 5
        assert coloured_graph.vertices[0].label == "5a199f9b"
        assert coloured_graph.vertices[1].label == "52a95d94"
        assert coloured_graph.vertices[2].label == "5a199f9b"
        assert coloured_graph.vertices[3].label == "ea42b623"
        assert coloured_graph.vertices[4].label == "ea42b623"

    def test_colourize_nonempty(self):
        """
        Tests if the colourize function returns different results when the graph is already coloured.
        """
        # coloured_graph_empty = colourize(self.graph)
        self.graph.vertices[1].label = "2"
        self.graph.vertices[11].label = "2"
        with open('graph1.dot', 'w') as gg:
            write_dot(self.graph, gg)
        coloured_graph_nonempty = colourize(self.graph, reset=False)
        with open('graph2.dot', 'w') as gg:
            write_dot(coloured_graph_nonempty, gg)
        # assert len(coloured_graph_empty.vertices) == len(coloured_graph_nonempty.vertices)
        # for i in range(len(coloured_graph_empty.vertices)):
        #     assert coloured_graph_empty.vertices[i].label != coloured_graph_nonempty.vertices[i].label
        # assert coloured_graph_nonempty.vertices[1].label == coloured_graph_nonempty.vertices[11].label
        # assert coloured_graph_nonempty.vertices[5].label == coloured_graph_nonempty.vertices[13].label
        # assert coloured_graph_nonempty.vertices[1].label != coloured_graph_nonempty.vertices[5].label
        # assert coloured_graph_nonempty.vertices[11].label != coloured_graph_nonempty.vertices[13].label
