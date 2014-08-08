import actors


class combat():
    'Represents an instance of combat between two or more actors.'

    def __init__(self):
        self.actors = actors.actors()

    def load_combat(self, file_name):
        import xml.etree.ElementTree as ET

        combat_tree = ET.parse(file_name)
        combat_root = combat_tree.getroot()

        self.load_actors(combat_root)

    def load_actors(self, combat_root):
        self.actors.load(combat_root)


class turn():
    'Represents a unit of combat.'
    pass

# Exercise the methods in this module
if __name__ == '__main__':
    c = combat()
    c.load_combat('combat_1.xml')

    for i in c.actors.keys():
        print(c.actors[i].name)