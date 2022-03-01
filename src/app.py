import discord
import os
import cloudinary
from dotenv import load_dotenv

# Load bot environment variables
load_dotenv()

cloudinary.config(
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key = os.getenv('CLOUDINARY_API_KEY'),
  api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

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
        await message.channel.send(cloudinary.CloudinaryImage(f"{map}.png").url)


client.run(os.getenv('TOKEN'))
