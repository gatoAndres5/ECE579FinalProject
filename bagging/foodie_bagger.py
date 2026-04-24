from bagging.bag import Bag

class Foodie_Bagger:
    def __init__(self):
        self.bags = []
        self.next_bag_id = 1

    def bagOrder(self, order_items):
        self.bags = [] # clear order
        large_items = [i for i in order_items if i.getSize() == 'large']
        medium_items = [i for i in order_items if i.getSize() == 'medium']
        small_items = [i for i in order_items if i.getSize() == 'small']

        if large_items:
            print("Rule R_large says: Bag large items.")
            for item in large_items:
                self.bagItem(item)
        if medium_items:
            print("Rule R_medium says: Bag medium items.")
            for item in medium_items:
                self.bagItem(item)
        if small_items:
            print("Rule R_small says: Bag small items.")
            for item in small_items:
                self.bagItem(item)

        print("Order bags: ")
        for b in range(len(self.bags)):
            print(f"Bag {b}: ")
            for i in self.bags[b].getItems():
                print(f"{i.getName()}")
        return self.bags;

    def bagItem(self, item):
        if item.isFrozen():
            print(f"Rule R_freezer says: Put {item.name} in a freezer bag.")
        if item.isFragile():
            print(f"Rule R_fragile says: {item.name} is fragile, do not mix with heavy items.")

        target_bag = self.findBag(item)
        target_bag.addItem(item)
        print(f"Rule R_add says: Put {item.name} in {target_bag.bagID}.")

    def findBag(self, item):
        # try to find an existing bag
        for bag in self.bags:
            if bag.can_fit(item):
                return bag
        
        print(f"Rule R_new says: Start a new bag.")
        bag_type = "freezer" if item.isFrozen() else "paper"
        new_bag = Bag(f"bag_{self.next_bag_id}", "FW", bagType=bag_type)
        self.bags.append(new_bag)
        self.next_bag_id += 1
        return new_bag
