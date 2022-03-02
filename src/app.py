import json
import os

import cloudinary
import discord
from dotenv import load_dotenv
from printy import printy

from PapunikaMap import PapunikaMap

# ingame name : papunika name
alias_names_arthetine = {
    "origins of stern": "stern"
}
alias_names_feiton = {
    "red moonshade": "red moon wastes",
    "kalaja": "kallazar",
    "wailing swamp": "rot water",
    "shady cliff": "siena monastery",
    "nameless valley": "nameless plateau"
}
alias_names_rohendel = {
    "breezesome brae": "wind hill",
    "elzowin's shade": "ancient flower garden",
    "rothun": "queen's garden",
    "lake shiverwave": "soaring harbor",
    "xeneela ruins": "the ruins of genail"
}
alias_names_yorn = {
    "yorn's cradle": "helm harbor",
    "unfinished garden": "lower dungeons",
    "hall of promise": "primordial lands",
    "iron hammer mine": "mines of innumerable riches",
    "black anvil mine": "mines of fire",
    "great castle": "isendelf"
}
alias_names_punika = {
    "starsand beach": "star sand beach",
    "tideshelf path": "shallow sea road",
    "tikatika colony": "tikku gardens",
    "secret forest": "mangrove forest"
}

# Load bot environment variables
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

client = discord.Client()
papunika_map_info_file = open('res/papunikaMapInfo.json')
papunika_map_info_data = json.loads(papunika_map_info_file.read())
papunika_map = PapunikaMap(**papunika_map_info_data)


@client.event
async def on_ready():
    printy(f'Logged in as [r]{client.user}@')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if message.content.startswith('!map'):
        map = msg.split("!map ", 1)[1]
        # TODO: get map by map layer, i.e: Kalaja 2F
        # TODO: get map by partial name, i.e: brae (Breezesome Brae)
        aliases = [
            alias_names_yorn, alias_names_feiton,
            alias_names_punika, alias_names_rohendel,
            alias_names_arthetine
        ]

        image_url = None
        map_id = None
        for map_zone in papunika_map.zones:
            if map_zone['name'].lower() == map.lower():
                image_url = cloudinary.utils.cloudinary_url(f"maps/{map_zone['id']}.png")[0]
                map_id = map_zone['id']

        if not image_url:
            for alias in aliases:
                for game_name, papunika_name in alias.items():
                    if game_name == map.lower():
                        map_zone = [zone for zone in papunika_map.zones if zone['name'].lower() == papunika_name][0]
                        if map_zone:
                            image_url = cloudinary.utils.cloudinary_url(f"maps/{map_zone['id']}.png")[0]
                            map_id = map_zone['id']
        if image_url:
            embed = discord.Embed()
            embed.set_author(name="Map from Papunika found!")
            embed.add_field(name=f"https://papunika.com/map/?z={map_id}&l=us", value="Link to papunika map")
            embed.set_image(url=image_url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Map not found!")

client.run(os.getenv('TOKEN'))
