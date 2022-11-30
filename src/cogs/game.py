import random
import re

import discord
from discord import app_commands
from discord.ext import commands

TESTING_SERVER = 983057539212120065


class Soko(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__
        self.matrix = []
        self.id_ = None
        self.bot = bot
        self.matrix_string = ''
        self.Inside_fill: str = ":black_large_square:"
        self.Boundaries: str = ":red_square:"
        self.Obstacle: str = ":brown_square:"
        self.Dump: str = ":cactus:"
        self.Player_emoji: str = ":dotted_line_face:"

        self.reaction_to_text = {
            "⬆️": "w",
            "⬅️": "a",
            "➡️": "d",
            "⬇️": "s"
        }

    async def end_game(self, user, channel, won=False, delete_channel=True, permanent=False):
        if delete_channel:
            await channel.delete()
        if permanent:
            await self.bot.db.execute(f"DELETE FROM running_games WHERE user_id={user}")
        if won:
            games_won = await self.bot.db.fetchrow(f"SELECT games_won FROM game_info WHERE user_id={user}")
            games_won = games_won["games_won"]
            await self.bot.db.execute(f"UPDATE game_info SET games_won={games_won + 1} WHERE user_id={user}")
        return

    async def generate_new_matrix(self, author: discord.Member, message: discord.Message):
        mat_width = 15
        mat_height = 9
        self.matrix: list = [[self.Inside_fill for _ in range(mat_width)] for _ in range(mat_height)]
        for i in range(mat_width):
            self.matrix[0][i] = self.Boundaries
            self.matrix[mat_height - 1][i] = self.Boundaries

        for n in range(mat_height):
            self.matrix[n][0] = self.Boundaries
            self.matrix[n][mat_width - 1] = self.Boundaries

        # OBSTACLES
        for f in range(random.randint(3, 7)):
            self.matrix[random.randint(2, mat_height - 3)][random.randint(2, mat_width - 3)] = self.Obstacle
            self.matrix[random.randint(1, mat_height - 2)][random.randint(1, mat_width - 2)] = self.Dump

        # PLAYER
        player_position = [random.randint(1, mat_height - 2), random.randint(1, mat_width - 2)]
        self.matrix[player_position[0]][player_position[1]] = self.Player_emoji

        # Initial Matrix to String
        self.matrix_string = f"{''.join(self.matrix[0])}\n" \
                             f"{''.join(self.matrix[1])}\n" \
                             f"{''.join(self.matrix[2])}\n" \
                             f"{''.join(self.matrix[3])}\n" \
                             f"{''.join(self.matrix[4])}\n" \
                             f"{''.join(self.matrix[5])}\n" \
                             f"{''.join(self.matrix[6])}\n" \
                             f"{''.join(self.matrix[7])}\n" \
                             f"{''.join(self.matrix[8])}\n"
        # Send to the channel
        Embed = discord.Embed(title="Game", description=f"{self.matrix_string}",
                              colour=discord.Colour.teal())

        await message.edit(embed=Embed)

        await self.bot.db.execute(
            f"UPDATE running_games SET "
            f"old_player_position = $1, matrix_row_0 = $2, matrix_row_1= $3, matrix_row_2 = $4, matrix_row_3 = $5, "
            f"matrix_row_4 = $6, matrix_row_5 = $7, matrix_row_6 = $8, "
            f"matrix_row_7 = $9, matrix_row_8 = $10, player_position = $11, game_won=False"
            f" WHERE user_id = {author.id}",
            player_position, self.matrix[0], self.matrix[1], self.matrix[2], self.matrix[3], self.matrix[4],
            self.matrix[5], self.matrix[6], self.matrix[7], self.matrix[8], player_position)

        print("Updated the matrix to a new one")

    async def move(self, direction, user_id, message: discord.Message, matrix, player_position, reaction: bool = False):
        game_won = False
        if direction == "w":
            new_player_position = [player_position[0] - 1, player_position[1]]
            print(f"New Position: {new_player_position}")

            if matrix[new_player_position[0]][new_player_position[1]] == ":red_square:":
                print(matrix[new_player_position[0]][new_player_position[1]])
                print("Found Collision")
                await message.channel.send("Boundary")

                return

            if matrix[new_player_position[0]][new_player_position[1]] == ":cactus:":
                print(matrix[new_player_position[0]][new_player_position[1]])
                print("Found Collision")
                await message.channel.send("Cactus")

                return

            # Check for Collision
            if matrix[new_player_position[0]][new_player_position[1]] == self.Obstacle:
                print("Found Obstacle")
                if matrix[new_player_position[0] - 1][new_player_position[1]] == self.Boundaries:
                    print("Found Boundary")
                    return

                elif matrix[new_player_position[0] - 1][new_player_position[1]] == self.Dump:
                    print("Found Dump")
                    matrix[new_player_position[0] - 1][new_player_position[1]] = self.Boundaries

                # For double obstacle
                elif matrix[new_player_position[0] - 1][new_player_position[1]] == self.Obstacle:
                    await message.channel.send("Double Collision")
                    return

                elif matrix[new_player_position[0] - 1][new_player_position[1]] == self.Inside_fill:
                    print(matrix[new_player_position[0] - 1][new_player_position[1]])
                    matrix[new_player_position[0] - 1][new_player_position[1]] = self.Obstacle

            matrix[player_position[0]][player_position[1]] = self.Inside_fill
            matrix[new_player_position[0]][new_player_position[1]] = self.Player_emoji
        #############################################################################################
        elif direction == "a":
            new_player_position = [player_position[0], player_position[1] - 1]
            print(f"New Position: {new_player_position}")

            if matrix[new_player_position[0]][new_player_position[1]] == ":red_square:":
                print(matrix[new_player_position[0]][new_player_position[1]])
                print("Found Collision")
                await message.channel.send("Boundary")

                return

            if matrix[new_player_position[0]][new_player_position[1]] == ":cactus:":
                print(matrix[new_player_position[0]][new_player_position[1]])
                print("Found Collision")
                await message.channel.send("Cactus")

                return

            # Check for Collision
            if matrix[new_player_position[0]][new_player_position[1]] == self.Obstacle:
                print("Found Obstacle")
                if matrix[new_player_position[0]][new_player_position[1] - 1] == self.Boundaries:
                    print("Found Boundary")
                    return

                elif matrix[new_player_position[0]][new_player_position[1] - 1] == self.Dump:
                    print("Found Dump")
                    matrix[new_player_position[0]][new_player_position[1] - 1] = self.Boundaries

                # For double obstacle
                elif matrix[new_player_position[0]][new_player_position[1] - 1] == self.Obstacle:
                    await message.channel.send("Double Collision")
                    return

                elif matrix[new_player_position[0]][new_player_position[1] - 1] == self.Inside_fill:
                    matrix[new_player_position[0]][new_player_position[1] - 1] = self.Obstacle

            matrix[player_position[0]][player_position[1]] = self.Inside_fill
            matrix[new_player_position[0]][new_player_position[1]] = self.Player_emoji
        #############################################################################################
        elif direction == "s":
            new_player_position = [player_position[0] + 1, player_position[1]]
            print(f"New Position: {new_player_position}")

            if matrix[new_player_position[0]][new_player_position[1]] == ":red_square:":
                print(matrix[new_player_position[0]][new_player_position[1]])
                print("Found Collision")
                await message.channel.send("Boundary")

                return

            if matrix[new_player_position[0]][new_player_position[1]] == ":cactus:":
                print(matrix[new_player_position[0]][new_player_position[1]])
                print("Found Collision")
                await message.channel.send("Cactus")

                return

            # Check for Collision
            if matrix[new_player_position[0]][new_player_position[1]] == self.Obstacle:
                print("Found Obstacle")
                if matrix[new_player_position[0] + 1][new_player_position[1]] == self.Boundaries:
                    print("Found Boundary")
                    return

                elif matrix[new_player_position[0] + 1][new_player_position[1]] == self.Dump:
                    print("Found Dump")
                    matrix[new_player_position[0] + 1][new_player_position[1]] = self.Boundaries

                # For double obstacle
                elif matrix[new_player_position[0] + 1][new_player_position[1]] == self.Obstacle:
                    await message.channel.send("Double Collision")
                    return

                elif matrix[new_player_position[0] + 1][new_player_position[1]] == self.Inside_fill:
                    print(matrix[new_player_position[0] + 1][new_player_position[1]])
                    matrix[new_player_position[0] + 1][new_player_position[1]] = self.Obstacle

            matrix[player_position[0]][player_position[1]] = self.Inside_fill
            matrix[new_player_position[0]][new_player_position[1]] = self.Player_emoji
        #############################################################################################
        elif direction == "d":

            new_player_position = [player_position[0], player_position[1] + 1]
            print(f"New Position: {new_player_position}")

            if matrix[new_player_position[0]][new_player_position[1]] == ":red_square:":
                print(matrix[new_player_position[0]][new_player_position[1]])
                print("Found Collision")
                await message.channel.send("Boundary")

                return

            if matrix[new_player_position[0]][new_player_position[1]] == ":cactus:":
                print(matrix[new_player_position[0]][new_player_position[1]])
                print("Found Collision")
                await message.channel.send("Cactus")

                return

            # Check for Collision
            if matrix[new_player_position[0]][new_player_position[1]] == self.Obstacle:
                print("Found Obstacle")
                if matrix[new_player_position[0]][new_player_position[1] + 1] == self.Boundaries:
                    print("Found Boundary")
                    return

                elif matrix[new_player_position[0]][new_player_position[1] + 1] == self.Dump:
                    print("Found Dump")
                    matrix[new_player_position[0]][new_player_position[1] + 1] = self.Boundaries

                # For double obstacle
                elif matrix[new_player_position[0]][new_player_position[1] + 1] == self.Obstacle:
                    await message.channel.send("Double Collision")
                    return

                elif matrix[new_player_position[0]][new_player_position[1] + 1] == self.Inside_fill:
                    print(matrix[new_player_position[0]][new_player_position[1] + 1])
                    matrix[new_player_position[0]][new_player_position[1] + 1] = self.Obstacle

            matrix[player_position[0]][player_position[1]] = self.Inside_fill
            matrix[new_player_position[0]][new_player_position[1]] = self.Player_emoji

        else:  # The direction is invalid(although it won't happen, but still in very rare circumstances)
            return

        matrix_string = f"{''.join(matrix[0])}\n" \
                        f"{''.join(matrix[1])}\n" \
                        f"{''.join(matrix[2])}\n" \
                        f"{''.join(matrix[3])}\n" \
                        f"{''.join(matrix[4])}\n" \
                        f"{''.join(matrix[5])}\n" \
                        f"{''.join(matrix[6])}\n" \
                        f"{''.join(matrix[7])}\n" \
                        f"{''.join(matrix[8])}\n"
        await self.bot.db.execute(
            f"UPDATE running_games SET player_position=$1 WHERE user_id=$2",
            new_player_position, user_id
        )

        # CHECK IF THE PLAYER HAS WON
        if self.Obstacle not in matrix_string:  # PLAYER HAS WON
            embed = discord.Embed(title="Game",
                                  description=f"Victory!"
                                              f" {matrix_string}"
                                              f"You have won the Game. React with 🆕 to start a New Game")
            await self.bot.db.execute(f"UPDATE running_games SET game_won=True WHERE user_id={user_id}")
            game_won = True
        else:
            embed = discord.Embed(title="Game", description=matrix_string)

        channel = await self.bot.fetch_channel(message.channel.id)
        messages = [message async for message in channel.history(oldest_first=True, limit=2)]
        original_msg = messages[0]
        if reaction is False:
            await channel.purge(limit=1)
        await original_msg.edit(embed=embed)
        old_row = player_position[0]
        print(f"old row :{old_row}")
        print(f"new row: {new_player_position[0]}")

        # Update the database
        # if old_row != new_player_position[0]:
        #     await self.bot.db.execute(
        #         f"UPDATE running_games SET matrix_row_{old_row} = $1, matrix_row_{new_player_position[0]} = $2 "
        #         f"WHERE "
        #         f"user_id={user_id};",
        #         matrix[old_row],
        #         matrix[new_player_position[0]])
        #
        # else:
        #     await self.bot.db.execute(f"UPDATE running_games SET "
        #                               f" matrix_row_{player_position[0]} = $1 "
        #                               f" matrix_row_{player_position[0] - 1} = $2 "
        #                               f" matrix_row_{player_position[0] + 1} = $3 "
        #                               f" WHERE user_id={user_id};",
        #                               matrix[player_position[0]],
        #                               matrix[player_position[0] - 1],
        #                               matrix[player_position[0] + 1])

        await self.bot.db.execute(
            f"UPDATE running_games SET "
            f"matrix_row_0 = $1, matrix_row_1 = $2, matrix_row_2 = $3, matrix_row_3 = $4, "
            f"matrix_row_4 = $5, matrix_row_5 = $6, matrix_row_6 = $7, matrix_row_7 = $8, "
            f"matrix_row_8 = $9, player_position = $10"
            f"WHERE user_id={user_id}",
            matrix[0], matrix[1], matrix[2], matrix[3], matrix[4], matrix[5], matrix[6], matrix[7], matrix[8],
            new_player_position
        )

        print("Movement Complete")

        if game_won:
            await self.end_game(user=user_id, channel=channel, won=True, delete_channel=False)
        return

    @commands.hybrid_command(name="play")
    @app_commands.guilds(TESTING_SERVER)
    async def game(self, ctx: commands.Context):
        check = await self.bot.db.fetchrow(
            f"SELECT user_id, channel_id FROM running_games WHERE user_id={ctx.author.id}")
        print(check)
        try:
            if len(check) != 0:
                running_channel = self.bot.get_channel(check["channel_id"])
                await ctx.send(f"You already have a running game in channel {running_channel.mention}")
                return
        except TypeError:
            pass

        channel = await ctx.guild.create_text_channel(name=f"game-by-{ctx.author}", overwrites={
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.author: discord.PermissionOverwrite(read_messages=True)})

        author = ctx.author
        self.id_ = channel.id

        try:
            await ctx.send(f"Continue in the channel {channel.mention}", ephemeral=True)
        except Exception as e:
            print(e)

        mat_width = 15
        mat_height = 9
        self.matrix: list = [[self.Inside_fill for _ in range(mat_width)] for _ in range(mat_height)]
        for i in range(mat_width):
            self.matrix[0][i] = self.Boundaries
            self.matrix[mat_height - 1][i] = self.Boundaries

        for n in range(mat_height):
            self.matrix[n][0] = self.Boundaries
            self.matrix[n][mat_width - 1] = self.Boundaries

        # OBSTACLES
        for f in range(random.randint(3, 7)):
            self.matrix[random.randint(2, mat_height - 3)][random.randint(2, mat_width - 3)] = self.Obstacle
            self.matrix[random.randint(1, mat_height - 2)][random.randint(1, mat_width - 2)] = self.Dump

        # PLAYER
        player_position = [random.randint(1, mat_height - 2), random.randint(1, mat_width - 2)]
        self.matrix[player_position[0]][player_position[1]] = self.Player_emoji

        # Initial Matrix to String
        self.matrix_string = f"{''.join(self.matrix[0])}\n" \
                             f"{''.join(self.matrix[1])}\n" \
                             f"{''.join(self.matrix[2])}\n" \
                             f"{''.join(self.matrix[3])}\n" \
                             f"{''.join(self.matrix[4])}\n" \
                             f"{''.join(self.matrix[5])}\n" \
                             f"{''.join(self.matrix[6])}\n" \
                             f"{''.join(self.matrix[7])}\n" \
                             f"{''.join(self.matrix[8])}\n"
        # Send to the channel
        Embed = discord.Embed(title="Game",
                              description=f"{self.matrix_string}Type`wasd`or use the reactions below to play",
                              colour=discord.Colour.teal())

        try:
            await channel.send(embed=Embed)
        except discord.Forbidden:
            await self.bot.db.close()
            quit()

        # Add reactions for reaction controls
        messages = [message async for message in channel.history(oldest_first=True, limit=2)]
        original_msg = messages[0]
        await original_msg.add_reaction("⬆️")
        await original_msg.add_reaction("⬅️")
        await original_msg.add_reaction("⬇️")
        await original_msg.add_reaction("➡️")
        await original_msg.add_reaction("❌")
        await original_msg.add_reaction("🆕")

        # Perform Database Operations
        x = await self.bot.db.fetch(f"SELECT 1 FROM game_info WHERE user_id = {author.id}")
        print(x)
        if len(x) == 0:
            games_started = 0
            await self.bot.db.execute(f"INSERT INTO game_info(user_id) VALUES({author.id});")
        else:
            games_started = await self.bot.db.fetch(f"SELECT games_started FROM game_info WHERE user_id={author.id};")
            games = re.split("=|>", str(games_started))
            games_started = games[1]

        print("Games started: " + games_started)

        await self.bot.db.execute(
            f"UPDATE game_info SET games_started={int(games_started) + 1} WHERE user_id={author.id}")

        await self.bot.db.execute(
            f"INSERT INTO running_games (user_id, channel_id, old_player_position,"
            f" matrix_row_0, matrix_row_1, matrix_row_2, matrix_row_3,"
            f" matrix_row_4, matrix_row_5, matrix_row_6,matrix_row_7, matrix_row_8,"
            f" player_position)"
            f" VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)",
            author.id, channel.id, player_position,
            self.matrix[0], self.matrix[1], self.matrix[2], self.matrix[3], self.matrix[4],
            self.matrix[5], self.matrix[6], self.matrix[7], self.matrix[8],
            player_position)

        print("here")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        channels = await self.bot.db.fetch(f"SELECT channel_id FROM running_games WHERE user_id={message.author.id};")
        if str(message.channel.id) in str(channels):
            if message.content.lower() == "stop" or "end" or "end game":
                await self.end_game(user=message.author.id, permanent=True, channel=message.channel, won=False,
                                    delete_channel=True)

            if message.content.lower() == "w" or "a" or "s" or "d":
                initial_matrix = await self.bot.db.fetchrow(
                    f"SELECT * FROM running_games WHERE user_id={message.author.id}")
                matrix = [initial_matrix["matrix_row_0"],
                          initial_matrix["matrix_row_1"],
                          initial_matrix["matrix_row_2"],
                          initial_matrix["matrix_row_3"],
                          initial_matrix["matrix_row_4"],
                          initial_matrix["matrix_row_5"],
                          initial_matrix["matrix_row_6"],
                          initial_matrix["matrix_row_7"],
                          initial_matrix["matrix_row_8"]]

                player_position: list = initial_matrix["player_position"]

                await self.move(direction=message.content.lower(),
                                message=message,
                                matrix=matrix,
                                player_position=player_position)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        if user == self.bot.user:
            return
        if reaction.emoji == str("⬆️") or str("⬅️") or str("➡️") or str("⬇️"):
            if reaction.emoji == str("❌"):
                await self.end_game(user=user.id, permanent=True, channel=reaction.message.channel, won=False,
                                    delete_channel=True)
                await reaction.remove(user)

            game_state = await self.bot.db.fetchrow(
                f"SELECT game_won FROM running_games WHERE user_id={user.id}")

            if game_state["game_won"]:
                await reaction.message.channel.send("You have already won the game.")
                return
            initial_matrix = await self.bot.db.fetchrow(
                f"SELECT * FROM running_games WHERE user_id={user.id}")
            matrix = [initial_matrix["matrix_row_0"],
                      initial_matrix["matrix_row_1"],
                      initial_matrix["matrix_row_2"],
                      initial_matrix["matrix_row_3"],
                      initial_matrix["matrix_row_4"],
                      initial_matrix["matrix_row_5"],
                      initial_matrix["matrix_row_6"],
                      initial_matrix["matrix_row_7"],
                      initial_matrix["matrix_row_8"]]

            player_position = initial_matrix["player_position"]

            print(f"Fed Player position {player_position}")
            await self.move(direction=self.reaction_to_text[str(reaction.emoji)], message=reaction.message,
                            matrix=matrix, player_position=player_position,
                            user_id=user.id, reaction=True)
            await reaction.remove(user=user)

        elif reaction.emoji == str("🆕"):
            await self.generate_new_matrix(user, reaction.message)
            await reaction.remove(user)

        elif reaction.emoji == str("❌"):
            await self.end_game(user=user.id, permanent=True, channel=reaction.message.channel, won=False,
                                delete_channel=True)
            await reaction.remove(user)


async def setup(bot):
    await bot.add_cog(Soko(bot))
