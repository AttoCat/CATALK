import os
import dotenv
import discord
from discord.ext import commands
import traceback
import asyncio
import signal
import requests

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
EXTENSIONS = [
    "cogs.timetable"]


def handler(signum, frame):
    print('signal catched')
    URL = "https://discord.com/api/channels/706779308211044352/messages"
    headers = {
        "Authorization": f"Bot {TOKEN}"}
    item = {"content": "こんにちは"}
    requests.post(URL, headers=headers, json=item)


signal.signal(signal.SIGTERM, handler)


class Catalk(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        for cog in EXTENSIONS:
            try:
                self.load_extension(cog)
                print(f"Loaded Extension {cog}.py.")
            except Exception:
                traceback.print_exc()


if __name__ == '__main__':
    bot = Catalk(command_prefix=PREFIX)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.start())
    except KeyboardInterrupt:
        loop.run_until_complete(bot.logout())
    # cancel all tasks lingering
    finally:
        loop.close()
