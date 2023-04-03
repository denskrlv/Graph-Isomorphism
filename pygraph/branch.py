import os
import time
from pygraph.graph_analyzer import *


def format_isomorphism_list(isomorphisms: list) -> List[list]:
    result = list()
    for pot_iso in isomorphisms:
        temp_list = list()
        temp_list.extend(pot_iso)
        for test_iso in isomorphisms:
            if pot_iso == test_iso:
                continue
            if pot_iso[0] in test_iso or pot_iso[1] in test_iso:
                temp_list.extend(test_iso)
        temp_list = list(set(temp_list))
        temp_list.sort()
        if temp_list not in result:
            result.append(temp_list)
    return result


def benchmark(directory):
    start = time.time()
    for filename in os.listdir(directory):
        print("Dataset:", filename)
        if "GIAut" in filename:
            print("Equivalence classes:\t\t\t#Aut:")
        elif "basicAut" in filename:
            print("Graph:\t\t\t#Aut:")
        else:
            print("Equivalence classes:")
        with open(directory + "/" + filename) as f:
            L = load_graph(f, read_list=True)
            start_time = time.time()
            count = 0
            equivalent = []
            automorphisms = {}
            if len(L[0]) == 1:
                left_graph = L[0][0]
                right_graph = fast_copy(left_graph)
                D = []
                I = []
                for v in left_graph.vertices:
                    v.g_num = 0
                    v.label = "1"
                    v.set_uid(count)
                    count += 1
                for v in right_graph.vertices:
                    v.g_num = 1
                    v.label = "1"
                    v.set_uid(count)
                    count += 1
                graph = left_graph + right_graph
                # with open('colorful' + filename + '.dot', 'w') as ff:
                #     write_dot(graph, ff)
                count = count_isomorphism(graph, D, I)
                print("0\t\t\t\t" + str(count))
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Elapsed time: {elapsed_time:.3f} seconds\n")
                continue
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
                    if "Aut" in filename:
                        count = count_isomorphism(graph, D, I)
                        if count > 0:
                            equivalent.append([i, j])
                            automorphisms[i] = count
                    else:
                        count = count_isomorphism(graph, D, I, count=False)
                        if count < 0:
                            equivalent.append([i, j])
            equivalent = format_isomorphism_list(equivalent)
            flat_equivalent = [item for sublist in equivalent for item in sublist]
            for i in range(len(L[0])):
                if i not in flat_equivalent:
                    equivalent.append([i])
            if "Aut" in filename:
                for equivalence_class in equivalent:
                    for element in equivalence_class:
                        if element in automorphisms:
                            print(str(equivalence_class) + "\t\t\t\t\t" + str(automorphisms[element]))
                        break
            else:
                for equivalence_class in equivalent:
                    print(equivalence_class)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Elapsed time: {elapsed_time:.3f} seconds\n")
    end = time.time()
    time_taken = end - start
    minutes = int(time_taken / 60)
    secs = time_taken % 60
    print(f"Total time for all graphs: {minutes} minute(s) and {secs:.2f} seconds\n")


benchmark("/Users/deniskrylov/Developer/Graph-Isomorphism/graphs/custom")
