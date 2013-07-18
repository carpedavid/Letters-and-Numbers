#    Letters and Numbers Engine
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
import actors
import story_engine_data

#Enumerations
class action_type:
	'Enumerated list of action types'
	
	Line, Choice, Description = range(3) 


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
		for child in chapters_root.findall('./chapter'):
			c = chapter()
			c.id = int(child.get('id'))
			c.file_id = child.get('file_id')
			self.chapters[c.id] = c

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
		for child in scenes_root.findall('./scene'):
			s = scene()
			s.id = child.get('id')
			s.file_id = child.get('file_id')
			self.scenes[s.id] = s

	def unload(self):
		'Unloads the details of the current chapter. Leaves only the basics needed for navigation.'
		self.scenes = None

class chapters(collections.OrderedDict):
	'Contains the collection of chapters in a story'

	_current_item = 0
	_max_item = 0

	def __init__(self):
		collections.OrderedDict.__init__(self)

	def move_next(self):
		self._max_item = len(self.keys())
		self._current_item += 1
		
	def move_previous(self):
		self._current_item -= 1
	
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
		actions_node = root.find('actions')
		
		for child in actions_node.findall('./action'):
			a = action()
			a.id = int(child.get('id'))
			a.type = child.get('type')
			a.actor_id = int(child.get('actor'))
			a.element = child
			self.actions[a.id] = a
	
	def play_scene(self):
		return self.actions[0].render_action(self.actors)
				
	def move_next(self):
		return self.actions.move_next(self.actors)
		
	def make_choice(self, action):
		self._current_item = int(action)
		return self[self._current_item].render_action(self.actors)

class scenes(collections.OrderedDict):
	'Contains the collection of scenes in a chapter.'
	
	_current_item = 0
	_max_item = 0

	def __init__(self):
		collections.OrderedDict.__init__(self)

	def move_next(self):
		self._max_item = len(self.keys())
		self._current_item += 1
		
	def move_previous(self):
		pass
	
	def go_to(self):
		pass
		
	def reset(self):
		pass

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

class actions(collections.OrderedDict):
	'Contains the collection of actions in a scene.'
	
	_current_item = 0
	_max_item = 0

	def __init__(self):
		collections.OrderedDict.__init__(self)

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

#Exercise the methods in this module
if __name__ == '__main__':

	#actors
	#import xml.etree.ElementTree as ET
	#scene_tree = ET.parse('scene_1.xml')
	#scene_root = scene_tree.getroot()

	#a = actors()
	#a.load(scene_root)
	
	#print('List of actors:')
	
	#for i in a.keys():
		#print(a[i].name + ' - ' + a[i].description)

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
	for k,v in s.chapters.items():
		v.load(v.file_id)
		print v.title
		print 'Loaded ' + str(len(v.scenes.keys())) + ' scenes.'
		for q,r in v.scenes.items():
			r.load(r.file_id)
			print r.intro
			print 'Loaded ' + str(len(r.actions.keys())) + ' actions.'
			for y, z in r.actions.items():
				print(z.id)
			r.unload()
			if r.actions == None:
				print 'Unloaded actions'
		v.unload()
		if v.scenes == None:
			print 'Unloaded scenes.'


	