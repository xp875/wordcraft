import rng
from world_generation import place
from world_generation import structures


class Cave(place.Place): 
	name = "Cave"

	# Name : (f0, f16)
	ores = {
		#"Stone" : (0.0, 0.0),
		"Coal" : (19.0, 25.0),
		"Iron" : (14.0, 26.0),
		"Diamond" : (2.0, 14.0),
		"Water" : (16.0, 16.0),
		"Magma" : (7.0, 26.0)
	}
	
	def __init__(self, location):
		super().__init__()

		self.location = location
		self.structures["Stone"] = rng.rand_int(10, 16)

		self.progress = 0.0
		self.immediate_progress = False
		self.player_placed = 0

		self.show_chance = False
		

	def describe(self):
		print("You are in the cave in a", self.location.biome)
		super().describe()
		rounded = int(self.progress*100+0.1)/100
		print("PROGRESS:", rounded)

	def toggle_show_chance(self):
		self.show_chance = not self.show_chance
		if self.show_chance:
			print("Now showing chance of ore generation\n")
		else:
			print("Now not showing chance of ore generation\n")
		return 0


	def generate_ores(self):
		x = self.progress
		for ore in self.ores:
			f0 = self.ores[ore][0]
			f1 = self.ores[ore][1]
			
			probability = rng.logarithmic(x, f0, f1, 16)

			a = "You unearthed" 
			if not self.immediate_progress:
				probability *= 0.4
				a = "You found"
			if self.location.world.day == 1:
				if ore=="Diamond":
					probability *= 0.2
			if self.show_chance:
				print(ore+":", rng.percentage(probability))
			if rng.chance(probability):
				print("\n"+a, ore)
				if self.have_structure(ore):
					self.structures[ore] += 1
				else:
					self.structures[ore] = 1

				if structures.structure_list[ore].is_fluid:
					self.update_fluids(ore)
					
			
		self.immediate_progress = False


	def increase_progress(self, x=1.0):
		self.progress += x
		self.immediate_progress = True


sample_cave = Cave(None)