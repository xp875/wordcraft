class Item_type:
	def __init__(self, craft=None):
		self.craft = craft

class St_item_type(Item_type):
	def __int__(self, craft=None):
		super().__init__(craft)

class Ust_item_type(Item_type):
	number = 0

	def __init__(self, craft=None, durability=None, usage=None, power=None):
		super().__init__(craft)
		self.durability = durability
		self.usage = usage
		self.power = power

	def increase_number(self, n=1):
		self.number += 1


class Crafting_recipe:
	def __init__(self, ingredients, need_crafting_table=True, output=1):
		self.ingredients = ingredients
		self.need_crafting_table = need_crafting_table
		self.output = output


item_list = {
	"wood": St_item_type(),
	"stone": St_item_type(),
	"dirt": St_item_type(),
	"sand": St_item_type(),
	"iron": St_item_type(),
	"diamond": St_item_type(),
	"coal": St_item_type(),
	
	"stick": St_item_type(
		craft = Crafting_recipe(
			{"wood" : 2}, 
			need_crafting_table = False,
			output=2
		)
	),
	"bed": St_item_type(
		craft = Crafting_recipe({"wood" : 3	})
	),
	"crafting_table": St_item_type(
		craft = Crafting_recipe(
			{"wood" : 4},
			need_crafting_table = False
		)
	),
	
	"wooden_pickaxe": Ust_item_type(
		craft = Crafting_recipe({"stick" : 1, "wood" : 2}), 
		durability = 30, 
		usage = "tool", 
		power = 1.0
	),
	"stone_pickaxe": Ust_item_type(
		craft = Crafting_recipe({"stick" : 1, "stone" : 2}), 
		durability = 50, 
		usage = "tool", 
		power = 1.15
	),
	"iron_pickaxe": Ust_item_type(
		craft = Crafting_recipe({"stick" : 1, "iron" : 2}), 
		durability = 90, 
		usage = "tool", 
		power = 1.25
	),
	"diamond_pickaxe": Ust_item_type(
		craft = Crafting_recipe({"stick" : 1, "diamond" : 2}), 
		durability = 150, 
		usage = "tool", 
		power = 1.4
	),

	"wooden_sword": Ust_item_type(
		craft = Crafting_recipe({"stick" : 1, "wood" : 1}), 
		durability = 30, 
		usage = "weapon", 
		power = 3
	),
	"stone_sword": Ust_item_type(
		craft = Crafting_recipe({"stick" : 1, "stone" : 1}), 
		durability = 50, 
		usage = "weapon", 
		power = 5
	),
	"iron_sword": Ust_item_type(
		craft = Crafting_recipe({"stick" : 1, "iron" : 1}), 
		durability = 90, 
		usage = "weapon", 
		power = 7
	),
	"diamond_sword": Ust_item_type(
		craft = Crafting_recipe({"stick" : 1, "diamond" : 1}), 
		durability = 150, 
		usage = "weapon", 
		power = 10
	),

	"iron_armour": Ust_item_type(
		craft = Crafting_recipe(
			{"iron" : 3}, 
			need_crafting_table = False
		), 
		durability = 90, 
		usage = "armour", 
		power = 2
	),
	"diamond_armour": Ust_item_type(
		craft = Crafting_recipe(
			{"diamond" : 3}, 
			need_crafting_table = False
		), 
		durability = 150, 
		usage = "armour", 
		power = 3
	),
	"dragon_armour": Ust_item_type(
		craft = Crafting_recipe(
			{"dragon_skin" : 1}, 
			need_crafting_table = False
		), 
		durability = 80, 
		usage = "armour", 
		power = 4
	),

	"torch": St_item_type(
		craft = Crafting_recipe(
			{"stick" : 1, "coal": 1}, 
			need_crafting_table = False
		)
	),

	"apple": St_item_type(),
	"raw_pork": St_item_type(),
	"cooked_pork": St_item_type(),
	"rotten_flesh": St_item_type(),
	"spider_eye": St_item_type(),

	"satay": St_item_type(
		craft = Crafting_recipe(
			{"raw_pork" : 1, "stick" : 1}, 
			need_crafting_table = False
		)
	),

	"glass": St_item_type(),
	"potion_bottle": St_item_type(
		craft = Crafting_recipe(
			{"glass": 1}, need_crafting_table=False
		)
	),
	"health_potion": St_item_type(
		craft = Crafting_recipe(
			{"potion_bottle": 1, "spider_eye": 1}, 
			need_crafting_table = False
		)
	),

	"eye_of_ender": St_item_type(),
	"portal_frame": St_item_type(
		craft = Crafting_recipe({
			"stone": 4, 
			"iron": 2, 
			"diamond": 1
		})
	),
	"end_portal": St_item_type(
		craft = Crafting_recipe({
			"eye_of_ender" : 3, 
			"portal_frame" : 3
		})
	),

	"dragon_egg": St_item_type(),
	"dragon_skin": St_item_type(),
	
	"bucket": St_item_type(
		craft = Crafting_recipe(
			{"iron" : 2}, 
			need_crafting_table = False
		)
	),
	"water_bucket": St_item_type(),
	"lava_bucket": St_item_type(), 
	"magma_bucket": St_item_type(),

	"sapling": St_item_type(), 
	"jungle_sapling": St_item_type(),

	"obsidian": St_item_type(),
	"furnace": St_item_type(
		craft = Crafting_recipe({"stone": 4, "coal": 4}),
	), 
	"nether_portal": St_item_type(
		craft = Crafting_recipe({"obsidian": 5})
	),

	"shield": St_item_type(
		craft = Crafting_recipe({"wood": 4, "iron": 1})
	),

	"frostflower": St_item_type(),
	"firerose": St_item_type(),
	"biobloom": St_item_type()
}

