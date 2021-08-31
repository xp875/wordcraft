class Pos:
	def __init__(self, x, y, dimension="O"):
		self.x = x
		self.y = y
		self.dimension = "O"

	def get_xy(self):
		return (self.x, self.y)

	def get_dxy(self):
		return (self.dimension, self.x, self.y)

	def equals(self, pos2):
		return self.x == pos2.x and self.y == pos2.y and self.dimension == pos2.dimension
