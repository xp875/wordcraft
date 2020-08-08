import random


def rand_int(a, b, seed=None):
    if seed != None:
        random.seed(seed)
    return random.randint(a, b)


def chance(percentage):
    return rand_int(1, 10000) <= percentage * 100

def percentage(x):
	return str(int(x*100)/100) + "%"

def weighted_choice(sample_space, seed=None):
    tot = 0

    for i in sample_space:
        tot += sample_space[i][0]
    res = rand_int(1, tot, seed)
    for i in sample_space:
        if res <= sample_space[i][0]:
            return i
        res -= sample_space[i][0]
    return -1


def choice(l):
    n = len(l)
    return l[rand_int(0, n - 1)]


def slanted(n):
    tot = n*(n + 1) / 2
    res = rand_int(1, tot)
    for i in range(n, 0, -1):
        if res <= i:
            return i
        res -= i


class Rand_range:
	def __init__(self, range):
		self.range = range

	def choose(self):
		if type(self.range) == type(1):
			return self.range

		elif type(self.range) ==  type(()):
			return rand_int(self.range[0], self.range[1])
			
		elif type(self.range) == type({0:0}):
			r = rand_int(1,10000)/100
			for i in self.range:
				if r<=self.range[i]:
					return i
				r -= self.range[i]
			return 0