from bet_exceptions import InvalidBetException
from bet_exceptions import InvalidDieValueException
from bet_exceptions import InvalidNonWildcardQuantityException
from bet_exceptions import InvalidWildcardQuantityException
from bet_exceptions import NonPalificoChangeException

class Bet(object):

	def __init__(self, quantity, value):
		self.quantity = quantity
		self.value = value

	def __repr__(self):
		return '{0}x {1}'.format(self.quantity, self.value)

DUDO = Bet(quantity=-1, value=1)

def create_bet(quantity, value, last_bet, player, game):
	"""Decide whether proposed bet is valid given the last bet. If it is valid, return a new Bet.
	Otherwise, throw the relevant exception.
	"""
	if value not in range(1, 7):
		raise InvalidDieValueException()
	if last_bet:
		if game.is_palifico_round() and player.palifico_round == -1 and value != last_bet.value:
			raise NonPalificoChangeException()
		if last_bet.value == 1 and value > 1 and quantity < last_bet.quantity * 2 + 1:
			raise InvalidNonWildcardQuantityException()
		if quantity <= last_bet.quantity and (value == last_bet.value or (value > 1 and value <= last_bet.value)):
			raise InvalidBetException()
		if value == 1 and last_bet.value > 1 and quantity < last_bet.quantity/2:
			raise InvalidWildcardQuantityException()
		return Bet(quantity, value)
	else:
		return Bet(quantity, value)
	