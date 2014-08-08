import collections

import actors


class action_type:
    'Enumerated list of action types'

    Line, Choice, Description = range(3)


class scene(collections.OrderedDict):
    'Represents a specific scene. Contains a collection of the actions.'

    # properties
    intro = None
    intro_image = None
    actors = None
    _current_action = None
    _max_action = None

    #methods
    def __init__(self):
        collections.OrderedDict.__init__(self)
        self.actors = actors.actors()
        self.intro = ''
        self.intro_image = ''
        self._current_action = 0
        self._max_action = 0

    def load_scene(self, file_name):
        import xml.etree.ElementTree as ET

        scene_tree = ET.parse(file_name)
        scene_root = scene_tree.getroot()

        self.load_actors(scene_root)
        self.load_actions(scene_root)

        self._max_action = len(self.keys())

    def load_actors(self, scene_root):
        self.actors.load(scene_root)

    def load_actions(self, scene_root):
        actions_node = scene_root.find('actions')

        for child in actions_node.findall('./action'):
            a = action()
            a.id = int(child.get('id'))
            a.type = child.get('type')
            a.actor_id = int(child.get('actor'))
            a.element = child
            self[a.id] = a

        self._current_action = 0

    def play_scene(self):
        return self[self.keys()[self._current_action]].render_action(self.actors)

    def move_next(self):
        self._current_action += 1
        if self._current_action >= self._max_action:
            return (None, None)
        else:
            return self[self.keys()[self._current_action]].render_action(self.actors)

    def make_choice(self, action):
        self._current_action = int(action)
        return self[self._current_action].render_action(self.actors)


class action():
    'Represents the actions of one actor during the scene.'

    def __init__(self):
        self.id = 0
        self.type = ''
        self.actor_id = 0

    def render_action(self, a):
        if self.type == 'line':
            return (self.render_line(a), action_type.Line)
        elif self.type == 'choice':
            return (self.render_choice(a), action_type.Choice)

    def render_line(self, a):
        return_string = a.get(self.actor_id).name + ': '
        return_string += self.element.text + '\n'

        return return_string

    def render_choice(self, a):
        action_root = self.element
        return_string = a.get(self.actor_id).name + '\n'
        for child in action_root.findall('action'):
            return_string += child.get('target') + ': ' + child.text + '\n'

        return return_string

# Exercise the methods in this module
if __name__ == '__main__':
    s = scene()
    s.load_scene('scene_1.xml')
    print(s.play_scene()[0])
    print(s.move_next()[0])
    print(s.move_next()[0])
    print(s.move_next()[0])
    print(s.move_next()[0])

