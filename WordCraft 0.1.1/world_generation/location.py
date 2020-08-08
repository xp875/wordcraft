import rng
from world_generation import cave
from world_generation import place


"""Name : (Relative chance of generation, 
					 Chance of cave,
					 Max number of trees)"""
biomes = {
	"Forest": (12, 50, 8),
	"Plains": (15, 85, 4),
	"Jungle": (4, 15, 12),
	"River": (7, 55, 1),
	"Ocean": (6, 0, 0), 
	"Lava lake": (3, 45, 0), 
	"Volcano": (1, 85, 0)
}


class Location(place.Place):

	def __init__(self, world, x_pos, biome=""):
		super().__init__()
		self.world = world
		self.x_pos = x_pos

		if biome == "":
			biome = rng.weighted_choice(biomes)
			self.biome = biome

		trees = rng.slanted(biomes[self.biome][2]+1)-1
		if trees > 0:
			if self.biome == "Jungle":
				self.structures["Jungle_tree"] = trees
			else:
				self.structures["Tree"] = trees
		

		self.cave = None
		if rng.chance(biomes[self.biome][1]):
			self.cave = cave.Cave(self)
		elif self.x_pos == 0.0:
			if rng.chance(biomes[self.biome][1]/2):
				self.cave = cave.Cave(self)

	def describe(self):
		print("You are in a", self.biome)
		super().describe()
		if self.cave != None:
			print("There is a cave")
		