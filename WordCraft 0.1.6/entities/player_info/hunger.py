import rng
from entities import effects

class Food_type:
	def __init__(self, hunger=0.0, sat_ratio=1.0, effects=[], need_hunger=True):
		self.hunger = hunger
		self.sat_ratio = sat_ratio
		self.effects = effects
		self.need_hunger = need_hunger


# bad: 0.3
# uncooked: 0.7
# ok: 1.0
# cooked: 1.3
# good: 1.6

food_stats= {
#food : (hunger, saturation ratio)
	"raw_pork" : Food_type(1.5, 0.7),
	"cooked_pork": Food_type(3.0, 1.3), 
	"rotten_flesh" : Food_type(0.5, 0.3, effects=[
		effects.Effect(
			"Hunger", 
			duration=3, 
			level=1)
	]),
	"spider_eye": Food_type(1.0, 0.3, effects=[
		effects.Effect(
			"Poison", 
			duration=3, 
			level=1)
	]),
	"apple" : Food_type(2.0, 1.0),
	"health_potion" : Food_type(effects=[
		effects.Effect(
			"Regeneration", 
			duration=4, 
			level=2)
	], need_hunger=False),
	"satay" : Food_type(1.5, 1.0)
}


class Hunger:

	healing_min_hunger = 2.0

	def __init__(self):
		self.hunger = 10.0
		self.max_hunger = 10.0
		self.saturation = 4.0
	

	def lose_hunger(self, x):
		self.hunger -= x
		if self.hunger < 0.0:
			self.hunger = 0.0


	def lose_saturation(self, x):
		self.saturation -= x
		lost_hunger = 0.0
		while self.saturation < -0.000000001:
			self.saturation += 0.5
			lost_hunger += 0.5
		if lost_hunger > 0.0:
			self.lose_hunger(lost_hunger)
	

	def exhaust(self, exh):
		self.lose_saturation(exh)


	def increase_hunger(self, x):
		self.hunger += x
		if self.hunger > self.max_hunger:
			exceeded = self.hunger - self.max_hunger
			self.hunger = self.max_hunger
			return exceeded
		return 0.0


	def increase_saturation(self, x):
		self.saturation += x
		if self.saturation > self.hunger:
			exceeded = self.saturation - self.hunger
			self.saturation = self.hunger
			return exceeded
		return 0.0


	def split(self, x):
		sat = rng.floor_round(x/2, 0.5)
		hung = x - sat
		return (hung, sat)


	def drain_hunger(self, x, bonus=False):
		if bonus:
			if self.hunger > self.healing_min_hunger and rng.chance(50):
				self.hunger -= 0.5
				x -= 0.5
			self.saturation -= x
		else:
			hs = self.split(x)
			self.hunger -= hs[0]
			self.saturation -= hs[1]
		if self.saturation < 0.0:
			self.saturation = 0.0
		if self.hunger < 0.0:
				self.hunger = 0.0


	def eat(self, hung, sat_ratio):
		extra_hunger = self.increase_hunger(hung)
		sat = (hung - 0.3*extra_hunger) * sat_ratio
		self.increase_saturation(sat)


	def get_healing(self, bonus=True):
		if self.hunger <= self.healing_min_hunger:
			return 0.0
		
		amount = 0.0
		if not bonus:
			if self.saturation <= 0.6:
				amount = 0.5
			else:
				amount = 1.0
		else:
			if self.saturation <= 0.2:
				amount = 0.5
			elif self.saturation <= 0.5:
				amount = 1.0
			elif self.saturation <= 0.8:
				amount = 1.5
			else:
				amount = 2.0
	
		if not bonus:
			hs = self.split(amount)
			if self.hunger - hs[0] <= self.healing_min_hunger:
				amount = self.hunger - self.healing_min_hunger
				hs = self.split(amount)
			if self.saturation - hs[1] < 0.0:
				amount = rng.floor_round(self.saturation * 2)
		else:
			if self.saturation < amount:
				amount = rng.floor_round(self.saturation)
		return amount

	def set_hunger(self, new_hunger, msg=True):
		if new_hunger > 10.0:
			new_hunger = 10.0
		if new_hunger < 0.0:
			new_hunger = 0.0
		self.hunger = new_hunger
		if self.saturation > self.hunger:
			self.saturation = self.hunger
		if msg:
			print("You now have", self.hunger, "hunger\n")

		


		