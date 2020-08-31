import os
import dotenv
import discord
from discord.ext import commands
import traceback

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
EXTENSIONS = [
    "cogs.timetable"]


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
    bot.run(TOKEN)
