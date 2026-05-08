from bagging.foodie_bagger import Foodie_Bagger
from bagging.item import Item
from order.order import Order
from routing.node import Node

def create_order():
    items = [
        Item(1, "pint of milk", "medium", frozen=True),
        Item(2, "gallon of water", "large", heavy=True),
        Item(3, "frozen pizza", "medium", frozen=True, fragile=True),
        Item(4, "bag of apples", "medium", heavy=True),
        Item(5, "loaf of bread", "small", fragile=True),
        Item(6, "bag of ice", "large", frozen=True, heavy=True)
    ]
    order = Order(1, "A", items)
    return order

order = create_order()

fw = Node(1, "FW", 0, 0)
bagger = Foodie_Bagger(fw)

print(f"Order: ")
for i in order.getItems():
    print(
    f"{i.getName():<20}  "
    f"size: {str(i.getSize()):<6}  "
    f"frozen: {str(i.isFrozen()):<5}  "
    f"fragile: {str(i.isFragile()):<5}  "
    f"heavy: {str(i.isHeavy()):<6}"
)

print(f"\nBagging simulation:")
bagger.bagOrder(order)