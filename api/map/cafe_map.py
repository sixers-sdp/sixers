import os

from networkx.drawing.nx_pydot import read_dot
from map import utils


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
current_map = read_dot(os.path.join(BASE_DIR, "dot_map.dot"))

tables = [n for n in current_map.nodes if n.lower().startswith('t')]
CHEF = 'chef'

adjacency = utils.get_adjacency_with_direction(current_map)