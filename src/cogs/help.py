import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        super().__init__
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help(self, ctx: commands.Context):
        """
        Shows General Information about the Bot
        :param ctx:
        :return:
        """
        Embed = discord.Embed(colour=discord.Colour.brand_red())

        Embed.add_field(name="How to Play", inline=False,
                        value=f"You are a player named {self.bot.user.display_name}, your work is to push :brown_square:"
                              f" on top of their correct "
                              "destination :cactus:")
        Embed.add_field(name="Features", inline=False,
                        value="➡️`Infinite Levels`\n"
                              "Each Map is randomly generated, the difficulty increases as you progress in the Game\n"
                              "➡️`Controls`\n"
                              f"{self.bot.user.display_name} uses reactions as controls which are better than `wasd`"
                              f"commands\n"
                              "➡️`Play/Pause Game`\n"
                              "Since Each Game of Sokoban is played in a dedicated channel of it's own which only "
                              "you can see! which not only improves the experience of the Player but also gives "
                              "the ability to complete the game afterwards by just heading to the Game channel")
        Embed.add_field(name="Commands", inline=False,
                        value="**`/play`** to start a new game, If you are not in one\n"
                              "**`/stop`** to stop any running game, If any\n"
                              "**`/help`** displays this\n"
                              "**`/top`** shows the top player of this game\n"
                              "**`/profile`** shows the profile of the given user\n"
                              "**`/feedback`** can be used to report any issues or suggestion")

        Embed.add_field(name="Extra", inline=False,
                        value="Made with ❤️ by `init#0329`\n"
                              f"Source Code: [{self.bot.user.display_name} Bot Code](https://github.com/parushb/zaxbot)")

        await ctx.send(embed=Embed)


async def setup(bot):
    await bot.add_cog(Help(bot))

