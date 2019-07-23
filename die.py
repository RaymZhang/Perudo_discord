from random import randrange

class Die(object):

	def __init__(self):
		self.roll()

	def roll(self):
		self.value = randrange(1,7)