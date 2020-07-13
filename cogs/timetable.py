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
                if not jugyo in self.classlist.values():
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
        tt[num-1] = value
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
                if not jugyo in self.classlist.values():
                    raise commands.BadArgument
            embed.add_field(
                name=f"{num}時間目",
                value=jugyo,
                inline=False)
            num += 1
            kekka.append(jugyo)
        await ttmsg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Timetable(bot))
