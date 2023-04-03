from pygraph.graph_analyzer import *
import unittest
from pygraph.helpers import load_graph_from


class TestFindDiscrete(unittest.TestCase):

    def test_find_discrete_4_7(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/basic/colorref_smallexample_4_7.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 2, 0), (1, 3, 1)}

    def test_find_discrete_4_16(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/basic/colorref_smallexample_4_16.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 0), (2, 3, 1)}

    def test_find_discrete_2_49(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/basic/colorref_smallexample_2_49.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 1)}

    def test_find_discrete_6_15(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/basic/colorref_smallexample_6_15.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 1), (2, 3, 1), (4, 5, 0)}

    def test_find_discrete_10_27(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/basic/cref9vert3comp_10_27.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 3, 0), (1, 8, 9, 0), (2, 4, 7, 0), (5, 6, 0)}

    def test_find_discrete_4_9(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/basic/cref9vert_4_9.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 3, 1), (1, 2, 1)}

    def test_find_discrete_4_1026(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/basic/colorref_largeexample_4_1026.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 1), (2, 3, 1)}

    def test_find_discrete_6_960(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/basic/colorref_largeexample_6_960.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 4, 1), (1, 3, 0), (2, 5, 1)}

    def test_find_discrete_b1(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/advanced/CrefBenchmark1.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 2, 0), (1, 3, 0)}

    def test_find_discrete_b2(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/advanced/CrefBenchmark2.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 2, 4, 1), (1, 3, 1)}

    def test_find_discrete_b3(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/advanced/CrefBenchmark3.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 2, 3, 1), (1, 4, 1)}

    def test_find_discrete_b4(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/advanced/CrefBenchmark4.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 1), (2, 3, 1)}

    def test_find_discrete_b5(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/advanced/CrefBenchmark5.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 9, 0), (1, 6, 7, 0), (2, 3, 4, 0), (5, 8, 0)}

    def test_find_discrete_b6(self):
        graph = load_graph_from(
            "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/advanced/CrefBenchmark6.grl")
        coloured_graph = colourize(graph)
        discrete_graphs = find_discrete(coloured_graph)
        assert discrete_graphs == {(0, 1, 0), (2, 3, 4, 0)}
