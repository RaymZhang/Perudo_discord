# -*- coding: utf-8 -*-

BAD_BET_ERROR = "Enchère non valide ! Une enchère doit être donnée sous la forme '!A*B' (A dés de valeur B), ou bien être '!Menteur' ou 'Compte exact'"

INVALID_DIE_VALUE_ERROR = 'Enchère non valide ! La valeur du dé doit être entre 1 et 6'
NON_PALIFICO_CHANGE_ERROR = 'Enchère non valide ! Pendant le palifico, la valeur du dé ne peut être changée.'
INVALID_NON_WILDCARD_QUANTITY = 'Enchère non valide ! La dernière enchère était en pacos. Si vous souhaitez changer la valeur, la quantité de dés doit être strictement supérieure au double de la quantité précédente.'
INVALID_WILDCARD_QUANTITY = 'Enchère non valide ! Pour faire une enchère valide en pacos, la quantité doit être supérieure à la moitié de la quantité précédente.'
INVALID_BET_EXCEPTION = 'Enchère non valide ! Vous devez indiquer une quantité strictement supérieure à la quantité précédente.'

INSUFFICIENT_BOTS = 'Il faut au moins  1 bot ! Ou trouvez-vous des amis.'
INSUFFICIENT_DICE = 'Il faut au moins un dé par personne.'

DASHES = '-' * 64
DASHES_NEW_LINE = DASHES + '\n'

def correct_dudo(quantity, value):
	return "Il n'y a que {0} {1}. Quel menteur !".format(quantity, value)

def incorrect_dudo(quantity, value):
	return "Il y a bien {0} {1}s. Ce n'était pas un menteur".format(quantity, value)

def correct_compte_exacte(quantity, value):
	return "Il y a exactement {0} {1}. Bien joué !".format(quantity, value)

def incorrect_compte_exacte(quantity, value):
	return "Il y a exactement {0} {1}s. C'est raté !".format(quantity, value)

def round_title(round_number, is_palifico_round):
	if is_palifico_round:
		title = "Tour {0} - C'est le PALIFICO\n".format(round_number)
	else:
		title = 'Tour {0}\n'.format(round_number)
	return DASHES_NEW_LINE + title + DASHES

def welcome_message(players):
		names_string = ''
		for player in players:
			names_string += player.name
			if players.index(player) == len(players) - 1:
				continue
			elif players.index(player) == len(players) - 2:
				names_string += ' et '
			else:
				names_string += ', '

		return DASHES_NEW_LINE + 'Jouons à Perudo ! Les joueurs {0}.'.format(names_string)

def winner(name):
	return DASHES_NEW_LINE + '{0} a gagné !\n'.format(name) + DASHES
