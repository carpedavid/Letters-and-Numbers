import collections


class inventory_limit_errors:
    'Enumerated list of errors encountered when adding items to the inventory'

    WeightLimit, ItemLimit = range(2)


class inventory(dict):
    'Represents the inventory for an individual actor.'

    def __init__(self):
        self.item_limit = 0
        self.weight_limit = 0

    def get_item(self, key):
        if key in self:
            return self[key]
        else:
            return None

    def add_item(self, item):
        if self.get_total_weight() + (item.weight * item.quantity) <= self.weight_limit:
            if len(self) < self.item_limit:
                self[item.id] = item
                return None
            else:
                return inventory_limit_errors.ItemLimit
        else:
            return inventory_limit_errors.WeightLimit

    def drop_item(self, item):
        if item.id in self:
            del self[item.id]
            return True
        else:
            return False

    def get_total_weight(self):
        total_weight = 0
        for i in self.keys():
            total_weight += (self[i].weight * self[i].quantity)
        return total_weight


class item():
    'Represents an in-game item.'

    def __init__(self):
        self.id = 0
        self.name = ''
        self.weight = 0
        self.description = ''
        self.quantity = 0

    def load(self, id):
        import xml.etree.ElementTree as ET

        item_tree = ET.parse(file_name)
        item_root = item_tree.getroot()

        node = item_root.find("./item[@id='" + str(self.id) + "']")

        self.id = id
        self.name = item_node.find('name').text
        self.weight = int(item_node.find('weight').text)
        self.description = item_node.find('description').text


class weapon(item):
    'Allows an actor to attack.'

    def __init__(self):
        self.attack = 0
        self.damage = 0


class armor(item):
    'Protects an actor from an attack.'

    def __init__(self):
        self.defense = 0

# Exercise the methods in this module
if __name__ == '__main__':
    current_inventory = inventory()
    current_inventory.weight_limit = 30
    current_inventory.item_limit = 3

    new_item = weapon()
    new_item.id = 1
    new_item.name = 'Spear'
    new_item.weight = 10
    new_item.description = 'A sharp, pointy stick.'
    new_item.quantity = 2

    result = current_inventory.add_item(new_item)
    if result is None:
        print('Added ' + new_item.name)
    elif result is inventory_limit_errors.ItemLimit:
        print('Inventory full. Too many items.')
    else:
        print('Inventory full. Too heavy.')

    new_item = weapon()
    new_item.id = 2
    new_item.name = 'Better Spear'
    new_item.weight = 10
    new_item.description = 'A sharper, pointier stick.'
    new_item.quantity = 1

    result = current_inventory.add_item(new_item)
    if result is None:
        print('Added ' + new_item.name)
    elif result is inventory_limit_errors.ItemLimit:
        print('Inventory full. Too many items.')
    else:
        print('Inventory full. Too heavy.')

    new_item = weapon()
    new_item.id = 3
    new_item.name = 'Best Spear'
    new_item.weight = 10
    new_item.description = 'The sharpest, pointiest stick.'
    new_item.quantity = 1

    result = current_inventory.add_item(new_item)
    if result is None:
        print('Added ' + new_item.name)
    elif result is inventory_limit_errors.ItemLimit:
        print('Inventory full. Too many items.')
    else:
        print('Inventory full. Too heavy.')

    for i in current_inventory.keys():
        current_item = current_inventory.get_item(current_inventory[i].id)
        print('Got ' + current_item.name)

    print('Inventory List:')
    for i in current_inventory.keys():
        print(current_inventory[i].name + ' - ' + current_inventory[i].description + ' x' + str(
            current_inventory[i].quantity))

    print('Total weight:' + str(current_inventory.get_total_weight()))

    for i in current_inventory.keys():
        old_item = current_inventory[i]
        current_inventory.drop_item(old_item)
        print('Dropped ' + old_item.name)

    print('Total weight:' + str(current_inventory.get_total_weight()))
