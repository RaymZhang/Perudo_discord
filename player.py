import random
from bet import Bet
from bet import DUDO
from bet import COMPTE_EXACT
from bet import create_bet
from bet_exceptions import BetException
from bet_exceptions import InvalidDieValueException
from bet_exceptions import NonPalificoChangeException
from bet_exceptions import InvalidNonWildcardQuantityException
from bet_exceptions import InvalidWildcardQuantityException
from bet_exceptions import InvalidBetException
from die import Die
from math import floor
from math import ceil
from strings import BAD_BET_ERROR
from strings import INVALID_DIE_VALUE_ERROR
from strings import NON_PALIFICO_CHANGE_ERROR
from strings import INVALID_NON_WILDCARD_QUANTITY
from strings import INVALID_WILDCARD_QUANTITY
from strings import INVALID_BET_EXCEPTION

class Player(object):

	def __init__(self, joueur, dice_number, client):
		self.joueur = joueur
		self.client = client
		self.name = str(joueur)

		self.palifico_round = -1
		self.dice = []
		for i in range(0, dice_number):
			self.dice.append(Die())

	def make_bet(self, current_bet):
		pass

	def roll_dice(self):
		for die in self.dice:
			die.roll()
		# Sort dice into value order e.g. 4 2 5 -> 2 4 5
		self.dice = sorted(self.dice, key=lambda die: die.value)

	def count_dice(self, value):
		number = 0
		for die in self.dice:
			if die.value == value or (not self.client.is_palifico_round() and die.value == 1):
				number += 1
		return number

class ComputerPlayer(Player):

	async def make_bet(self, current_bet):
		total_dice_estimate = len(self.dice) * len(self.game.players)
		if current_bet is None:
			# CPU is the first player, so make a conservative estimate
			value = random.choice(self.dice).value
			quantity_limit = (total_dice_estimate - len(self.dice))/6
			if value > 1:
				quantity_limit *= 2
			quantity = self.count_dice(value) + random.randrange(0, quantity_limit + 1)
			bet = create_bet(quantity, value, current_bet, self, self.game)
		else:
			# Estimate the number of dice in the game with the bet's value
			if current_bet.value == 1 or self.game.is_palifico_round():
				# There should be twice as many of any value than 1
				limit = ceil(total_dice_estimate/6.0) + random.randrange(0, ceil(total_dice_estimate/4.0))
			else:
				limit = ceil(total_dice_estimate/6.0) * 2 + random.randrange(0, ceil(total_dice_estimate/4.0))
			if current_bet.quantity >= limit:
				return DUDO
			else:
				bet = None
				while bet is None:
					if self.game.is_palifico_round() and self.palifico_round == -1:
						# If it is a Palifico round and the player has not already been palifico,
						# the value cannot be changed.
						value = current_bet.value
						quantity = current_bet.quantity + random.randrange(0, 2)
					else:
						value = random.choice(self.dice).value
						if value == 1:
							if current_bet.value > 1:
								quantity = int(ceil(current_bet.quantity/2.0))
							else:
								quantity = current_bet.quantity + random.randrange(0, 2)
						else:
							if current_bet.value == 1:
								quantity = current_bet.quantity * 2 + 1
							else:
								quantity = current_bet.quantity + random.randrange(0, 2)
					try:
						bet = create_bet(quantity, value, current_bet, self, self.game)
					except BetException:
						bet = None

		return bet

class HumanPlayer(Player):

	def check(self):
		return lambda m: m.author == self.joueur and m.channel == self.client.perudo_chanel and m.content.startswith('!')

	async def make_bet(self, current_bet):
		string = "C'est à toi de jouer, voici tes dés :"
		await self.client.perudo_chanel.send("C'est à {0.mention} de jouer" .format(self.joueur))
		for die in self.dice:
			string += ' {0}'.format(die.value)
		print(self.name + string)
		await self.joueur.send(self.name + string)

	

	


		bet = None
		while bet is None:
			bet_input = await self.client.wait_for('message', check = self.check())
			bet_input = bet_input.content[1:]
			print(str(bet_input))

			if bet_input.lower() == 'menteur':
				return DUDO
			if bet_input.lower() == 'compte exact':
				return COMPTE_EXACT
				
			if '*' not in bet_input:
				await self.client.perudo_chanel.send(BAD_BET_ERROR)
				print(BAD_BET_ERROR)
				continue
			bet_fields = bet_input.split('*')
			if len(bet_fields) < 2:
				await self.client.perudo_chanel.send(BAD_BET_ERROR)
				print(BAD_BET_ERROR)
				continue

			try:
				quantity = int(bet_fields[0])
				value = int(bet_fields[1])

				try:
					bet = create_bet(quantity, value, current_bet, self, self.client)
				except InvalidDieValueException:
					bet = None
					print(INVALID_DIE_VALUE_ERROR)
					await self.client.perudo_chanel.send(INVALID_DIE_VALUE_ERROR)
				except NonPalificoChangeException:
					bet = None
					print(NON_PALIFICO_CHANGE_ERROR)
					await self.client.perudo_chanel.send(NON_PALIFICO_CHANGE_ERROR)
				except InvalidNonWildcardQuantityException:
					bet = None
					print(INVALID_NON_WILDCARD_QUANTITY)
					await self.client.perudo_chanel.send(INVALID_NON_WILDCARD_QUANTITY)
				except InvalidWildcardQuantityException:
					bet = None
					print(INVALID_WILDCARD_QUANTITY)
					await self.client.perudo_chanel.send(INVALID_WILDCARD_QUANTITY)
				except InvalidBetException:
					bet = None
					print(INVALID_BET_EXCEPTION)
					await self.client.perudo_chanel.send(INVALID_BET_EXCEPTION)
			except ValueError:
				print(BAD_BET_ERROR)
				await self.client.perudo_chanel.send(BAD_BET_ERROR)

		return bet