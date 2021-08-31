import rng
import items 

class Structure:
	def __init__(self, hardness, drops, placed_from=None, is_fluid=False, is_solid=True):
		self.hardness = hardness
		self.drops = drops
		self.placed_from = placed_from
		self.is_fluid = is_fluid
		self.is_solid = is_solid

	def drop(self):
		d = {}
		for i in self.drops:
			n = self.drops[i].choose()
			if n > 0:
				d[i] = n
		return d


structure_list = {
	"Stone" : Structure(1.0, {"stone":rng.Rand_range(1)}, "stone"),
	"Dirt" : Structure(0.0, {"dirt":rng.Rand_range(1)}, "dirt"),
	"Sand" : Structure(0.0, {"sand":rng.Rand_range(1)}, "sand"),
	"Coal" : Structure(1.0, {"coal":rng.Rand_range((1,2))}),
	"Iron" : Structure(1.15, {"iron":rng.Rand_range(1)}),
	"Diamond" : Structure(1.25, {"diamond":rng.Rand_range(1)}),
	"Tree" : Structure(0.0, {
		"wood": rng.Rand_range(4), 
		"stick": rng.Rand_range({1: 30}),
		"apple": rng.Rand_range({1: 25}),
		"sapling": rng.Rand_range({1: 25, 2: 50})
	}),
	"Jungle_tree" : Structure(0.0, {
		"wood": rng.Rand_range((6, 8)), 
		"stick": rng.Rand_range({1: 40}),
		"jungle_sapling": rng.Rand_range({1: 25, 2: 50})
	}),
	"Water" : Structure(0.0, {"water_bucket": rng.Rand_range(1)}, "water_bucket", True, is_solid=False),
	"Lava" : Structure(0.0, {"lava_bucket": rng.Rand_range(1)}, "lava_bucket", True, is_solid=False),
	"Magma" : Structure(0.0, {"magma_bucket": rng.Rand_range(1)}, "magma_bucket", True, is_solid=False),
	"Crafting_table" : Structure(0.0, {"crafting_table":rng.Rand_range(1)}, "crafting_table"),
	"Bed" : Structure(0.0, {"bed":rng.Rand_range(1)}, "bed"),
	"Obsidian" : Structure(1.4, {"obsidian":rng.Rand_range(1)}, "obsidian"),
	"Furnace": Structure(1.0, {"furnace": rng.Rand_range(1)}, "furnace"),
	"Sapling": Structure(0.0, {"sapling": rng.Rand_range(1)}, "sapling", is_solid=False), 
	"Jungle_sapling": Structure(0.0, {"jungle_sapling": rng.Rand_range(1)}, "jungle_sapling", is_solid=False),
	"Frostflower": Structure(0.0, {"frostflower": rng.Rand_range(1)}, "frostflower", is_solid=False),
	"Firerose": Structure(0.0, {"firerose": rng.Rand_range(1)}, "firerose", is_solid=False),
	"Biobloom": Structure(0.0, {"biobloom": rng.Rand_range(1)}, "biobloom", is_solid=False)
} 

item_to_structure = {}

for name, struc in structure_list.items():
	if struc.placed_from != None:
		item_to_structure[struc.placed_from] = name