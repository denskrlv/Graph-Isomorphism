from framework.graph import *
from framework.graph_analyzer import colorize
import unittest


class TestColorize(unittest.TestCase):

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

    def test_colorize_deepcopy(self):
        colored_graph = colorize(self.graph)
        assert colored_graph is not self.graph
        assert colored_graph.vertices is not self.graph.vertices
        assert colored_graph.edges is not self.graph.edges
        for i in range(len(colored_graph.vertices)):
            assert colored_graph.vertices[i] is not self.graph.vertices[i]
        for i in range(len(colored_graph.edges)):
            assert colored_graph.edges[i] is not self.graph.edges[i]

    def test_colorize_empty(self):
        colored_graph = colorize(self.graph)
        assert len(colored_graph.vertices) == 5
        assert colored_graph.vertices[0].label == "5a199f9b"
        assert colored_graph.vertices[1].label == "52a95d94"
        assert colored_graph.vertices[2].label == "5a199f9b"
        assert colored_graph.vertices[3].label == "ea42b623"
        assert colored_graph.vertices[4].label == "ea42b623"

    def test_colorize_nonempty(self):
        colours = {"1": [self.graph.vertices[0], self.graph.vertices[3]],
                   "2": [self.graph.vertices[1], self.graph.vertices[2], self.graph.vertices[5]]}
        # FIXME: vertices in the colours dict still linked to the original graph
        colored_graph = colorize(self.graph, colours)
        # print(self.graph)
        assert len(colored_graph.vertices) == 5
        assert colored_graph.vertices[0].label == "1"
        assert colored_graph.vertices[1].label == "2"
        assert colored_graph.vertices[2].label == "1"
        assert colored_graph.vertices[3].label == "2"
