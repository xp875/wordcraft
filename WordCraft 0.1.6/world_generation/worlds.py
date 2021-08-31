from world_generation import location
from world_generation import position
import rng

class World:
	nighttime = 20
	daytime = 36

	size_limit = 128
	number_limit = 2**32

	def is_generated(self, pos):
		m = self.map[pos.dimension]
		return pos.get_xy() in m

	def within_size_limit(self, pos):
		for i in pos.get_xy():
			if i >= self.size_limit /2:
				return False
			if i < -self.size_limit/2:
				return False
		return True

	def generate_location(self, pos):
		if self.is_generated(pos):
			return
		if not self.within_size_limit(pos):
			return
		self.map[pos.dimension][pos.get_xy()] = location.Location(self, pos, self.location_seed[pos.get_xy()])

	def set_location_seeds(self):
		seeds = {}
		pt = 0
		do = [(0, 0)]

		dy = [0, 0, 1, -1]
		dx = [1, -1, 0, 0]

		while pt < len(do):
			pt += 1

			if do[pt-1] in seeds:
				continue
			
			seeds[do[pt-1]] = rng.rand_int(-self.number_limit//2, self.number_limit//2-1)
			#print(curr)

			for j in range(4):
				new = (do[pt-1][0]+dx[j], do[pt-1][1]+dy[j])
				can = True
				for i in new:
					if i >= self.size_limit /2 or i < -self.size_limit/2:
						can = False
						break
				if can: 
					do.append(new)
			
		return seeds


	def __init__(self, seed):
		self.seed = seed

		rng.set_seed(self.seed)
		self.location_seed = self.set_location_seeds()

	
		self.map = {"O": {}, "N": {}, "E": {}}

		self.spawn_pos = position.Pos(0, 0)
		self.loaded = []

		for i in range(-8, 8):
			for j in range(-8, 8):
				pos = position.Pos(i, j)
				self.generate_location(pos)
		self.generate_location(position.Pos(0, 0, "E"))

		self.time = 0
		self.day = 1

		self.game_rules = {
			"Do Daylight Cycle" : True,
			"Spawn Mobs" : True,
			"Mobs Attack" : True, 
			#"mob_loot" : True,
			"Structures Drop" : True,
			#"Use Item Durability": True,
			#"can_respawn": True
			#"keep_inventory" : False, 
			"Lava Damage" : True,
			"Natural Regeneration": True,
		}
		self.difficulty = 2


	def get_location(self, pos):
		return self.map[pos.dimension][pos.get_xy()]

	def get_spawn(self):
		return self.spawn_pos

	def check_time(self):
		if location == "end":
			self.time = -1
		elif self.time == self.nighttime:
			#prints a message when it reaches night time
			print("\nIt is now night! Sleep or beware of monsters!")
		elif self.time == self.daytime:
			self.time = 0
			self.day += 1
			#prints a message when it reaches day time (new day)
			print("\nIt is now day. It is day", self.day)

	def print_game_rules(self, change):
		gr = []
		for i in self.game_rules:
			gr.append(i)
			print(len(gr), end=") ")
			print(i, self.game_rules[i], sep=": ")
		print("")

		if not change:
			return 

		x = input("Change: ")
		try:
			i = int(x) - 1
			if i < 0 or i >= len(gr):
				print("Out of range\n")
				return -1
			b = self.game_rules[gr[i]] 
			self.game_rules[gr[i]] = not b
			print(gr[i], "changed from", b, "to", not b, '\n')
			return
		except:
			print("Expected number", '\n')
			return -1
