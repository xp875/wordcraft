
from entities.player_info import inventory
from entities.player_info import hunger
import rng
import items
from world_generation import structures
from entities import effects



class Player:
	def __init__(self, world):

		self.pos = world.spawn_pos

		self.world = world
		self.location = world.get_location(self.pos)
		self.place = self.location

		self.moves = 0

		self.health = 10.0
		self.max_health = 10.0

		self.hunger = hunger.Hunger()

		self.effects = effects.Effects_list()

		self.xp = 0

		self.inventory = inventory.Inventory()
		
		self.has_won = False
		self.winning_moves = -1
		self.cheats = False
		self.has_cheated = False

		self.advancements = {
			"Stone Age": False,
			"Getting an Upgrade": False,
			"Acquire Hardware": False,
			"Suit Up": False,
			"Hot Stuff": False,
			"Team Trees": False, 
			"Stike!": False,
			"Mine All Day": False,
			"Obsidian": False,
			"Diamonds!": False,
			"Cover me with Diamonds": False,
			"The End": False,
			"Free the End": False,
		}

	def get_location(self):
		return self.location

	def get_place(self):
		return self.place

	def is_in_place(self, place):
		if self.location == self.place:
			return False
		for i in self.location.places:
			if i.name == place:
				return True
				
		return False

	def set_pos(self, new_pos):
		if self.place != self.location:
			return -1
		if not self.world.within_size_limit(new_pos):
			return -1
		
		if not self.world.is_generated(new_pos):
			self.world.generate_location(new_pos)
		self.pos = new_pos
		self.location = self.world.get_location(self.pos)
		self.place = self.location
		self.location.describe()
		self.print_pos()
		return 0

	def get_x_pos(self):
		return self.pos.x

	def get_y_pos(self):
		return self.pos.y
	
	def get_dimension(self):
		return self.pos.dimension

	def get_pos(self):
		return self.pos.get_xy()

	def print_pos(self):
		print("POSITION: ", self.pos.x, ", ", self.pos.y, sep="")

	def get_health(self):
		if self.health == int(self.health):
			return int(self.health)
		return self.health

	def print_health_sentence(self):
		print("You now have", self.get_health(), "health")

	def set_health(self, new_health, msg=True):
		#cap at 10
		if new_health > 10.0:
				new_health = 10.0
		#cap at 0
		if new_health < 0.0:
				new_health = 0.0

		self.health = new_health
		if msg:
			self.print_health_sentence()

	def heal_health(self, amount, msg=True):
		self.set_health(self.health + amount, msg)

	def damage_health(self, amount):
		self.set_health(self.health - amount)

	def print_hearts(self):
		s = ""
		s += "Health: " 
		s += '/'*int(self.health*2)
		s += '.'*int((self.max_health-self.health)*2)
		s += "\nHunger: "
		s += '/'*int(self.hunger.hunger*2)
		s += '.'*int((self.hunger.max_hunger-self.hunger.hunger)*2)
		
		s += "   " 
		stroke_saturation = True
		if stroke_saturation:
			satp = 0
			sat = (0.5, 1.5, 3.5, 6.0, 8.5)
			for i in sat:
				if self.hunger.saturation >= i:
					satp += 1
				else:
					break
			s += satp*"/" + (5-satp)*"."	
		else:
			s += format(self.hunger.saturation, ".3f")		
		
		print(s)
		
		return
		# (\/)(\/)::::
		#	 \/	 \/	 ::
		a = int(self.health) * "(\/)"
		b = int(self.health) * " \/ "
		if self.health != int(self.health):
				a += "(\\::"
				b += " \\: "

		a += int(10 - self.health) * "::::"
		b += int(10 - self.health) * " :: "

		print(a + "\n" + b)

	def enter_place(self, place):
		for i in self.location.places:
			if i.name == place:
				self.place = i
				return 0
		return -1

	def exit_place(self):
		if self.place == self.location:
			return -1
		self.place = self.location
		return 0


	def gain_item(self, item, n=1, message=True):
		if items.is_ust(item):
			i = items.Ust_item(item)
			self.inventory.add_ust_item(i)
			if message:
				print("You got:", end=" ")
				i.print()
			self.inventory.update_item(i)
			return

		self.inventory.add_st_item(item, n)
		if message:
			print("You got: ", item, " ×", n, sep="")

	def lose_item(self, item, n=1):
		if items.is_ust(item):
			return -1

		self.inventory.remove_st_item(item, n)
		

	def mine_structure(self, s):
		place = self.place

		if not place.have_structure(s) or place.structure_number(s) == 0:
			print("There is no", s, "here\n")
			return -1
		if structures.structure_list[s].hardness > self.inventory.get_power("tool"):
				pickaxe = items.power_to_pickaxes[structures.structure_list[s].hardness]
				print("You need a", pickaxe, "or better to mine", s, "\n")
				return -1

		if structures.structure_list[s].is_fluid:
			if not self.inventory.has_st_item("bucket"):
					print("You need a bucket to collect fluids\n")
					return -1
			self.lose_item("bucket")

		place.remove_structure(s)
		if self.is_in_place("Cave"):
			if structures.structure_list[s].hardness >= 1.0:
				if self.place.player_placed > 0:
					self.place.player_placed -= 1
				else:
					self.place.increase_progress(self.inventory.get_power("tool"))

		if self.inventory.inventory["tool"]!= None and structures.structure_list[s].hardness > 0:
			self.inventory.inventory["tool"].lose_durability()
			self.inventory.update_equipment()
		self.hunger.exhaust(0.1)

		if self.world.game_rules["Structures Drop"]:
			drops = structures.structure_list[s].drop()
			for i in drops:
					self.gain_item(i, drops[i])

		return 0


	def place_structure(self, s):
		struc = None
		item = None

		s = s[0].upper()+s[1:].lower()
		if s in structures.structure_list:
			item = structures.structure_list[s].placed_from
			struc = s
		else:
			item = s[0].lower()+s[1:]
			if item not in items.item_list:
				print("No such structure\n")
				return -1
			if item not in structures.item_to_structure:
				print("You cannot place this\n")
				return -1
			struc = structures.item_to_structure[item]

		if self.cheats == False and not self.inventory.has_st_item(item):
			print("You do not have", item, "\n")
			return -1

		displaced_fluid = False
		if structures.structure_list[struc].is_solid:
			fluids = []
			for i in self.place.structures:
				if structures.structure_list[i].is_fluid:
					fluids.append(i)
			
			if len(fluids) > 0:	
				done = False
				choices = ""
				abb = {}
				for i in fluids:
					choices += i[0] + "/"
					abb[i[0]] = i
				choices+="blank"

				while not done:
					f = input("Fluid to displace ("+choices+"): ")
					
					if f != "":
						if f.upper() in abb:
							f = abb[f.upper()]
						else:
							f = f[0].upper() + f[1:]

						if f not in abb.values():
							print("There is no", f, "here")
						else:
							self.place.remove_structure(f)
							print("You placed down", struc, "in", f)
							done = True
							displaced_fluid = True
					else:
						done = True

		if not displaced_fluid:
			print("You placed down", struc)
			
		self.place.add_structure(struc)

		if self.cheats == False:
			self.lose_item(item)

		if structures.structure_list[struc].is_fluid:
			if self.cheats == False:
				self.gain_item("bucket", 1, False)
			self.place.update_fluids(struc)

		if self.is_in_place("Cave") and structures.structure_list[struc].hardness > 0.0:
			self.place.player_placed += 1
		return 0


	def eat_food(self, item):
		if item not in hunger.food_stats:
			print("You can't eat that\n")
			return -1
		food_stat = hunger.food_stats[item]
		if food_stat.need_hunger and self.hunger.hunger == self.hunger.max_hunger:
			print("You are already at max hunger\n")
			return -1
		if not self.inventory.has_st_item(item):
			print("You do not have", item, "\n")
			return -1

		self.inventory.remove_st_item(item)
		
		hung = food_stat.hunger
		sat_rat = food_stat.sat_ratio

		if hung > 0:
			self.hunger.eat(hung, sat_rat)
			#print(hung, sat)
			print("You ate", item+". You now have", self.hunger.hunger, "hunger")
		else:
			print("You consumed", item)

		for eff in food_stat.effects:
			self.effects.add_effect(eff)	
		return food_stat.need_hunger


	def regenerate_health(self, bonus=False):
		if not self.world.game_rules["Natural Regeneration"]:
			return
		if self.health == self.max_health:
			return
		
		heal = self.hunger.get_healing(bonus)
		if heal + self.health > self.max_health:
			heal = self.max_health-self.health
		if heal == 0.0:
			return
		self.hunger.drain_hunger(heal, bonus)
		self.heal_health(heal, False)
		print("\nYou healed", heal, "health. You now have", self.health, "health")


	def update_effects(self):
		for eff in self.effects.effects:
			if eff.type == "Regeneration":
				healing = 0.5*eff.level
				self.heal_health(healing, False)
				print("\nYou healed", healing, "health from", eff.to_string(), "effect")
				print("You now have", self.health, "health")
			elif eff.type == "Hunger":
				hung = 0.5*eff.level
				self.hunger.lose_hunger(hung)
			elif eff.type == "Poison":
				damage = 0.5*eff.level
				if self.health - damage > 0:
					self.health -= damage
					print("\nYou lost", damage, "health from", eff.to_string(), "effect")
		self.effects.update()
	


	def winning(self):
		if self.winning_moves >= 0:
			print("You have completed the game! Great job!\n")
			print("Moves taken to complete:", self.winning_moves)
			if self.has_cheated == False:
				with open("winning.txt", "a") as win:
					win.write(str(self.winning_moves))
				#grades your winning
				if self.winning_moves <= 200:
					print("That is legendary!")
				elif self.winning_moves <= 300:
					print("That is epic!")
				elif self.winning_moves <= 400:
					print("That is superb!")
				elif self.winning_moves <= 500:
					print("That is awesome!")
				else:
					print("That is great!")
			else:
				print("That is great!")
			print("")


	def update(self):
		if self.world.game_rules["Lava Damage"] and self.place.have_structure("Lava"):
			damage = 2
			print("\nLava burnt you!")
			self.damage_health(damage)
		self.update_effects()
			
			