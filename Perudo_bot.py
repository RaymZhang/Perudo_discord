
import asyncio
import discord

TOKEN = 'NjAzMjQwNTI2OTI5NTkyMzMy.XTckVA.-X645DFcJT-3kA7P0RrA7AVRRlU'


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

client = MyClient()
client.run(TOKEN)


