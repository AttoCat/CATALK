import discord
import dotenv
import os

dotenv.load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


@client.event
async def on_ready():
    print("on_ready 正常に起動しました\n No error occurred")
    print(discord.__version__)
