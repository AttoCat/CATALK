import discord
from discord.ext import commands


class Timetable(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(682218950268157982)
        self.ttlog = self.guild.get_channel(712238123605557269)
        self.ttch = self.guild.get_channel(711397925103599621)
        self.classlist = {
            "こ": "国語", "す": "数学", "り": "理科", "しゃ": "社会",
            "え": "英語", "ほ": "保体", "お": "音楽", "び": "美術",
            "ぎ": "技術", "か": "家庭", "ど": "道徳", "そ": "総合",
            "が": "学活", "た": "その他"}

    @commands.is_owner()
    @commands.command()
    async def say(self, ctx, *, content):
        await ctx.send(content)

    @commands.group()
    async def tt(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')
            return

    @tt.command()
    async def set(self, ctx, *args):
        args = list(args)
        if len(args) > 6:
            return
        embed = discord.Embed(
            title="時間割",
            description="明日の時間割",
            color=0x0080ff)
        num = 1
        kekka = []
        for jugyo in args:
            if jugyo in self.classlist:
                jugyo = self.classlist[jugyo]
            else:
                if jugyo not in self.classlist.values():
                    raise commands.BadArgument
            embed.add_field(
                name=f"{num}時間目",
                value=jugyo,
                inline=False)
            num += 1
            kekka.append(jugyo)
        await self.ttch.send(embed=embed)
        await self.ttlog.send(",".join(kekka))

    @tt.command()
    async def edit(self, ctx, num: int, value):
        id = self.ttlog.last_message_id
        msg = await self.ttlog.fetch_message(id)
        tt = msg.content.split(",")
        tt[num - 1] = value
        chid = self.ttch.last_message_id
        ttmsg = await self.ttch.fetch_message(chid)
        kekka = []
        embed = discord.Embed(
            title="時間割",
            description="明日の時間割",
            color=0x0080ff)
        for jugyo in tt:
            if jugyo in self.classlist:
                jugyo = self.classlist[jugyo]
            else:
                if jugyo not in self.classlist.values():
                    raise commands.BadArgument
            embed.add_field(
                name=f"{num}時間目",
                value=jugyo,
                inline=False)
            num += 1
            kekka.append(jugyo)
        await ttmsg.edit(embed=embed)

    @commands.command()
    async def fetch(self, ctx, arg: int):
        _ = await ctx.channel.fetch_message(arg)

    @commands.command()
    async def test(self, ctx):
        a = 15
        await eval(f"ctx.send({a})")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title="Error",
                description=(
                    "あなたにこのコマンドを実行する権限がありません！\nYou don't have permission."),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                title="Error",
                description=(
                    "不正な引数です！\nInvalid argument passed."),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error",
                description="想定しない引数が渡されました！\nInvalid input.",
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        elif isinstance(error, discord.NotFound):
            print("NotFound")
            return
        elif isinstance(error, commands.TooManyArguments):
            embed = discord.Embed(
                title="Error",
                description="引数の数が不正です！\nInvalid input.",
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        else:
            embed = discord.Embed(
                title="Error",
                description=(
                    f"不明なエラーが発生しました。\nエラー内容:\n{error}"),
                color=0xff0000)
            await ctx.message.delete()
            await ctx.channel.send(embed=embed)
            return

    @commands.command()
    async def t(self, ctx):
        embed = discord.Embed(
            title="「BadArgument(不正な引数）エラーです。」と表示されたんだけど！",
            description="理由:その役職が存在しない")
        embed.add_field(
            name="対処法", value="その役職が存在するか**よく確かめる**\nよくあるのが大文字小文字のミス。", inline=False)
        embed.add_field(
            name="対処法2", value="**--create 引数**を付けてコマンドを使う\n例:`!rp2 add 役職 --create`", inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Timetable(bot))
