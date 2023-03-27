from discord.ext import commands
import discord


class Top(commands.Cog):
    def __init__(self, bot):
        super().__init__
        self.bot = bot

    @commands.hybrid_command(name="top", with_app_command=True)
    async def top(self, ctx: commands.Context):
        """
        Shows Top Players of this game
        :param ctx:
        :return:
        """
        info = await self.bot.db.fetch(
            f"with cte as (select *,dense_rank() over(order by games_won desc) as RANK from game_info)"
            f" Select rank, username, games_won from cte where rank<11")
        print(info)

        ranks = []
        username = []
        games_won = []
        r, u, w = "", "", ""

        if len(info) < 10:
            players = len(info)
        else:
            players = 10
        for i in range(players):
            ranks.append(info[i][0])
            username.append(info[i][1])
            games_won.append(info[i][2])

            r = r + f"`{ranks[i]}`\n"
            u = u + f"`{username[i]}`\n"
            w = w + f"`{games_won[i]}`\n"
        print(r)
        r = r.replace("`1`", ":first_place:")
        r = r.replace("`2`", ":second_place:")
        if players > 2:
            r = r.replace("`3`", ":third_place:")

        Embed = discord.Embed(title=f"Top {players} Zax Players", color=discord.Colour.gold())
        Embed.add_field(name="Rank", value=r)
        Embed.add_field(name="Username", value=u)
        Embed.add_field(name="Games Won", value=w)

        await ctx.send(embed=Embed)


async def setup(bot):
    await bot.add_cog(Top(bot))
