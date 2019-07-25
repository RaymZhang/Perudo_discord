BAD_BET_ERROR = 'Bad bet! Bet must be of the form A*B (A dice of value B) or the word "dudo"'

INVALID_DIE_VALUE_ERROR = 'Illegal bet! Die value must be between 1 and 6.'
NON_PALIFICO_CHANGE_ERROR = 'Illegal bet! During a palifico round, only current or former palificos can change the bet value.'
INVALID_NON_WILDCARD_QUANTITY = 'Illegal bet! The last bet\'s die value was 1. If the value is changed to another die value, the quantity must be at least twice the last quantity plus one.'
INVALID_WILDCARD_QUANTITY = 'Illegal bet! If the bet value is changed to 1, the quantity must be at least half the last quantity.'
INVALID_BET_EXCEPTION = 'Illegal bet! A bet must have either a higher quantity or a higher value than the last bet.'

INSUFFICIENT_BOTS = 'You need at least 1 bot! You can\'t play alone!'
INSUFFICIENT_DICE = 'You need at least 1 die each!'

DASHES = '-' * 64
DASHES_NEW_LINE = DASHES + '\n'

def correct_dudo(quantity, value):
	return 'There are only {0} {1}s. Good dudo!'.format(quantity, value)

def incorrect_dudo(quantity, value):
	return 'There are actually {0} {1}s. Incorrect dudo!'.format(quantity, value)

def round_title(round_number, is_palifico_round):
	if is_palifico_round:
		title = 'Round {0} - PALIFICO ROUND\n'.format(round_number)
	else:
		title = 'Round {0}\n'.format(round_number)
	return DASHES_NEW_LINE + title + DASHES

def welcome_message(players):
		names_string = ''
		for player in players:
			names_string += player.name
			if players.index(player) == len(players) - 1:
				continue
			elif players.index(player) == len(players) - 2:
				names_string += ' and '
			else:
				names_string += ', '

		return DASHES_NEW_LINE + 'Welcome to Perudo! {0} are playing.'.format(names_string)

def winner(name):
	return DASHES_NEW_LINE + '{0} wins!\n'.format(name) + DASHES
