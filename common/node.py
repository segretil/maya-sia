"""
Definition de la classe Node pour modele hierachique
"""

class Node:

	def __init__(self, name, parent = None):
		self.parent = parent
		self.name = name
		self.fils = []
		self.translate = []
		self.rotate = []
		self.position = []

	@staticmethod
	def readInfo(f, end=False):
		"""
		f lit les 3 prochaines lignes
		ET doit aussi ignore la ligne du {
		"""

		#### Lire l'accolade #####
		l = Node.readline(f)
		if l[0] != "{":
			print("Invalid input")
			raise

		#### OFFSET ####
		l = Node.readline(f)
		if l[0] != "OFFSET":
			print("Invalid input")
			raise
		offset = [float(l[o]) for o in range(1, 4)]

		if end is True:
			return offset

		#### CHANNELS ###
		l = Node.readline(f)
		if l[0] != "CHANNELS":
			print("Invalid input")
			raise

		number_channels = int(l[1])
		rotation = []
		position = []
		for i in range(2, 2 + number_channels):
			if "rotation" in l[i]:
				rotation.append(l[i][0])
			if "position" in l[i]:
				position.append(l[i][0])

		# if len(rotation) == 0:
		# 	rotation = None
		# if len(position) == 0:
		# 	position = None

		return offset, position, rotation

	@staticmethod
	def CreateChild(parent, f):
		l = Node.readline(f)
		if l[0] == "JOINT":
			Child = Node(l[1], parent)
			offset, position, rotation = Node.readInfo(f)
			Child.translate = offset; Child.position = position; Child.rotate = rotation
			parent.fils.append(Child)
			Node.CreateChild(Child, f)
		elif l[0] == "End":
			Child = Node(l[1], parent)
			offset = Node.readInfo(f, True)
			Child.translate = offset
			parent.fils.append(Child)
			Node.CreateChild(parent, f)
		elif l[0] == "}":
			Node.CreateChild(parent, f)
		elif l[0] == "MOTION":
			return
		else:
			print("Invalid input")
			raise

	@staticmethod
	def readline(f):
		"""
		TODO : Check EOL
		"""
		l = f[0].replace("\t", "")
		f.pop(0)
		while len(l) == 0:
			l = f[0].replace("\t", "")
			f.pop(0)

		l = l.split(" ")
		return l

	@staticmethod
	def createStructureFromBVH(file_name):
		Root = Node(None)
		with open(file_name) as f: # Use file to refer to the file object
			f = f.read().strip()
			f = f.split("\n")
			line = Node.readline(f)

			while (line[0] != "ROOT"):
				line = Node.readline(f)
				if line is None: # On n'a pas trouvé la root dans le fichier
					return Root

			Root.name = line[1]
			offset, position, rotation = Node.readInfo(f)
			Root.translate = offset; Root.position = position; Root.rotate = rotation

			Node.CreateChild(Root, f);

			print("ROOT NODE CREATED")

			return Root

	def __str__(self):
		string = ""
		string += "JOINT " + self.name + "\n"
		string += "{\n"
		string += "OFFSET " + " ".join([str(i) for i in self.translate]) + "\n"
		# print("LEN OF psoition + rotate", len(self.position) + len(self.rotate))
		if len(self.position) + len(self.rotate) != 0:
			string += "CHANNELS " + str(len(self.position) + len(self.rotate)) + " "
			if len(self.position) != 0:
				string += " ".join([(str(i) + "position") for i in self.position]) + " "
			if len(self.rotate) != 0:
				string += " ".join([(str(i) + "rotation") for i in self.rotate]) + "\n"

		for i in self.fils:
			child_str = i.__str__()
			if child_str is not None:
				string += child_str

		return string
