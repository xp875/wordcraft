import math
import rng
from world_generation import place

def logarithmic(x, f0, fn, n):
	a = (fn - f0)/math.log(n+1)
	f = a*math.log(x+1)+f0
	return f


class Cave(place.Place): 
	max_stone = 16

	# Name : (f0, f16)
	ores = {
		#"Stone" : (0.0, 0.0),
		#"Coal" : (34.0, 44.0),
		"Iron" : (14.0, 25.0),
		"Diamond" : (2.0, 15.0),
		#"Water" : (20.0, 17.0),
		#"Lava" : (4.0, 36.0)
	}
	
	def __init__(self, location):
		super().__init__()

		self.location = location
		stone = rng.slanted(self.max_stone)

		self.structures["Stone"] = stone
		self.progress = 0.0
		self.immediate_progress = False
		self.show_chance = False
		

	def describe(self):
		print("You are in the cave in a", self.location.biome)
		super().describe()
		rounded = int(self.progress*100+0.1)/100
		print("Progress", rounded)

	def toggle_show_chance(self):
		self.show_chance = not self.show_chance
		if self.show_chance:
			print("Now showing chance of ore generation\n")
		else:
			print("Now not showing chance of ore generation\n")
		return 0

	def generate_ores(self):
		x = self.progress
		n = self.max_stone
		for ore in self.ores:
			f0 = self.ores[ore][0]
			f1 = self.ores[ore][1]
			
			probability = logarithmic(x, f0, f1, n)

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
			
		self.immediate_progress = False


	def increase_progress(self, x=1.0):
		self.progress += x
		self.immediate_progress = True

