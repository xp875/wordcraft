#WordCraft 0.1.1

import rng
import player
from world_generation import world
import items


location = "forest"

world = world.World()
player = player.Player(world)

day = 1
time = 0

moves = 0

score = 0

luck = 1.0

cheats = False
cheated = False

done = False
win = -1
show_hearts = False


#all the items that the player can collect 


#tools that the player is using

#objects in the surroundings of locations

forest_surr = {
	"tree" : 8,
	"cave" : 1,
	"chest" : 0
}

cave_surr = {
	"stone" : float("inf"),
	"iron" : 0,
	"diamond" : 0,
	"chest" : 0
}


#mob info

forest_passive_mobs =	{}
forest_hostile_mobs = {}
cave_hostile_mobs = {}
end_hostile_mobs = {}
ed = {}

forest_passive_mob_cap = 3
forest_hostile_mob_cap = 2
cave_hostile_mob_cap = 2


#intro

def intro():
	name = "WordCraft"
	if rng.chance(0.01):
		name = "Worcdraft"
	print("""
Welcome to """+name+""", a text-based game based on Minecraft.

Version: 0.1.1 
Please read info.txt to learn about the updates. Please report any bugs you find. 

	""")


#experience / score
def gain_xp(amount):
	global score
	score += amount


#winning
def winning():
	if win >= 0:
		print("You have completed the game! Great job!\n")
		print("Moves taken to complete:", win)
		if cheated == False:
			
			#grades your winning
			if win <= 200:
				print("That is legendary!")
				gain_xp(100)
			elif win <= 300:
				print("That is epic!")
				gain_xp(80)
			elif win <= 400:
				print("That is superb!")
				gain_xp(50)
			elif win <= 500:
				print("That is awesome!")
				gain_xp(20)
			else:
				print("That is great!")
		else:
			print("That is great!")
		print("")


#location description

def desc_location(line1=True):
	"""
	if location == "forest":
		if line1:
			print("You are in a forest")

		for x in forest_surr:
			if forest_surr[x] == 1:
				print("There is a", x)
			elif forest_surr[x] > 1:
				print("There are", forest_surr[x], x+'s')
		

	elif location == "cave":
		if line1:
			print("You are in a cave")

		for x in cave_surr:
			if x == "stone":
				print("There is stone")
			elif cave_surr[x] > 0:
				print("There is", cave_surr[x], x)
		for x in cave_hostile_mobs:
			print("There is a ", cave_hostile_mobs[x]["type"], \
					", ", x, sep="")
			
	
	"""
	if location == "end":
		if line1:
			print("You are in the end")
		if ed != {}:
			print("There is the enderdragon, ", end = "")
			if ed["active"]:
				print("ready to attack")
			else:
				print("flying around")
		for x in end_hostile_mobs:
			print("There is an ", end_hostile_mobs[x]["type"], \
					", ", x, sep="")


	elif player.get_y_pos() == 1.0:			
		player.location().describe()
		for x in forest_passive_mobs:
			print("There is a ", forest_passive_mobs[x]["type"],\
					", ", x, sep="")
		for x in forest_hostile_mobs:
			print("There is a ", forest_hostile_mobs[x]["type"], \
					", ", x, sep="")
	elif player.get_y_pos() == 0.0:
		player.location().cave.describe()
		for x in cave_hostile_mobs:
			print("There is a ", cave_hostile_mobs[x]["type"], \
					", ", x, sep="")
	player.print_pos()


#details display

def print_time(e):
	print("Time: ", end="")
	if time < 0:
		print("undefined", end=e)
	elif time < world.nighttime:
		print(time, "(day); Day", day, end=e)
	else:
		print(time, "(night); Day", day, end=e)


def print_moves(e):
	print("Moves:", moves, end=e)


def print_location(e):
	print("Location:", location, end=e)


def print_health(e):
	print("Health:", player.get_health(), end=e)
	
def print_pickaxe(e):
	print("Pickaxe:", player.pickaxe, end=e)

def print_sword(e):
	print("Sword: ", player.sword, " (", player.attack_damage, " attack damage)",\
			sep="",end=e)

def print_armour(e):
	print("Armour: ", player.armour, " (", player.armour_protection, \
			" protection)", sep="", end=e) 

def print_details():
	t = "	 |	 "
	print_time(t)
	print_moves(t)
	print_location(t)
	print_health("\n")
	print_pickaxe(t)
	print_sword(t)
	print_armour("\n")



#time

def check_time():
	global time
	global day
	global forest_hostile_mob_cap
	global cave_hostile_mob_cap

	if location == "end":
		time == -1	
	elif time == world.nighttime:
		#prints a message when it reaches night time
		print("\nIt is now night! Sleep or beware of monsters!")
	elif time == world.daytime:
		time = 0
		day += 1
		world.time = 0
		world.day += 1
		#prints a message when it reaches day time (new day)
		print("\nIt is now day. It is day", day)

		if day == 2:
			forest_hostile_mob_cap = 3
			cave_hostile_mob_cap = 3
		elif day == 3:
			forest_hostile_mob_cap = 4
			

