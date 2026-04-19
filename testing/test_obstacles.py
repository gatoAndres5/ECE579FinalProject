import random

from routing.node import Node
from routing.edge import Edge
from obstacle.obstacle import Obstacle
from obstacle.obstacle_detection import ObstacleDetection
from obstacle.obstacle_manager import ObstacleManager
from routing.environment_graph import EnvironmentGraph


def build_simple_graph():
    graph = EnvironmentGraph()

    a = Node(1, "A", 0, 0)
    b = Node(2, "B", 1, 0)
    c = Node(3, "C", 2, 0)

    graph.addNode(a)
    graph.addNode(b)
    graph.addNode(c)

    e1 = Edge(1, 1, a, b, True, "A_B")
    e2 = Edge(2, 1, b, c, True, "B_C")

    graph.addEdge(e1)
    graph.addEdge(e2)

    return graph, a, b, c, e1, e2


def test_obstacle_stores_edge():
    _, _, _, _, e1, _ = build_simple_graph()

    obstacle = Obstacle(1, e1)

    assert obstacle.obstacleID == 1
    assert obstacle.getEdge() == e1


def test_obstacle_manager_adds_obstacle_and_blocks_edge():
    _, _, _, _, e1, _ = build_simple_graph()
    manager = ObstacleManager(spawnRate=0.0)

    manager.addObstacle(1, e1)

    assert len(manager.obstacles) == 1
    assert manager.obstacles[0].obstacleID == 1
    assert manager.obstacles[0].getEdge() == e1
    assert e1.isPassable is False


def test_obstacle_detection_senses_nearby_obstacle():
    _, a, _, _, e1, _ = build_simple_graph()
    manager = ObstacleManager(spawnRate=0.0)
    manager.addObstacle(1, e1)

    detector = ObstacleDetection(manager.obstacles, sensorRange=1)

    detected = detector.sense(a)

    assert len(detected) == 1
    assert detected[0].getEdge() == e1


def test_obstacle_manager_removes_obstacle_and_unblocks_edge():
    _, _, _, _, e1, _ = build_simple_graph()
    manager = ObstacleManager(spawnRate=0.0)
    manager.addObstacle(1, e1)

    manager.removeObstacle(1)

    assert len(manager.obstacles) == 0
    assert e1.isPassable is True


def test_random_obstacle_generation_spawns_when_rate_is_one():
    random.seed(1)

    graph, _, _, _, _, _ = build_simple_graph()
    manager = ObstacleManager(spawnRate=1.0)

    obstacle = manager.maybeSpawn(graph)

    assert obstacle is not None
    assert len(manager.obstacles) == 1
    assert obstacle.getEdge().isPassable is False


def test_random_obstacle_generation_does_not_spawn_when_rate_is_zero():
    random.seed(1)

    graph, _, _, _, _, _ = build_simple_graph()
    manager = ObstacleManager(spawnRate=0.0)

    obstacle = manager.maybeSpawn(graph)

    assert obstacle is None
    assert len(manager.obstacles) == 0