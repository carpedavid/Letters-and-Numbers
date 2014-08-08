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

#    This data access module contains rudimentary file support.
#    All files must be in the same directory.
#    Edit the following line to change the directory

data_directory = 'data'


class Actor():
    def __init__(self):
        pass

    def load(self, actor_id):
        import xml.etree.ElementTree as Et

        tree = Et.parse(data_directory + '/actors_catalogue.xml')
        root = tree.getroot()

        actor_node = root.find("./actor[@id='" + str(actor_id) + "']")

        return actor_node