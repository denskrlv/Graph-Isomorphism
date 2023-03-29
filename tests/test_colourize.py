from framework.graph import *
from framework.graph_analyzer import colourize
import unittest


class TestColourize(unittest.TestCase):

    def setUp(self) -> None:
        self.graph = Graph(False, 0)
        a = Vertex(self.graph)
        b = Vertex(self.graph)
        c = Vertex(self.graph)
        d = Vertex(self.graph)
        e = Vertex(self.graph)
        self.graph.add_edge(Edge(a, b))
        self.graph.add_edge(Edge(a, c))
        self.graph.add_edge(Edge(b, c))
        self.graph.add_edge(Edge(a, d))
        self.graph.add_edge(Edge(d, e))
        self.graph.add_edge(Edge(c, e))
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
        coloured_graph_empty = colourize(self.graph)
        self.graph.vertices[0].label = "2"
        self.graph.vertices[1].label = "3"
        coloured_graph_nonempty = colourize(self.graph, reset=False)
        assert len(coloured_graph_empty.vertices) == len(coloured_graph_nonempty.vertices)
        assert coloured_graph_empty.vertices[0].label != coloured_graph_nonempty.vertices[0].label
        assert coloured_graph_empty.vertices[1].label != coloured_graph_nonempty.vertices[1].label
        assert coloured_graph_empty.vertices[2].label != coloured_graph_nonempty.vertices[2].label
        assert coloured_graph_empty.vertices[3].label != coloured_graph_nonempty.vertices[3].label
        assert coloured_graph_empty.vertices[4].label != coloured_graph_nonempty.vertices[4].label
