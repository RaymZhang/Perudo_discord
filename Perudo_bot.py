
import asyncio
import discord

TOKEN = 'NjAzMjQwNTI2OTI5NTkyMzMy.XTdMlw.bqwjDe6FxuwjYPZAycrwNLaMjGE'


import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        print("The bot is ready!")
        await client.change_presence(activity=discord.Game(name="Playing Perudo"))


    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

        if message.content.startswith('!hello'):
            msg = 'Hello {0.author.mention}'.format(message)
            await message.channel.send(msg)

        # if str(message.author) == 'Ourshanabi#5500' :
        #         await message.channel.send('Ce que dit {0.author.mention} est incroyable. Il est si beau, si fort !' .format(message))

client = MyClient()
client.run(TOKEN)


