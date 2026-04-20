from order.order import Order
from order.destination import Destination
from order.item import Item
from order.order_manager import OrderManager


def test_order_initialization():
    order = Order(1, "Kitchen")
    assert order.orderId == 1
    assert order.destination == "Kitchen"
    assert order.status == "WAITING"
    assert order.items == []


def test_order_update_status():
    order = Order(1, "Kitchen")
    order.updateStatus("ASSIGNED")
    assert order.getStatus() == "ASSIGNED"


def test_destination_coordinates():
    dest = Destination(1, "Room A", (3, 5))
    assert dest.getCoords() == (3, 5)


def test_item_properties():
    item = Item(1, 100, "Ice Cream", "SMALL", True, False)
    assert item.isFrozen() is True
    assert item.isFragile() is False
    assert item.getSize() == "SMALL"


def test_order_manager_dispatch_and_complete():
    order1 = Order(1, "Room A")
    manager = OrderManager([order1], [], [])

    assert manager.getNextOrder() == order1

    dispatched = manager.dispatchOrder()
    assert dispatched == order1
    assert order1 in manager.activeOrders
    assert order1 not in manager.pendingOrders
    assert order1.getStatus() == "ASSIGNED"

    manager.markComplete(order1)
    assert order1 in manager.completedOrders
    assert order1 not in manager.activeOrders
    assert order1.getStatus() == "DELIVERED"