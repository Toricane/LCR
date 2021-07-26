import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xf04b14

    guild_ids = [868567807133106206]

    @cog_ext.cog_slash(name="queue",
                       description="Queue a game!",
                       guild_ids=guild_ids)
    async def queue(self, ctx: SlashContext):
        await ctx.defer()
        embed = discord.Embed(
            title="Click the button to join the queue!",
            description=f"Users in the queue:\n{ctx.author.mention}",
            color=self.color)
        buttons = [
            create_button(style=ButtonStyle.green,
                          label="Join",
                          custom_id="join"),
            create_button(style=ButtonStyle.red,
                          label="Leave",
                          custom_id="leave")
        ]
        buttons2 = [
            create_button(style=ButtonStyle.green,
                          label="Start",
                          custom_id="start"),
            create_button(style=ButtonStyle.red,
                          label="Cancel",
                          custom_id="cancel")
        ]
        action_row = create_actionrow(*buttons)
        action_row2 = create_actionrow(*buttons2)
        embed.set_footer(
            text=f"This game's host is {ctx.author}: {ctx.author.id}")
        await ctx.send(embed=embed, components=[action_row, action_row2])

    @cog_ext.cog_component()
    async def join(self, ctx: ComponentContext):
        await ctx.defer(edit_origin=True)
        embed = ctx.origin_message.embeds[0]
        if f"{ctx.author.mention}" not in embed.description:
            embed.description += f"\n{ctx.author.mention}"
            await ctx.edit_origin(embed=ctx.origin_message.embeds[0])
        else:
            await ctx.edit_origin(
                content=f"{ctx.author.mention}, you are already in the queue!")

    @cog_ext.cog_component()
    async def leave(self, ctx: ComponentContext):
        await ctx.defer(edit_origin=True)
        embed = ctx.origin_message.embeds[0]
        if f"{ctx.author.mention}" in embed.description:
            embed.description = embed.description.replace(
                f"\n{ctx.author.mention}", "")
            await ctx.edit_origin(embed=embed)
        else:
            await ctx.edit_origin(
                content=f"{ctx.author.mention}, you are not in the queue!")

    @cog_ext.cog_component()
    async def start(self, ctx: ComponentContext):
        await ctx.defer(edit_origin=True)
        embed = ctx.origin_message.embeds[0]
        _, host = embed.footer.text.split(": ")
        host = int(host)
        if ctx.author.id == host:
            players = embed.description.replace("Users in the queue:\n",
                                                "").split("\n")
            buttons = [
                create_button(style=ButtonStyle.blue,
                              label="Roll",
                              custom_id="roll"),
                create_button(style=ButtonStyle.red,
                              label="End",
                              custom_id="end")
            ]
            action_row = create_actionrow(*buttons)
            new_embed = discord.Embed(
                title="Welcome to the game of Left Center Right!",
                description=f"Players:\n",
                color=self.color)
            for player in players:
                new_embed.description += f"{player}, "
            new_embed.description += "\n\nLook below for the game!\nIf you don't know how to play, try `/how to play`"
            new_embed.set_footer(
                text=f"This game's host is {ctx.author}: {ctx.author.mention}")
            await ctx.edit_origin(content="", embed=new_embed, components=[])
            game_embed = discord.Embed(title="Token distribution:",
                                       color=self.color)
            game_embed.add_field(name="Center", value="None", inline=False)
            for player in players:
                guy = await self.bot.fetch_user(
                    int(
                        player.replace("<@", "").replace("!",
                                                         "").replace(">", "")))
                game_embed.add_field(
                    name=f"{guy.name}#{guy.discriminator}",
                    value=
                    "<:chip:868688636772777996> <:chip:868688636772777996> <:chip:868688636772777996>"
                )
            game_embed.set_footer(text=f"This game's host is {ctx.author}: {ctx.author.mention}")
            guy = await self.bot.fetch_user(
                    int(
                        players[0].replace("<@", "").replace("!",
                                                         "").replace(">", "")))
            roll_embed = discord.Embed(title=f"{guy.name}#{guy.discriminator}'s turn:",
                                       description=":blue_square: :blue_square: :blue_square:",
                                       color=self.color)
            roll_embed.set_footer(text=f"This game's host is {ctx.author}: {ctx.author.mention}")
            await ctx.send(embeds=[game_embed, roll_embed], components=[action_row])
        else:
            await ctx.edit_origin(
                content=f"{ctx.author.mention}, you are not the host!")

    @cog_ext.cog_component()
    async def cancel(self, ctx: ComponentContext):
        embed = ctx.origin_message.embeds[0]
        _, host = embed.footer.text.split(": ")
        host = int(host)
        if ctx.author.id == host:
            await ctx.defer(edit_origin=True)
            await ctx.edit_origin(content="The queue was cancelled.",
                                  embed=None,
                                  components=[])
        else:
            await ctx.edit_origin(
                content=f"{ctx.author.mention}, you are not the host!")

    @cog_ext.cog_component()
    async def end(self, ctx: ComponentContext):
        await ctx.defer(edit_origin=True)
        await ctx.edit_origin(content="The host ended the game.",
                              embed=None,
                              components=[])


def setup(bot):
    bot.add_cog(Game(bot))
