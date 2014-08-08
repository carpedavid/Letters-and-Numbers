# Letters and Numbers Engine
#    Copyright (C) 2013  David Garrett
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import collections
import uuid

import actors
import story_engine_data



#Enumerations
class action_type:
    'Enumerated list of action types'

    Line, Choice, Description = range(3)


class action_style:
    'Enumerated list of styles'
    Spoken, Thought, Action, Custom = range(4)


#Classes
class story:
    'The high-level objects that represents an interactive story.'

    def __init__(self):
        self.title = ''
        self.author = ''
        self.cover_image = ''
        self.copyright_statement = ''
        self.chapters = chapters()

    def load(self, file_id):
        s = story_engine_data.story()
        root = s.load(file_id)

        self.title = root.get('title').strip()
        self.author = root.get('author').strip()
        self.cover_image = root.get('cover_image').strip()

        copyright_statement_root = root.find('copyright_statement')
        self.copyright_statement = copyright_statement_root.text.strip()

        chapters_root = root.find('chapters')
        self.chapters.load(chapters_root)

    def save_state(self, u):
        if u == None:
            u = uuid.uuid4()

        story_engine_data.story.save_state(self, u)


class chapters(collections.OrderedDict):
    'Contains the collection of chapters in a story'

    _current_item = 0
    _max_item = 0

    def __init__(self):
        collections.OrderedDict.__init__(self)

    def load(self, root):
        for child in root.findall('./chapter'):
            c = chapter()
            c.id = int(child.get('id'))
            c.file_id = child.get('file_id')
            self[c.id] = c

    def move_next(self):
        self._max_item = len(self.keys())
        self._current_item += 1

    def move_previous(self):
        self._current_item -= 1

    def go_to(self):
        pass

    def reset(self):
        pass


class chapter:
    'Represents an individual chapter in a story.'

    def __init__(self):
        self.id = 0
        self.title = ''
        self.file_id = ''
        self.scenes = None

    def load(self, file_id):
        'Loads the details for the current chapter.'
        self.scenes = scenes()

        c = story_engine_data.chapter()
        root = c.load(file_id)

        self.title = root.get('title').strip()

        scenes_root = root.find('scenes')
        self.scenes.load(scenes_root)

    def unload(self):
        'Unloads the details of the current chapter. Leaves only the basics needed for navigation.'
        self.scenes = None


class scenes(collections.OrderedDict):
    'Contains the collection of scenes in a chapter.'

    _current_item = 0
    _max_item = 0

    def __init__(self):
        collections.OrderedDict.__init__(self)

    def load(self, root):
        for child in root.findall('./scene'):
            s = scene()
            s.id = child.get('id')
            s.file_id = child.get('file_id')
            self[s.id] = s

    def move_next(self):
        self._max_item = len(self.keys())
        self._current_item += 1

    def move_previous(self):
        pass

    def go_to(self):
        pass

    def reset(self):
        pass


class scene():
    'Represents a specific scene.'

    def __init__(self):
        self.intro = ''
        self.intro_image = ''
        self.actors = None
        self.actions = None

    def load(self, file_id):
        s = story_engine_data.scene()
        root = s.load(file_id)

        self.intro_image = root.get('intro_image').strip()
        intro_root = root.find('intro')
        self.intro = intro_root.text.strip()
        self.load_actors(root)
        self.load_actions(root)

    def unload(self):
        self.actors = None
        self.actions = None

    def load_actors(self, root):
        self.actors = actors.actors()
        self.actors.load(root)

    def load_actions(self, root):
        self.actions = actions()
        actions_root = root.find('actions')
        self.actions.load(actions_root)

    def play_scene(self):
        return self.actions[0].render_action(self.actors)

    def move_next(self):
        return self.actions.move_next(self.actors)

    def make_choice(self, action):
        self._current_item = int(action)
        return self[self._current_item].render_action(self.actors)


