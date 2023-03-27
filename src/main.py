from discord.ext import commands
import discord
import asyncio
import os
import asyncpg
import logging
from dotenv import load_dotenv
from threading import Thread

load_dotenv()

TOKEN = os.environ["zax_token"]


def alive():
    from flask import Flask

    app = Flask('')

    @app.route('/')
    def main_():
        return "Your Bot Is Ready"

    def run():
        app.run(host="0.0.0.0", port=8000)

    run()


server = Thread(target=alive)


async def database_pool(bot):
    try:
        bot.db = await asyncpg.create_pool(os.environ["neon_database"], statement_cache_size=0)

        print("Connected to the database")
    except asyncpg.ClientCannotConnectError:
        print("Couldn't connect to database")

    await bot.db.execute("CREATE TABLE IF NOT EXISTS game_info("
                         " user_id BIGINT,"
                         " games_won INTEGER DEFAULT 0,"
                         " games_started INTEGER DEFAULT 0,"
                         " level INTEGER DEFAULT 0,"
                         " username TEXT)")

    await bot.db.execute("CREATE TABLE IF NOT EXISTS running_games("
                         " user_id BIGINT,"
                         " channel_id BIGINT,"
                         " player_position INTEGER[],"
                         " game_won BOOLEAN DEFAULT false,"
                         " matrix_row_0 TEXT[],"
                         " matrix_row_1 TEXT[],"
                         " matrix_row_2 TEXT[],"
                         " matrix_row_3 TEXT[],"
                         " matrix_row_4 TEXT[],"
                         " matrix_row_5 TEXT[],"
                         " matrix_row_6 TEXT[],"
                         " matrix_row_7 TEXT[],"
                         " matrix_row_8 TEXT[],"
                         " old_player_position INTEGER[])")

    await bot.db.execute("CREATE TABLE IF NOT EXISTS users("
                         " user_id BIGINT,"
                         " username TEXT)")


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
            if not os.path.exists("cogs/player_data/temp_files"):
                os.makedirs(name="cogs/player_data/temp_files")
                open("cogs/player_data/live_players.txt", "w").close()
                open("cogs/player_data/running_channels.txt", "w").close()

    bot = UtilityBot(command_prefix="!", intents=intents, help_command=None)
    asyncio.run(load_cogs(bot))  # load the bot modules

    def run():
        handler = logging.FileHandler(filename="discord.log", encoding="utf-8")
        bot.server = server
        bot.run(token=TOKEN, log_handler=handler)

    run()


async def load_cogs(bot):
    for filename in os.listdir("cogs/"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cogs.{filename[:-3]}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
