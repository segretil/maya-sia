"""
Definition de la classe Node pour modele hierachique
"""

class Node:

	def __init__(self, parent = None):
         self.parent = parent
		 self.fils = []
		 self.translate = []
		 self.rotate = []

	@staticmethod
    def createStructureFromBVH(file_name):
        with open(file_name) as file: # Use file to refer to the file object
			data = file.read()
