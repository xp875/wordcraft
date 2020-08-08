import rng
import items 

class Structure:
	def __init__(self, hardness, drops, placed_from=None, is_fluid=False):
		self.hardness = hardness
		self.drops = drops
		self.placed_from = placed_from
		self.is_fluid = is_fluid

	def drop(self):
		d = {}
		for i in self.drops:
			n = self.drops[i].choose()
			if n > 0:
				d[i] = n
		return d


structure_list = {
	"Stone" : Structure(items.pickaxes["wooden_pickaxe"], {"stone":rng.Rand_range(1)}, "stone"),
	"Coal" : Structure(items.pickaxes["wooden_pickaxe"], {"coal":rng.Rand_range(1)}),
	"Iron" : Structure(items.pickaxes["stone_pickaxe"], {"iron":rng.Rand_range(1)}),
	"Diamond" : Structure(items.pickaxes["iron_pickaxe"], {"diamond":rng.Rand_range(1)}),
	"Tree" : Structure(0.0, {
		"wood": rng.Rand_range(4), 
		"stick": rng.Rand_range({1: 75}),
		"apple": rng.Rand_range({1: 25}),
		"sapling": rng.Rand_range({1: 25, 2: 50})
	}),
	"Jungle_tree" : Structure(0.0, {
		"wood": rng.Rand_range((6, 8)), 
		"stick": rng.Rand_range({1: 75}),
		"jungle_sapling": rng.Rand_range({1: 25, 2: 50})
	}),
	"Water" : Structure(0.0, {"water_bucket": rng.Rand_range(1)}, "water_bucket", True),
	"Lava" : Structure(0.0, {"lava_bucket": rng.Rand_range(1)}, "lava_bucket", True),
	"Crafting_table" : Structure(0.0, {"crafting_table":rng.Rand_range(1)}, "crafting_table"),
	"Bed" : Structure(0.0, {"bed":rng.Rand_range(1)}, "bed"),
} 
