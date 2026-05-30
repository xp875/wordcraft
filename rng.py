import random
import math

def set_seed(seed=None):
	if seed != None:
		random.seed(seed)

def rand_int(a, b):
	return random.randint(a, b)

def rand_float():
	return random.random()

def chance(percentage):
  return rand_float()*100 <= percentage

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

	def choose(self, seed=None):
		if type(self.range) == type(1):
			return self.range

		elif type(self.range) ==  type(()):
			set_seed(seed)
			return rand_int(self.range[0], self.range[1])
			
		elif type(self.range) == type({0:0}):
			set_seed(seed)
			r = rand_int(1,10000)/100
			for i in self.range:
				if r<=self.range[i]:
					return i
				r -= self.range[i]
			return 0

def logarithmic(x, f0, fn, n):
	a = (fn - f0)/math.log(n+1)
	f = a*math.log(x+1)+f0
	return f


def floor_round(x, accuracy=0.5):
	return x//accuracy*accuracy

def rand_round(x, accuracy=0.5):
	base = floor_round(x, accuracy)
	extra = x-base
	add_extra = chance(extra/accuracy*100)
	if add_extra:
		return base+accuracy
	else:
		return base

def to_roman_numeral(x):
	roman_numeral = {
		1: "I",
		2: "II",
		3: "III",
		4: "IV",
		5: "V",
		6: "VI",
		7: "VII",
		8: "VIII",
		9: "IX",
		10: "X"
	}
	if x in roman_numeral:
		return roman_numeral[x]
	return str(x)