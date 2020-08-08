class Mob:

	def __init__(self, max_health, health):
		self.max_health = max_health
		self.health = health
		self.name = ""
		self.lifetime = 0

	def update(self):
		self.lifetime += 1

	def die(self):
		pass

	def take_damage(self, damage):
		if self.health < damage:
			self.die()
		else:
			self.health -= damage

		

class Zombie(Mob):
	def __init__(self):
		super.__init__()
		self.attack_damage = (1.5, 2.5)


