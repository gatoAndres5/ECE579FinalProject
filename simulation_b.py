from bagging.foodie_bagger import Foodie_Bagger
from bagging.item import Item
from order.order import Order
from routing.node import Node

def create_order():
    items = [
        Item(1, "gallon water", "large"),
        Item(2, "gallon water", "large"),
        Item(3, "pint of ice cream", "small", frozen=True),
        Item(4, "granola box", "medium"),
        Item(5, "loaf of bread", "medium", fragile=True)
    ]
    order = Order(1, "A", items)
    return order

order = create_order()

fw = Node(1, "FW", 0, 0)
bagger = Foodie_Bagger(fw)

print(f"Order: ")
for i in order.getItems():
    print(f"{i.getName()}")


print(f"Bagging simulation:")
bagger.bagOrder(order)