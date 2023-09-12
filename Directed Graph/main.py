from Graph.graph import Graph
from UI.ui import UI
g = Graph()
ui = UI(g)
# ui.read_graph()
ui.start_ui()


# Functionality demo
# data - 1 5 9 (edge from 1 to 5 exists and has the value of 9)

# print("\n----------D E M O----------\n")
# print(g.check_edge_existence(1,5)) # Should be true
# new_graph = g.make_copy()
# print(new_graph.check_edge_existence(1,5)) # Again, should be true
# new_graph.remove_vertex(1)
# print(new_graph.check_edge_existence(1,5)) # Should be false
# print(g.check_edge_existence(1,5)) # Should be true
