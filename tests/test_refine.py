import os
import unittest

from framework.graph import Graph, Vertex, Edge
from framework.graph_io import load_graph, write_dot
from pygraph.graph_analyzer import refine, colourize


class TestRefine(unittest.TestCase):

    def setUp(self) -> None:
        """
        Sets up the test graph.
        """
        self.graph = Graph(False, 0)
        q0 = Vertex(self.graph)
        q1 = Vertex(self.graph)
        q2 = Vertex(self.graph)
        q3 = Vertex(self.graph)
        q4 = Vertex(self.graph)
        q5 = Vertex(self.graph)
        q6 = Vertex(self.graph)
        q7 = Vertex(self.graph)
        self.graph.add_edge(Edge(q0, q1))
        self.graph.add_edge(Edge(q1, q2))
        self.graph.add_edge(Edge(q1, q3))
        self.graph.add_edge(Edge(q2, q3))
        self.graph.add_edge(Edge(q0, q4))
        self.graph.add_edge(Edge(q4, q5))
        self.graph.add_edge(Edge(q5, q6))
        self.graph.add_edge(Edge(q4, q7))
        self.graph.add_edge(Edge(q5, q7))
        self.graph.add_edge(Edge(q6, q7))

    def test_refine(self):
        refined_graph = refine(self.graph)
        # assert len(refined_graph.vertices) == len(self.graph.vertices)

    def test_compare1(self):
        directory = "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/advanced"
        for filename in os.listdir(directory):
            print("Dataset:", directory + "/" + filename)
            with open(directory + "/" + filename) as f:
                L = load_graph(f, read_list=True)
                graph = Graph(False, 0)
                i = 0
                for g in L[0]:
                    for v in g.vertices:
                        v.g_num = i
                    graph = graph + g
                    i += 1
            result = colourize(graph)

    def test_compare2(self):
        directory = "/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/advanced"
        for filename in os.listdir(directory):
            num = 0
            print("Dataset:", directory + "/" + filename)
            with open(directory + "/" + filename) as f:
                L = load_graph(f, read_list=True)
                graph = Graph(False, 0)
                i = 0
                for g in L[0]:
                    for v in g.vertices:
                        v.g_num = i
                    graph = graph + g
                    i += 1
            result = refine(graph)
