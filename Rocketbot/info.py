import textwrap

from disnake.ext import commands, tasks
import disnake

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.description = textwrap.dedent((f"""
        **General**
        `{self.bot.prefix[0]}help` - help command
        **Tasks**
        `{self.bot.prefix[0]}assign [pings]` [a, c, create, A] - creates/assgins a task to multiple people
        `{self.bot.prefix[0]}generate_board` [gb] - creates the task board in the `tasks` channel 
        -----If you don't have a `task` channel, it will auto-create one
        """))


    @commands.command()
    async def help(self, ctx):
        embed = disnake.Embed(title="Help Panel", description=self.description, color=disnake.Color.blurple())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)



