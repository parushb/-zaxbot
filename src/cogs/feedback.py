from discord.ext import commands

OWNER_ID = 756144925086711905


class feedback(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__
        self.bot = bot

    @commands.hybrid_command(name="feedback")
    async def feedback(self, ctx: commands.Context, message: str):
        """
        Send the given message to the bot developer
        :param ctx:
        :param message: The actual message
        :return: None
        """
        member = self.bot.get_user(OWNER_ID)
        await member.send(f"Feedback From `{ctx.author}` in server '{ctx.guild.name}'\n```{message}```")
        await ctx.send("Feedback sent successfully", ephemeral=True)


async def setup(bot):
    await bot.add_cog(feedback(bot))
