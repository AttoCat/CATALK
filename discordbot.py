import os

import discord
import dotenv
import datetime
Start_ID = 704619077141921872
d_today = datetime.date.today()

dotenv.load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


@client.event
async def greet():
    channel = client.get_channel(Start_ID)
    await channel.send("正常に起動しました")


@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)
    await greet()


@client.event
async def on_message(message):
    if message.content == "おはよう！":
        await message.channel.send("おはようございますご主人さま" + "今日の日付は" + d_today + "日です。")


client.run(TOKEN)
