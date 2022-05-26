import disnake
from disnake.ext import commands, tasks
import itertools
import aiohttp
from.info import Info
from .assign_task import AssignTask
from .manager import csv_manager
from .testing_dashboard import testing

class RocketBot(commands.Bot):
    intents = disnake.Intents.all()
    def __init__(self):
        self.prefix = ["r.", "r ", "R.", "R "]

        self.my_guilds = [958488149724635146]

        super().__init__(command_prefix=self.prefix, intents=RocketBot.intents)
        self.statuss = itertools.cycle(
            [disnake.Game('Open Rocket Simulator'), disnake.Activity(type=disnake.ActivityType.watching, name="Past MDRA Launch Videos"), disnake.Game(f'{self.prefix[0]}help'), disnake.Game("Rockets.io")])
        self.remove_command('help')

    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.change_presence(activity=next(self.statuss))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        self.remind.start()
        print(f"{self.user.name} is ready")

    async def get_random_quote(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://quote-garden.herokuapp.com/api/v3/quotes/random") as response:
                json_data = await response.json()
                data = json_data['data']
                return(data[0]['quoteText'])

    @tasks.loop(hours=6)
    async def remind(self):
        manager = csv_manager()
        tasks = await manager.organize()
        for task in tasks:
            guild = disnake.utils.get(self.guilds, id=848238227583926272)
            user = disnake.utils.get(guild.members, id=int(task[0]))
            quote = await self.get_random_quote()
            await user.send(f"You have a task: **{task[1]}** that is due: **{task[2]}**\n\n Random Quote to motivate you: `{quote}`")

