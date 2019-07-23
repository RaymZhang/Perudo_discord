import config
import random
import sys
import time
from bet import Bet
from bet import DUDO
from player import ComputerPlayer
from player import HumanPlayer
from strings import correct_dudo
from strings import incorrect_dudo
from strings import INSUFFICIENT_BOTS
from strings import INSUFFICIENT_DICE
from strings import round_title
from strings import welcome_message
from strings import winner

# cd desktop\\perudo_discord


# "Burn all you love."
bot_names = ['Winston', 'Luke', 'Jeff', 'Jia', 'Ben']

names = ['Toto', 'Wallis']

class Perudo(object):

	def __init__(self, names, player_number, dice_number):
		self.round = 0
		self.players = []

		for name in names:
			self.players.append(
				HumanPlayer(
					name=name,
					dice_number=dice_number,
					game=self
				)
			)
		for i in range(0, player_number):
			self.players.append(
				ComputerPlayer(
					name=self.get_random_name(),
					dice_number=dice_number,
					game=self
				)
			)

		random.shuffle(self.players)

		print(welcome_message(self.players))

		self.first_player = random.choice(self.players)

		while len(self.players) > 1:
			self.run_round()

		print(winner(self.players[0].name))

	def run_round(self):
		self.round += 1
		for player in self.players:
			player.roll_dice()

		print(round_title(round_number=self.round, is_palifico_round=self.is_palifico_round()))
		round_over = False
		current_bet = None
		current_player = self.first_player
		print('{0} will go first...'.format(current_player.name))
		while not round_over:
			next_player = self.get_next_player(current_player)
			next_bet = current_player.make_bet(current_bet)
			bet_string = None
			if next_bet == DUDO:
				bet_string = 'Dudo!'
			else:
				bet_string = next_bet
			print('{0}: {1}'.format(current_player.name, bet_string))
			if next_bet == DUDO:
				self.pause(0.5)
				self.run_dudo(current_player, current_bet)
				round_over = True
			else:
				current_bet = next_bet

			if len(self.players) > 1:
			 	current_player = next_player

			self.pause(0.5)

		self.pause(1)

	def run_dudo(self, player, bet):
		dice_count = self.count_dice(bet.value)
		if dice_count >= bet.quantity:
			print(incorrect_dudo(dice_count, bet.value))
			self.first_player = player
			self.remove_die(player)
		else:
			print(correct_dudo(dice_count, bet.value))
			previous_player = self.get_previous_player(player)
			self.first_player = previous_player
			self.remove_die(previous_player)

	def count_dice(self, value):
		number = 0
		for player in self.players:
			number += player.count_dice(value)

		return number

	def remove_die(self, player):
		player.dice.pop()
		msg = '{0} loses a die.'.format(player.name)
		if len(player.dice) == 0:
			msg += ' {0} is out!'.format(player.name)
			self.first_player = self.get_next_player(player)
			self.players.remove(player)
		elif len(player.dice) == 1 and player.palifico_round == -1:
			player.palifico_round = self.round + 1
			msg += ' Last die! {0} is palifico!'.format(player.name)
		else:
			msg += ' Only {0} left!'.format(len(player.dice))
		print(msg)

	def is_palifico_round(self):
		if len(self.players) < 3:
			return False
		for player in self.players:
			if player.palifico_round == self.round:
				return True
		return False

	def get_random_name(self):
		random.shuffle(bot_names)
		return bot_names.pop()

	def get_next_player(self, player):
		return self.players[(self.players.index(player) + 1) % len(self.players)]

	def get_previous_player(self, player):
		return self.players[(self.players.index(player) - 1) % len(self.players)]

	def pause(self, duration):
		if config.play_slow:
			time.sleep(duration)

def get_argv(args, index, default):
	try:
		value = args[index]
	except IndexError:
		value = default
	return value


###☻

def main(args):
	try:
		name = get_argv(args, 1, 'Player')
		bot_number = int(get_argv(args, 2, 3))
		# if bot_number < 1:
		# 	print(INSUFFICIENT_BOTS)
		# 	return
		dice_number = int(get_argv(args, 3, 5))
		if dice_number < 1:
			print(INSUFFICIENT_DICE)
			return

		Perudo(names, bot_number, dice_number)
	except ValueError:
		print ('Args must be of the form <name> <bot_number> <dice_number>, where bot_number and dice_number are integers.')
		return

if __name__ == '__main__':
	main(sys.argv)