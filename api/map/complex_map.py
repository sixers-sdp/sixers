import networkx as nx
from networkx.drawing.nx_pydot import write_dot


current_map = nx.Graph()

tables = ['t1', 't2', 't3', 't4']
CHEF = 'chef'

# add tables:
current_map.add_nodes_from(tables)

# add chef:
current_map.add_nodes_from([CHEF])

# add connecting nodes:
current_map.add_nodes_from(['cross1', 'cross2', 'cross3'])

current_map.add_edge('chef', 'cross1', color='red')
current_map.add_edge('cross1', 'cross2')
current_map.add_edge('cross2', 't3')
current_map.add_edge('cross2', 't4')

current_map.add_edge('cross2', 'cross3')
current_map.add_edge('cross3', 't1')
current_map.add_edge('cross3', 't2')
