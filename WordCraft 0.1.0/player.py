import rng


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

	def gain_item(self, item, n=1, message=True):
		if item not in self.inventory:
			self.inventory[item] = n
		else:
			self.inventory[item] += n
		if message:
			print("You gained", n, item)

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
		if self.get_y_pos() == 0.0:
			if not self.location().cave.have_structure(s):
				print("There is no", s, "here\n")
				return -1
			if self.location().cave.structure_number(s) == 0:
				print("You have not found", s, "\n")
				return -1
			self.location().cave.remove_structure(s)
			self.location().cave.increase_progress()
			self.gain_item(self.world.structure_to_item[s])
			
			return 0
		
		elif self.get_y_pos() == 1.0:
			if not self.location().have_structure(s):
				print("There is no", s, "here\n")
				return -1
			if self.location().structure_number(s) == 0:
				print("There is no more", s, "\n")
				return -1
			
			if s == "Tree" or s == "Wood":
				print("You chopped down a tree. You gain 4 wood", end = "")
				self.gain_item("wood", 4, False)
				if rng.chance(75):
					print(", 1 stick", end = "")
					self.gain_item("stick", 1, False)
				if rng.chance(25):
					print(", 1 apple", end = "")
					self.gain_item("apple", 1, False)	
				print("")
				self.location().remove_structure(s)
				
			else:
				self.location().remove_structure(s)
				self.gain(self.world.structure_to_item[s])

			return 0

	
