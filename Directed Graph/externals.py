import random
from itertools import permutations
from math import inf
from sys import  maxsize
from myqueue import MyQueue
from Graph.graph import Graph


def check_vertices(graph, vertex_1, vertex_2):
    if vertex_1 == vertex_2:
        return False
    if graph.check_edge_existence(vertex_1, vertex_2) == True:
        return False
    return True


def read_graph_external(graph):
    print("'Ello mate, let me read this graph for ya")
    file = open("D:\\Uni\Graph Algorithms\Directed Graph\\test_graph.txt", "r+")
    line = file.readline().strip()
    vertices, edges = line.split(" ")
    graph.initialise_vertices(int(vertices))
    graph.initialise_edges(int(edges))
    graph.initialise_inbounds()
    graph.initialise_outbounds()
    # count = 0
    while line:
        line = file.readline()
        if line != "":
            vertex_1, vertex_2, edge_id = line.strip().split(" ")
            graph.add_to_outbounds(int(vertex_1), int(vertex_2))
            graph.add_to_inbounds(int(vertex_2), int(vertex_1))
            graph.add_edge(int(vertex_1), int(vertex_2), int(edge_id))
            # print(count)
            # count+= 1


def write_graph_external(graph):
    file = open("D:\\Uni\Graph Algorithms\Directed Graph\\test_graph.txt", "w")
    vertices = graph.vertices
    edges = graph.edges

    # Writing the number of vertices and edges
    line = str(len(vertices)) + " " + str(edges) + "\n"
    file.write(line)

    #getting the set of outbounds for each vertex
    outbounds = graph.outbounds

    #getting the list of edges and their ids (values
    ids = graph.costs

    #for each vertex, we parse through its outbounds, get the value of the edge and write it into the file
    for i in graph.parse_vertices():
        for j in graph.parse_outbounds(i):
            key = str(i) + "-" + str(j)
            value = ids[key]
            line = str(i) + " " + str(j) + " " + str(value) + "\n"
            file.write(line)

    print("Hey there, jimbo! Check your file for a surprise!")


def random_graph_external(vertices, edges):
    if edges > vertices * (vertices + 1):
        print("Too many edges!")
    else:
        new_graph = Graph()
        new_graph.initialise_vertices(vertices)
        new_graph.initialise_edges(edges)
        new_graph.initialise_outbounds()
        new_graph.initialise_inbounds()
        i = 1
        while i <= edges:
            vertex_1 = random.randint(0, vertices-1)
            vertex_2 = random.randint(0, vertices-1)
            if check_vertices(new_graph, vertex_1, vertex_2) is True:
                new_graph.add_edge(vertex_1, vertex_2, i)
                new_graph.add_to_inbounds(vertex_2, vertex_1)
                new_graph.add_to_outbounds(vertex_1, vertex_2)
                # print(str(vertex_1) + " " + str(vertex_2))
                i += 1

        # print("Aight, we done here!")
        return new_graph


def lowest_length(graph, vertex_1, vertex_2):
    q = MyQueue()
    q.enqueue(vertex_1)
    visited = [False for vertex in graph.vertices]
    visited[vertex_1] = True

    prev = [None for vertex in graph.vertices]
    while not q.is_empty():
        node = q.dequeue()
        neighbors = graph.get_vertex_outbounds(node)
        for next in neighbors:
            if not visited[next]:
                q.enqueue(next)
                visited[next] = True
                prev[next] = node


    path = []
    at = vertex_2
    while at !=None:
        path.append(at)
        at = prev[at]
    path.reverse()
    if len(path) == 0:
        print("no path")
    else:
        print("The length of the path is: " + str(len((path))))

        for i in range(0,len(path)-1):
            print(path[i], end="->")
        print(path[len(path)-1])

