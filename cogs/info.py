import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_commands import create_option


howToPlay = """
This game requires 3 or more players to start
Each player is dealt 3 chips (<:chip:868688636772777996>)
The first player rolls 3 dice (or the same number of <:chip:868688636772777996>s if they have less <:chip:868688636772777996>s than 3) which each (die) has one :regional_indicator_l: (left) face, :star: (center) face, :regional_indicator_r: (right) face, and three :diamond_shape_with_a_dot_inside: (dot) faces

If one of the dice lands on :regional_indicator_l:, the player passes one <:chip:868688636772777996> to the player left of them.
If one of the dice lands on :star:, the player passes one <:chip:868688636772777996> to the center.
If one of the dice lands on :regional_indicator_r:, the player passes one <:chip:868688636772777996> to the player right of them.
If one of the dice lands on :diamond_shape_with_a_dot_inside:, the player keeps one <:chip:868688636772777996>.
The next player clockwise :arrows_clockwise: gets their turn
If you have no <:chip:868688636772777996>s left, you are still in the game, but skip your turn till you get a <:chip:868688636772777996> since it is possible for a player to pass a <:chip:868688636772777996> to you.
If you get something like three :regional_indicator_l:s, you must pass all 3 of your <:chip:868688636772777996>s to the player left of you.

The winner of the game is the person with the last <:chip:868688636772777996>(s) left!
"""


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guild_ids = [868567807133106206]

    @cog_ext.cog_subcommand(base="how", subcommand_group="to", name="play", description="How to play!", guild_ids=guild_ids)
    async def how_to_play(self, ctx):
        await ctx.defer(hidden=True)
        await ctx.send(howToPlay, hidden=True)
    

    @cog_ext.cog_slash(name="help", description="Get help about the bot!", guild_ids=guild_ids, options=[
        create_option(name="command",
                      description="Get help about a specific command!",
                      option_type=3,
                      required=False)
    ])
    async def _help(self, ctx, command=None):
        if command == None:
            pass
        elif command == "how_to_play":
            await ctx.defer(hidden=True)
            await ctx.send(howToPlay, hidden=True)
        else:
            pass



def setup(bot):
    bot.add_cog(Game(bot))