power_to_pickaxes = {
	1.0: "wooden_pickaxe", 
	1.15: "stone_pickaxe", 
	1.25: "iron_pickaxe", 
	1.4: "diamond_pickaxe"
}


sample_ust_item = Ust_item_type()
def is_ust(item_type):
	return type(item_list[item_type]) == type(sample_ust_item)


class Item:
	def __init__(self, type):
		self.type = type
		self.name = type
		
class Ust_item(Item):
	def __init__(self, type):	
		super().__init__(type)
		self.name = self.type + str(item_list[self.type].number)
		item_list[self.type].increase_number()
		self.max_durability = item_list[self.type].durability
		self.durability = self.max_durability
		self.enchantments = []

	def usage(self):
		return item_list[self.type].usage

	def power(self):
		return item_list[self.type].power

	def lose_durability(self):
		self.durability -= 1

	def get_durability_percentage(self):

		f = self.durability / self.max_durability
		s = str(int(f*100)) + "%"
		return s 

	def print(self, e="\n"):
		print(self.type, self.power(), self.get_durability_percentage(), sep=" / ", end=e)


class St_item(Item):
	stack_limit = 10000

	def __init__(self, type, stack_size=1):
		super().__init__(type)
		self.stack_size = stack_size

	def decrease_stack_size(self, n=1):
		if self.stack_size < n:
			return -1
		self.stack_size -= n
		return 0

	def increase_stack_size(self, n=1):
		if self.stack_size + n > self.stack_limit:
			return -1
		self.stack_size += n
		return 0

	def print(self):
		print(self.type + " "*(18-len(self.type)) + "×" + str(self.stack_size))
		


#shows a specific crafting recipe in the format
# (amount) ingedient + (amount) ingredient + ... => (amount) output
def print_crafting(m, e="\n"):
	x = item_list[m].craft.ingredients

	n = len(x)
	count = 0
	for i in x:
		count += 1
		if x[i] == 1:
			#omits coefficient if only 1
			print(i, end=" ")
		else:
			print(x[i], i, end=" ")
		if count <= n-1:
			print("+ ", end="")
	print("->", end=" ")
	if item_list[m].craft.output != 1:
		print(item_list[m].craft.output, end=" ")
	print(m)


def craft(player, m):

	recipe = item_list[m].craft.ingredients

	#checking the player has enough ingredients
	for ingredient in recipe:
		item_number = player.inventory.count_st_item(ingredient)
		if item_number < recipe[ingredient]:
			print("Cannot craft " + m + ": not enough " + ingredient)
			print_crafting(m)
			print("You only have:", item_number, ingredient)
			print("")
			return -1

	
	print_crafting(m)
	n = item_list[m].craft.output
	player.gain_item(m, n, is_ust(m))
	if not is_ust(m):
		print("You now have", player.inventory.count_st_item(m), m)
	for ingredient in recipe:
		player.lose_item(ingredient, recipe[ingredient])
		print(ingredient, "left:", player.inventory.count_st_item(ingredient))

	#if crafted a better tool, or armour, will need to update
	return 0


smelting = {
	"raw_pork": "cooked_pork",
	"sand": "glass"
}

def smelt(player, i):
	if i not in smelting:
		print("You cannot smelt that\n")
		return -1
	if not player.inventory.has_st_item(i):
		print("You do not have \"", i, "\"\n", sep="")
		return -1
	player.lose_item(i)
	player.gain_item(smelting[i])
	return 0


class Storage():
	def __init__(self, capacity):
		self.capacity = 1000000
		self.storage = []

	def has_st_item(self, type):
		for i in self.storage:
			if i.type == type:
				return True
		return False

	def count_st_item(self, type):
		n = 0
		for i in self.storage:
			if i.type == type:
				n += i.stack_size
		return n

	def has_ust_item(self, name):
		for i in self.storage:
			if i.name == name:
				return True
		return False
	
	def get_ust_item(self, name):
		for i in self.storage:
			if i.name == name:
				return i
		return -1

	def add_st_item(self, item_type, n=1):
		for i in self.storage:
			if i.type == item_type:
				i.increase_stack_size(n)
				return
		self.storage.append(St_item(item_type, n))
		
	def add_ust_item(self, ust_item):
		self.storage.append(ust_item)

	def remove_st_item(self, item, n=1):
		for i in self.storage:
			if i.type == item:
				if n > i.stack_size:
					return -1
				if n == i.stack_size:
					self.storage.remove(i)
					return 0
				i.decrease_stack_size(n)
				return
		return -1

	def remove_ust_item(self, name):
		if name == None:
			return -1
		for i in self.storage:
			if i.name == name:
				self.storage.remove(i)
				return i
		return -1

	def clear(self):
		self.storage = []
	


