import os

import dotenv
import datetime
import discord

dotenv.load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# const
CH_STARTUP = int(os.getenv("CH_STARTUP", "706779308211044352"))
CH_TIMETABLE = int(os.getenv("CH_TIMETABLE", "711397925103599621"))
CH_SAVE_TIMETABLE = int(os.getenv("CH_SAVE_TIMETABLE", "712238123605557269"))


# lists
greetings = [
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

subjects = [
    "英語", "国語", "数学", "理科", "社会", "保体",
    "音楽", "美術", "技術", "家庭", "道徳", "総合", "学活", "その他"
]

error_channels = [
    CH_STARTUP, CH_TIMETABLE, CH_SAVE_TIMETABLE
]

timetable = []

# function


async def error_channel(message):
    embed = discord.Embed(
        title="Error",
        description=(
            "ここでは実行できません！\n"
            "Cannot run program here!"
        ),
        color=0xff0000
    )
    await message.delete()
    await message.channel.send(embed=embed, delete_after=10)


async def send_greeting(message):
    if message.channel.id in error_channels:
        await error_channel(message)
        return
    d_now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    d_today = d_now.strftime(f"\n今日の日付は%-m月%-d日です。")
    msg = greetings[d_now.hour]
    await message.channel.send(f"{msg}" + d_today)


async def set_timetable(message):
    global timetable
    global save_timetable # timetableを文字列で保存する変数
    global ttembed

    # ここからエラー処理
    if message.channel.id in error_channels:
        await error_channel(message)
        return
    if len(timetable) > 6:
        embed = discord.Embed(
            title="Error",
            description=f"引数の数が不正です！\nInvalid input.",
            color=0xff0000
        )
        await message.delete()
        await message.channel.send(embed=embed, delete_after=10)
        return
    # ここまでエラー処理


    timetable = message.content[9:].split()
    embed = discord.Embed(
        title="時間割",
        color=0x0080ff
    )
    num = 1 # 1時間目から始まるので1で初期化
    for subject in timetable:
        # 先に不正かどうかのチェック
        if not subject in subjects:
            embed = discord.Embed(
                title="Error",
                description=f"不正な引数です！\nInvalid argument passed.",
                color=0xff0000)
            await message.channel.send(embed=embed, delete_after=10)
            return #引っかかれば終了

        # チェックが通ればembedに追加
        embed.add_field(
            name=f"{num}時間目",
            value=timetable[num - 1],
            inline=False
        )
        num += 1 #インクリメント
    ttembed = embed
    save_timetable = " ".join(timetable) #ここでリストから文字列へ操作
    await client.get_channel(CH_TIMETABLE).send(embed=ttembed)
    
    #文字列をdiscordにも送信して保存しておく
    await client.get_channel(CH_SAVE_TIMETABLE).send(save_timetable) 


async def edit_timetable(message):
    if message.channel.id in error_channels:
        await error_channel(message)
        return
    CH_TIMETABLE = 711397925103599621
    contentlist = message.content[10:].split()
    idn = (int(contentlist[0]) - 1)
    ttchannel = client.get_channel(CH_TIMETABLE)
    message_id = int(ttchannel.last_message_id)
    message_content = await ttchannel.fetch_message(message_id)
    tt[idn] = str(contentlist[1])
    newembed = discord.Embed(
        title="時間割",
        description="明日の時間割",
        color=0x0080ff)
    num = 0
    for jugyo in tt:
        num += 1
        t = f"{num}時間目"
        newembed.add_field(
            name=t,
            value=tt[num - 1],
            inline=False)
        if not tt[num - 1] in subjects:
            embed = discord.Embed(
                title="Error",
                description=f"不正な引数です！\nInvalid argument passed.",
                color=0xff0000)
            await message.delete()
            await message.channel.send(embed=embed, delete_after=10)
            return
    await message.delete()
    await message_content.edit(embed=newembed)
    await client.get_channel(CH_SAVE_TIMETABLE).send(tt)


# event
@client.event
async def on_ready():
    print(discord.__version__)
    channel = client.get_channel(CH_STARTUP)
    await channel.send("正常に起動しました")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    elif (message.content == "やあ！") or (message.content == "やあ!"):
        await send_greeting(message)
    elif message.content.startswith("ct!ttset "):
        await set_timetable(message)
    elif message.content.startswith("ct!ttedit "):
        await edit_timetable(message)

client.run(TOKEN)
