import discord
client = discord.Client()


@client.event
async def on_ready():
    print("on_ready 正常に起動しました")
    print(discord.__version__)

client.run("NzA0NjE5NzU0MTA2NzgxNzQ5.XqfyeA.4tGoPySZyW7TL3jSoN5cdIPiJuQ")
