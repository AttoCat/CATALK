import os

import dotenv
import datetime
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='ct!')
dotenv.load_dotenv()
client = discord.Client()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


Start_ID = 706779308211044352
TT_ID = 711397925103599621
TTlog_ID = 712238123605557269
tt = []
classlist = {
    "こ": "国語", "す": "数学", "り": "理科", "しゃ": "社会",
    "え": "英語", "ほ": "保体", "お": "音楽", "び": "美術",
    "ぎ": "技術", "か": "家庭", "ど": "道徳", "そ": "総合",
    "が": "学活", "た": "その他"}
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


async def error_channel(message):
    embed = discord.Embed(
        title="Error",
        description=(
            "ここでは実行できません！\nCannot perform this operation here."),
        color=0xff0000)
    await message.delete()
    await message.channel.send(embed=embed, delete_after=10)


async def error_arguments(message):
    await message.delete()
    embed = discord.Embed(
        title="Error",
        description=f"不正な引数です！\nInvalid argument passed.",
        color=0xff0000)
    await message.channel.send(embed=embed, delete_after=10)


async def error_number_of_arguments(message):
    await message.delete()
    embed = discord.Embed(
        title="Error",
        description=f"引数の数が不正です！\nInvalid input.",
        color=0xff0000)
    await message.channel.send(embed=embed, delete_after=10)


async def aisatu(message):
    d_now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    d_today = d_now.strftime(f"\n今日の日付は%-m月%-d日です。")
    msg = morning[d_now.hour]
    await message.channel.send(f"{msg}" + d_today)


async def timetable(message):
    num = 0
    embed = discord.Embed(
        title="時間割",
        description="明日の時間割",
        color=0x0080ff)
    if len(tt) > 6:
        await error_number_of_arguments(message)
        return
    for jugyo in tt:
        num += 1
        if tt[num - 1] in classlist:
            tt[num - 1] = classlist[str(tt[num - 1])]
        t = f"{num}時間目"
        embed.add_field(
            name=t,
            value=tt[num - 1],
            inline=False)
        if not tt[num - 1] in classlist.values():
            await error_arguments(message)
            return
    global ttembed
    ttembed = embed
    await message.channel.send(embed=ttembed)


async def set_tt(message):
    global tt
    tt = message.content[9:].split()
    await timetable(message)
    await message.channel.send(embed=ttembed)
    log_tt = ','.join(tt)
    await client.get_channel(TTlog_ID).send(log_tt)
    await message.delete()


async def edit_tt(message):
    global tt
    if tt == []:
        logch = client.get_channel(TTlog_ID)
        logid = logch.last_message_id
        savett = await logch.fetch_message(logid)
        tt = savett.content.split(',')
    contentlist = message.content[10:].split()
    try:
        idn = (int(contentlist[0]) - 1)
    except ValueError:
        await error_arguments(message)
        return
    ttchannel = client.get_channel(TT_ID)
    message_id = int(ttchannel.last_message_id)
    message_content = await ttchannel.fetch_message(message_id)
    subject = str(contentlist[1])
    try:
        tt[idn] = subject
    except IndexError:
        await error_arguments(message)
        return
    await timetable(message)
    newembed = ttembed
    await message.delete()
    await message_content.edit(embed=ttembed)
    log_tt = ','.join(tt)
    await client.get_channel(TTlog_ID).send(log_tt)


async def print_role(message):
    member = message.guild.members
    sinrai = message.guild.get_role(682220525992280095)
    checklist = []
    num = 0
    for check in member:
        role = member[num].roles
        if sinrai in role:
            checklist.append("○ " + str(member[num]))
        else:
            checklist.append("✕ " + str(member[num]))
        num += 1
    msg = "\n".join(checklist)
    embed = discord.Embed(
        title="ロールチェックの結果",
        description=f"信頼できる人\n{msg}"
    )
    await message.delete()
    await message.channel.send(embed=embed)


async def bougen(message):
    await message.channel.send("死ね！")


async def protect(message):
    await message.channel.send("ab!protect 602668987112751125")


@client.event
async def on_ready():
    print(discord.__version__)
    channel = client.get_channel(Start_ID)
    await channel.send("正常に起動しました")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    elif message.channel.id == Start_ID:  # 起動ログチャンネルで発言してもエラー&削除
        return
    elif (message.content == "やあ！") or (message.content == "やあ!"):
        await aisatu(message)
    elif message.content.startswith("ct!ttset "):
        await set_tt(message)
    elif message.content.startswith("ct!ttedit "):
        await edit_tt(message)
    elif message.content == "ct!role":
        await print_role(message)
    elif message.content == "ct!bougen":
        await bougen(message)
    elif message.content == "ct!protect":
        await protect(message)

client.run(TOKEN)
