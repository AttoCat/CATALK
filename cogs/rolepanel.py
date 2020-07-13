import asyncio
import io
import math
import typing
import os
import re
import traceback
import datetime
import argparse
import collections
from concurrent import futures
import functools
from textwrap import dedent

import discord
from discord.ext import commands


class MyArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        raise commands.BadArgument(message)


class Role_panel(commands.Cog):  # 役職パネルの機能(パブリック)
    __slots__ = ('bot', 'channel_ids', 'name', 'log_channel',
                 'firstlaunch', 'traceback_channel')
    title_format = '役職パネル({0})({1}ページ目)'
    pattern = re.compile(r'役職パネル\((.+?)\)\((\d+?)ページ目\)')
    EMOJI = 0x0001f1e6
    EMOJIS = []
    for i in range(20):
        EMOJIS.append(chr(EMOJI + i))
    del i
    join_message = dedent(
        """
        役職パネルBOTv2を導入していただき、ありがとうございます。
        ヘルプはこちら
        https://kesigomon.hatenablog.jp/entry/2020/04/25/010627
        https://kesigomon.hatenablog.jp/draft/k4HCKE7iTitzyNqz7VxNbNGmkmA
        prefixは「!rp2」または「!rolepanel2」です。

        役職パネルのサポートは、「ケシゴモンのギルド」でやっています。
        「役職パネル相談室」でどうぞ。
        https://discord.gg/k765nXt
        """
    )
    help_order = ('help', 'role', 'add', 'remove', 'donate')

    def __init__(self, bot, name=None):
        self.bot: commands.Bot = bot
        self.firstlaunch = True
        self.name = name if name is not None else type(self).__name__

    def log(self, text):
        asyncio.ensure_future(self.log_channel.send(text), loop=self.bot.loop)

    @staticmethod
    async def try_to_send(channel, *args, **kwargs):
        try:
            return await channel.send(*args, **kwargs)
        except discord.Forbidden:
            return None

    @commands.Cog.listener()
    async def on_ready(self):
        if self.firstlaunch:
            self.firstlaunch = False
            self.bot.loop.create_task(self._update_activity())
        self.log_channel = self.bot.get_channel(682776223813861454)
        self.traceback_channel = self.bot.get_channel(682776237785350180)
        self.log(f'{self.bot.user.name}:起動しました')

    async def _update_activity(self):
        while not self.bot.is_closed():
            guild = len(self.bot.guilds)
            games = [
                discord.Activity(name=name, type=discord.ActivityType.playing) for name in
                (
                    f"!rp2 | {guild}のサーバーが導入しています。",
                    f"!rp2 | サポートサーバー: https://discord.gg/k765nXt",
                )
            ]
            for game in games:
                await self.bot.change_presence(activity=game)
                await asyncio.sleep(60)

    @commands.group(name="rolepanel2", aliases=['rp2'])
    async def rolepanel(self, ctx):
        command = ctx.invoked_subcommand
        if command is not None:
            self.log(
                f"{ctx.author}が{ctx.guild}の{ctx.channel}で{command.name}を使用しました")

    @rolepanel.command()
    async def stop(self, ctx):
        if ctx.author.id in (264397679705063424, 427879630456750082):
            await ctx.send("停止します")
            await self.bot.close()

    @rolepanel.command(brief='このメッセージを表示します')
    async def help(self, ctx: commands.Context):
        parent: commands.Group = ctx.command.parent
        inline = False
        embed = discord.Embed(
            title='役職パネルヘルプ',
            description="[更に詳しいヘルプはこちら](https://kesigomon.hatenablog.jp/draft/k4HCKE7iTitzyNqz7VxNbNGmkmA)"
        )
        [embed.add_field(name=c.name, value=c.brief, inline=inline)
         for c in (parent.get_command(i) for i in self.help_order)]
        await ctx.send(embed=embed)

    @commands.guild_only()
    @rolepanel.command(brief='このサーバーの役職とIDを表示します')
    async def role(self, ctx: commands.Context, page=0):
        try:
            page = int(page)
        except ValueError:
            await ctx.send('ページには数字を入れてください')
            return
        title = 'Botが取得できるロール一覧です。'
        description = ''
        nowpage = 0
        for role in (i for i in reversed(ctx.guild.roles) if not i.is_default()):
            temp_description = '{1}(ID:{0})\n'.format(role.id, role.mention)
            if len(description + temp_description) <= 2048:
                description += temp_description
            elif page == nowpage:
                break
            else:
                description = temp_description
                nowpage += 1
        embed = discord.Embed(title=title, description=description)
        embed.set_footer(text=(
            f'今のページは{nowpage + 1}です。"!rp2 role <番号>"と打つとそのページを表示します。'
            + '「削除」と入力すると即削除、「維持」と入力すると削除せずにそのままにします。'
        ))
        message1 = await ctx.send(embed=embed)

        def check(m):
            return (
                m.author == ctx.author
                and m.channel == ctx.channel
                and m.content in ('削除', '維持')
            )

        try:
            message2 = await self.bot.wait_for(
                event='message',
                check=check,
                timeout=30
            )
        except asyncio.TimeoutError:
            try:
                await message1.delete()
            except discord.NotFound:
                pass
        else:
            if message2.content == '削除':
                await message1.delete()
            if message2.content == '維持':
                await ctx.send('このまま役職一覧を維持します')

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if ctx.cog is self:
            permission: discord.Permissions = ctx.channel.permissions_for(
                ctx.me)
            if isinstance(error, commands.CommandInvokeError):
                error = error.original
            if isinstance(error, commands.NoPrivateMessage):
                content = 'サーバー内でのみ使用できます。'
            elif isinstance(error, commands.MissingRequiredArgument):
                content = '引数が足りません。必要な引数を与えてください。'
            elif isinstance(error, commands.BadArgument):
                content = 'BadArgument(不正な引数）エラーです。\n'
                content += error.args[0]
            elif isinstance(error, commands.ArgumentParsingError):
                content = 'ArgumentParsingErrorエラーです。\n' \
                          + error.args[0]
            elif isinstance(error, discord.Forbidden):
                content = dedent(
                    """
                    権限不足です。以下の権限があるかもう一度確かめてください。
                    （チャンネルの追加設定、このBOTに付けられている役職など）
                    """
                )
                if not permission.send_messages:
                    content += '・メッセージを送信\n'
                if not permission.embed_links:
                    content += '・埋め込みリンク\n'
                if not permission.read_message_history:
                    content += '・メッセージ履歴を読む\n'
                if not permission.add_reactions:
                    content += '・リアクションを追加\n'
            else:
                stream = io.StringIO()
                stream.write(dedent(
                    f"""
                    サーバー：{ctx.guild.name}(ID:{ctx.guild.id})
                    チャンネル:{ctx.channel.name}(ID:{ctx.channel.id})
                    ユーザー:{ctx.author}(ID:{ctx.author.id})
                    打ったコマンド:{ctx.message.content}
                    """
                ))
                traceback.print_exception(
                    type(error), error, error.__traceback__, file=stream)
                stream.seek(0)
                file1 = discord.File(stream, filename='traceback.txt')
                await self.traceback_channel.send(file=file1)
                content = (
                    '何らかの想定されていないエラーが発生しました。\n'
                    'サポートサーバーにお問い合わせください。'
                )
            if permission.send_messages:
                sendto = ctx.channel
            else:
                sendto = ctx.author
            await sendto.send(content)

    def convert(self, message: discord.Message):
        """
        タイトルを確認し、役職パネルのタイトルなら
        タグとページを返す関数
        そうでなければNoneを返す。
        """
        if message.author != self.bot.user:
            return None
        try:
            match = self.pattern.search(message.embeds[0].title)
        except (TypeError, IndexError):
            return None
        else:
            if match:
                return match.groups()
            else:
                return None

    async def check1(self, ctx, role):
        if not await self.check2(ctx):
            return False
        elif ctx.author.top_role <= role and ctx.guild.owner != ctx.author:
            await ctx.send(f'{role.name}は、あなたの一番上の役職以上の役職でないので、追加/削除できません。')
        else:
            return True

    @staticmethod
    async def check2(ctx):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send('あなたに「役職の付与」の権限がないので、このコマンドを実行できません。')
        else:
            return True

    def create_converter(self, ctx, converter):
        def callback(arg):
            fut = asyncio.run_coroutine_threadsafe(
                converter.convert(ctx, arg),
                self.bot.loop
            )
            return fut.result()

        return callback

    async def parse_args1(self, ctx, *args):
        def fn():
            # add か remove用argument parser
            parser = MyArgumentParser()
            parser.add_argument("roles", nargs="+")
            parser.add_argument("--channel", "-c", default=ctx.channel,
                                type=self.create_converter(ctx, commands.TextChannelConverter()))
            parser.add_argument("--tag", "-t", default=None)
            parser.add_argument("--emoji", default=None)
            parser.add_argument("--color", default=0,
                                type=self.create_converter(ctx, commands.ColourConverter()))
            parser.add_argument("--create", action='store_true')
            parser.add_argument("--delete", action='store_true')
            return parser.parse_args(args)

        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            return await asyncio.wrap_future(executor.submit(fn))

    @commands.guild_only()
    @rolepanel.command(brief='役職パネルに役職を追加します')
    async def add(self, ctx, *args):
        """
        役職を追加します。
        """
        # add不可ならスルー
        if not await self.check2(ctx):
            return
        # argument parse
        result = await self.parse_args1(ctx, *args)
        if result.create:
            roles = []
            for name in result.roles:
                role = await ctx.guild.create_role(name=name)
                roles.append(role)
        else:
            converter = commands.RoleConverter()
            roles = [await converter.convert(ctx, arg) for arg in result.roles]
        # タグを指定（指定されて無ければデフォルト)
        tag = result.tag
        if tag is None:
            tag = "デフォルト"
        emoji = result.emoji
        if emoji is not None and len(result.roles) >= 2:
            raise commands.BadArgument(
                message="絵文字引数を取っている場合、役職を複数取ることはできません。")

        def check(m):
            # ここで、役職パネルのメッセージであるか、タグが同じであるかを確認する！
            data = self.convert(m)
            return data is not None and data[0] == tag

        channel = result.channel
        history = await channel.history(limit=None, oldest_first=True).filter(check).flatten()
        page = len(history)
        history = collections.deque(history)
        m = None
        for role in roles:
            if not await self.check1(ctx, role):
                continue
            while True:
                if m is None:
                    try:
                        # 次のパネルを出す
                        m = history.pop()
                    except IndexError:
                        # もう貼れるパネルが無ければ新しく作る
                        if emoji is None:
                            emoji = self.EMOJIS[0]
                        embed = discord.Embed(
                            title=self.title_format.format(tag, page + 1),
                            description='{0}:{1}'.format(emoji, role.mention),
                            colour=result.color
                        )
                        page += 1
                        m = await channel.send(embed=embed)
                        await m.add_reaction(emoji)
                        emoji = None
                        break
                if await self.add_to_role_message(m, role, emoji):
                    # もし既存パネルに追加できればこの役職終わり
                    break
                m = None

    async def add_to_role_message(self, message, role, emoji):
        """
        既存パネルに役職追加
        add できれば True返す
        """

        # 絵文字が20以上ならaddできない
        if len(message.reactions) >= 20:
            return False
        embed = message.embeds[0]
        description = embed.description
        # 多分description なしの場合想定？
        # あとコード補完用
        if isinstance(description, str):
            lines = description.splitlines()
            # デフォルト A~Tの絵文字サーチ
            if emoji is None:
                for i, character in enumerate(self.EMOJIS):
                    if character not in description:
                        break
                else:
                    # もうつけられる絵文字がなければreturn False
                    return False
            # 絵文字指定時
            else:
                character = emoji
                i = len(lines)
            if character not in description:
                # 最初にリアクションを確認(つけられないならここでエラーになるので全止め可能)
                await message.add_reaction(character)
                new_lines = '\n'.join(
                    lines[0:i]
                    + ['{0}:{1}'.format(character, role.mention)]
                    + lines[i:len(lines) + 1]
                )
                embed.description = new_lines
                await message.edit(embed=embed)
                return True

    @commands.guild_only()
    @rolepanel.command(brief='役職パネルから役職を削除します')
    async def remove(self, ctx, *args):
        """
        役職を削除します。
        """
        # remove不可ならスルー
        if not await self.check2(ctx):
            return
        # argument parse
        result = await self.parse_args1(ctx, *args)
        converter = commands.RoleConverter()
        roles = [await converter.convert(ctx, arg) for arg in result.roles]
        tag = result.tag
        channel = result.channel
        for role in roles:  # type: discord.Role
            if not await self.check1(ctx, role):
                continue
            # 全脱出用
            break1 = False
            async for m in channel.history(oldest_first=True):
                data = self.convert(m)
                # タグが指定されていて、違うならスキップ
                if data is None or (tag is not None and data[0] != tag):
                    continue
                embed = m.embeds[0]
                description = embed.description
                lines = description.splitlines(keepends=True)
                for line in lines[:]:
                    # 役職メンションがあれば
                    if role.mention in line:
                        # その行を消す
                        embed.description = description.replace(line, '')
                        # パネル編集
                        await m.edit(embed=embed)
                        # 絵文字除去
                        await m.remove_reaction(line.replace(":" + role.mention, ""), self.bot.user)
                        break1 = True
                        if result.delete:
                            await role.delete()
                        break
                embed = m.embeds[0]
                description = embed.description
                if not description:
                    await m.delete()
                if break1:
                    break

    async def before_edit(self, ctx: commands.Context, *args) \
            -> typing.Tuple[typing.Union[None, discord.Message], argparse.Namespace]:
        # edit か　delete_panel用。
        # メッセージ返す
        def fn():
            parser = MyArgumentParser()
            parser.add_argument("oldtag")
            parser.add_argument("page", type=int, default=1)
            parser.add_argument("--tag", "-t", default=None)
            parser.add_argument("--color", default=None,
                                type=self.create_converter(ctx, commands.ColourConverter()))
            # argument parse
            return parser.parse_args(args)

        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            result = await asyncio.wrap_future(executor.submit(fn))

        async for message in ctx.history(limit=None):
            data = self.convert(message)
            if data is None:
                continue
            tag, page = data
            if tag == result.oldtag and int(page) == result.page:
                break
        else:
            message = None
        return message, result

    @commands.guild_only()
    @rolepanel.command(brief="v1から引き継ぎをします")
    async def hikitugi(self, ctx, channel=None):
        if channel is None:
            channel = ctx.channel
        async for message in channel.history(limit=None, oldest_first=True):
            if (
                message.author.id != 542980279455973378
                or not message.embeds
            ):
                continue
            embed = message.embeds[0]
            new_message = await channel.send(embed=embed)
            for reaction in message.reactions:
                await new_message.add_reaction(reaction)

    @commands.guild_only()
    @rolepanel.command(brief="パネルを編集します")
    async def edit(self, ctx, *args):
        # edit不可ならスルー
        if not await self.check2(ctx):
            return
        # まずはメッセージ取得
        message, result = await self.before_edit(ctx, *args)
        if message is None:
            await ctx.send("パネルが見つかりませんでした")
            return
        embed: discord.Embed = message.embeds[0]

        # カラー編集
        if result.color is not None:
            embed.colour = result.color

        # タグ編集
        if result.tag is not None:
            lastpage = 0
            async for mes in ctx.history(limit=None):
                data = self.convert(mes)
                if data is None:
                    continue
                tag, page = data
                if tag == result.tag:
                    lastpage = max(lastpage, int(page))
            embed.title = self.title_format.format(result.tag, lastpage + 1)
        await message.edit(embed=embed)

    @commands.guild_only()
    @rolepanel.command(aliases=[], brief='もう存在しない役職の行を削除します')
    async def autoremove(self, ctx):
        if not await self.check2(ctx):
            return
        prog = re.compile(r'<@&(\d*)>')
        guild: discord.Guild = ctx.guild
        async for message in ctx.history(limit=None, oldest_first=True):
            message: discord.Message
            data = self.convert(message)
            if data is None:
                continue
            embed = message.embeds[0]
            description = embed.description
            # コード補完用
            if isinstance(description, str):
                # 1行ごとにテキストを取る
                lines = description.splitlines()
                for index, line in enumerate(lines.copy()):
                    # 役職のIDを取得
                    role_id = int(prog.search(line).group(1))
                    role = guild.get_role(role_id)
                    # 役職が無いならその行は消す！
                    if role is None:
                        del lines[index]
                if lines:
                    embed.description = "\n".join(lines)
                    await message.edit(embed=embed)
                else:
                    await message.delete()

    @commands.guild_only()
    @commands.command(brief="使用したチャンネル内のメッセージIDのパネルを探しリアクションをつけ直します")
    # 仮実装、argparse使うようにするならchannelの引数を渡してfetchするべき
    async def refresh(self, ctx, *args):
        def fn():
            parser = MyArgumentParser()
            parser.add_argument("--channel", "-c", default=ctx.channel,
                                type=self.create_converter(ctx, commands.TextChannelConverter()))
            return parser.parse_args(args)
        result = fn()
        try:
            message = await result.channel.fetch_message()
        except ValueError:
            await ctx.send("そのメッセージはパネルではないようです")
        if not await self.check2(ctx):
            return
        if message.author == self.bot.user and message.embeds:
            await message.clear_reactions()
            embed = message.embeds[0]
            lines = embed.description.splitlines()
            for i in range(len(lines)):
                character = chr(0x0001f1e6 + i)
                await message.add_reaction(character)

    @rolepanel.command(brief='寄付URLを表示します。\nBOTが気に入ったならぜひどうぞ！')
    async def donate(self, ctx):
        await ctx.send(
            '寄付はこちらからどうぞ。\nhttps://www.paypal.me/kesigomon\n'
            'また、Kesigomon#4752にDMでアマギフを送ってもらっても構いません')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        message = reaction.message
        if self.convert(message):
            try:
                await message.remove_reaction(reaction, user)
            except discord.Forbidden:
                pass
            match2 = re.search(str(reaction.emoji) +
                               r':<@&(\d*)>', message.embeds[0].description)
            if match2:
                guild: discord.Guild = message.guild
                role = guild.get_role(int(match2.group(1)))
                if role is None:
                    description = '役職が存在しないか、見つかりませんでした。'
                else:
                    if role not in user.roles:
                        try:
                            await user.add_roles(role)
                        except discord.Forbidden:
                            error = True
                        else:
                            description = '{0}の役職を付与しました。'.format(role.mention)
                            self.log(
                                f"{guild}の{message.channel}の役職パネルで{user}が{role}の付与成功")
                            error = False
                    else:
                        try:
                            await user.remove_roles(role)
                        except discord.Forbidden:
                            error = True
                        else:
                            description = '{0}の役職を解除しました'.format(role.mention)
                            self.log(
                                f"{guild}の{message.channel}の役職パネルで{user}が{role}の解除成功")
                            error = False
                    if error:
                        description = '役職の設定に失敗しました。\n'
                        if not guild.me.guild_permissions.manage_roles:
                            description += 'BOTに「役職の管理」の権限が無いかも？'
                            self.log(
                                f"{guild}の{message.channel}の役職パネルで{user}が{role}の付与失敗(権限不足)")
                        elif guild.me.top_role <= role:
                            description += 'BOTの一番上の役職よりも高い役職をつけようとしてるかも？'
                            self.log(
                                f"{guild}の{message.channel}の役職パネルで{user}が{role}の付与失敗(役職位置)")
                        else:
                            description += 'エラーの原因がぜんぜんわからん！'
                            self.log(f"{guild}の{message.channel}の役職パネルで{user}が{role}の付与失敗"
                                     "(意☆味☆不☆明なエラー)")
                await self.try_to_send(
                    message.channel,
                    user.mention,
                    embed=discord.Embed(description=description),
                    delete_after=10
                )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user:
            return
        cache = self.bot._connection._messages
        # キャッシュに入ってる(reaction_addがすでに作動している)
        if payload.message_id in (m.id for m in cache):
            return
        channel = self.bot.get_channel(payload.channel_id)
        try:
            message = await channel.fetch_message(payload.message_id)
        except (discord.Forbidden, discord.NotFound):
            return
        if self.convert(message):
            cache.append(message)
            user = self.bot.get_guild(
                payload.guild_id).get_member(payload.user_id)
            if payload.emoji.is_unicode_emoji():
                reaction = next(
                    r for r in message.reactions if not r.custom_emoji and r.emoji == payload.emoji.name)
            else:
                reaction = next(
                    r for r in message.reactions if r.custom_emoji and r.emoji.id == payload.emoji.id)
            await self.on_reaction_add(reaction, user)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        owner: discord.Member = guild.owner
        await owner.send(self.join_message)
        self.log(f"BOTが{guild}に導入された")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.log(f"BOTが{guild}から退出した")


def setup(bot):
    bot.add_cog(Role_panel(bot))
