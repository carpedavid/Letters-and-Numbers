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
		
		#combat statistics
		self.speed = 0
		self.strength = 0
		self.intelligence = 0
	
	def import_actor(self, id):
		import xml.etree.ElementTree as ET
		actor_tree = ET.parse('actors_catalogue.xml')
		actor_root = actor_tree.getroot()
		
		actor_node = actor_root.find("./actor[@id='" + str(id) + "']")
		
		self.id = int(id)
		self.name = actor_node.find('name').text
		self.description = actor_node.find('description').text
		
#Exercise the methods in this module
if __name__ == '__main__':
	import xml.etree.ElementTree as ET
	scene_tree = ET.parse('scene_1.xml')
	scene_root = scene_tree.getroot()

	a = actors()
	a.load(scene_root)
	
	print('List of actors:')
	
	for i in a.keys():
		print(a[i].name + ' - ' + a[i].description)