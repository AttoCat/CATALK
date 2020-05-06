import os

import dotenv
import datetime
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
        d_now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
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
        elif 11 < (d_now.hour) < 18:
            await message.channel.send(d_now.strftime(
                f"こんにちは。もう正午を過ぎています。「おはよう」と言うには遅い時間ですよ。\n"
                f"今日の日付は%-m月%-d日です。"))
            return
        else:
            await message.channel.send(d_now.strftime(
                f"おはようございます。\n"
                f"今日の日付は%-m月%-d日です。"))

client.run(TOKEN)
