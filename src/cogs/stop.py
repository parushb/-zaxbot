import discord
from discord.ext import commands
from discord import app_commands


async def ask_perms(ctx, perm=None):
    try:
        await ctx.send("Looks Like I don't have the required perms to functions properly,\n"
                       f"Please grant me the following permission(s)\n```\n{perm}\n```")
    except discord.ext.commands.BotMissingPermissions:
        await ctx.guild.owner.send(content=
                                   f"Looks like I dont have the required Permissions to Work Properly\n"
                                   f"Please grant me the following permissions so that I can work as intended\n"
                                   f"```\n"
                                   f"Manage Channels\nRead Messages\nSend messages\nManage Messages\n"
                                   f"Embed Links\nRead Message history\nAdd Reactions\nAdd Reactions\n"
                                   f"Use Slash Commands\n```")


class Stop(commands.Cog):
    def __init__(self, bot):
        super().__init__

        self.bot: commands.Bot = bot

    @commands.hybrid_command(name="stop")
    async def stop(self, ctx: commands.Context):

        check = await self.bot.db.fetchrow(
            f"SELECT user_id, channel_id FROM running_games WHERE user_id={ctx.author.id}")
        try:
            if len(check) != 0:
                running_channel = self.bot.get_channel(check["channel_id"])
                await running_channel.delete()

                await self.bot.db.execute(f"DELETE FROM running_games WHERE user_id={ctx.author.id}")
                try:
                    await ctx.send(f"Stopped your running game")
                except discord.ext.commands.BotMissingPermissions:
                    await ask_perms(ctx, "send_messages")

                return
        except TypeError:
            pass
