from world_generation import structures
import rng

class Place:
	def __init__(self):
		self.structures = {}
	
	def describe(self):
		for i in self.structures:
			if structures.structure_list[i].is_fluid:
				print("There is", i)
			elif self.structures[i] == 1:
				print("There is", self.structures[i], i)
			else:
				print("There are", self.structures[i], i)
				
		
	def have_structure(self, s):
		return s in self.structures
	
	def structure_number(self, s):
		if not self.have_structure(s):
			return 0
		return self.structures[s]

	def add_structure(self, s, n=1):
		if n == 0:
			return
		if not self.have_structure(s):
			self.structures[s] = n
		else:
			self.structures[s] += n

	def remove_structure(self, ore, n=1):
		if not self.have_structure(ore):
			return -1
		if n >= self.structure_number(ore):
			del self.structures[ore]
		else:
			self.structures[ore] -= n

	def update_fluids(self, f):
		if f == "Water":
			lava = self.structure_number("Lava")
			if lava > 0:
				self.remove_structure("Lava", lava)
				self.add_structure("Obsidian", lava)
				print("Water mixed with Lava to form Obsidian")
			if self.have_structure("Magma"):
				self.remove_structure("Magma")
				self.remove_structure("Water")
				self.add_structure("Obsidian")
				print("Water mixed with Magma to form Obsidian")
		if f == "Magma" or f == "Lava":
			if self.have_structure("Water"):
				self.remove_structure("Water")
				self.remove_structure(f)
				self.add_structure("Stone")
				print(f, "mixed with Water to form Stone")
	
	def transform_magma(self):
		if not self.have_structure("Magma"):
			return
		x = self.structure_number("Magma")
		chance = rng.logarithmic(x, 5, 10, 10)
		if self.name == "Cave":
			chance *= 3
		bonus = self.structure_number("Firerose") - self.structure_number("Frostflower")
		chance *= 1.25 ** bonus
		if rng.chance(chance):
			self.remove_structure("Magma")
			self.add_structure("Lava")
			print("\nMagma turned into lava!")
		

	def update(self):
		self.transform_magma()
		return
