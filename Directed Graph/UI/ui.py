from Graph.graph import Graph
from exception import GraphException
from externals import read_graph_external, write_graph_external, random_graph_external, lowest_length, lowest_cost_walk, \
    kruskal, TSP


class UI:
    def __init__(self, graph):
        self._graph = graph

    def read_graph(self):
        read_graph_external(self._graph)

    def write_graph(self):
        write_graph_external(self._graph)
        print("Graph written!")

    def random_graph(self):
        vertices = int(input("Give the number of vertices: "))
        edges = int(input("Give the number of edges: "))
        self._graph = random_graph_external(vertices, edges)
        print("Random graph generated!")

    def vertices_number(self):
        print("Nr of vertices: " + str(self._graph.vertices_count()))

    def check_edge(self):
        vertex_1 = int(input("First vertex: "))
        vertex_2 = int(input("Second vertex: "))
        if self._graph.check_edge_existence(vertex_1, vertex_2) is True:
            print("There exists an edge between " + str(vertex_1) + " and " + str(vertex_2))
        else:
            print("There's no edge between " + str(vertex_1) + " and " + str(vertex_2))

    def vertex_degrees(self):
        vertex = int(input("Vertex: "))
        inbounds = self._graph.get_vertex_inbounds(vertex)
        outbounds = self._graph.get_vertex_outbounds(vertex)
        print("Inbounds: ")
        print(inbounds)
        print("Outbounds: ")
        print(outbounds)

    def edge_endpoints(self):
        edge = int(input("Edge id: "))
        endpoints = self._graph.get_edge_endpoints(edge)
        print(str(endpoints) + " has the ID " + str(edge))

    def add_vertex(self):
        vertex = int(input("Value of the vertex: "))
        self._graph.add_vertex(vertex)

    def remove_vertex(self):
        vertex = int(input("Value of the vertex: "))
        self._graph.remove_vertex(vertex)

    def add_edge(self):
        edge = int(input("Value of the edge: "))
        vertex_1 = int(input("First vertex: "))
        vertex_2 = int(input("Second vertex: "))
        self._graph.add_edge(vertex_1, vertex_2, edge)
        self._graph.add_to_inbounds(vertex_2, vertex_1)
        self._graph.add_to_outbounds(vertex_1, vertex_2)

    def remove_edge(self):
        edge = int(input("Value of the edge: "))
        self._graph.remove_edge(edge)

    def copy_graph(self):
        copy = Graph()
        edges = self._graph.edges
        vertices = self._graph.vertices_count()
        graph_edges = self._graph.costs
        copy.initialise_edges(edges)
        copy.initialise_vertices(vertices)
        copy.initialise_inbounds()
        copy.initialise_outbounds()
        for edge in graph_edges:
            v1, v2 = edge.split("-")
            copy.add_edge(int(v1), int(v2), graph_edges.get(edge))
            copy.add_to_inbounds(int(v2), int(v1))
            copy.add_to_outbounds(int(v1), int(v2))

        # print("Alright mate, you've got a copy now")
        return copy

    def print_menu(self):
        print("0. Exit\n"
              "1. Read a graph from a file\n"
              "2. Write a graph into a file\n"
              "3. Generate a random graph\n"
              "4. Get the number of vertices of the graph\n"
              "5. Check if there exists an edge between two vertices\n"
              "6. In degree & Out degree of a vertex\n"
              "7. Endpoints of a certain edge\n"
              "8. Add a vertex\n"
              "9. Remove vertex\n"
              "10. Add edge\n"
              "11. Remove edge\n"
              "12. Copy the graph\n"
              "13. Print menu\n"
              "14. Lowest path\n"
              "15. Lowest cost walk\n"
              "16. Minimum spanning tree\n"
              "17. Solve the TSP\n")

    def lowest_length(self):
        v1 = int(input("vertex1: "))
        v2 = int(input("vertex2: "))
        lowest_length(self._graph, v1, v2)

    def lowest_cost_walk(self):
        v1 = int(input("vertex1: "))
        v2 = int(input("vertex2: "))
        lowest_cost_walk(self._graph, v1, v2)

    def min_span_tree(self):
        kruskal(self._graph)

    def TSP_solve(self):
        v = int(input("Give starting vertex"))
        TSP(self._graph, v)

    def start_ui(self):
        done = False
        commands = {
            '13': self.print_menu,
            '1': self.read_graph,
            '2': self.write_graph,
            '3': self.random_graph,
            '4': self.vertices_number,
            '5': self.check_edge,
            '6': self.vertex_degrees,
            '7': self.edge_endpoints,
            '8': self.add_vertex,
            '9': self.remove_vertex,
            '10': self.add_edge,
            '11': self.remove_edge,
            '12': self.copy_graph,
            '14': self.lowest_length,
            '15': self.lowest_cost_walk,
            '16': self.min_span_tree,
            '17': self.TSP_solve
        }
        self.print_menu()
        while not done:
            command = input("command> ")
            if command in commands:
                try:
                    commands[command]()
                except GraphException as ge:
                    print(ge)
            elif command == '0':
                done = True
                print("Cheerio!")
            else:
                print("Invalid command!")


