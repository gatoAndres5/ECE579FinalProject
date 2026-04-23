import pytest

from robot.robot import Robot
from bagging.bag import Bag
from robot.fleet_manager import Fleet_Manager
from order.order import Order

def test_fleet_manager_init():
    fm = Fleet_Manager()
    assert len(fm.robots) == 0

def test_add_robot():
    fm = Fleet_Manager()
    fm.addRobot()
    fm.addRobot()
    assert len(fm.robots) == 2
    assert fm.robots[0].getID() == 0
    assert fm.robots[1].getID() == 1
    for robot in fm.robots:
        assert robot.getStatus() == "ready"
    assert fm.hasAvailableRobot() == True

def test_assign_order():
    fm = Fleet_Manager()
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
    fm = Fleet_Manager()
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

def test_grasper():
    r = Robot(0)
    assert r.grasper.isOpen()
    r.grasper.openGrasper()
    assert r.grasper.isOpen()
    r.grasper.closeGrasper()
    assert not r.grasper.isOpen()
    assert not r.grasper.getItemHeld()
