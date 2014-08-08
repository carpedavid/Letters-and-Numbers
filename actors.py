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

import actors_data

class actors(dict):
	'Contains all of the actors in a scene or in combat.'
		
	def load(self, root):
		actors_nodes = root.find('actors')

		for child in actors_nodes.iter('actor'):
			a = actor()
			a.import_actor(child.get('id'))
			self[a.id] = a
	
class actor():
	'Represents one of the actors.'
	
	def __init__(self):
		self.id = 0
		self.name = ''
		self.description = ''
		self.image = ''
		
		#combat statistics
		self.speed = 0
		self.strength = 0
		self.intelligence = 0
	
	def import_actor(self, id):
		a = actors_data.actor()

		actor_node = a.load(id)
		
		self.id = int(id)
		self.name = actor_node.find('name').text
		self.description = actor_node.find('description').text
		
		if actor_node.find('image') != None:
			self.image = actor_node.find('image').text
		
#Exercise the methods in this module
if __name__ == '__main__':
	pass