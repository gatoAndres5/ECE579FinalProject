import pytest

from robot.robot import Robot
from bagging.bag import Bag
from robot.fleet_manager import Fleet_Manager
from order.order import Order
from routing.node import Node

# Fleet Manager 

def test_fleet_manager_init():
    fw = Node(1, "FW", 0, 0)
    fm = Fleet_Manager(fw)
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
    fm = Fleet_Manager(fw)
    fm.addRobot()
    fm.addRobot()
    order1 = Order(1, "123 Main St")
    order2 = Order(2, "456 Elm St")
    fm.assignOrder(order1)
    fm.assignOrder(order2)
    assert fm.robots[0].getStatus() == "busy"
    assert fm.robots[1].getStatus() == "busy"
    assert fm.robots[0].getCurrentOrder() == order1
    assert fm.robots[1].getCurrentOrder() == order2
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

