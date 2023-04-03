from pygraph.graph_analyzer import *
from pygraph.helpers import load_graph_from
import unittest


class TestFindDiscrete(unittest.TestCase):

    def test_find_discrete_4_7(self):
        graph = load_graph_from("colorref_smallexample_4_7.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 2, 0), (1, 3, 1)}

    def test_find_discrete_4_16(self):
        graph = load_graph_from("colorref_smallexample_4_16.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 0), (2, 3, 1)}

    def test_find_discrete_2_49(self):
        graph = load_graph_from("colorref_smallexample_2_49.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 1)}

    def test_find_discrete_6_15(self):
        graph = load_graph_from("colorref_smallexample_6_15.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 1), (2, 3, 1), (4, 5, 0)}

    def test_find_discrete_10_27(self):
        graph = load_graph_from("cref9vert3comp_10_27.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 3, 0), (1, 8, 9, 0), (2, 4, 7, 0), (5, 6, 0)}

    def test_find_discrete_4_9(self):
        graph = load_graph_from("cref9vert_4_9.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 3, 1), (1, 2, 1)}

    def test_find_discrete_4_1026(self):
        graph = load_graph_from("colorref_largeexample_4_1026.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 1), (2, 3, 1)}

    def test_find_discrete_6_960(self):
        graph = load_graph_from("colorref_largeexample_6_960.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 4, 1), (1, 3, 0), (2, 5, 1)}