def lowest_cost_walk(graph, vertex_1, vertex_2):
    """
    Function that finds the lowest cost walk between two vertices
    Using Ford's algorithm
    If there are negative cost cycles accessible from the starting vertex, a message will be printed
    :param graph: the graph in use
    :param vertex_1: the starting vertex
    :param vertex_2: the destination vertex
    :return: the lowest cost walk, or a message
    """


    distance = [inf for i in range(graph.vertices_count())]
    prev = [inf for i in range(graph.vertices_count())]
    vertices = graph.vertices
    edges = graph.costs
    distance[vertex_1] = 0
    index = 0
    done = True
    while done and index < len(vertices):
        done = False
        for edge in edges:
            cost = edges[edge]
            first_v, second_v = edge.split("-")
            first_v = int(first_v)
            second_v = int(second_v)
            if distance[first_v] + cost < distance[second_v] and distance[first_v] != inf:
                distance[second_v] = distance[first_v] + cost
                prev[second_v] = first_v
                done = True
        index += 1

    for edge in edges:
        cost = edges[edge]
        first_v, second_v = edge.split("-")
        first_v = int(first_v)
        second_v = int(second_v)
        if distance[second_v] > distance[first_v] + cost and distance[first_v] != inf:
            print("Negative weight cycle")
            return


    path = []
    at = vertex_2
    while at != inf:
        path.append(at)
        at = prev[at]
    path.reverse()
    if len(path) == 0:
        print("no walk")
    else:
        print("Minimum cost walk: " + str(distance[vertex_2]))

        for i in range(0,len(path)-1):
            print(path[i], end="->")
        print(path[len(path)-1])

def kruskal(graph):

    sorted_graph = sorted(convert_to_undirected(graph), key=lambda x: x[2])
    result = []
    i = 0
    e = 0
    n = graph.vertices_count()
    set = [0] * n
    for i in range(n):
        set[i] = [i]

    for edge in sorted_graph:
        set_u = find_set(n, edge[0], set)
        set_v = find_set(n, edge[1], set)
        if set_u != set_v:
            result.append(edge)

            for value in set[set_v]:
                set[set_u].append(value)
            set[set_v].clear()


    minimumCost = 0
    print("Edges in the constructed MST")
    for u, v, weight in result:
        minimumCost += weight
        print("%d -- %d == %d" % (u, v, weight))
    print("Minimum Spanning Tree", minimumCost)

def find_set(n, vertex, set):
    for i in range(n):
        if vertex in set[i]:
            return i

def find(parent, i):
    if parent[i] == i:
        return i
    find(parent, parent[i])

def union(parent, rank, x, y):
    xroot = find(parent, x)
    yroot = find(parent, y)

    if rank[xroot] < rank[yroot]:
        parent[xroot] = yroot
    elif rank[xroot] > rank[yroot]:
        parent[yroot] = xroot
    else:
        parent[yroot] = xroot
        rank[xroot] += 1

def convert_to_undirected(graph):
    all_costs = graph.costs
    undirected = []
    keys = list(all_costs.keys())
    for key in keys:
        reverse_key, index = find_index_of_reverse_key(keys, key)
        if(index != -1):
            a_to_b = all_costs[key]
            b_to_a = all_costs[reverse_key]
            if(a_to_b < b_to_a):
                all_costs.pop(reverse_key)
                keys.pop(keys.index(reverse_key))
            else:
                all_costs.pop(key)
                keys.pop(keys.index(key))

    for key in keys:
        v = []
        v1, v2 = key.split("-")
        v1 = int(v1)
        v2 = int(v2)
        v.append(v1)
        v.append(v2)
        v.append(all_costs[key])
        undirected.append(v)

    return undirected

def find_index_of_reverse_key(all_keys, key):
    vertex1, vertex2 = key.split("-")
    new_key = vertex2 + "-" + vertex1
    try:
        val = all_keys.index(new_key)
        return new_key, val
    except ValueError:
        return new_key, -1


def TSP(graph, s):
    print("Given a digraph with costs, find a minimum cost Hamiltonian cycle (i.e., solve the TSP)\n")
    vertex = []
    V = graph.vertices_count()
    for i in range(V):
        if i != s:
            vertex.append(i)

    path = []
    path.append(s)

    min_path = maxsize
    next_permutation = permutations(vertex)
    for i in next_permutation:
            current_path_cost = 0
            k = s
            done = False
            for j in i:
                if graph.check_edge_existence(k ,j) is False:
                    done = True
                    break
                current_path_cost += graph.get_cost(k ,j)
                k = j
            if graph.check_edge_existence(k ,s) is False:
                done = True

            if done is False:
                current_path_cost += graph.get_cost(k, s)
                if current_path_cost < min_path:
                    min_path = current_path_cost
                    path.clear()
                    path.append(s)
                    for j in i:
                        path.append(j)


    if(len(path) != 1):
        print(min_path)
        print(path)

    else:
        print("No minimum cost Hamiltonian cycle")