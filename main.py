import os
import time
from framework.graph_analyzer import *
from framework.graph_io import load_graph
from utils.utils import fast_copy


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


def process_aut(graphs: List):
    count = 0
    print("Graph:\t\t\tNumber of automorphisms:")
    for i in range(len(graphs)):
        left_graph = graphs[i]
        for v in left_graph.vertices:
            v.g_num = 0
            v.label = 1
            v.set_uid(count)
            count += 1
        right_graph = fast_copy(left_graph)
        for v in right_graph.vertices:
            v.g_num = 1
            v.label = 1
            v.set_uid(count)
            count += 1
        graph = left_graph + right_graph
        generate_automorphism(graph, [], [])
        order = compute_order(X)
        print(str(i) + ":\t\t\t\t" + str(order))


def process_gi(graphs: List, aut: bool):
    count = 0
    equivalent = []
    automorphisms = {}
    if aut:
        print("Sets of isomorphic graphs:\t\t\tNumber of automorphisms:")
    else:
        print("Sets of isomorphic graphs:")
    for i in range(len(graphs) - 1):
        for j in range(i + 1, len(graphs)):
            left_graph = graphs[i]
            right_graph = graphs[j]
            for v in left_graph.vertices:
                v.g_num = 0
                v.label = 1
                v.set_uid(count)
                count += 1
            for v in right_graph.vertices:
                v.g_num = 1
                v.label = 1
                v.set_uid(count)
                count += 1
            graph = left_graph + right_graph
            result = check_isomorphism(graph, [], [], count=False)
            if result < 0:
                equivalent.append([i, j])
                if aut:
                    automorphisms[i] = get_order(left_graph)
    equivalent = format_isomorphism_list(equivalent)
    if aut:
        for i in range(len(graphs)):
            found = False
            for pair in equivalent:
                if i in pair:
                    found = True
                    break
            if not found:
                equivalent.append([i])
                left_graph = graphs[i]
                order = get_order(left_graph)
                automorphisms[i] = order
    flat_equivalent = [item for sublist in equivalent for item in sublist]
    for i in range(len(graphs)):
        if i not in flat_equivalent:
            equivalent.append([i])
    if aut:
        for equivalence_class in equivalent:
            for element in equivalence_class:
                if element in automorphisms:
                    print(str(equivalence_class) + "\t\t\t\t\t\t" + str(automorphisms[element]))
                break
    else:
        for equivalence_class in equivalent:
            print(equivalence_class)


def get_order(g: Graph) -> int:
    count = 0
    left_graph = g
    for v in left_graph.vertices:
        v.g_num = 0
        v.label = 1
        v.set_uid(count)
        count += 1
    right_graph = fast_copy(left_graph)
    for v in right_graph.vertices:
        v.g_num = 1
        v.label = 1
        v.set_uid(count)
        count += 1
    graph = left_graph + right_graph
    generate_automorphism(graph, [], [])
    order = compute_order(X)
    if order > 0:
        return order
    return 0


def benchmark(directory):
    start = time.time()
    for filename in os.listdir(directory):
        start_time = time.time()
        with open(directory + "/" + filename) as f:
            L = load_graph(f, read_list=True)
        print("Dataset:", filename)
        if "Aut" in filename and "GI" not in filename:
            process_aut(L[0])
        else:
            if "GIAut" in filename:
                process_gi(L[0], True)
            else:
                process_gi(L[0], False)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.3f} seconds\n")
    end = time.time()
    time_taken = end - start
    minutes = int(time_taken / 60)
    secs = time_taken % 60
    print(f"Total time for all graphs: {minutes} minute(s) and {secs:.2f} seconds\n")


benchmark("graphs/delivery")
