import os

import discord
import dotenv

dotenv.load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)


async def on_message(message)
if message.content == "おはよう！":
    await message.channel.send("おはようございますご主人さま" + "今日の日付は"　+ date.today() + "日です。")

client.run(TOKEN)
