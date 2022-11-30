import discord
from discord.ext.commands import Cog

TESTING_SERVER = 983057539212120065

class BaseEvents(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is ready!')

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

    @Cog.listener()
    async def on_connect(self):
        print(f'{self.bot.user} has connected!')
        await self.bot.tree.sync(guild=discord.Object(id=TESTING_SERVER))


async def setup(bot):
    await bot.add_cog(BaseEvents(bot))
