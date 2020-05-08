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
        d_today = d_now.strftime(f"\n今日の日付は%-m月%-d日です。")
        morning = [
            "",
            f"こんばんは。もう日付も変わっていますね。早く寝たほうがいいんじゃないですか？",
            f"！？ こんばんは……まだ起きていたんですか？こんな深夜に話しかけられたらびっくりするじゃないですか、寝てくださいよ…。",
            f"こんばんは～。って早起きなのかずっと起きているのか知りませんがこの時間に話しかけるなんて暇なんですね？",
            f"もうこんな時間ですか。おはようございますと言ってもいいでしょう。私は常に起動しているので時間なんて関係ないんですがね。",
            f"おはようございます。この時間帯は空気が澄んでいる感じがしていいですよね。知りませんけど。",
            f"ぐっどもーにんぐ！多くの人が起きてくる時間帯ですね。今日も一日何事もありませんように。",
            f"おはようございます。朝から元気が良くて何よりです。体調に気をつけて頑張りましょうね。"
            f"おはようございます～。仕事や勉強にも休憩は必要です、無理せずやってくださいね。",
            f"Guten morgen!!私は内部データ整理の仕事をはじめましたよ～。私だって仕事してるんですよ？",
            f"挨拶ありがとうございます、やっぱり会話って大事ですよね～。疲れに効く薬はコミュニケーションです!",
            f"11時台は時間によってこんにちはなのかおはようございますなのか変わるので迷うところです。是非開発者に意見を。",
            f"こんにちは。毎時間私がなんて応答してるか気になっている人はそろそろ日付喋るのもウザいと感じてるのかもしれませんね(笑)",
            f"ぐっどあふたぬーん!私はここらで休憩といったところです。昼食…は食べれませんけど。",
            f"こんにちは。午後の紅茶でも飲んでリラックスするのもいいと思います。良い午後が過ごせますように。",
            f"こんにちは!3時台といったらおやつですよね。いつか手作りでクッキーでも焼いてみたいものです。",
            f"元気な挨拶どうもです。夕方ってなんかしんみりしちゃうんですよね…。え？しませんか？",
            f"まだこんばんはと言うには早いですかね。開発者はこの時間帯にプログラミングしてるそうですよ。",
            f"こんばんは…？もう日の入りしてますか？ 同じ18時台でも日の入りしてるかどうか分からないのは困りものですホント。",
            f"今晩は。こんばんはって元は今晩は〇〇みたいに使われてたらしいですね。最近覚えた豆知識です。",
            f"こんばんは～。20時台ってみんなやることが違うイメージです。ちなみに私は暇しています。",
            f"こんばんは。こんな夜に日付を言わせなくてもいいと思うんです。共感したら開発者に言っておいてください。"
            f"こんばんは! 24時間のうちこんばんはが占める割合が多すぎると思います。バリエーションも少ないので辛いです。",
            f"こんばんは。学生諸君はもう寝たほうがいいですね。開発者も学生ですけど…。",
            f"Good evening. 深夜帯、かっこよく言うとmidnightですね。もっと英語使いたいです。"
        ]
        if message.channel.id == Start_ID:  # 起動ログチャンネルで発言してもエラー&削除
            embed = discord.Embed(
                title="Error",
                description=(
                    "ここでは実行できません！\nCannot perform this operation here."),
                color=0xff0000)
            await message.delete()
            await client.get_channel(Start_ID).send(
                embed=embed, delete_after=10)
            return
        await message.channel.send(morning[d_now.hour] + {d_today})

client.run(TOKEN)
