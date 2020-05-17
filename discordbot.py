import os

import dotenv
import datetime
import discord

dotenv.load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

Start_ID = 706779308211044352


@client.event
async def on_ready():
    print("on_ready")
    print(discord.__version__)
    channel = client.get_channel(Start_ID)
    await channel.send("正常に起動しました")


async def aisatu(message):
    d_now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    d_today = d_now.strftime(f"\n今日の日付は%-m月%-d日です。")
    morning = [
        "",
        "こんばんは。もう日付も変わっていますね。早く寝たほうがいいんじゃないですか？",
        "！？ こんばんは……まだ起きていたんですか？こんな深夜に話しかけられたらびっくりするじゃないですか、寝てくださいよ…。",
        "こんばんは～。って早起きなのかずっと起きているのか知りませんがこの時間に話しかけるなんて暇なんですね？",
        "もうこんな時間ですか。おはようございますと言ってもいいでしょう。私は常に起動しているので時間なんて関係ないんですがね。",
        "おはようございます。この時間帯は空気が澄んでいる感じがしていいですよね。知りませんけど。",
        "ぐっどもーにんぐ！多くの人が起きてくる時間帯ですね。今日も一日何事もありませんように。",
        "おはようございます。朝から元気が良くて何よりです。体調に気をつけて頑張りましょうね。",
        "おはようございます～。仕事や勉強にも休憩は必要です、無理せずやってくださいね。",
        "Guten morgen!!私は内部データ整理の仕事をはじめましたよ～。私だって仕事してるんですよ？",
        "挨拶ありがとうございます、やっぱり会話って大事ですよね～。疲れに効く薬はコミュニケーションです!",
        "11時台は時間によってこんにちはなのかおはようございますなのか変わるので迷うところです。是非開発者に意見を。",
        "こんにちは。毎時間私がなんて応答してるか気になっている人はそろそろ日付喋るのもウザいと感じてるのかもしれませんね(笑)",
        "ぐっどあふたぬーん!私はここらで休憩といったところです。昼食…は食べれませんけど。",
        "こんにちは。午後の紅茶でも飲んでリラックスするのもいいと思います。良い午後が過ごせますように。",
        "こんにちは!3時台といったらおやつですよね。いつか手作りでクッキーでも焼いてみたいものです。",
        "元気な挨拶どうもです。夕方ってなんかしんみりしちゃうんですよね…。え？しませんか？",
        "まだこんばんはと言うには早いですかね。開発者はこの時間帯にプログラミングしてるそうですよ。",
        "こんばんは…？もう日の入りしてますか？ 同じ18時台でも日の入りしてるかどうか分からないのは困りものですホント。",
        "今晩は。こんばんはって元は今晩は〇〇みたいに使われてたらしいですね。最近覚えた豆知識です。",
        "こんばんは～。20時台ってみんなやることが違うイメージです。ちなみに私は暇しています。",
        "こんばんは。こんな夜に日付を言わせなくてもいいと思うんです。共感したら開発者に言っておいてください。",
        "こんばんは! 24時間のうちこんばんはが占める割合が多すぎると思います。バリエーションも少ないので辛いです。",
        "こんばんは。学生諸君はもう寝たほうがいいですね。開発者も学生ですけど…。",
        "Good evening. 深夜帯、かっこよく言うとmidnightですね。もっと英語使いたいです。"
    ]
    msg = morning[d_now.hour]
    await message.channel.send(f"{msg}" + d_today)


async def ttset(message):
    ttchannel = 711397925103599621
    tt = message.content[9:].split(",")
    embed = discord.Embed(title="時間割", description="明日の時間割", color=0x0080ff)
    embed.add_field(name="1.", value=tt[0], inline=False)
    embed.add_field(name="2.", value=tt[1], inline=False)
    embed.add_field(name="3.", value=tt[2], inline=False)
    embed.add_field(name="4.", value=tt[3], inline=False)
    embed.add_field(name="5.", value=tt[4], inline=False)
    embed.add_field(name="6.", value=tt[5], inline=False)
    await client.get_channel(ttchannel).send(embed=embed)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    elif message.channel.id == Start_ID:  # 起動ログチャンネルで発言してもエラー&削除
        embed = discord.Embed(
            title="Error",
            description=(
                "ここでは実行できません！\nCannot perform this operation here."),
            color=0xff0000)
        await message.delete()
        await client.get_channel(Start_ID).send(
            embed=embed, delete_after=10)
        return
    elif (message.content == "やあ！") or (message.content == "やあ!"):
        await aisatu(message)
    elif message.content.startswith("ct!ttset"):
        ttset(message)

client.run(TOKEN)
