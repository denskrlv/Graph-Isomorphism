import os
import time
from framework.graph_analyzer import *


def benchmark(directory):
    start = time.time()
    for filename in os.listdir(directory):
        print("Dataset:", directory + "/" + filename)
        with open(directory + "/" + filename) as f:
            L = load_graph(f, read_list=True)
            start_time = time.time()
            count = 0
            for i in range(len(L[0]) - 1):
                for j in range(i + 1, len(L[0])):
                    left_graph = L[0][i]
                    right_graph = L[0][j]
                    D = []
                    I = []
                    for v in left_graph.vertices:
                        v.g_num = i
                        v.label = "1"
                        v.set_uid(count)
                        count += 1
                    for v in right_graph.vertices:
                        v.g_num = j
                        v.label = "1"
                        v.set_uid(count)
                        count += 1
                    graph = left_graph + right_graph
                    count = count_isomorphism(graph, D, I)
                    if count > 0:
                        print(str([i, j]) + " " + str(count))
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time:.3f} seconds\n")
    end = time.time()
    time_taken = end - start
    minutes = int(time_taken / 60)
    secs = time_taken % 60
    print(f"Total time for all graphs: {minutes} minute(s) and {secs:.2f} seconds\n")


benchmark("graphs/custom")