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
        d_today = d_now.strftime("今日の日付は % -m月 % -d日です。")
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
        elif 12 <= d_now.hour <= 19:
            msg = f"こんにちは。もう正午を過ぎています。「おはよう」と言うには遅い時間ですよ。\n{d_today}"
        elif 20 <= d_now.hour <= 23:
            msg = f"こんばんは。もう夜です。朝ではないこと、本当はあなたもわかっているんでしょう？\n{d_today}"
        elif d_now.hour == 24:
            msg = f"こんばんは。もうおはようについてはスルーします。日付も変わったところですし早く寝ましょうよ。\n{d_today}"
        elif 24 < d_now.hour < 3:
            msg = f"え…？まだ起きているんですか…？もう夜中ですよ。明らかにおはようじゃないでしょうが！\n{d_today}"
        elif 3 <= d_now.hour <= 5:
            msg = f"おはようございます、なんでしょうか。まだ日は昇っていませんが。\n{d_today}"
        else:
            msg = f"おはようございます。\n{d_today}"
        await message.channel.send(msg)

client.run(TOKEN)
