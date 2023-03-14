# from framework.graph import *
# from framework.graph_io import *
# import os
# import time
# from utils.graph_analyzer import *
#
# g_analyzer = GraphAnalyzer()
#
#
# def benchmark(directory):
#     total_time = 0
#     for filename in os.listdir(directory):
#         print("Dataset:", directory + "/" + filename)
#         with open(directory + "/" + filename) as f:
#             L = load_graph(f, read_list=True)
#             graph = Graph(False, 0)
#             i = 0
#             for g in L[0]:
#                 for v in g.vertices:
#                     v.g_num = i
#                 graph = graph + g
#                 i += 1
#         start_time = time.time()
#         result = g_analyzer.weisfeiler_lehman(graph)
#         end_time = time.time()
#         elapsed_time = end_time - start_time
#         total_time += elapsed_time
#         for r in result:
#             if r[-1] == 1:
#                 print(r[:-1], "discrete")
#             else:
#                 print(r[:-1])
#         print(f"Elapsed time: {elapsed_time:.4f} seconds\n")
#     print(f"Total time: {total_time:.4f} seconds\n")
#
# # TEST ZONE
# # benchmark('test_graphs/CRefFriday2023')
import time

from framework.graph import *
from framework.graph_io import *
import os
import time
from utils.graph_analyzer import *
g_analyzer = GraphAnalyzer()


def benchmark(directory):
    total_time = 0
    for filename in os.listdir(directory):
        print("Dataset:", directory + "/" + filename)
        with open(directory + "/" + filename) as f:
            L = load_graph(f, read_list=True)
            graph = Graph(False, 0)
            # i = 0
            # for g in L[0]:
            #     for v in g.vertices:
            #         v.g_num = i
            #     graph = graph + g
            #     i += 1
            for i in range(len(L[0]) - 1):
                for j in range(i + 1, len(L[0])):
                    left_graph = L[0][i]
                    right_graph = L[0][j]
                    for v in left_graph.vertices:
                        v.g_num = i
                    for v in right_graph.vertices:
                        v.g_num = j
                    graph = left_graph + right_graph
                    start_time = time.time()
                    count = g_analyzer.count_isomorphism(graph)
                    if count == 1:
                        print([i, j])
                    print("Count: " + str(count))
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    total_time += elapsed_time
                    with open('graph' + str(i) + 'x' + str(j) + '.dot', 'w') as gg:
                        write_dot(graph, gg)
        # for r in result:
        #     if r[-1] == 1:
        #         print(r[:-1], "discrete")
        #     else:
        #         print(r[:-1])
        print(f"Elapsed time: {elapsed_time:.4f} seconds\n")
    print(f"Total time: {total_time:.4f} seconds\n")

benchmark("graphs")
