pickaxes = {
	"wooden_pickaxe": 1.0,
	"stone_pickaxe": 1.15, 
	"iron_pickaxe": 1.25,
	"diamond_pickaxe": 1.4
}
power_to_pickaxes = {
	1.0: "wooden_pickaxe", 
	1.15: "stone_pickaxe", 
	1.25: "iron_pickaxe", 
	1.4: "diamond_pickaxe"
}

swords = {
	"wooden_sword": 3.0,
	"stone_sword": 5.0,
	"iron_sword": 7.0,
	"diamond_sword": 10.0,

}

armour = {
	"iron_armour": 2.0,
	"diamond_armour": 3.0,
	"dragon_armour": 4.0
}

item_list = [
	"wood",
	"stone",
	"iron",
	"diamond",
	
	"stick",
	"bed",
	"crafting_table",
	
	"wooden_pickaxe",
	"stone_pickaxe",
	"iron_pickaxe",
	"diamond_pickaxe",

	"wooden_sword",
	"stone_sword",
	"iron_sword",
	"diamond_sword",

	"iron_armour",
	"diamond_armour",
	"dragon_armour",

	"apple",

	"meat",
	"rotten_flesh",
	"spider_eye",

	"satay",

	"potion_bottle",
	"health_potion",

	"eye_of_ender",
	"portal_frame",
	"end_portal",

	"dragon_egg",
	"dragon_skin",
	
	"bucket",
	"water_bucket",
	"lava_bucket", 

	"sapling", 
	"jungle_sapling",
]



#crafting

#all the crafting recipes
crafting = {

	#crafted item : {
	#	 ingredient 1 : amount, ingredient 2 : amount ...
	#}
	"stick" : {"wood" : 1},
	"wooden_pickaxe" : {"stick" : 1, "wood" : 2},
	"stone_pickaxe" : {"stick" : 1, "stone" : 2},
	"iron_pickaxe" : {"stick" : 1, "iron" : 2},
	"diamond_pickaxe" : {"stick" : 1, "diamond" : 2},
	"bed" : {"wood" : 3	},
	"crafting_table" : {"wood" : 4},
	"wooden_sword" : {"stick" : 1, "wood" : 1},
	"stone_sword" : {	"stick" : 1, "stone" : 1},
	"iron_sword" : {"stick" : 1, "iron" : 1},
	"diamond_sword" : {	"stick" : 1, "diamond" : 1},
	"iron_armour" : {"iron" : 3	},
	"diamond_armour" : {"diamond" : 3	},
	"health_potion" : {"potion_bottle" : 1, "spider_eye" : 1},
	"portal_frame" : {"stone" : 4, "iron" : 2, "diamond" : 1},
	"end_portal" : {"eye_of_ender" : 3, "portal_frame" : 3},
	"satay" : {"meat" : 1, "stick" : 1},
	"dragon_armour" : {"dragon_skin" : 1},
	"bucket" : {"iron" : 2}

}

#shows a specific crafting recipe in the format
# (amount) ingedient + (amount) ingredient + ... => output
def print_crafting(m, e="\n"):
	x = crafting[m]
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
	print("=>", m, end=e)	


def craft(player, m):

	#alternative spellings 
	if m == "sticks":
		m = "stick"
	elif m == "wood_pickaxe":
		m = "wooden_pickaxe"
	elif m == "wood_sword":
		m = "wooden_sword"
	if m[-5:] == "armor":
		m = m[:-5]+"armour"
		
	if not m in crafting:
		print("You cannot craft \"", m, "\"\n", sep="")
		return -1

	recipe = crafting[m]

	#checking the player has enough ingredients
	for ingredient in recipe:
		if player.item_number(ingredient) < recipe[ingredient]:
			print("Cannot craft " + m + ": not enough " + ingredient)
			print_crafting(m)
			print("You only have:", player.item_number(ingredient), ingredient)
			print("")
			return -1

	print("Crafted " + m + "!")
	print_crafting(m)
	player.gain_item(m, 1, False)
	for ingredient in recipe:
		player.lose_item(ingredient, recipe[ingredient])
		print(ingredient, "left:", player.item_number(ingredient))

	#if crafted a better tool, or armour, will need to update
	return 0





"""

(\/)(\/)(\/)(\/)(\::::::
 \/  \/  \/  \/  \:  ::  

{--}{--}{--}{--}{-:: :::
{--}{--}{--}{--}{-::::::

[\/][\/][\/][\/][\::::::
|__||__||__||__||_:: :::



[][][][][][]:.:.:.:.     
()(.:...............     {}{}{}{}{}{}{}{}{}{}{}{}

"""
