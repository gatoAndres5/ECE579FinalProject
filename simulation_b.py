from bagging.foodie_bagger import Foodie_Bagger
from bagging.item import Item
from order.order import Order
from routing.node import Node

def create_order():
    items = [
        Item(1, "gallon of milk", "large", heavy=True),
        Item(2, "gallon of water", "large", heavy=True),
        Item(3, "frozen pizza", "medium", frozen=True, fragile=True),
        Item(4, "bag of apples", "medium", heavy=True),
        Item(5, "loaf of bread", "medium", fragile=True),
        Item(6, "bag of ice", "large", frozen=True)
    ]
    order = Order(1, "A", items)
    return order

order = create_order()

fw = Node(1, "FW", 0, 0)
bagger = Foodie_Bagger(fw)

print(f"Order: ")
for i in order.getItems():
    print(f"{i.getName()}, size={i.getSize()}, frozen={i.isFrozen()}, fragile={i.isFragile()}, heavy={i.isHeavy()}")


print(f"Bagging simulation:")
bagger.bagOrder(order)