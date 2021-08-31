import rng

class Effect:
	def __init__(self, type, duration=0, level=1):
		self.type = type
		self.duration = duration
		self.level = level
	
	def get_type(self):
		return self.type
	def get_duration(self):
		return self.duration
	def get_level(self):
		return self.level
	
	def reduce_duration(self, t=1):
		self.duration -= t
		if self.duration <= 0:
			self.duration = 0
			return 0
		return 1

	def copy(self):
		return Effect(self.type, self.duration, self.level)

	def to_string(self):
		num = ' '+ rng.to_roman_numeral(self.level)
		if self.level == None:
			num = ""
		return self.type + num


effects_list = {
	"Regeneration": (1, 20),
	"Poison": (1, 20),
	"Hunger": (1, 20)
}

class Effects_list:
	def __init__(self):
		self.effects = []

	def search_index(self, effect_type):
		i = 0
		for eff in self.effects:
			if eff.type == effect_type:
				return i
			i += 1
		return -1

	def add_effect(self, eff):
		eff = eff.copy()
		searched = self.search_index(eff.type)
		if searched != -1:
			eff0 = self.effects[searched]
			if eff0.level < eff.level or eff0.duration < eff.duration:
				self.remove_effect(eff0)
				self.effects.append(eff)
				print("You got", eff.to_string(), " effect for", eff.duration, "time")
		else:
			self.effects.append(eff.copy())
			print("You got", eff.to_string(), "effect for", eff.duration, "time")

	def remove_effect(self, effect):
		self.effects.remove(effect)

	def remove_effect_index(self, i):
		del self.effects[i]

	def size(self):
		return len(self.effects)

	def update(self):
		removed = []
		for i in range(self.size()):
			e = self.effects[i]
			if e.duration <= 1:
				removed.append(i)
			else:
				e.reduce_duration()

		new_effects = []
		for i in removed:
			print(self.effects[i].to_string(), "effect wore off")
		for i in range(len(self.effects)):
			if i not in removed:
				new_effects.append(self.effects[i])
		self.effects = new_effects		

	def print(self):
		for eff in self.effects:
			print(eff.to_string()+",", eff.duration, "duration")
		if len(self.effects) == 0:
			print("None")