import os

import discord
import dotenv


dotenv.load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
client.run(TOKEN)


@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)
