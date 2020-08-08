import rng
import items
from world_generation import structures

class Player:

	def __init__(self, world):

		self.world = world

		self.moves = 0

		self.health = 10.0
		self.max_health = 10.0

		self.score = 0

		self.pos = [0.0, 1.0]
		self.velocity = 0.0

		self.inventory = {}

		self.pickaxe = "nothing"
		self.mining_strength = 0

		self.sword = "nothing"
		self.attack_damage = 1

		self.armour = "nothing"
		self.armour_protection = 0


	def location(self):
		return self.world.get_location(self.pos[0])

	def move_pos(self, difference):
		if self.get_y_pos() != 1.0:
			print("You cannot move when in the cave\n")
			return -1
		if not self.world.within_size_limit(self.pos[0]+difference):
			return
		self.pos[0] += difference
		if not self.world.is_loaded(self.pos[0]):
			self.world.generate_location(self.pos[0])
		self.world.get_location(self.pos[0]).describe()
		self.print_pos()
		return 0

	def get_x_pos(self):
		return self.pos[0]

	def get_y_pos(self):
		return self.pos[1]

	def get_pos(self):
		return tuple(self.pos)
	
	def print_pos(self):
		print("Position:", self.get_pos())

	def get_health(self):
		if self.health == int(self.health):
			return int(self.health)
		return self.health

	def print_health_sentence(self):
		print("You now have", self.get_health(), "health")

	def set_health(self, new_health):
		#cap at 10
		if new_health > 10.0:
			new_health = 10.0
		#cap at 0
		if new_health < 0.0:
			new_health = 0.0
  
		self.health = new_health
		self.print_health_sentence()

	def heal_health(self, amount):
		self.set_health(self.health + amount) 

	def damage_health(self, amount):
		self.set_health(self.health - amount) 

	def print_hearts(self):
		# (\/)(\/)::::
		#  \/  \/  :: 
		a = int(self.health)*"(\/)"
		b = int(self.health)*" \/ "
		if self.health != int(self.health):
			a += "(\\"
			b += " \\"

		a += (10-int(self.health))*"::::"
		b += (10-int(self.health))*" :: "

		print(a+"\n"+b)

	def enter_cave(self):
		if self.location().cave == None:
			return -1
		self.pos[1] -= 1
		return 0

	def exit_cave(self):
		if self.pos[1] != 0.0:
			return -1
		self.pos[1] = 1.0
		return 0

	def update_pickaxe(self, m, e=""):
		if m not in items.pickaxes:
			return 
		if self.mining_strength < items.pickaxes[m]:
			self.pickaxe = m
			self.mining_strength = items.pickaxes[m]
			print("You are now using", m, e)

	def update_sword(self, m, e=""):
		if m not in items.swords:
			return
		if self.attack_damage < items.swords[m]:
			self.sword = m
			self.attack_damage = items.swords[m]
		
		print("You are now using ", m, " (", \
					self.attack_damage, " attack damage)"+e, sep = "")

		
	def update_armour(self, m, e = ""):
		if m not in items.armour:
			return
		if self.armour_protection < items.armour[m]:
			self.armour = m
			self.armour_protection = items.armour[m]
			print("You are now eqquiped with ", m, " (", \
					self.armour_protection, " protection)"+e, sep = "")
		
	def update_all(self, m, e=""):
		self.update_armour(m, e)
		self.update_pickaxe(m, e)
		self.update_sword(m, e)

	def gain_item(self, item, n=1, message=True):
		if item not in self.inventory:
			self.inventory[item] = n
		else:
			self.inventory[item] += n
		if message:
			print("You gained", n, item)
		self.update_all(item)

	def lose_item(self, item, n=1):
		if item not in self.inventory:
			return -1
		if self.inventory[item] < n:
			return -1
		if self.inventory[item] == n:
			del self.inventory[item]
		else:
			self.inventory[item] -= n
		return 0

	def have_item(self, item):
		return item in self.inventory

	def item_number(self, item):
		if not self.have_item(item):
			return 0
		return self.inventory[item]


	def mine_structure(self, s):
		place = self.location()
		if self.get_y_pos() == 0.0:
			place = self.location().cave
		
		if not place.have_structure(s) or place.structure_number(s) == 0:
			print("There is no", s, "here\n")
			return -1
		if structures.structure_list[s].hardness > self.mining_strength:
			pickaxe = items.power_to_pickaxes[structures.structure_list[s].hardness]
			print("You need a", pickaxe,"or better to mine", s, "\n")
			return -1


		place.remove_structure(s)
		if self.get_y_pos() == 0:
			self.location().cave.increase_progress(self.mining_strength)
		if self.world.game_rules["structure_drops"]:
			drops = structures.structure_list[s].drop()
			for i in drops:
				self.gain_item(i, drops[i])
			
		return 0
	


	