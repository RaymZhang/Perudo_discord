class BetException(Exception):
	pass

class InvalidDieValueException(BetException):
	"""Raised when a value not between 1 and 6 is bet."""
	pass

class NonPalificoChangeException(BetException):
	"""Raised when a non-palifico player changes the value during a palifico round."""
	pass

class InvalidNonWildcardQuantityException(BetException):
	"""Raised when a player changes the value from a wildcard to something else but bets too small a quantity."""
	pass

class InvalidWildcardQuantityException(BetException):
	"""Raised when a player changes the value to a wildcard but bets too small a quantity."""
	pass

class InvalidBetException(BetException):
	"""Raised when a bet does not have either a higher quantity or a higher value."""
	pass