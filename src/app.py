import discord
import os
from dotenv import load_dotenv

# Load bot environment variables
load_dotenv()

client = discord.Client()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('!map'):
        map = msg.split("!map ", 1)[1]
        await message.channel.send(map)


client.run(os.getenv('TOKEN'))
