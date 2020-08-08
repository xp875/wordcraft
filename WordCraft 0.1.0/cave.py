import math
import rng

def logarithmic(x, f0, fn, n):
	a = (fn - f0)/math.log(n+1)
	f = a*math.log(x+1)+f0
	return f


class Cave: 
	max_stone = 16

	# Name : (f0, f16)
	ores = {
		#"Stone" : (0, 0),
		#"Coal" : (34, 44),
		"Iron" : (18, 33),
		"Diamond" : (3, 20),
		#"Water" : (20, 17),
		#"Lava" : (4, 36)
	}
	
	def __init__(self, location):
		self.location = location
		stone = rng.slanted(self.max_stone)
		self.structures = {}
		for ore in self.ores:
			self.structures[ore] = 0
		self.structures["Stone"] = stone
		self.progress = 0.0
		self.immediate_progress = False
		self.show_chance = False
		

	def describe(self):
		print("You are in the cave in a", self.location.biome)
		for i in self.structures:
			if self.structures[i] > 0:
				print("There is", self.structures[i], i)
		print("Progress:", self.progress)

	def toggle_show_chance(self):
		self.show_chance = not self.show_chance
		if self.show_chance:
			print("Now showing chance of ore generation\n")
		else:
			print("Now not showing chance of ore generation\n")
		return 0

	def generate_ores(self):
		for ore in self.ores:
			probability = logarithmic(self.progress, self.ores[ore][0], self.ores[ore][1], self.max_stone)

			if self.immediate_progress:
				if self.show_chance:
					print(ore+":", rng.percentage(probability))
				if rng.chance(probability):
					print("\nYou unearthed", ore)
					self.structures[ore] += 1
			else:
				if self.show_chance:
					print(ore+":", rng.percentage(probability/2))
				if rng.chance(probability/2):
					print("\nYou found", ore)
					self.structures[ore] += 1
		self.immediate_progress = False


	def have_structure(self, s):
		return s in self.structures
	
	def structure_number(self, s):
		if not self.have_structure(s):
			return -1
		return self.structures[s]

	def remove_structure(self, ore, n=1):
		self.structures[ore] -= n

	def increase_progress(self, x=1.0):
		self.progress += x
		self.immediate_progress = True

