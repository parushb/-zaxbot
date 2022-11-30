from discord.ext import commands
import discord
import asyncio
import os
import asyncpg
import logging
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("zax_token")


async def database_pool(bot):
    try:
        bot.db = await asyncpg.create_pool("postgresql://bot_manager@localhost/bot_server")
        print("Connected to the database")
    except asyncpg.ClientCannotConnectError:
        print("Couldn't connect to database")


def logger() -> logging.Logger:
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    handler = logging.FileHandler('broken.log')
    handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
    log.addHandler(handler)
    return log


def main():

    # set the bot intents
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    intents.message_content = True
    intents.reactions = True

    class UtilityBot(commands.Bot):

        async def setup_hook(self) -> None:
            await database_pool(bot)

    bot = UtilityBot(command_prefix="!", intents=intents)
    asyncio.run(load_cogs(bot))  # load the bot modules

    def run():
        handler = logging.FileHandler(filename="discord.log", encoding="utf-8")
        bot.run(token=TOKEN, log_handler=handler)

    run()


async def load_cogs(bot):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            print(filename)
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cogs.{filename[:-3]}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
