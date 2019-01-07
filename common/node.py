"""
Definition de la classe Node pour modele hierachique
"""

class Node:

	def __init__(self, parent):
         self.parent = parent
		 self.fils = []
		 self.translate = []
		 self.rotate = []

