import pytest

from bagging.item import Item
from bagging.bag import Bag
from bagging.foodie_bagger import Foodie_Bagger
from routing.node import Node
from order.order import Order

def create_order():
    items = [
        Item(1, "1-gallon water", "large"),
        Item(2, "1-gallon water", "large"),
        Item(3, "pint of ice cream", "small", frozen=True),
        Item(4, "granola box", "medium"),
        Item(5, "loaf of bread", "medium", fragile=True)
    ]
    order = Order(1, "A", items)
    return order

def test_bagging():
    fw = Node(1, "FW", 0, 0)
    bagger = Foodie_Bagger(fw)
    order = create_order()
    bagger.bagOrder(order)

    assert len(bagger.bags) == 3
    assert bagger.bags[0].bagType == "paper"
    assert bagger.bags[1].bagType == "paper"
    assert bagger.bags[2].bagType == "freezer"

def test_location():
    fw = Node(1, "FW", 0, 0)
    bagger = Foodie_Bagger(fw)
    order = create_order()
    bagger.bagOrder(order)

    assert len(bagger.bags) == 3
    # start at FW, match node
    assert bagger.bags[0].getLocation() == fw;
    assert bagger.bags[1].getLocation() == fw;
    assert bagger.bags[2].getLocation() == fw;
    
def test_empty_order():
    fw = Node(1, "FW", 0, 0)
    bagger = Foodie_Bagger(fw)
    bagger.bagOrder(None)
    assert len(bagger.bags) == 0

def test_capacity_limit():
    items = [
        Item(1, "test item", "large"),
        Item(2, "test item", "large"),  
        Item(3, "test item", "large"),
    ]
    order = Order(1, "A", items)
    # should have: bag 0 [large, large], bag 1 [large]
    fw = Node(1, "FW", 0, 0)
    bagger = Foodie_Bagger(fw)
    bagger.bagOrder(order)
    assert len(bagger.bags) == 2
    assert len(bagger.bags[0].items) == 2
    assert bagger.bags[0].current_weight == 10
    assert len(bagger.bags[1].items) == 1
    assert bagger.bags[1].current_weight == 5

def test_fragile_and_heavy():
    items = [
        Item(1, "fragile item", "small", fragile=True),
        Item(2, "heavy item", "large")
    ]
    order = Order(1, "A", items)
    fw = Node(1, "FW", 0, 0)
    bagger = Foodie_Bagger(fw)
    bagger.bagOrder(order)
    assert len(bagger.bags) == 2
    assert len(bagger.bags[0].items) == 1
    assert len(bagger.bags[1].items) == 1

def test_freezer():
    items = [
        Item(1, "ice cream", "small", frozen=True),
        Item(2, "popsicles", "small", frozen=True),
        Item(3, "frozen peas", "small", frozen=True)
    ]
    order = Order(1, "A", items)
    fw = Node(1, "FW", 0, 0)
    bagger = Foodie_Bagger(fw)
    bagger.bagOrder(order)
    # small items should all be in one freezer bag
    assert len(bagger.bags) == 1
    assert bagger.bags[0].bagType == "freezer"
    assert len(bagger.bags[0].items) == 3