class actions(collections.OrderedDict):
    'Contains the collection of actions in a scene.'

    _current_item = 0
    _max_item = 0

    def __init__(self):
        collections.OrderedDict.__init__(self)

    def load(self, root):
        for child in root.findall('./action'):
            a = action()
            a.load(child)
            self[a.id] = a

    def move_next(self, actors):
        self._max_item = len(self.keys())
        self._current_item += 1

        if self._current_item >= self._max_item:
            return (None, None)
        else:
            return self[self.keys()[self._current_item]].render_action(actors)

    def move_previous(self, actors):
        self._max_item = len(self.keys())
        self._current_item -= 1

        if self._current_item >= self._max_item:
            return (None, None)
        else:
            return self[self.keys()[self._current_item]].render_action(actors)

    def go_to(self, id, actors):
        self._max_item = len(self.keys())
        self._current_item = id

        if self._current_item >= self._max_item:
            return (None, None)
        else:
            return self[self.keys()[self._current_item]].render_action(actors)

    def reset(self, actors):
        _current_item = 0


class action():
    'Represents the actions of one actor during the scene.'

    def __init__(self):
        self.id = 0
        self.type = ''
        self.style = 0
        self.actor_id = 0
        self.prerequisites = prerequisites()
        self.consequences = consequences()

    def load(self, root):
        self.id = int(root.get('id'))
        self.type = root.get('type')
        self.actor_id = int(root.get('actor'))
        self.element = root
        p_root = root.find('prerequisites')
        self.prerequisites.load(p_root)
        c_root = root.find('consequences')
        self.consequences.load(c_root)

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


class choice():
    'Represents a choice made by an actor.'

    def __init__(self):
        self.id = 0
        self.prompt = ''
        self.style = 0
        self.actor_id = 0
        self.actions = actions()

    def load(self, root):
        for child in root.findall('./action'):
            a = action()
            a.id = int(child.get('id'))
            a.type = child.get('type')
            a.actor_id = int(child.get('actor'))
            a.element = child
            self[a.id] = a


class prerequisites(collections.OrderedDict):
    'A collection of prerequisites.'

    def __init__(self):
        collections.OrderedDict.__init__(self)

    def load(self, root):
        i = 0
        if root != None:
            for child in root.findall('./prerequisite'):
                i += 1
                p = prerequisite()
                p.target = child.get('target')
                p.value = child.get('value')
                p.operator = child.get('operator')
                self[i] = p


class prerequisite():
    'Condition for an action to be a viable choice.'

    def __init__(self):
        self.target = None
        self.value = None
        self.operator = None

    def evaluate(self):
        pass


class consequences(collections.OrderedDict):
    'A collection of consequences.'

    def __init__(self):
        collections.OrderedDict.__init__(self)

    def load(self, root):
        i = 0
        if root != None:
            for child in root.findall('./consequence'):
                i += 1
                c = consequence()
                c.target = child.get('target')
                c.value = child.get('value')
                c.operator = child.get('operator')
                self[i] = c


class consequence():
    'Effect of choosing a specific action.'

    def __init__(self):
        self.target = None
        self.value = None
        self.operator = None

    def apply(self):
        pass

#Exercise the methods in this module
if __name__ == '__main__':

    #story
    print('-------------------------------------------------------------------')
    print('Testing Story')
    print('-------------------------------------------------------------------')
    s = story()
    s.load('story_1.xml')
    print(s.title)
    print(s.author)
    print(s.cover_image)
    print(s.copyright_statement)

    #chapters
    print('-------------------------------------------------------------------')
    print('Testing Chapters')
    print('-------------------------------------------------------------------')
    for k, v in s.chapters.items():
        v.load(v.file_id)
        print v.title
        print 'Loaded ' + str(len(v.scenes.keys())) + ' scenes.'
        for q, r in v.scenes.items():
            r.load(r.file_id)
            print r.intro
            print 'Loaded ' + str(len(r.actions.keys())) + ' actions.'
            for y, z in r.actions.items():
                print(r.actors[z.actor_id].name)
            r.unload()
            if r.actions == None:
                print 'Unloaded actions'
        v.unload()
        if v.scenes == None:
            print 'Unloaded scenes.'
    s.save_state(None)


	