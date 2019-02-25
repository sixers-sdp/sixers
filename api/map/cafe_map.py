import networkx as nx
from networkx.drawing.nx_pydot import write_dot


g = nx.Graph()

tables = ['t1', 't2', 't3', 't4']
CHEF = 'chef'

# add tables:
g.add_nodes_from(tables)

# add chef:
g.add_nodes_from([CHEF])

# add connecting nodes:
g.add_nodes_from(['cross1', 'cross2', 'cross3'])

g.add_edge('chef', 'cross1', color='red')
g.add_edge('cross1', 'cross2')
g.add_edge('cross2', 't3')
g.add_edge('cross2', 't4')

g.add_edge('cross2', 'cross3')
g.add_edge('cross3', 't1')
g.add_edge('cross3', 't2')


if __name__ == '__main__':
    pos = nx.nx_agraph.graphviz_layout(g)
    nx.draw(g, pos=pos)
    write_dot(g, 'generated.dot')
