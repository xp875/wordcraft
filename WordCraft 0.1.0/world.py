import rng
import cave



"""Name : (Relative chance of generation, 
					 Chance of cave,
					 Max number of trees)"""
biomes = {
	"Forest": (12, 50, 8),
	"Plains": (15, 75, 4),
	"Jungle": (4, 20, 12),
	"River": (7, 10, 1),
	"Ocean": (6, 0, 0), 
	"Lava lake": (3, 35, 0), 
	"Volcano": (1, 55, 0)
}

class Location:

	def __init__(self, world, x_pos, biome=""):
		self.world = world
		self.x_pos = x_pos
		self.structures = {}

		if biome == "":
			biome = rng.weighted_choice(biomes)
			self.biome = biome

		if biomes[self.biome][2] > 0:
			self.structures["Tree"] = rng.slanted(biomes[self.biome][2]+1)-1

		self.cave = None
		if rng.chance(biomes[self.biome][1]):
			self.cave = cave.Cave(self)

	def describe(self):
		print("You are in a", self.biome)
		for i in self.structures:
			if self.structures[i] == 1:
				print("There is 1", i)
			elif self.structures[i] > 2:
				print("There are", self.structures[i], i+"s")
		if self.cave != None:
			print("There is a cave")
		

	def have_structure(self, s):
		return s in self.structures
	
	def structure_number(self, s):
		if not self.have_structure(s):
			return -1
		return self.structures[s]

	def remove_structure(self, s, n=1):
		self.structures[s] -= n

class World:	
	nighttime = 20
	daytime = 36

	size_limit = 256

	structure_to_item = {

		"Stone" : "stone",
		#"Coal" : "coal",
		"Iron" : "iron",
		"Diamond" : "diamond",
		#"Water" : "water_bucket",
		#"Lava" : "lava_bucket"

	}


	def __init__(self):
		self.seed = 0

		first_location = Location(self, 0.0)
		self.map = {0: first_location}

		self.time = 0
		self.day = 1

	def get_first_biome(self):
		return self.map[0].biome

	def is_loaded(self, x_pos):
		return x_pos in self.map

	def within_size_limit(self, x_pos):
		if x_pos >= self.size_limit /2:
			return False
		if x_pos < -self.size_limit/2:
			return False
		return True

	def generate_location(self, x_pos):
		if x_pos in self.map:
			return
		if not self.within_size_limit(x_pos):
			return
		self.map[x_pos] = Location(self, x_pos)

	def get_location(self, x_pos):
		return self.map[x_pos]

	

	



	



