import json
import discord
import os
import cloudinary
from dotenv import load_dotenv
from PapunikaMap import PapunikaMap
from keep_alive import keep_alive

# Load bot environment variables
load_dotenv()

cloudinary.config(
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key = os.getenv('CLOUDINARY_API_KEY'),
  api_secret = os.getenv('CLOUDINARY_API_SECRET')
)

client = discord.Client()
papunika_map_info_file = open('res/papunikaMapInfo.json')
papunika_map_info_data = json.loads(papunika_map_info_file.read())
papunika_map = PapunikaMap(**papunika_map_info_data)


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
        map_zone = [map_zone for map_zone in papunika_map.zones if map_zone['name'].lower() == map.lower()][0]

        await message.channel.send(cloudinary.utils.cloudinary_url(f"maps/{map_zone['id']}.png")[0])


keep_alive()
client.run(os.getenv('TOKEN'))
