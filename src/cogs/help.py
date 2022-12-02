import discord
from discord import app_commands
from discord.ext import commands



class Help(commands.Cog):

    def __init__(self, bot):
        super().__init__
        self.bot = bot

    @commands.hybrid_command(name="help")
    async def help(self, ctx: commands.Context):
        Embed = discord.Embed(colour=discord.Colour.brand_red())

        Embed.add_field(name="How to Play", inline=False,
                        value="You are a player named Zax, your work is to push :brown_square: on top of their correct "
                              "destination :cactus:")
        Embed.add_field(name="Features", inline=False,
                        value="➡️`Infinite Levels`\n"
                              "Each Map is randomly generated, the difficulty increases as you progress in the Game"
                              "➡️`Varied Controls`\n"
                              "Zax has multiple control options to improve the player's experience,"
                              " including reactions and wasd commands!"
                              "➡️`Play/Pause Game`\n"
                              "Since Each Game of Sokoban is played in a dedicated channel of it's own which only "
                              "you can see! which not only improves the experience of the Player but also gives "
                              "the ability to complete the game afterwards by just heading to the channel of the Game!")
        Embed.add_field(name="Commands", inline=False,
                        value="**`/play`** to start a new game, If you are not in one\n"
                              "**`/stop`** to stop any running game, If any\n"
                              "**`/help`** displays this")

        Embed.add_field(name="", inline=False,
                        value="Made with ❤️ by `init#0329`\n"
                              "Source Code: [Zax Bot Code](https://github.com/parushb/zaxbot)")

        await ctx.send(embed=Embed)


async def setup(bot):
    await bot.add_cog(Help(bot))

