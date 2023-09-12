from exception import GraphException

class Graph:
    def __init__(self):
        self._edges = None
        self._vertices = []
        self._inbounds = {}
        self._outbounds = {}
        self._ids = {}

    def initialise_edges(self, edges):
        self._edges = edges

    def initialise_vertices(self, vertices):
        for index in range(0, vertices):
            self._vertices.append(index)

    def initialise_inbounds(self):
        for index in range(len(self._vertices)):
            self._inbounds[index] = []

    def initialise_outbounds(self):
        for index in range(len(self._vertices)):
            self._outbounds[index] = []

    def get_vertex_inbounds(self, vertex):
        if vertex in self._vertices:
            return self._inbounds[vertex]

    def get_vertex_outbounds(self, vertex):
        if vertex in self._vertices:
            return self._outbounds[vertex]

    def add_to_inbounds(self, main_vertex, inbound_vertex):
        self._inbounds[main_vertex].append(inbound_vertex)

    def add_to_outbounds(self, main_vertex, outbound_vertex):
        self._outbounds[main_vertex].append(outbound_vertex)

    def parse_inbounds(self, vertex):
        vertices = self.get_vertex_inbounds(vertex)
        for each_vertex in vertices:
            yield each_vertex

    def parse_outbounds(self, vertex):
        vertices = self.get_vertex_outbounds(vertex)
        for each_vertex in vertices:
            yield each_vertex

    def parse_edge_ids(self):
        for endpoints, id in self._ids.items():
            yield id

    def parse_edges(self):
        for endpoints, id in self._ids.items():
            yield endpoints, id

    def get_in_degree(self, vertex):
        return len(self.get_vertex_inbounds(vertex))

    def get_out_degree(self, vertex):
        return len(self.get_vertex_outbounds(vertex))

    def add_id(self, first_vertex, second_vertex, id):
        key = str(first_vertex) + '-' + str(second_vertex)
        self._ids[key] = id

    def get_outbounds(self, vertex):
        return self._outbounds[vertex]

    def check_edge_existence(self, main_vertex, second_vertex):
        if main_vertex not in self._vertices:
            return False
        elif second_vertex in self.get_vertex_outbounds(main_vertex):
            return True
        else:
            return False

    def change_edge_id(self, first_vertex, second_vertex, new_id):
        key = str(first_vertex) + '-' + str(second_vertex)
        if key in self._ids.keys():
            self._ids[key] = new_id

    def get_edge_endpoints(self, edge_id):
        for endpoints, id in self._ids.items():
            if id == edge_id:
                return endpoints
        raise GraphException("There is no edge with this id!")

    @property
    def inbounds(self):
        return self._inbounds

    def set_inbound(self, key, value):
        self._inbounds[key] = value

    @property
    def outbounds(self):
        return self._outbounds

    def set_outbound(self, key, value):
        self._outbounds[key] = value

    @property
    def costs(self):
        return self._ids

    def get_cost(self, v1, v2):
        edge = str(v1) + "-" + str(v2)
        return self._ids[edge]

    def set_id(self, key, value):
        self._ids[key] = value

    @property
    def edges(self):
        return self._edges

    @property
    def vertices(self):
        return self._vertices

    def vertices_count(self):
        return len(self._vertices)

    def parse_vertices(self):
        for vertex in self._vertices:
            yield vertex

    def add_vertex(self, vertex):
        if vertex not in self._vertices:
            self._vertices.append(vertex)
            self._inbounds[vertex] = []
            self._outbounds[vertex] = []
        else:
            raise GraphException("This vertex already exists!")

    def remove_vertex(self, vertex):
        if vertex in self._vertices:

            # removing the vertex from the vertices that has it as inbound
            for each_vertex in self._inbounds:
                if vertex in self.get_vertex_inbounds(each_vertex):
                    self._inbounds[each_vertex].remove(vertex)

            del self._inbounds[vertex]

            #removing the outbounds from that vertex
            del self._outbounds[vertex]

            #removing the vertex from the list of vertices
            self._vertices.remove(vertex)
        else:
            raise GraphException("This vertex does not exist!")

    def find_vertex(self, search_vertex):
        vertices = self.parse_vertices()
        for vertex in vertices:
            if vertex == search_vertex:
                return True, vertex
        return False

    def check_key(self, key):
        for i in self._ids.keys():
            if i == key:
                return True
        return False

    def check_id(self, id):
        for i in self._ids.values():
            if i == id:
                return True
        return False

    def get_key(self, id):
        for i in self._ids.keys():
            if self._ids[i] == id:
                return i


    def add_edge(self, vertex_1, vertex_2, edge_id):
        key = str(vertex_1) + '-' + str(vertex_2)
        #if (self.check_key(key) is False):
        self._ids[key] = edge_id
            #self.add_to_inbounds(vertex_2, vertex_1)
            #self.add_to_outbounds(vertex_1, vertex_2)
        # else:
            # GraphException("Could not add this edge!")

    def remove_edge(self, edge_id):
        if self.check_id(edge_id) is True:
            del self._ids[self.get_key(edge_id)]

    def make_copy(self):
        copy = Graph()
        edges = self._edges
        vertices = self.vertices_count()
        graph_edges = self._ids
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
