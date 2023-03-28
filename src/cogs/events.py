import discord
from discord.ext.commands import Cog


class BaseEvents(Cog):
    def __init__(self, bot):
        self.bot: discord.ext.commands.Bot = bot

    @Cog.listener()
    async def on_ready(self):

        await self.bot.change_presence(activity=discord.Game('/play'))
        print(f'{self.bot.user} is ready!')

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

    @Cog.listener()
    async def on_connect(self):
        print(f'{self.bot.user} has connected!')
        await self.bot.tree.sync()

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):

        Embed = discord.Embed(colour=discord.Colour.brand_red())

        Embed.add_field(name="How to Play", inline=False,
                        value=f"You are a player named {self.bot.user.display_name}, your work is to push :brown_square: on top of their correct "
                              "destination :cactus:")
        Embed.add_field(name="Features", inline=False,
                        value="➡️`Infinite Levels`\n"
                              "Each Map is randomly generated, the difficulty increases as you progress in the Game\n"
                              "➡️`Varied Controls`\n"
                              f"{self.bot.user.display_name} has multiple control options to improve the player's experience,"
                              " including reactions and wasd commands!\n"
                              "➡️`Play/Pause Game`\n"
                              "Since Each Game of Sokoban is played in a dedicated channel of it's own which only "
                              "you can see! which not only improves the experience of the Player but also gives "
                              "the ability to complete the game afterwards by just heading to the channel of the Game!")
        Embed.add_field(name="Commands", inline=False,
                        value="**`/play`** to start a new game, If you are not in one\n"
                              "**`/stop`** to stop any running game, If any\n"
                              "**`/help`** displays this\n"
                              "**`/top`** shows the top player of this game\n"
                              "**`/profile`** shows the profile of the given user\n"
                              "**`/feedback`** can be used to report any issues or suggestion")

        Embed.add_field(name="Extras", inline=False,
                        value="Made with ❤️ by `init#0329`\n"
                              f"Source Code: [{self.bot.user.display_name} Bot Code](https://github.com/parushb/zaxbot)")
        try:
            await guild.system_channel.send(content="**Hello Nerds**, Here's some info about me", embed=Embed)
        except discord.ext.commands.MissingPermissions:
            await guild.owner.send(content=f"Hi, It's Bot {self.bot.user} from server {guild.name}\n"
                                           f"Looks like I dont have the required Permissions to Work Properly\n"
                                           f"Please grant me the following permissions so that I can work as intended\n"
                                           f"```\n"
                                           f"Manage Channels\nRead Messages\nSend messages\nManage Messages\n"
                                           f"Embed Links\nRead Message history\nAdd Reactions\nAdd Reactions\n"
                                           f"Use Slash Commands\n```")

        # ADD USERS TO DATABASE
        members_ = await self.bot.db.fetch(f"SELECT user_id FROM users")

        for guild_member in guild.members:
            if members_ is not None:
                if not guild_member.bot:
                    if guild_member.id not in members_:
                        username = f"{guild_member.name}#{guild_member.discriminator}"
                        await self.bot.db.execute(f"INSERT INTO users(username, user_id) VALUES($1, $2)",
                                                  username, guild_member.id)

                        await self.bot.db.execute(f"INSERT INTO game_info(user_id, username) VALUES($1, $2)",
                                                  guild_member.id, username)
            else:
                if not guild_member.bot:
                    username = f"{guild_member.name}#{guild_member.discriminator}"
                    await self.bot.db.execute(f"INSERT INTO users(username, user_id) VALUES($1, $2)",
                                              username, guild_member.id)

                    await self.bot.db.execute(f"INSERT INTO game_info(user_id, username) VALUES($1, $2)",
                                              guild_member.id, username)

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        members = await self.bot.db.fetchrow("SELECT user_id FROM users")
        if not member.bot:
            if members is not None:
                if member.id not in members:
                    await self.bot.db.execute(f"INSERT INTO users(username, user_id) VALUES($1, $2)",
                                              f"{member.name}#{member.discriminator}", member.id)
            else:
                await self.bot.db.execute(f"INSERT INTO users(username, user_id) VALUES($1, $2)",
                                          f"{member.name}#{member.discriminator}", member.id)


async def setup(bot):
    await bot.add_cog(BaseEvents(bot))
