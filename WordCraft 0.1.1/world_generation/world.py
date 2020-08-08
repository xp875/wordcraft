from world_generation import location




class World:
	nighttime = 20
	daytime = 36
	size_limit = 256

	def __init__(self):
		self.seed = 0
		
		first_location = location.Location(self, 0.0)
		self.map = {0: first_location}

		self.time = 0
		self.day = 1

		self.game_rules = {
			"daylight_cycle" : True,
			"mob_spawning" : True,
			"mob_attacking" : True, 
			#"mob_loot" : True,
			"structure_drops" : True,
			#"can_respawn": True
			#"keep_inventory" : False, 
			#"natural_regeneration" : True,
			#"fire_damage" : True,
		}


	def get_first_biome(self):
		return self.map[0].biome

	def is_loaded(self, x_pos):
		return x_pos in self.map

	def within_size_limit(self, x_pos):
		if x_pos >= self.size_limit /2:
			return False
		if x_pos < -self.size_limit/2:
			return False
		return True

	def generate_location(self, x_pos):
		if x_pos in self.map:
			return
		if not self.within_size_limit(x_pos):
			return
		self.map[x_pos] = location.Location(self, x_pos)

	def get_location(self, x_pos):
		return self.map[x_pos]
