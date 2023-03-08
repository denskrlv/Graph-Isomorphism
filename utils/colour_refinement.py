import os
import time

from framework.graph import *
from framework.graph_io import load_graph, write_dot


def refine_colour(graph: Graph) -> Graph:
    # Make all labels equal to their degree
    for vertex in graph.vertices:
        vertex.label = vertex.degree

    # Make a dict with what labels correspond to what neighbors
    labels_dict = dict()
    # This dict stores what vertices need their label changed
    vertex_dict = dict()

    # This will loop until the refinement is done
    while not refinement_done(graph):
        labels_dict.clear()
        vertex_dict.clear()
        # We go through the vertices and store what label corresponds to what neighbours
        for vertex in graph.vertices:
            # Store what label is associated with given neighbours
            if vertex.label not in labels_dict:
                labels_dict[vertex.label] = get_neighbours_label(vertex.neighbours)
                continue

            # If vertex has same label and neighbours as in dict, continue
            if labels_dict[vertex.label] == get_neighbours_label(vertex.neighbours):
                continue

            # If neighbours are unique, create new label
            if get_neighbours_label(vertex.neighbours) not in labels_dict.values():
                label = graph._next_label()
                labels_dict[label] = get_neighbours_label(vertex.neighbours)
                vertex_dict[label] = [vertex]
                continue

            # If we get here that means that this vertex needs its label changed, so add it to the dict
            vertex_dict[get_key(labels_dict, get_neighbours_label(vertex.neighbours))].append(vertex)

        # Go through the dict and assign the new labels to the vertices
        for label in vertex_dict:
            for vertex in vertex_dict[label]:
                vertex.label = label
    return graph


def get_key(dictionary: dict, value):
    for key in dictionary:
        if dictionary[key] == value:
            return key
    return None


def refinement_done(graph: Graph) -> bool:
    labels_dict = dict()
    for vertex in graph.vertices:
        # Store what label is associated with given neighbours
        if vertex.label not in labels_dict:
            labels_dict[vertex.label] = get_neighbours_label(vertex.neighbours)
            continue
        # If we find two vertices with the same label but different neighbours, refinement isn't done
        if labels_dict[vertex.label] != get_neighbours_label(vertex.neighbours):
            return False
    return True


def get_neighbours_label(neighbours: List[Vertex]) -> List[int]:
    result = list()
    for neighbour in neighbours:
        result.append(neighbour.label)
    result.sort()
    return result


def separate_graphs(graph: Graph, number: int) -> dict:
    interval = int(len(graph.vertices) / number)
    key = 0
    result = dict()
    result[key] = []
    count = 0
    for vertex in graph.vertices:
        if count == interval:
            key += 1
            result[key] = []
            count = 0
        result[key].append(vertex)
        count += 1
    return result


def check_isomorphism(graph: Graph, number: int):
    graph = refine_colour(graph)
    graphs_dict = separate_graphs(graph, number)
    labels_dict = dict()
    for key in graphs_dict:
        labels_dict[key] = []
        for vertex in graphs_dict[key]:
            labels_dict[key].append(vertex.label)
        labels_dict[key].sort()
    isomorphisms_list = list()
    for key in labels_dict:
        for test_key in labels_dict:
            if key == test_key:
                continue
            if labels_dict[key] == labels_dict[test_key]:
                temp_list = [key, test_key]
                temp_list.sort()
                if temp_list not in isomorphisms_list:
                    isomorphisms_list.append(temp_list)
    isomorphisms_list = format_isomorphism_list(isomorphisms_list)
    for isomorphism in isomorphisms_list:
        if is_discrete(labels_dict, isomorphism[0]):
            print(str(isomorphism) + " discrete")
            continue
        print(isomorphism)


def is_discrete(labels_dict: dict, key: int) -> bool:
    labels_list = labels_dict[key]
    no_duplicates_list = list(set(labels_list))
    if len(labels_list) == len(no_duplicates_list):
        return True
    return False


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


def assignment():
    total_time = 0
    directory_name = "benchmark_files"
    for file in os.listdir("C:\\Users\\Paul\\PycharmProjects\\pythonProject\\" + directory_name):
        print(file)
        print("Sets of possibly isomorphic graphs:")
        with open("C:\\Users\\Paul\\PycharmProjects\\pythonProject\\" + directory_name + "\\" + file) as f:
            g = load_graph(f, read_list=True)
            final_graph = Graph(False, 0)
            number = 0
            for graph in g[0]:
                final_graph = final_graph + graph
                number += 1
        file_time_start = time.perf_counter()
        check_isomorphism(final_graph, number)
        file_time_end = time.perf_counter()
        print(f"Time:{file_time_end - file_time_start: 0.2f} seconds")
        total_time += (file_time_end - file_time_start)
        print()
    print(f"Total time:{total_time: 0.2f} seconds")


assignment()