def sleep():
	global time
	global day

	#need to have a bed
	if not player.have_item("bed"):
		print("You need to have a bed to sleep\n")
		return -1
	#need to be at night
	if time < world.nighttime:
		print("You can only sleep at night\n")
		return -1
	#need to be in the forest
	if location != "forest":
		print("You can only sleep in the forest\n")
		return -1
	#need to have no hostile mobs around
	if len(forest_hostile_mobs)>0:
		print("You may not rest now, there are monsters nearby\n")
		return -1
	
	print("zzz...")
	world.time = -1
	world.day += 1
	time = -1
	day += 1
	print("You have skipped to the day. It is day", day)
	


#health


def die():
	#called when health decreased to 0
	global health
	global done
	
	if player.health > 0:
		print("Error, you did not die")
		return
	player.health = 0
	done = True
	#ends the game


	


#generating objects

def grow_trees():
	#only grow trees in day time
	if time >= world.nighttime:
		return
	global forest_surr
	if forest_surr["tree"] >= 10:
		return

	chance = 10
	if day > 1:
		chance += 10
	chance += max(0,5*(8-forest_surr["tree"])//2)
	
	if rng.chance(chance*luck):
		print("\nA tree has grown")
		forest_surr["tree"] += 1

#treasure chests generated randomly
def generate_chest():
	global cave_surr
	global forest_surr
	surr	= {}
	if location == "forest":
		surr = forest_surr
	elif location == "cave":
		surr = cave_surr
	else:
		return
	#will not generate if already have a chest
	if surr["chest"] > 0:
		return
	
	chance = 3
	if rng.rand_int(1, 100) <= chance*luck:
		surr["chest"] += 1
		print("\nYou find a chest. There may be treasure inside!")


#chest loot
		
chest_loot = [
[ #0 : common loot 
	("wood", (8, 16)),
	("apple", (3, 5)),
	("rotten_flesh", (4, 10)),
	("stick", (2, 5)),
	("crafting_table", (1, 3)),
	("spider_eye", (1, 4))
],
[ #1 : tools loot
	"stone_pickaxe",
	"stone_sword",
	"iron_pickaxe",
	"iron_sword",
	"iron_armour",
	"diamond_pickaxe", 
	"diamond_sword", 
	"diamond_armour",
	"wooden_sword",
	"wooden_pickaxe"
], 
[ #2 : rare loot
	("iron", (2, 5)),
	("stone", (16, 26))
], 
[ #3 : epic loot
	("diamond", (1, 2)),
	("health_potion", (1, 1)),
	("portal_frame",(1, 1)),
	("eye_of_ender", (1, 1))
] ]

def open_chest():
	global cave_surr
	global forest_surr

	#checking there is a chest
	surr	= {"chest" : 0}
	if location == "forest":
		surr = forest_surr
	elif location == "cave":
		surr = cave_surr

	if surr["chest"] < 1:
		print("There is no chest here\n")
		return -1
	surr["chest"] -= 1 

	nothing = True
	#the amount of loot from each category
	loot_amount = [rng.rand_int(0, 2), rng.rand_int(0, 2), rng.rand_int(0, 2), 0]
	if rng.rand_int(1, 100) <= 30:
		loot_amount[3] = 1
		if rng.rand_int(1, 100) <= 25:
			loot_amount[3] += 1

	#duplicate the list because we will remove elements
	loot2 = []
	for i in chest_loot:
		v=[]
		v.extend(i)
		loot2.append(v)
		
	loot2.extend(chest_loot)
	
	#i is the category
	for i in range(4):
		#in category i, we choose loot_amount[i] things
		for j in range(loot_amount[i]):
			
			#choose a random (item : (lo, hi)) from loot2[i]
			l = rng.choice(loot2[i])
			item = l
			k = 0
			if i == 1:
				k = 1
			if i != 1:
				#if in other categories, we choose based on the lower and
				#upper bound
				item = l[0]
				k = rng.rand_int(l[1][0], l[1][1])

			#remove the chosen item so no duplicates
			loot2[i].remove(l)
			
			print("You got", k, item)
			nothing = False
			player.gain_item(item, k)
			
	#if there is nothing
	if nothing:
		print("You got nothing :(")
	return 0
	

#mobs


#mob death

#mob drops
# mob type : {
#	 drop item : {
#		 quantity : percent chance } } 

mob_drops = {
	"pig" : {
		"meat" : {
			1 : 33,
			2 : 50,
			3 : 100
		}
	},
	"zombie" : {
		"rotten_flesh" : {
			1 : 33,
			2 : 50
		},
		"iron" : {
			1 : 6
		}
	},
	"spider" : {
		"spider_eye" : {
			1 : 33,
			2 : 50			
		}
	},
	"enderman" : {
		"eye_of_ender" : {
			1 : 33,
			2 : 50
		},
		"diamond" : {
			1 : 5
		}
	},
	"witch" : {
		"potion_bottle" : {
			1 : 50,
			2 : 100,
		},
		"spider_eye" : {
			1 : 50
		},
		"apple" : {
			1 : 50
		},
		"health_potion" : {
			1 : 10
		}
	}	
}


def kill_mob(m, moblist):
	global forest_passive_mobs
	global forest_hostile_mobs
	global cave_hostile_mobs
	global end_hostile_mobs

	print(m, "died")
	
	mob_type = moblist[m]["type"]
	drops = mob_drops[mob_type]

	#drop all items
	for drop_item in drops:
		for drop_amount in drops[drop_item]:
			chance = drops[drop_item][drop_amount]
			if rng.rand_int(1, 100) <= chance*luck:
				print(m, "dropped", drop_amount, drop_item)
				player.gain_item(drop_item, drop_amount)
				break
	moblist.pop(m)

	if mob_type == "pig":
		gain_xp(2)
	elif mob_type == "zombie":
		gain_xp(5)
	elif mob_type == "enderman" or mob_type == "witch":
		gain_xp(8)
	elif mob_type == "spider":
		gain_xp(3)

	

def attack_mob(m):
	global forest_passive_mobs
	global forest_hostile_mobs
	global cave_hostile_mobs
	global end_hostile_mobs
	moblist = {}
	
	if location == "forest":
		
		if m in forest_passive_mobs:
			moblist = forest_passive_mobs
		elif m in forest_hostile_mobs:
			moblist = forest_hostile_mobs
		else:
			print("There is no ", m, " here\n", sep="\"")
			return -1
		
	elif location == "cave" :
		moblist = cave_hostile_mobs
		if not m in moblist:
			print("There is no ", m, " here\n", sep="\"")
			return -1

	elif location == "end":
		moblist = end_hostile_mobs
		if not m in moblist:
			print("There is no ", m, " here\n", sep="\"")
			return -1
			
	
	print("You attacked ", m, " with ", player.sword, ". ", sep="", end="")
	print("You dealt", player.attack_damage, "damage")

	moblist[m]["health"] -= player.attack_damage
	#if health reaches 0, kill it
	if moblist[m]["health"] <= 0:
		kill_mob(m, moblist)
	
	else:
		print(m, "has", moblist[m]["health"], "health left")


	return 0
	


#pig

pig_count = 0

def spawn_pig():
	global pig_count
	new_pig = {"type" :	"pig",
				"health" : 4,
				"lifetime" : 0}
	name = "pig" + str(pig_count)
	forest_passive_mobs[name] = new_pig
	print("\nYou see a pig,", name)
	pig_count += 1

def move_pig(m):
	global forest_passive_mobs
	moblist = forest_passive_mobs
	moblist[m]["lifetime"] += 1

#zombie

zombie_count = 0


def spawn_zombie():
	global zombie_count
	new_mob = {"type" :	"zombie",
				"health" : 10,
				"lifetime" : 0}
	name = "zombie" + str(zombie_count)
	forest_hostile_mobs[name] = new_mob
	print("\nYou see a zombie,", name)
	zombie_count += 1		

def move_zombie(m):
	global forest_hostile_mobs
	moblist = forest_hostile_mobs
	moblist[m]["lifetime"] += 1
	
	damage = 2

	#small chance to attack through armour
	if player.armour_protection > 0 and	rng.rand_int(1, 100) <= 22:
		print("\n", m, " attacked you through your armour! "\
				"You take ", damage, " damage", sep = "")
		player.damage_health(damage)
		if player.get_health() <= 0:
			print("You were slain by zombie")
			die()
	else:
		#armour reduces damage, but cap at 0
		damage_taken = max(0, damage - player.armour_protection)
		print("\n", m, " attacked you! You take ", damage ," - ", player.armour_protection, \
			" = ", damage_taken, " damage", sep = "")
		player.damage_health(damage_taken)
		if player.get_health() <= 0:
			print("You were slain by a zombie")
			die()

	if time < world.nighttime:
		damage = rng.rand_int(4, 7)
		print("")
		print(m, "burnt in sunlight. It takes", damage, "damage")
		moblist[m]["health"] -= damage
		if moblist[m]["health"] <= 0:
			return "kill"
		else:
			print(m, "has", moblist[m]["health"], \
				"health left")
	
	return ""

#spider

spider_count = 0


def spawn_spider():
	global spider_count
	
	new_mob = {"type" :	"spider",
				"health" : 6,
				"lifetime" : 0}
	name = "spider" + str(spider_count)
	cave_hostile_mobs[name] = new_mob
	print("\nYou see a spider,", name)
	spider_count += 1		

def move_spider(m):
	global cave_hostile_mobs
	moblist = cave_hostile_mobs
	moblist[m]["lifetime"] += 1

	
	damage = 1
	#higher damage on second day
	if day >= 2:
		damage = rng.rand_int(1, 2)
	#higher damage at night 
	if time >= world.nighttime:
		damage = rng.rand_int(2, 4)
		if day >= 2:
			damage = rng.rand_int(4, 5)

	#armour reduces damage, but cap at 0
	damage_taken = max(0, damage - player.armour_protection)
	print("\n", m, " bit you! You take ", damage ," - ", player.armour_protection, \
			" = ", damage_taken, " damage", sep = "")
	player.damage_health(damage_taken)
	if player.get_health() <= 0:
		print("You were bitten by spider")
		die()

	
	return ""


#enderman

enderman_count = 0


def spawn_enderman(end = False):
	
	global forest_hostile_mobs
	global end_hostile_mobs
	moblist = forest_hostile_mobs
	if end:
		moblist = end_hostile_mobs
	
	global enderman_count
	new_mob = {"type" :	"enderman",
				"health" : 20,
				"lifetime" : 0}
	name = "enderman" + str(enderman_count)
	moblist[name] = new_mob
	print("\nYou see an enderman,", name)
	enderman_count += 1
		

def move_enderman(m, end = False):
	global forest_hostile_mobs
	global end_hostile_mobs
	moblist = forest_hostile_mobs
	
	if end:
		moblist = end_hostile_mobs
		
	moblist[m]["lifetime"] += 1

	if moblist[m]["lifetime"] <= 1 and end:
		return ""

	#small chance to not attack
	if rng.rand_int(1, 100) <= 10:
		print(m, "teleported around")
		return ""
	
	damage = rng.rand_int(4, 5)
	#armour reduces damage, but cap at 0
	damage_taken = max(0, damage - player.armour_protection)
	print("\n", m, " hit you! You take ", damage ," - ", player.armour_protection, \
			" = ", damage_taken, " damage", sep = "")
	player.damage_health(damage_taken)
	if player.get_health() <= 0:
		print("You were killed by enderman")
		die()
	
	return ""




#witch

witch_count = 0


def spawn_witch():

	global witch_count
	
	new_mob = {"type" :	"witch",
				"health" : 15,
				"lifetime" : 0}
	name = "witch" + str(witch_count)
	forest_hostile_mobs[name] = new_mob
	print("\nYou see witch,", name)
	witch_count += 1		

def move_witch(m):
	global forest_hostile_mobs
	moblist = forest_hostile_mobs
	moblist[m]["lifetime"] += 1

	#chance to heal itself
	mob_health = moblist[m]["health"]
	will_heal = False
	if mob_health <= 10:
		if rng.rand_int(1, 100) <= 50:
			will_heal = True

	if not will_heal:
		#attack
		damage = 4
		#armour reduces damage, but cap at 0
		damage_taken = max(0, damage - player.armour_protection)
		print("\n", m, " poisoned you! You take ", damage ," - ", player.armour_protection, \
				" = ", damage_taken, " damage", sep = "")
		player.damage_health(damage_taken)
		if player.get_health() <= 0:
			print("You were poisoned by witch")
			die()
		
	else:
		#healing
		healing = rng.rand_int(7, 12)
		if mob_health + healing > 15:
			healing = 15 - mob_health 
		moblist[m]["health"] += healing
		print("")
		print(m, "drank a health potion and healed",healing, "health.")
		print(m, "now has", moblist[m]["health"], "health")
		

	return ""


#enderdragon


def spawn_enderdragon():
	global ed
	
	new_mob = {
		"type" : "enderdragon",
		"health" : 200,
		"max_health" : 200,
		"lifetime" : 0,
		"stage" : 1,
		"active" : True,
		"waiting" : False,
		"cycle_time" : 0,
		"cycle_length" : 3,
		"acid_attack" : 2
	}
	ed = new_mob
	print("The enderdragon appears and flies towards you, ready to attack.")


def print_enderdragon_health():
	
	if ed == {}:
		return
	
	#					ENDERDRAGON
	#+--------------------------------------------------+
	#|////////////////////////////////////////			|
	#+--------------------------------------------------+

	h = ed["health"]
	#each slash (bar) corresponds to 4 health
	bars = h//4
	if bars == 0:
		bars = 1
	s = " "*20 + "ENDERDRAGON"
	s += "\n+" + 50*"-" + "+\n|"
	s += bars*"/" + (50-bars)*" " +"|\n"
	s += "+" + 50*"-" + "+\n"
	print(s)
		


def kill_enderdragon():
	global ed
	
	print("\nThe enderdragon hovers upwards, shakes violently and fades away")
	print("Congratulations! You have slain the enderdragon")
	ed = {}
	#get dragon_skin
	print("You gain dragon_skin!")
	player.gain_item("dragon_skin", 1, False)
	gain_xp(150)
	if win == -1:
		#get dragon_egg, but only the first time ed. is killed.
		#if have killed ed. before, then win would be the number of moves
		print("\nYou gain the legendary dragon_egg!")
		print("Return to the forest to complete the game")
		player.gain_item("dragon_egg", 1, False)
	else:
		print("You may return to the forest now")
	


def attack_enderdragon():
	global ed

	if ed["active"] == False:
		print("You cannot reach the enderdragon when it is flying\n")
		return -1

	print("You hit at the enderdragon with ", player.sword, ". ", sep="", end="")
	print("You dealt", player.attack_damage, "damage")

	ed["health"] -= player.attack_damage
	if ed["health"] <= 0:
		kill_enderdragon()
		
	else:
		print("The enderdragon has", ed["health"], \
		"health left")
	return 0
	

def enderdragon_attack():
	#acid attack, more damage
	#only happens once per cycle
	if ed["cycle_time"] == ed["acid_attack"]:
		damage = rng.rand_int(5,7)
		damage_taken = max(0, damage-player.armour_protection)
		print("\nThe enderdragon spews acid at you! You take ", \
				damage ," - ", player.armour_protection, \
				" = ", damage_taken, " damage", sep = "")
		player.damage_health(damage_taken)
		if player.get_health() <= 0:
			print("\nYou were burnt by enderdragon's acid breath")
			die()
	#normal attack, less damage
	#all other attacks
	else:
		damage = 4
		if ed["stage"] == 2:
			damage = rng.rand_int(4, 5)
		damage_taken = max(0, damage - player.armour_protection)
		print("\nThe enderdragon bumps into you. You take ", \
				damage ," - ", player.armour_protection, \
				" = ", damage_taken, " damage", sep = "")
		player.damage_health(damage_taken)
		if player.get_health() <= 0:
			print("\nYou were killed by enderdragon")
			die()
				


def move_enderdragon():
	global ed
	if ed == {}:
		return
	
	
	ed["lifetime"] += 1

	if ed["stage"] == 1:
		#when the ed. reaches 100 health, it enters stage 2
		if ed["health"] <= 100:
			ed["stage"] = 2
			print("\nThe enderdragon roars. It enters the second stage")

			if ed["active"]:
				print("The enderdragon flies off.")
			print("The enderdragon may have a surprise for you...")
			
			ed["cycle_time"] = 0
			ed["cycle_length"] = -2
			ed["waiting"] = True
			ed["active"] = False

			return
			
			
	if ed["lifetime"] <= 1:
		return

	#waiting for player to kill enderman
	if ed["waiting"]:
		if ed["cycle_length"] == -2:
			for i in range(3):
				spawn_enderman(True)
			ed["cycle_length"] = -1
			return
		if end_hostile_mobs == {}:
			ed["cycle_time"] = -1
		else:
			return

	#actively attacking
	if ed["active"]:
		enderdragon_attack()
		ed["cycle_time"] += 1

		#if done with attacking, fly off
		if ed["cycle_time"] == ed["cycle_length"]:
			ed["cycle_time"] = 0

			ed["cycle_length"] = 1
			if ed["stage"] == 2:
				ed["cycle_length"] = 2
			
			ed["active"] = False
			print("The enderdragon flies off.")

	#flying off 
	else:
		regen = rng.rand_int(1, 3)
		if ed["stage"] == 2:
			regen = rng.rand_int(3, 5)
		print("\nThe enderdragon regenerates", regen, "health")
		ed["health"] += regen
		if ed["health"] > 200:
			ed["health"] = 200

		ed["cycle_time"] += 1

		#if done with flying off, go back and attack 
		if ed["cycle_time"] == ed["cycle_length"] or \
			 ed["waiting"]:
			ed["waiting"] = False
			ed["cycle_time"] = 0
			ed["active"] = True
			
			ed["cycle_length"] = 3
			if ed["stage"] == 2:
				ed["cycle_length"] = rng.rand_int(4, 5)
			
			next_acid = rng.rand_int(0, ed["cycle_length"]-1)
			ed["acid_attack"] = next_acid
			
			print("The enderdragon flies back, ready to attack")

		


#general
		
def spawn_mobs():
	if location == "forest":

		#pig
		if len(forest_passive_mobs) < forest_passive_mob_cap:
			chance = 17
			if time >= world.nighttime:
				chance = 5
			if rng.rand_int(1, 100) <= chance:
				spawn_pig()

		#nighttime hostile mobs	 
		if time >= world.nighttime and \
		len(forest_hostile_mobs) < forest_hostile_mob_cap:
			#zombie
			if rng.rand_int(1, 100) <= 20:
				spawn_zombie()

			#second day mobs
			if time >= world.nighttime and day >= 2:
				#enderman
				if rng.rand_int(1, 100) <= 12:
					spawn_enderman()
					
				#witch
				if rng.rand_int(1, 100) <= 15:
					spawn_witch()

	#cave mobs
	elif location == "cave":
		if len(cave_hostile_mobs) < cave_hostile_mob_cap:
			#spider
			chance = 5
			if day >= 2:
				chance += 5
			if day >= 3:
				chance += 5
			if time >= world.nighttime:
				chance += 15
		
			if rng.rand_int(1, 100) <= chance:
				spawn_spider()


			
def move_mobs():
	#move all the mobs
	if location == "forest":
		for mob in forest_passive_mobs:
			mob_type = forest_passive_mobs[mob]["type"]
			if done:
				return
			#pig
			if mob_type == "pig":
				move_pig(mob)
				
		killed_mobs = []
		
		for mob in forest_hostile_mobs:
			if done:
				return
			mob_type = forest_hostile_mobs[mob]["type"]
			#zombie
			if mob_type == "zombie":
				res = move_zombie(mob)
				#when the zombie burns and dies
				if res == "kill":
					killed_mobs.append(mob)
			#enderman
			elif mob_type == "enderman":
				move_enderman(mob)
			#witch		
			elif mob_type == "witch":
				res = move_witch(mob)
				
		for i in killed_mobs:
			kill_mob(i, forest_hostile_mobs)
			
	elif location == "cave":
		for mob in cave_hostile_mobs:
			if done:
				return
			mob_type = cave_hostile_mobs[mob]["type"]
			#spider
			if mob_type == "spider":
				res = move_spider(mob)

	elif location == "end":
		move_enderdragon()
		for mob in end_hostile_mobs:
			if done:
				return
			mob_type = end_hostile_mobs[mob]["type"]
			#enderman in the end
			if mob_type == "enderman":
				res = move_enderman(mob, True)

				


#eating

food_list = {
	#food : health given by eating
	"meat" : 2,
	"rotten_flesh" : 1,
	"spider_eye": -2,
	"apple" : 3,
	"health_potion" : 8,
	"satay" : 3
}

def eat(m):
	
	if not m in food_list:
		print("You cannot eat that\n")
		return -1
	#check the player has the item
	if not player.have_item(m):
		print("You do not have any", m, "\n")
		return -1

	print("You consumed ",m,". ", sep="",end="")
	player.lose_item(m)
	healing = food_list[m]

	#heal health
	if healing >= 0:
		print("You heal ",healing, " health", sep ="")
		player.heal_health(healing)
	#damage health
	else:
		print("You take ",-healing, " damage", sep ="")
		player.damage_health(-healing)
		if player.get_health() <= 0:
			print("You were poisoned!")
			die()
	
	return 0
	


#inventory display

def print_inventory():
	print("Inventory")
	empty = True
	for p in player.inventory:
		if player.inventory[p] > 0:
			#star * tools that are currently used
			if p==player.pickaxe or p==player.sword or p==player.armour:
				print("*", end="")
			
			print(p, player.inventory[p], sep=": ")
			empty = False
	#if there is nothing, i.e. all 0
	if empty:
		print("(empty)")



#location change

def goto(m):
	global location
	global time
	
	if location == "forest":
			
		if m == "forest":
			print("You are already in the forest\n")
			return -1
		#go to cave
		elif m == "cave":	
			if player.location().cave == None:
				print("There is no cave here\n") 
				return -1

			player.enter_cave()
			location = "cave"
			desc_location(False)
		#go to end
		elif m == "end":
			#need end portal
			if not player.have_item("end_portal"):
				print("You need an end_portal to go to the end\n")
				return -1
			else:
				print("Entering the end...\n")
				print("You are in the end")
				location = "end"
				spawn_enderdragon()
				time = -1
				gain_xp(20)
			
		else:
			print("You cannot enter that\n")
			return -1
			
	elif location == "cave":
		
		if m == "cave":
			print("You are already in the cave\n")
			return -1
		#go back to forest
		if m == "forest":	
			location = "forest"
			player.exit_cave()
			
			desc_location(False)
		else:
			print("There is no", m, "here\n")
			return -1
	elif location == "end":
		if ed == {}:
			#go back to forest (after killing ed.)
			if m=="forest":
				global win
				global forest_hostile_mobs
				global day
				
				
				print("You return to the forest")
				location = "forest"
				if win == -1:
					win = moves + 1
					winning()
				forest_hostile_mobs = {}
				world.day += 1
				day += 1
				desc_location(False)
			else:
				print("You can't go there\n")
				return -1
		else:
			print("There is nowhere to hide\n")
			return -1
	return 0



#commands	

def make_move():

	#prompt
	#not case sensitive
	s = input("==> ").lower()
	
	m = s.split()
	global location
	global done
	global forest_surr
	global cave_surr
	global show_hearts
	global moves
	global time
	global day
	global cheats
	global cheated
	global luck

	#blank command
	if len(m) == 0:
		
		print("Expected command\n")
		return
	
	#exit game command
	elif m[0] == "done" or m[0] == "quit":
		#confirm message
		s = input("Are you sure you want to end the game? (YES/NO): ")
		if s == "YES":
			done = True
		else:
			print("Game continues")
		print("")
		return
	

	#hearts command
	elif m[0]=="hearts":
		#toggle
		show_hearts = not show_hearts
		print("")
		if show_hearts:
			player.print_hearts()
		return

	#details command
	elif m[0] == "details":
		print_details()
		print("")
		return

	#time command
	elif m[0] == "time" or m[0] == "t":
		print_time("\n\n")
		return

	#moves command
	elif m[0] == "moves":
		print_moves("\n\n")
		return

	#location command
	elif m[0] == "location" or m[0] == "where":
		print_location("\n\n")
		return

	#health command
	elif m[0] == "health" or m[0] == "h":
		print_health("\n\n")
		return

	#pickaxe command
	elif m[0] == "pickaxe" or m[0] == "pick" or m[0] == "pic"\
		 or m[0]=="tool" or m[0]=="tools":
		print_pickaxe("\n\n")
		return

	#sword command
	elif m[0] == "sword" or m[0] == "weapon":
		print_sword("\n\n")
		return

	#armour command
	elif m[0]=="armour" or m[0]=="armor" or m[0]=="protection":
		print_armour("\n\n")
		return

	#view command
	elif m[0] == "look" or m[0] == "view" or m[0]=="v":
		desc_location()
		print("")
		return

	#inventory command
	elif m[0]=="i" or m[0]=="e" or m[0]=="inventory":
		print_inventory()
		print("")
		return

	#mine command
	elif m[0]=="break" or m[0]=="mine" or m[0]=="destroy" \
		or m[0]=="harvest" or	m[0]=="gather" or m[0]=="dig"\
		or m[0]=="m" or m[0]=="collect" or m[0]=="take" or \
		m[0] == "get" or m[0]=="chop" or m[0]=="cut":
		if len(m) < 2:
			print("An object was expected\n")
			return

		s = m[1][0].upper() + m[1][1:]
		res = player.mine_structure(s)

		if res == -1:
			return		
			
	#go command
	elif m[0]=="go" or m[0]=="enter" or m[0]=="goto" \
		 or m[0]=="go_to" or m[0]=="into":
		if len(m) < 2:
			print("A location was expected\n")
			return
		
		res = goto(m[1])
		if res == -1:
			return

	#wait command		 
	elif m[0] == "wait" or m[0] == "w":
		print("Time passes")

	#back command
	elif m[0]=="out" or m[0]=="return" or \
		 m[0]=="back" or m[0]=="escape":
		#just go back to the forest
		res = goto("forest")
		if res == -1:
			return
			

	#craft command
	elif m[0] == "craft" or m[0] == "make" or m[0] == "create"\
		or m[0] == "c" or m[0] == "brew":
		if len(m) == 1:
			print("Expected an item to be crafted\n")
			return

		#need a crafting table if not in forest
		if location != "forest" and not player.have_item("crafting_table"):
			print("You need a crafting table to craft items when not in the forest!\n")
			return 
		
		res = items.craft(player, m[1])
		if res == -1:
			return
		
		#crafting table can break when not in forest
		if location != "forest" and rng.rand_int(1, 5) == 1:
			player.lose_item("crafting_table")
			print("Your crafting_table broke! crafting_table left:", end = " ")
			print(player.item_number("crafting_table"))


	#sleep command
	elif m[0] == "sleep":
		res = sleep()
		if res == -1:
			return

	#attack command
	elif m[0]=="attack" or m[0]=="kill" or[0]=="fight" or m[0]=="k":
		if len(m) == 1:
			print("Expected mob\n")
			return
		#enderdragon
		if (m[1] == "enderdragon" or m[1] == "ed") and\
			 ed != {} and location == "end":
			res = attack_enderdragon()
		#other mobs
		else:
			res = attack_mob(m[1])
		if res == -1:
			return

	#eat command
	elif m[0]=="eat" or m[0]=="drink" or m[0]=="consume":
		if len(m) == 1:
			print("Expected food item\n")
			return
		res = eat(m[1])
		if res == -1:
			return
		
	#open command
	elif m[0] == "open":
		if len(m) == 1:
			print("Expected object to open\n")
			return
		#open chest
		if m[1] != "chest":
			print("No such thing here\n")
			return

		res = open_chest()
		if res == -1:
			return

	elif m[0] == "move":
		if location == "end":
			print("You cannot move when in the end\n")
			return 
		if player.get_y_pos() != 1.0:
			print("You cannot move when in a cave\n")
			return 
		if len(m) == 1:
			print("Please specify move left or move right\n")
			return

		movement = 0
		if m[1] == "right":
			movement = 1
		elif m[1] == "left":
			movement = -1
		else:
			print("You can only move left or move right\n")
			return
		if not world.within_size_limit(player.get_x_pos() + movement):
			print("You have reached the world size limit\n")
			return
		else:
			res = player.move_pos(movement)
			if res == -1:
				return 

	elif m[0] == "chance":
		if player.get_y_pos() != 0.0:
			print("You are not in a cave\n")
			return 
		player.location().cave.toggle_show_chance()
		return 
		
	#cheats

	elif m[0] == "cheats":
		if len(m) == 1:
			print("Cheats on or cheats off?\n")
			return
		if m[1] == "off" or m[1] == "false":
			cheats = False
			print("Cheats turned off\n")
			return
		elif m[1] == "on" or m[1] == "true":
			cheats = True
			print("Cheats turned on\n")
			cheated = True
			return
		else:
			print("Cheats on or cheats off?\n")
			return
		
	#give command (cheats)
	elif m[0] == "give":
		if cheats == False:
			print("Enable cheats to use this command\n")
			return
		if len(m) == 1:
			print("Expected item\n")
			return
		item = m[1]
		k = 1
		try:
			k = int(m[2])
			if k < 0:
				k = 0
		except:
			pass
		if item == "gear":
			player.gain_item("diamond_sword")
			player.gain_item("diamond_pickaxe", 1)
			player.gain_item("diamond_armour", 1)
			player.gain_item("apple", 1000)
			player.gain_item("health_potion", 7)
			player.gain_item("end_portal")
			return
		if item not in items.item_list:
			print("No such item\n")
			return
		player.gain_item(item, k)
		print("")
		return
			

	#summon command (cheats)
	elif m[0] == "summon" or m[0] == "spawn":
		if cheats == False:
			print("Enable cheats to use this command\n")
			return 
		mob = ""
		try:
			mob = m[1]
		except:
			print("Expected mob\n")
			return

		#spawn the mob
		if location == "forest":
			if mob == "pig":
				spawn_pig()
			elif mob == "zombie":
				spawn_zombie()
			elif mob == "enderman":
				spawn_enderman()
			elif mob == "witch":
				spawn_witch()
			elif mob == "spider" or mob == "enderdragon" or mob == "ed":
				print("Sorry, you can't spawn that here\n")
				return
			else:
				print("No such mob\n")
				return
				
		elif location == "cave":
			if mob == "spider":
				spawn_spider()
			elif mob=="pig" or mob=="zombie" or mob=="enderman" or\
				 mob=="witch" or mob=="enderdragon" or mob=="ed":
				print("Sorrry, you can't spawn that here\n")
				return
			else:
				print("No such mob\n")
				return

		elif location == "end":
			if mob == "enderman":
				spawn_enderman(True)
			elif mob=="pig" or mob=="zombie" or mob=="spider" or\
				 mob=="witch" or mob=="enderdragon" or mob=="ed": 
				print("Sorry, you can't spawn that here\n")
				return
			else:
				print("No such mob\n")
				return
				
		print("")
		return

	#heal command (cheats)
	elif m[0] == "heal" or m[0] == "set_health":
		if cheats == False:
			print("Enable cheats to use this command\n")
			return
		
		new_health = 10
		try:
			new_health = float(m[1])
		except:
			print("Invalid health input\n")
			return

		if new_health*2 != int(new_health*2):
			print("Health must be an integer multiple of 0.5\n")
			return
		
		player.set_health(new_health)
		
		#die
		if player.get_health() <= 0:
			print("You were killed by thinking too hard")
			die()
		print("")
		return
	
	#luck command (cheats)
	elif m[0] == "luck" or m[0] == "set_luck":
		if cheats == False:
			print("Enable cheats to use this command\n")
			return
		new_luck = 1.0
		try:
			new_luck = float(m[1])
		except:
			print("Invalid luck input\n")
			return
		print("Changed luck from", luck, "to", new_luck)
		luck = new_luck
		print("")
		return

	elif m[0]=="game_rule" or m[0]=="gr" or m[0]=="gamerule":
		if not cheats:
			print("Enable cheats to use this command\n")
			return 
		if len(m) == 1:
			print("Expected game rule\n")
			return 
		if not m[1] in world.game_rules:
			print("No such gamerule found\n")
			return
		if len(m) == 2:
			print("Expected boolean value\n")
			return
		res = True
		if m[2] == "false":
			res = False
		elif m[2] == "true":
			res = True
		else:
			print("Value given should be a boolean\n")
			return 

		world.game_rules[m[1]] = res
		print("Game rule", m[1], "set to", res, "\n")
		return

			
			
	#command not recognised	
	else:
		print("The command ",m[0]," was not recognised", sep="\"")
		print("")
		return

	#if did not return, means it is an active move
	#increase number of moves and time 
	moves += 1
	
	if world.game_rules["daylight_cycle"]:
		if location == "forest" or location == "cave":
			time += 1
			world.time += 1
			check_time()

	#do all the other stuff that happens when time passes

	if world.game_rules["mob_attacking"]:
		move_mobs()

	if world.game_rules["mob_spawning"]:
		spawn_mobs()

	#if location == "forest":
		#grow_trees()
	
	if player.get_y_pos() == 0:
		player.location().cave.generate_ores()
	#generate_chest()

	

	#will print the enderdragon health if in the end
	print("")
	if location == "end":
		print_enderdragon_health()

	#will show the hearts if turned on
	if show_hearts:
		player.print_hearts()
	

def main():
	global done

	#start the game, intro
	intro()

	desc_location()

	print("")

	#keep inputting a move
	while True:
		make_move()
		if done:
			break


	#Game End
	print("Game Over!\n")

	#check if used cheats
	if cheated:
		print("Cheats were used in this game\n")
	else:
		print("No cheats were used\n")

	#print inventory, moves, and winning
		
	print_inventory()
	print("")
	print_moves("\n\n")
	print("Score:", score, "\n")

	winning()
	
	print("\nThank you for playing.")
	
main()

input("Enter anything to exit the program ")
