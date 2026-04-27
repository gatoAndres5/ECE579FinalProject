import pytest

from robot.robot import Robot
from bagging.bag import Bag
from bagging.item import Item
from robot.fleet_manager import Fleet_Manager
from order.order import Order
from routing.node import Node
from routing.edge import Edge
from routing.environment_graph import EnvironmentGraph
from bagging.foodie_bagger import Foodie_Bagger
from routing.path_planner import PathPlanner
from obstacle.obstacle import Obstacle

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

    e5 = Edge(5, 1, a, fw, True)
    e6 = Edge(6, 1, b, a, True)
    e7 = Edge(7, 2, c, fw, True)
    e8 = Edge(8, 1, b, c, True)

    edges = [e1, e2, e3, e4, e5, e6, e7, e8]

    for edge in edges:
        graph.addEdge(edge)

    return graph, nodes, edges

def build_graph2():
    graph = EnvironmentGraph()

    # Nodes
    fw = Node(1, "FW", 0, 0)
    a = Node(2, "A", 1, 0)
    b = Node(3, "B", 2, 0)

    nodes = [fw, a, b]

    for node in nodes:
        graph.addNode(node)

    # Edges (directed)
    e1 = Edge(1, 1, fw, a, True)
    e2 = Edge(2, 1, a, b, True)

    e3 = Edge(3, 1, a, fw, True)
    e4 = Edge(4, 1, b, a, True)

    e5 = Edge(5, 10, fw, b, True)
    e6 = Edge(6, 10, b, fw, True)

    edges = [e1, e2, e3, e4, e5, e6]

    for edge in edges:
        graph.addEdge(edge)

    return graph, nodes, edges

def test_fleet_manager_init():
    eg, n, e = build_graph()
    fw = n[0]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)
    assert len(fm.robots) == 0
    assert fm.eg == eg

def test_add_robot():
    eg, n, e = build_graph()
    fw = n[0]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)
    fm.addRobot()
    fm.addRobot()
    assert len(fm.robots) == 2
    assert fm.robots[0].getID() == 0
    assert fm.robots[1].getID() == 1
    for robot in fm.robots:
        assert robot.getBattery() == 100 # fully charged
        assert robot.getStatus() == "ready"
        assert robot.getPosition() == fw
    assert fm.hasAvailableRobot() == True

def test_assign_order():
    eg, n, e = build_graph()
    b = n[2]
    fw = n[0]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)
    fm.addRobot()
    fm.addRobot()

    items = [
        Item(1, "fragile item", "small", fragile=True),
        Item(2, "heavy item", "large")
    ]
    order = Order(1, b, items)
    bagger = Foodie_Bagger(fw)
    bags = bagger.bagOrder(order)
    assert bags is not None

    assigned_robot = fm.dispatchOrder(order, bags)
    assert assigned_robot.getID() == 0
    assert fm.robots[0].getCurrentOrder() == order
    assert fm.robots[0].getStatus() == "busy"
    assert fm.robots[1].getStatus() == "ready"
    assert fm.robots[0].completeOrder() == None # not yet at destination

def test_all_assigned():
    eg, n, e = build_graph()
    fw = n[0]
    a = n[1]
    b = n[2]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)
    fm.addRobot()
    fm.addRobot()
    items1 = [
        Item(1, "fragile item", "small", fragile=True),
        Item(2, "heavy item", "large")
    ]
    items2 = [
        Item(1, "fragile item", "small", fragile=True),
        Item(2, "heavy item", "large")
    ]
    order1 = Order(1, a, items1)
    order2 = Order(2, b, items2)

    bagger = Foodie_Bagger(fw)
    bags1 = bagger.bagOrder(order1)
    bags2 = bagger.bagOrder(order2)
    assert bags1 is not None
    assert bags2 is not None

    fm.dispatchOrder(order1, bags1)
    fm.dispatchOrder(order2, bags2)

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
    assert fm.dispatchOrder(order3, None) == None

# Robot 

def test_robot_init():
    eg, n, e = build_graph()
    fw = n[0]
    a = n[1]
    b = n[2]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)

    r = Robot(fm, 10324, fw, eg, true_obstacles)
    assert r.getCurrentOrder() == None
    assert r.getPosition() == fw
    assert len(r.bags) == 0
    assert r.status == "ready"

def test_grasper():
    eg, n, e = build_graph()
    fw = n[0]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)
    r = Robot(fm, 0, fw, eg, true_obstacles)
    assert r.grasper.isOpen()
    r.grasper.openGrasper()
    assert r.grasper.isOpen()
    r.grasper.closeGrasper()
    assert not r.grasper.isOpen()
    assert not r.grasper.getItemHeld()

# Movement

def test_move():
    eg, n, e = build_graph()
    fw = n[0]
    a = n[1]
    b = n[2]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)

    items1 = [
        Item(1, "fragile item", "small", fragile=True),
        Item(2, "heavy item", "large")
    ]
    order = Order(1, a, items1)
    bagger = Foodie_Bagger(fw)
    bags1 = bagger.bagOrder(order)
    assert bags1 is not None

    robot = Robot(fm, 1, fw, eg, true_obstacles)
    fm.addRobot(robot)
    fm.dispatchOrder(order, bags1)
    assert robot.getCurrentOrder() == order
    assert len(robot.bags) == 2
    assert robot.getBattery() == 100
    assert pathplanner.calculatePathCost([fw, a]) == 1

    assert robot.getPosition() == fw
    assert robot.movementController.setDestination(a)
    assert robot.movementController.getDestination() == a
    assert robot.getPosition() == fw

    #robot.status = 'busy' # manually set to busy since testing w/o an order
    assert robot.getStatus() == 'busy'
    assert len(robot.bags) == 2

    robot.tick()
    assert robot.getPosition() == a
    assert robot.movementController.getDestination() == fw
    assert robot.getBattery() == 99
    assert len(robot.bags) == 0

    robot.tick() # move back to FW
    print(f"Pos: {robot.position.name}")
    assert robot.getPosition() == fw
    assert robot.getBattery() == 98

    robot.tick()
    assert robot.status == 'ready'

