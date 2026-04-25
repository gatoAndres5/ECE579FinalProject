import pytest

from robot.robot import Robot
from bagging.bag import Bag
from robot.fleet_manager import Fleet_Manager
from order.order import Order
from routing.node import Node
from routing.edge import Edge
from routing.environment_graph import EnvironmentGraph

# Fleet Manager 

def build_graph():
    graph = EnvironmentGraph()

    # Nodes
    fw = Node(1, "FW", 0, 0)
    a = Node(2, "A", 1, 0)
    b = Node(3, "B", 2, 0)
    c = Node(4, "C", 1, 1)

    nodes = [fw, a, b, c]

    for node in nodes:
        graph.addNode(node)

    # Edges (directed)
    e1 = Edge(1, 1, fw, a, True)
    e2 = Edge(2, 1, a, b, True)
    e3 = Edge(3, 2, fw, c, True)
    e4 = Edge(4, 1, c, b, True)

    edges = [e1, e2, e3, e4]

    for edge in edges:
        graph.addEdge(edge)

    return graph, nodes, edges

def test_fleet_manager_init():
    eg, n, e = build_graph()
    fw = n[0]
    fm = Fleet_Manager(fw, eg, )
    assert len(fm.robots) == 0

def test_add_robot():
    fw = Node(1, "FW", 0, 0)
    fm = Fleet_Manager(fw)
    fm.addRobot()
    fm.addRobot()
    assert len(fm.robots) == 2
    assert fm.robots[0].getID() == 0
    assert fm.robots[1].getID() == 1
    for robot in fm.robots:
        assert robot.getStatus() == "ready"
    assert fm.hasAvailableRobot() == True

def test_assign_order():
    fw = Node(1, "FW", 0, 0)
    fm = Fleet_Manager(fw)
    fm.addRobot()
    fm.addRobot()
    order = Order(1, "123 Main St")
    assigned_robot_id = fm.assignOrder(order)
    assert assigned_robot_id == 0
    assert fm.robots[0].getCurrentOrder() == order
    assert fm.robots[0].getStatus() == "busy"
    assert fm.robots[1].getStatus() == "ready"
    assert fm.robots[0].completeOrder() == None # not yet at destination

def test_all_assigned():
    fw = Node(1, "FW", 0, 0)
    a = Node(2, "123 Main St", 20, 10);
    b = Node(3, "456 Elm St", 10, 20);
    fm = Fleet_Manager(fw)
    fm.addRobot()
    fm.addRobot()
    order1 = Order(1, a)
    order2 = Order(2, b)
    fm.assignOrder(order1)
    fm.assignOrder(order2)

    assert fm.robots[0].getStatus() == "busy"
    o1 = fm.robots[0].getCurrentOrder()
    assert o1 == order1
    assert o1.getDestination() == a

    assert fm.robots[1].getStatus() == "busy"
    o2 = fm.robots[1].getCurrentOrder();
    assert o2 == order2
    assert o2.getDestination() == b

    assert fm.hasAvailableRobot() == False
    order3 = Order(3, "789 Oak St")
    assert fm.assignOrder(order3) == None

# Robot 

def test_robot_init():
    fw = Node(1, "FW", 0, 0)
    r = Robot(10324, fw)
    assert r.getCurrentOrder() == None;
    assert r.getLocation() == fw
    assert len(r.bags) == 0
    assert r.status == "ready"

def test_grasper():
    fw = Node(1, "FW", 0, 0)
    r = Robot(0, fw)
    assert r.grasper.isOpen()
    r.grasper.openGrasper()
    assert r.grasper.isOpen()
    r.grasper.closeGrasper()
    assert not r.grasper.isOpen()
    assert not r.grasper.getItemHeld()

def test():
    assert 0 == "TODO call foodie_bagger.fufillorder"


# test robot movement; leave simulation for now
# create fleetmanager, robots, give them destinations
# test their movement
# and grasper