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


def check_false_twins(v1: Vertex, v2: Vertex) -> bool:
    if v1.is_adjacent(v2):
        return False
    if len(v1.neighbours) != len(v2.neighbours):
        return False
    if len(v1.neighbours) != len(set(v1.neighbours + v2.neighbours)):
        return False
    return True


def check_twins(v1: Vertex, v2: Vertex) -> bool:
    if not v1.is_adjacent(v2):
        return False
    if len(v1.neighbours) != len(v2.neighbours):
        return False
    v1_neighbours = list(v1.neighbours)
    v2_neighbours = list(v2.neighbours)
    v1_neighbours.remove(v2)
    v2_neighbours.remove(v1)
    if len(v1_neighbours) != len(set(v1_neighbours + v2_neighbours)):
        return False
    return True


def recolor_twins(colors_dict: dict, color_class: str) -> List:
    twins = list()
    count = 2
    for color in colors_dict:
        if color == color_class:
            continue
        if len(colors_dict[color]) >= 4:
            vertices = colors_dict[color]
            for i in range(int(len(vertices) / 2) - 1):
                for j in range(1, int(len(vertices) / 2)):
                    if check_false_twins(vertices[i], vertices[j]) or check_twins(vertices[i], vertices[j]):
                        vertices[i].label = str(count)
                        # vertices[j].label = str(count + 1)
                        mid = int(len(vertices) / 2)
                        vertices[mid + i].label = str(count)
                        # vertices[mid + j].label = str(count + 1)
                        count += 1
                        twins.append(vertices[i].uid)
                        twins.append(vertices[j].uid)
                        twins.append(vertices[mid + i].uid)
                        twins.append(vertices[mid + j].uid)
            # if check_false_twins(vertices[0], vertices[1]) or check_twins(vertices[0], vertices[1]):
            #     vertices[1].label = str(count)
            #     vertices[3].label = str(count)
            #     count += 1
    return twins


def process_Aut(graph: Graph):
    count = 0
    print("Graph:\t\t\t#Aut:")
    for v in graph.vertices:
        v.g_num = 0
        v.label = 1
        v.set_uid(count)
        count += 1
    right_graph = fast_copy(graph)
    for v in right_graph.vertices:
        v.g_num = 1
        v.label = 1
        v.set_uid(count)
        count += 1
    graph = graph + right_graph
    generate_automorphism(graph, [], [])
    order = compute_order(X)
    print("0\t\t\t\t" + str(order))


def process_GI(graphs: List, aut: bool):
    count = 0
    equivalent = []
    automorphisms = {}
    if aut:
        print("Equivalence classes:\t\t\t#Aut:")
    else:
        print("Equivalence classes:")
    for i in range(len(graphs) - 1):
        for j in range(i + 1, len(graphs)):
            left_graph = graphs[i]
            right_graph = graphs[j]
            for v in left_graph.vertices:
                v.g_num = i
                v.label = 1
                v.set_uid(count)
                count += 1
            for v in right_graph.vertices:
                v.g_num = j
                v.label = 1
                v.set_uid(count)
                count += 1
            graph = left_graph + right_graph
            if aut:
                count = count_isomorphism(graph, [], [])
                if count > 0:
                    equivalent.append([i, j])
                    automorphisms[i] = count
            else:
                count = count_isomorphism(graph, [], [], count=False)
                if count < 0:
                    equivalent.append([i, j])
    equivalent = format_isomorphism_list(equivalent)
    flat_equivalent = [item for sublist in equivalent for item in sublist]
    for i in range(len(graphs)):
        if i not in flat_equivalent:
            equivalent.append([i])
    if aut:
        for equivalence_class in equivalent:
            for element in equivalence_class:
                if element in automorphisms:
                    print(str(equivalence_class) + "\t\t\t\t\t" + str(automorphisms[element]))
                break
    else:
        for equivalence_class in equivalent:
            print(equivalence_class)


def benchmark(directory):
    start = time.time()
    for filename in os.listdir(directory):
        start_time = time.time()
        with open(directory + "/" + filename) as f:
            L = load_graph(f, read_list=True)
        print("Dataset:", filename)
        if "basicAut" in filename:
            process_Aut(L[0][0])
        else:
            if "Aut" in filename:
                process_GI(L[0], True)
            else:
                process_GI(L[0], False)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.3f} seconds\n")
    end = time.time()
    time_taken = end - start
    minutes = int(time_taken / 60)
    secs = time_taken % 60
    print(f"Total time for all graphs: {minutes} minute(s) and {secs:.2f} seconds\n")


benchmark("graphs/custom")
