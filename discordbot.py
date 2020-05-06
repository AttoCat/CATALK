import os

import dotenv
from datetime import datetime, timedelta
import discord

dotenv.load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

Start_ID = 706779308211044352


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
    if (message.content == "おはよう！") or (message.content == "おはよう!"):
        if message.channel.id == Start_ID:  # 起動ログチャンネルで発言してもエラー&削除
            embed = discord.Embed(
                title="Error",
                description=(
                    "ここでは実行できません！\nCannot perform this operation here."),
                color=0xff0000)
            await client.get_channel(Start_ID).send(
                embed=embed, delete_after=10)
            await message.delete()
            return
        d_now = datetime.utcnow() + timedelta(hours=9)
        d_today = d_now.strftime(f"今日の日付は%-m月%-d日です。")
        if 11 < (d_now.hour) < 18:
            content = f"おはようございます。\n{d_today}"
        else:
            content = f"こんにちは。もう正午を過ぎています。「おはよう」と言うには遅い時間ですよ。\n{d_today}"
        await message.channel.send(content)

client.run(TOKEN)
