import pytest

from routing.Node import Node
from routing.Edge import Edge
from routing.EnvironmentGraph import EnvironmentGraph
from routing.PathPlanner import PathPlanner


def build_graph():
    graph = EnvironmentGraph()

    # Nodes
    fw = Node(1, "FW", 0, 0)
    a = Node(2, "A", 1, 0)
    b = Node(3, "B", 2, 0)
    c = Node(4, "C", 1, 1)

    for node in [fw, a, b, c]:
        graph.addNode(node)

    # Edges (directed)
    e1 = Edge(1, 1, fw, a, True)
    e2 = Edge(2, 1, a, b, True)
    e3 = Edge(3, 2, fw, c, True)
    e4 = Edge(4, 1, c, b, True)

    for edge in [e1, e2, e3, e4]:
        graph.addEdge(edge)

    return graph, fw, a, b, c, e2


def extract_names(path):
    return [node.name for node in path]


# Test 1: normal shortest path
def test_path_planner_basic():
    graph, fw, a, b, c, _ = build_graph()
    planner = PathPlanner(graph)

    path = planner.calculate_path(fw, b)

    names = extract_names(path)

    assert names == ["FW", "A", "B"]


# Test 2: obstacle forces replanning
def test_path_planner_with_obstacle():
    graph, fw, a, b, c, edge_ab = build_graph()
    planner = PathPlanner(graph)

    # Block A -> B
    edge_ab.setPassibility(False)

    path = planner.calculate_path(fw, b)

    names = extract_names(path)

    assert names == ["FW", "C", "B"]