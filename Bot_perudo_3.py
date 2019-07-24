import asyncio
import discord
import random

TOKEN = 'NjAyOTExMTA0ODI5NzUxMjk2.XThNfw.4AN847PilCW_PqtdJjqv_sEF4Mw'
server_ID = 451307339933417472

liste_dés = [':stop_button:',':Paco:',':D2:',':D3:',':D4:',':D5:',':D6:']
liste_dés = [':stop_button:',':bird:',':two:',':three:',':four:',':five:',':six:']


class MyClient(discord.Client):

    jeu_on = 0
    nombre_joueurs = 0
    liste_joueurs = []
    nombre_dés = []

    async def lancer_les_dés(self,N,L1,L2):
        lancers = []
        for i in range(N):
            self.joueur = self.id.get_member_named(str(L1[i]))
            if L2[i] > 0:
                res = 'Voici les résultats de ton lancer :'
                for j in range(L2[i]):
                    x = random.random(1,6)
                    lancers.append(x)
                    res = res + ' {}'.format(liste_dés[x])
                await self.joueur.send(res)
        return lancers


    async def on_ready(self):
        print('Logged on as', self.user)
        print("The bot is ready!")
        self.id = client.get_guild(451307339933417472)
        # self.Simon = self.id.get_member_named("Krak#0491")
        # self.Raymond = self.id.get_member_named('Ourshanabi#5500')
        # self.Luc = self.id.get_member_named('Wallis#4469')
        await client.change_presence(activity=discord.Game(name="un jeu avec DD"))


    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return


        if message.content == '!Perudo' and self.jeu_on == 0:
            self.jeu_on = 1
            await message.channel.send('Qui veut jouer au Perudo ?')

        if message.content == 'Moi !' and self.jeu_on == 1:
            joueur = message.author
            if joueur not in self.liste_joueurs:
                self.liste_joueurs.append(joueur)
                self.nombre_dés.append(5)
                await message.channel.send('{0.author.mention} est inscrit(e)'.format(message))
            else :
                await message.channel.send('{0.author.mention}, tu joues déjà'.format(message))

        if message.content == '!joueurs' and self.jeu_on == 1:
            await message.channel.send('Voici la liste des joueurs déjà inscrits :')
            for joueur in self.liste_joueurs :
                await message.channel.send(joueur)

        if message.content == 'Débutons la partie' and self.jeu_on == 1:
            self.jeu_on = 2
            self.nombre_joueurs = len(self.liste_joueurs)
            random.shuffle(self.liste_joueurs)
            await message.channel.send('Êtes-vous prêts ?')
            await message.channel.send('Vous jouerez dans cet ordre :')
            for joueur in self.liste_joueurs :
                await message.channel.send('{}'.format(joueur.mention))
            #res = self.lancer_les_dés(self.nombre_joueurs, self.liste_joueurs, self.nombre_dés)
            await message.channel.send('{}'.format(self.nombre_joueurs))
            await message.channel.send('{}'.format(self.liste_joueurs))
            await message.channel.send('{}'.format(self.nombre_dés))

            res = self.lancer_les_dés(self.nombre_joueurs, self.liste_joueurs, self.nombre_dés)





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