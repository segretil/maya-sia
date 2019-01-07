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
		self.frame_time = 0

	@staticmethod
	def readInfo(f, info_frame, end=False):
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
			if "position" in l[i]:
				frame_numbers = [l[i][0], []]
				for k in range(len(info_frame)):
					frame_numbers[1].append(info_frame[k].pop(0))
				position.append(frame_numbers)
			if "rotation" in l[i]:
				frame_numbers = [l[i][0], []]
				for k in range(len(info_frame)):
					frame_numbers[1].append(info_frame[k].pop(0))
				position.append(frame_numbers)

		# if len(rotation) == 0:
		# 	rotation = None
		# if len(position) == 0:
		# 	position = None

		return offset, position, rotation

	@staticmethod
	def CreateChild(parent, f, info_frame):
		l = Node.readline(f)
		if l[0] == "JOINT":
			Child = Node(l[1], parent)
			offset, position, rotation = Node.readInfo(f, info_frame)
			Child.translate = offset; Child.position = position; Child.rotate = rotation
			parent.fils.append(Child)
			Node.CreateChild(Child, f, info_frame)
		elif l[0] == "End":
			Child = Node(l[1], parent)
			offset = Node.readInfo(f, info_frame, True)
			Child.translate = offset
			parent.fils.append(Child)
			Node.CreateChild(parent, f, info_frame)
		elif l[0] == "}":
			Node.CreateChild(parent, f, info_frame)
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

		info_frame = []

		with open(file_name) as motion_info:
			f = motion_info.read().strip()
			f = f.split("\n")
			line = Node.readline(f)

			while (Node.readline(f)[0] != "MOTION"):
				continue

			print("ROOT NODE CREATED")
			number_of_frames = int(Node.readline(f)[1])
			Root.frame_time = float(Node.readline(f)[2])

			info_frame = [[float(j) for j in i.split(" ")] for i in f]


		with open(file_name) as f: # Use file to refer to the file object
			f = f.read().strip()
			f = f.split("\n")
			line = Node.readline(f)

			while (line[0] != "ROOT"):
				line = Node.readline(f)
				if line is None: # On n'a pas trouvé la root dans le fichier
					return Root

			Root.name = line[1]
			offset, position, rotation = Node.readInfo(f, info_frame)
			Root.translate = offset; Root.position = position; Root.rotate = rotation

			Node.CreateChild(Root, f, info_frame);

			# We need to assert that info_frame is fully empty
			for i in info_frame:
				assert len(i) == 0

			return Root

	def __str__(self):
		string = ""
		string += "JOINT " + self.name + "\n"
		string += "{\n"
		string += "OFFSET " + " ".join([str(i) for i in self.translate]) + "\n"
		if len(self.position) + len(self.rotate) != 0:
			string += "CHANNELS " + str(len(self.position) + len(self.rotate)) + " "
			if len(self.position) != 0:
				string += " ".join([(str(i[0]) + "position") for i in self.position]) + " "
			if len(self.rotate) != 0:
				string += " ".join([(str(i[0]) + "rotation") for i in self.rotate]) + "\n"

		for i in self.fils:
			child_str = i.__str__()
			if child_str is not None:
				string += child_str

		return string
