from networkx import Graph
from typing import Sequence


direction_mapping = {
    'n': 'north',
    'e': 'east',
    'w': 'west',
    's': 'south',
}

def get_adjacency_with_direction(graph: Graph):
    """
    Processes graph that uses port properties and returns list
    """
    unpacked = set()

    for source_node, targets in graph.adjacency():
        for target, edges in targets.items():
            for edge in edges.values():
                unpacked.add((source_node, target, direction_mapping[edge['tailport']]))
                unpacked.add((target, source_node, direction_mapping[edge['headport']]))

    return unpacked
