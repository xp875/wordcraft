import rng
from world_generation import cave
from world_generation import place

class Biome:
	def __init__(self, chance, place={}, generate={}, spawn={}):
		self.chance = chance
		self.place = place
		self.generate = generate
		self.spawn = spawn


biomes = {
	"Forest": Biome(13, 
		{cave.Cave: 50}, 
		{"Tree": rng.Rand_range((5, 8)), 
		"Dirt": rng.Rand_range((4, 6))}
	),
	"Plains": Biome(11, 
		{cave.Cave: 85}, 
		{"Sapling": rng.Rand_range((0, 3)), 
			"Biobloom": rng.Rand_range((0, 3)), 
			"Dirt": rng.Rand_range((4, 6))
		}
	),
	"Jungle": Biome(4, 
		{cave.Cave: 15}, 
		{"Jungle_tree": rng.Rand_range((3, 6)), 
			"Tree": rng.Rand_range((3, 6)),
			"Jungle_sapling": rng.Rand_range((1, 4)), 
		"Dirt": rng.Rand_range((2, 4))}
	),
	"River": Biome(7, 
		{cave.Cave: 55}, 
		{"Water": rng.Rand_range((25, 35)), 
			"Biobloom": rng.Rand_range((0, 3)), 
		"Sand": rng.Rand_range((2, 5))}
	),
	"Ocean": Biome(6, 
		{}, 
		{"Water": rng.Rand_range((90, 110)),
		"Sand": rng.Rand_range((5, 9))},
		
	),
	"Lava lake": Biome(3, 
		{cave.Cave: 40}, 
		{"Magma": rng.Rand_range((6, 12)), 
			"Stone": rng.Rand_range((3, 8)), 
			"Coal": rng.Rand_range((0, 2)),}
	),
	"Volcano": Biome(1, 
		{cave.Cave: 85}, 
		{"Magma": rng.Rand_range((6, 12)), 
			"Firerose": rng.Rand_range((6, 8)), 
			"Stone": rng.Rand_range((0, 8)), 
			"Coal": rng.Rand_range((0, 3)),
			"Iron": rng.Rand_range((0, 2))}
	),
	"Tundra": Biome(6, 
		{cave.Cave: 45}, 
		{"Frostflower": rng.Rand_range((6, 8))}
	),

}

def choose_biome(seed):
	tot = 0

	for i in biomes:
		tot += biomes[i].chance
	rng.seed = seed
	res = rng.rand_int(1, tot)
	for i in biomes:
		if res <= biomes[i].chance:
				return i
		res -= biomes[i].chance
	return -1


class Location(place.Place):
	name = "Location"

	def __init__(self, world, pos, seed):

		super().__init__()
		self.world = world
		self.pos = pos

		self.seed = seed
		
		biome = choose_biome(self.seed)
		self.biome = biome

		generate = biomes[self.biome].generate
		rng.set_seed(self.seed)
		for i in generate:
			self.add_structure(i, generate[i].choose())
		
		if self.pos.equals(self.world.spawn_pos) or rng.chance(20):
			self.add_structure("Crafting_table")

		self.places = []
		place = biomes[self.biome].place
		for i in place:
			if rng.chance(place[i]):
				self.places.append(i(self))

	def describe(self):
		print("You are in a", self.biome)
		super().describe()
		for i in self.places:
			print("There is a", i.name)

	def have_place(self, place):
		for i in self.places:
			if i.name == place:
				return True
		return False

	def get_place(self, place):
		for i in self.places:
			if i.name == place:
				return i
		return -1

	saplings = ["Sapling", "Jungle_sapling"]
	trees = ["Tree", "Jungle_tree"]
	growing_chance = [5.0, 3.5]

	def grow_trees(self):
		for i in range(len(self.saplings)):
			s = self.saplings[i]
			t = self.trees[i]
			c = self.growing_chance[i]
			c *= 1.25 ** self.structure_number("Biobloom")
			if self.world.time >= self.world.nighttime:
				c /= 4
			for j in range(self.structure_number(s)):
				if rng.chance(c):
					self.remove_structure(s)
					self.add_structure(t)
					if self.structure_number("Biobloom") > 0:
						print("Biobloom helped a", t, "grow!")
					else:
						print("\nA", t, "grew")

	def update(self):
		super().update()
		self.grow_trees()

		