from framework.graph import Graph
from pygraph.helpers import fast_copy


class Painter:

    def colourize(self, graph: Graph, reset: bool = True) -> Graph:
        """
        Colorizes the graph using Weisfeiler Lehman algorithm.
        :param graph: A graph that should be (re-)colorized
        :param reset: If True, the colours of the graph will be reset before colorization
        :return: The colorized graph
        """
        coloured_graph = fast_copy(graph)
        colours = {}
        if reset:
            for v in coloured_graph.vertices:
                v.label = "1"
            colours["1"] = coloured_graph.vertices
        else:
            for v in coloured_graph.vertices:
                colours.setdefault(str(v.label), []).append(v)

        converged = False
        number_of_partitions = self._check_partitions(colours)
        for i in range(1000):
            self._step(colours)
            self._update_dict(colours)
            new_number_of_partitions = self._check_partitions(colours)
            if new_number_of_partitions == number_of_partitions:
                converged = True
                break
            else:
                number_of_partitions = new_number_of_partitions
        if not converged:
            raise TimeoutError("Limit 1000 iterations exceeded! Colorization failed.")

        return coloured_graph