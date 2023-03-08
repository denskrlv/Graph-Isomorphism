import hashlib
from framework.graph import *


class GraphAnalyzer(object):
    
    def weisfeiler_lehman(self, G):
        colours = {}

        '''
        Step 1. 
        To initialize the algorithm we set C_{0,n} = 1 for all nodes n.
        Then we add all nodes to the dictionary with value of the colour '1'.
        '''
        for v in G.vertices:
            v.label = "1"
        colours["1"] = G.vertices

        '''
        Steps 2 - N.
        We compute L_{1,n} for every node.
        Then we compress the L_{1,n} to labels C_{1,n} for all nodes.
        After that we sort the labels and assign new colours according to the rule:
        - for the smallest label color is alpha_{i+1}
        - for larger label the color is alpha_{i+2}
        and so on.
        '''
        number_of_partitions = 0
        converged = False
        for i in range(1000):
            self._step(colours)
            self._update_dict(colours)
            new_number_of_partitions = self._check_partitions(colours)
            if new_number_of_partitions == number_of_partitions:
                print("Colorified succesfully! Iterations:", i)
                converged = True
                break
            else:
                number_of_partitions = new_number_of_partitions
        if (not converged):
            print("Limit 1000 iterations exceeded! Colorification failed.")

        '''
        Step N+1.
        Filter the vertices according to the graph_num and put it as values in dictionary.
        Labels that represent the colours of each graph are already sorted so to check identical graphs 
        we just need to compare all combinations of arrays.
        '''
        graphs = {}
        for _, value in colours.items():
            for v in value:
                graphs.setdefault(v.g_num, []).append(v.label) 
        identical_graphs = self._find_identical(graphs)
        
        '''
        Step N+2.
        Check the graphs for discreteness. If the len of the set equals the len of the initial array,
        that means that array is filled only with unique elements and it discrete.
        '''
        for ig in identical_graphs:
            if len(set(graphs[ig[0]])) == len(graphs[ig[0]]):
                ig.append(1)
            else:
                ig.append(0)

        return identical_graphs

    def _find_identical(self, graphs):
        identical = {}
        for key, value in graphs.items():
            value_key = tuple(value)
            if value_key in identical:
                identical[value_key].append(key)
            else:
                identical[value_key] = [key]
        output = [group for group in identical.values() if len(group) > 1]
        return output
    
    def _step(self, colours):
        colours_copy = colours.copy()
        for key, value in colours_copy.items():
            if value != []:
                compressed_labels = []
                for v in value:
                    cl = self._get_compressed_label(v)
                    compressed_labels.append(cl)
                self._map_values_with_colours(compressed_labels, key, colours)


    def _get_compressed_label(self, V):
        cl = V.label
        neighbours = []
        for n in V.neighbours:
            neighbours.append(n.label)
        neighbours = sorted(neighbours)
        str_neighbours = cl.join(str(n) for n in neighbours)
        hash_cl = hashlib.sha256(str_neighbours.encode())
        hash_label = hash_cl.hexdigest()
        hash_label = hash_label[:8]
        return (V, hash_label)

    def _map_values_with_colours(self, labels, curr_key, colours):
        for l in labels:
            l[0].label = l[1]
            colours.setdefault(l[1], []).append(l[0])
            colours[curr_key].remove(l[0])

    def _check_partitions(self, colours):
        return len(colours.keys())

    def _update_dict(self, colours):
        colours_copy = colours.copy()
        for key, value in colours_copy.items():
            if value == []:
                del colours[key]