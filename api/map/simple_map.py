import networkx as nx
from networkx.drawing.nx_pydot import write_dot


current_map = nx.Graph()

tables = ['t1', 't2', 't3']
CHEF = 'chef'

# add tables:
current_map.add_nodes_from(tables)

# add chef:
current_map.add_nodes_from([CHEF])


current_map.add_edge('chef', 't1', color='red')
current_map.add_edge('t1', 't2', color='blue')
current_map.add_edge('chef', 't3', color='red')
