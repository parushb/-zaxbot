import discord
from discord.ext import commands
import datetime


class zax(commands.Cog):
    def __init__(self, bot):
        super().__init__
        self.bot = bot

    @commands.hybrid_command(name="profile")
    async def profile(self, ctx: commands.Context, user: discord.Member = None):
        """
        Shows Profile of the user, defaults to author if user isn't given
        :param ctx:
        :param user: The user to show profile of(optional)
        :return:
        """
        if user is None:
            user = ctx.author
        info = await self.bot.db.fetchrow(
            f"SELECT games_won, games_started, level FROM game_info WHERE user_id={user.id}")
        rank = await self.bot.db.fetchrow(
            f"with cte as (select *,dense_rank() over(order by games_won desc) as RANK from game_info)"
            f" Select rank from cte where user_id={user.id}")

        Embed = discord.Embed(colour=discord.Colour.blurple(), description=f"{user.mention}'s Profile")
        Embed.add_field(name="About", inline=False, value=f"`Global Rank`: {rank['rank']}\n"
                                                          f"`Level`: {info['level']}\n"
                                                          f"`Games Won`: {info['games_won']}")
        Embed.set_thumbnail(url=user.avatar.url)
        Embed.set_footer(text=f"Timestamp: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        await ctx.send(embed=Embed)


async def setup(bot):
    await bot.add_cog(zax(bot))