def test_bag_space():
    eg, n, e = build_graph()
    fw = n[0]
    a = n[1]
    b = n[2]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)

    items1 = [
        Item(1, "fragile item", "small", fragile=True),
        Item(2, "heavy item", "large")
    ]
    order = Order(1, a, items1)
    bagger = Foodie_Bagger(fw)
    bags1 = bagger.bagOrder(order)
    assert bags1 is not None

    robot = Robot(fm, 1, fw, eg, true_obstacles)
    fm.addRobot(robot)
    robot.bags = [None, None, None, None, None, None]
    # no space; cannot assign
    assert fm.dispatchOrder(order, bags1) is None

    robot2 = Robot(fm, 2, fw, eg, true_obstacles)
    fm.addRobot(robot2)
    assert fm.dispatchOrder(order, bags1) == robot2

def test_battery_empty():
    eg, n, e = build_graph()
    fw = n[0]
    a = n[1]
    b = n[2]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)

    items1 = [
        Item(1, "fragile item", "small", fragile=True),
        Item(2, "heavy item", "large")
    ]
    order = Order(1, a, items1)
    bagger = Foodie_Bagger(fw)
    bags1 = bagger.bagOrder(order)
    assert bags1 is not None

    robot = Robot(fm, 1, fw, eg, true_obstacles)
    fm.addRobot(robot)
    robot.battery = 1
    assert fm.dispatchOrder(order, bags1) is None
    # cannot dispatch; battery too low

    robot2 = Robot(fm, 2, fw, eg, true_obstacles)
    fm.addRobot(robot2)
    assert fm.dispatchOrder(order, bags1) == robot2

def test_charging():
    eg, n, e = build_graph()
    fw = n[0]
    a = n[1]
    b = n[2]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)
    robot = Robot(fm, 1, fw, eg, true_obstacles)
    robot.battery = 90
    robot.status = "charging"

    robot.tick()
    assert robot.getBattery() == 95

    robot.tick()
    assert robot.getBattery() >= 100
    assert robot.getStatus() == "ready"

def dead():
    eg, n, e = build_graph()
    fw = n[0]
    a = n[1]
    b = n[2]
    true_obstacles = None
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)

    items1 = [
        Item(1, "fragile item", "small", fragile=True),
        Item(2, "heavy item", "large")
    ]
    order = Order(1, a, items1)
    bagger = Foodie_Bagger(fw)
    bags1 = bagger.bagOrder(order)
    assert bags1 is not None

    robot = Robot(fm, 1, fw, eg, true_obstacles)
    fm.addRobot(robot)
    fm.dispatchOrder(order, bags1)
    assert robot.getCurrentOrder() == order
    assert robot.getBattery() == 100
    assert fm.calculatePathCost([fw, a]) == 1

    assert robot.getPosition() == fw
    assert robot.movementController.setDestination(a)
    assert robot.movementController.getDestination() == a
    assert robot.getPosition() == fw

    assert robot.getStatus() == 'busy'

    robot.tick()
    assert robot.getPosition() == a
    assert robot.movementController.getDestination() == fw
    assert robot.getBattery() == 99

    robot.battery = 0
    robot.tick()
    assert robot.getStatus() == "dead"
    assert robot.getPosition() == a

# in main simulation loop, all robots should call tick() to synchronize in time

def test_multiple_orders():
    # 1. Setup the World
    eg, n, e = build_graph2()
    fw = n[0]
    a = n[1]  # distance FW -> A is 1
    b = n[2]  # distance A -> B is 1, but FW -> B is 10
    
    true_obstacles = None 
    pathplanner = PathPlanner(eg)
    fm = Fleet_Manager(fw, eg, true_obstacles, pathplanner)

    items_A = [Item(1, "apple", "small")]
    items_B = [Item(2, "heavy box", "large")]
    
    order_A = Order(1, a, items_A)
    order_B = Order(2, b, items_B)
    
    bagger = Foodie_Bagger(fw)
    bags_A = bagger.bagOrder(order_A)
    bags_B = bagger.bagOrder(order_B)

    robot = Robot(fm, 1, fw, eg, true_obstacles)
    fm.addRobot(robot)

    for bag in bags_A + bags_B:
        robot.addBag(bag, fw)
        
    assert len(robot.bags) == len(bags_A) + len(bags_B)
    robot.status = 'busy' 

    # A should be targeted first, since B is further
    robot.movementController.setItinerary([order_B, order_A])
    assert robot.movementController.currentTargetOrder == order_A
    assert robot.movementController.activeItinerary == [order_B]

    robot.tick()
    assert robot.getPosition() == a
    # should have unloaded order A's bags
    assert len(robot.bags) == len(bags_B)
    assert all(bag in robot.bags for bag in bags_B)
    assert all(bag not in robot.bags for bag in bags_A)
    assert robot.movementController.currentTargetOrder == order_B

   
    robot.tick()
    assert robot.getPosition() == b
    assert len(robot.bags) == 0
    # itinerary should be empty, triggering the return trip
    assert robot.movementController.currentTargetOrder is None
    assert robot.movementController.destinationNode == fw

    robot.tick()
    # move to A, shorter path
    assert robot.getPosition() == a
    assert robot.getBattery() < 100 

    robot.tick()
    assert robot.getPosition() == fw
    
    assert robot.status in ['ready', 'charging']

