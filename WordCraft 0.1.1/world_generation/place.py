
class Place:
	def __init__(self):
		self.structures = {}
	
	def describe(self):
		for i in self.structures:
			if self.structures[i] >= 2:
				print("There are", self.structures[i], i)
			else:
				print("There is", self.structures[i], i)
		
	def have_structure(self, s):
		return s in self.structures
	
	def structure_number(self, s):
		if not self.have_structure(s):
			return 0
		return self.structures[s]

	def remove_structure(self, ore, n=1):
		if not self.have_structure(ore):
			return -1
		if n >= self.structure_number(ore):
			del self.structures[ore]
		else:
			self.structures[ore] -= n
