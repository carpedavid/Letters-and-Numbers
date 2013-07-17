#This data access module contains rudimentary file support.
#All files must be in the same directory.
class story():
	def load(self, file_name):
		import xml.etree.ElementTree as ET
		tree = ET.parse(file_name)
		root = tree.getroot()
		return root

class chapter():
	def load(self, file_name):
		import xml.etree.ElementTree as ET
		tree = ET.parse(file_name)
		root = tree.getroot()
		return root

class scene():
	def load(self, file_name):
		import xml.etree.ElementTree as ET
		tree = ET.parse(file_name)
		root = tree.getroot()
		return root