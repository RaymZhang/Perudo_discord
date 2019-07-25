import config
import random
import sys
import time
from bet import Bet
from bet import DUDO
#from bet import EXACT

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



import asyncio
import discord
import random

TOKEN = 'NjAzMjQwNTI2OTI5NTkyMzMy.XTdMlw.bqwjDe6FxuwjYPZAycrwNLaMjGE'
#'NjAyOTExMTA0ODI5NzUxMjk2.XThNfw.4AN847PilCW_PqtdJjqv_sEF4Mw'
server_ID = 451307339933417472

Perudo_chanel_id = 602963108448960553

liste_dés = [':stop_button:',':Paco:',':D2:',':D3:',':D4:',':D5:',':D6:']
liste_dés = [':stop_button:',':bird:',':two:',':three:',':four:',':five:',':six:']


class MyClient(discord.Client):

	async def on_ready(self):
		print('Logged on as', self.user)
		print("The bot is ready!")
		self.jeu_on = 0
		self.nombre_joueurs = 0
		self.liste_joueurs = []
		self.nombre_dés = []
		self.dice_number = 5

		self.id = self.get_guild(451307339933417472)
		self.perudo_chanel = self.get_channel(602963108448960553)

		# self.Simon = self.id.get_member_named("Krak#0491")
		# self.Raymond = self.id.get_member_named('Ourshanabi#5500')
		# self.Luc = self.id.get_member_named('Wallis#4469')
		await client.change_presence(activity=discord.Game(name="un jeu avec DD"))


	async def on_message(self, message):
		# don't respond to ourselves
		if message.author == self.user:
			return


		if message.content == '!perudo' and self.jeu_on == 0 and message.channel == self.perudo_chanel:
			self.jeu_on = 1
			await message.channel.send('Qui veut jouer au Perudo ?')

		if message.content == 'moi' and self.jeu_on == 1 and message.channel == self.perudo_chanel:
			joueur = message.author
			if joueur not in self.liste_joueurs:
				self.liste_joueurs.append(joueur)
				self.nombre_dés.append(5)
				await message.channel.send('{0.author.mention} est inscrit(e)'.format(message))
			else :
				await message.channel.send('{0.author.mention}, tu joues déjà'.format(message))

		if message.content == '!joueurs' and self.jeu_on == 1 and message.channel == self.perudo_chanel:
			await message.channel.send('Voici la liste des joueurs déjà inscrits :')

			for joueur in self.liste_joueurs :
				await message.channel.send('{}'.format(joueur.mention))

		if message.content == '!jouer' and self.jeu_on == 1 and message.channel == self.perudo_chanel:
			self.jeu_on = 2
			await self.perudo()
			self.jeu_on = 0
			self.liste_joueurs = []

		if message.content == '!reset' and str(message.author) == 'Ourshanabi#5500' and message.channel == self.perudo_chanel:
			self.jeu_on = 0
			self.liste_joueurs = []


	async def perudo(self):

		self.round = 0
		self.round = 0
		self.players = []


		for joueur in self.liste_joueurs:
			self.players.append(
				HumanPlayer(
					joueur = joueur,
					dice_number = self.dice_number,
					client = self
				)
			)

		random.shuffle(self.players)

		print(welcome_message(self.players))
		await self.perudo_chanel.send(welcome_message(self.players))

		self.first_player = random.choice(self.players)

		while len(self.players) > 1:
			await self.run_round()

		print(winner(self.players[0].name))

		await self.perudo_chanel.send(winner(self.players[0].name))

	async def run_round(self):
		self.round += 1
		for player in self.players:
			player.roll_dice()

		print(round_title(round_number = self.round, is_palifico_round=self.is_palifico_round()))
		await self.perudo_chanel.send(\
			round_title(round_number = self.round, is_palifico_round=self.is_palifico_round()))

		round_over = False
		current_bet = None
		current_player = self.first_player
		print('{0} joue en premier...'.format(current_player.name))
		await self.perudo_chanel.send('{0} will go first...'.format(current_player.name))

		while not round_over:
			next_player = self.get_next_player(current_player)
			next_bet = await current_player.make_bet(current_bet)
			bet_string = None
			if next_bet == DUDO:
				bet_string = 'MENTEUR!'
			else:
				bet_string = next_bet
			print('{0}: {1}'.format(current_player.name, bet_string))
			await self.perudo_chanel.send('{0}: {1}'.format(current_player.name, bet_string))

			if next_bet == DUDO:
				self.pause(0.5)
				await self.run_dudo(current_player, current_bet)
				round_over = True
			else:
				current_bet = next_bet

			if len(self.players) > 1:
				current_player = next_player

			self.pause(0.5)

		self.pause(1)

	async def run_dudo(self, player, bet):
		dice_count = self.count_dice(bet.value)
		if dice_count >= bet.quantity:
			print(incorrect_dudo(dice_count, bet.value))
			await self.perudo_chanel.send(incorrect_dudo(dice_count, bet.value))

			self.first_player = player
			await self.remove_die(player)
		else:
			print(correct_dudo(dice_count, bet.value))
			await self.perudo_chanel.send(correct_dudo(dice_count, bet.value))
			previous_player = self.get_previous_player(player)
			self.first_player = previous_player
			await self.remove_die(previous_player)

	def count_dice(self, value):
		number = 0
		for player in self.players:
			number += player.count_dice(value)

		return number

	async def remove_die(self, player):
		player.dice.pop()
		msg = '{0} Perd un dé.'.format(player.name)
		if len(player.dice) == 0:
			msg += ' {0} is out!'.format(player.name)
			self.first_player = self.get_next_player(player)
			self.players.remove(player)
		elif len(player.dice) == 1 and player.palifico_round == -1:
			player.palifico_round = self.round + 1
			msg += ' Dernier dé ! {0} est palifico!'.format(player.name)
		else:
			msg += ' Plus que {0} !'.format(len(player.dice))
		print(msg)
		await self.perudo_chanel.send(msg)


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



			# self.jeu_on = 2
			# self.nombre_joueurs = len(self.liste_joueurs)
			# random.shuffle(self.liste_joueurs)
			# await message.channel.send('Êtes-vous prêts ?')
			# await message.channel.send('Vous jouerez dans cet ordre :')
			# for joueur in self.liste_joueurs :
			#     await message.channel.send('{}'.format(joueur.mention))
			# #res = self.lancer_les_dés(self.nombre_joueurs, self.liste_joueurs, self.nombre_dés)
			# await message.channel.send('{}'.format(self.nombre_joueurs))
			# await message.channel.send('{}'.format(self.liste_joueurs))
			# await message.channel.send('{}'.format(self.nombre_dés))

			# res = self.lancer_les_dés(self.nombre_joueurs, self.liste_joueurs, self.nombre_dés)





		# if message.content == 'Je lance un dé':
		#     dé = random.randint(0,5)
		#     await message.channel.send('{0.author.mention} lance un dé'.format(message))
		#     await message.channel.send('Le dé roule...'.format(message))
		#     await message.channel.send('C\'est un {} !'.format(liste_dés[dé]))

#            await message.channel.send('{0.author.mention} a fait un {:2}'.format(message, liste_dés[dé]))

		# if message.content.startswith('!hello'):
		#     msg = 'Hello {0.author.mention}'.format(message)
		#     await message.channel.send(msg)

		# if str(message.author) == 'Wallis#4469' :

		# if message.author != self.user:
		#     self.joueur = self.id.get_member_named(str(message.author))
		#     #await message.channel.send('Ce que dit {0.author.mention} est incroyable. Il est si beau, si fort !' .format(message))
		#     await self.joueur.send('Salut !')
		#     #await self.Simon.send('Cela est bien vrai')
		#     #await self.Luc.send('Cela est bien vrai')

		# if message.content == 'Je lance un dé':
		#     dé = random.randint(1,6)
		#     self.joueur = self.id.get_member_named(str(message.author))
		#     await self.joueur.send('Tu fais un {} !'.format(liste_dés[dé]))




client = MyClient()
client.run(TOKEN)