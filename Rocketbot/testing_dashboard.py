from disnake.ext import commands
import disnake
import os
import requests

os.environ['NO_PROXY'] = '127.0.0.1'

class testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="get_task")
    async def got_tasks_questinooo_mark(self, ctx):
        response = requests.get(f"http://127.0.0.1:5000/api/v1/gettasks?&guild_id={936775141315199007}&user_id={742015954967593101}").json()
        await ctx.send(response)
