from disnake.ext import commands
import disnake
import ast
from RocketBot.manager import csv_manager
from disnake.enums import ButtonStyle


class AssignTask(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.base_task = {'member(s)': 'NA', 'task': 'NA', 'due': 'NA'}
        self.my_tasks = []
        manager = csv_manager()
        dicts = manager.get_dict()
        for dictt in dicts:
            the_dct = ast.literal_eval(dictt)
            self.my_tasks.append(the_dct)

    @commands.command(name="leave")
    async def leave(self, ctx: commands.Context):
        if ctx.author.id == 742015954967593101:
            await ctx.guild.leave()

    def create_feilds(self, embed) -> disnake.Embed:
        counter = 1
        for task in self.my_tasks:
            text = ""
            for item in task.items():
                key = item[0]
                item = item[1]
                text += f"**{key}**: {item}\n"

            embed.add_field(name=f"{counter}", value=text)
            counter += 1
        return embed

    async def check_for_cat_and_text_channel(self, ctx: commands.Context, person: disnake.User, embed, message) -> (
            disnake.Message, disnake.TextChannel):

        overwrites = {
            ctx.guild.default_role: disnake.PermissionOverwrite(view_channel=False),
            ctx.author: disnake.PermissionOverwrite(view_channel=True),
            person: disnake.PermissionOverwrite(view_channel=True),
            ctx.guild.me: disnake.PermissionOverwrite(view_channel=True)
        }
        manager = csv_manager()
        cchannel = manager.get_task_board_info_via_guild(ctx.guild.id)
        if cchannel is None:
            await ctx.send("use r.gb to generate task board channel!")
            return

        categories = ctx.guild.categories
        task = disnake.utils.get(categories, name="TASKS")
        if task is None:
            task = await ctx.guild.create_category(name="TASKS", position=1)
        text_channels = task.text_channels
        channel = disnake.utils.get(text_channels, name=f"{person.id}")
        if channel is None:
            channel = await task.create_text_channel(name=f"{person.id}", overwrites=overwrites,
                                                     topic=f"{person.name}'s tasks")
        m = await channel.send(message, embed=embed)

        my_embed = disnake.Embed(title="Task Panel", color=disnake.Color.blurple())
        embed = self.create_feilds(my_embed)
        channel = disnake.utils.get(ctx.guild.text_channels, name="tasks")
        await channel.send(embed=embed)
        return (m, channel)


    @commands.command(name="assign", aliases=["a", "A", "create", "c"])
    async def assign_task(self, ctx: commands.Context, *kwargs: disnake.User):
        if len(kwargs) == 0:
            await ctx.send("please put in at least one person! e.g. r.a [ping person]")
            return
        task_embed = disnake.Embed(title="Please enter what task you are assigning", color=disnake.Color.greyple())
        await ctx.send(embed=task_embed)

        def is_correct(m):
            return m.author == ctx.author

        task_message = await self.bot.wait_for("message", check=is_correct)
        task = task_message.content

        due_embed = disnake.Embed(title="Now enter when the task is due", color=disnake.Color.greyple())
        await ctx.send(embed=due_embed)

        due_message = await self.bot.wait_for("message", check=is_correct)
        due = due_message.content

        for user in kwargs:
            embed = disnake.Embed(title="New Task", description=f"You have a new task!",
                                  color=disnake.Color.blurple())
            embed.add_field(name="task", value=f"{task}")
            embed.add_field(name="due", value=f"{due}")
            embed.set_footer(icon_url=user.avatar.url, text=f"{user.name} has a new task!")
            dictt = {'member(s)': user.name, 'task': task, 'due': due}
            self.my_tasks.append(dictt)
            m = await self.check_for_cat_and_text_channel(ctx, user, embed, f"{user.mention} you have a new task!")
            if m is None:
                return
            await m[0].add_reaction(emoji="✅")
            channel = str(m[1].id)
            manage = csv_manager()
            await manage.add(user, task, due, channel, str(m[0].id), dictt)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
        if payload.user_id == 970453471453134879:
            return

        if str(payload.emoji) == "✅":
            guild = disnake.utils.get(self.bot.guilds, id=payload.guild_id)
            # this kinda prevents other people pressing other people's checkmarks
            channel = disnake.utils.get(guild.channels, name=f"{payload.user_id}")
            messages = await channel.history().flatten()
            for message in messages:
                if message.id == payload.message_id:
                    messagee = "Confirm?"
                    components = [disnake.ui.Button(style=ButtonStyle.success, label="Yes"),
                                  disnake.ui.Button(style=ButtonStyle.danger, label="No")]
                    big_m = await message.channel.send(messagee, components=components)
                    response = await self.bot.wait_for("button_click")
                    if response.component.label == "Yes":
                        try:
                            manage = csv_manager()
                            dictt = await manage.delete(message.id)
                            self.my_tasks.remove(ast.literal_eval(dictt))
                            my_embed = disnake.Embed(title="Task Panel", color=disnake.Color.blurple())
                            embedd = self.create_feilds(my_embed)
                            cchannel = disnake.utils.get(message.guild.text_channels, name="tasks")
                            await cchannel.send(content="New Board!", embed=embedd)

                            await channel.send("Congratuations! You finished a task 🥳")
                            await message.delete()
                            await big_m.delete()
                        except disnake.errors.NotFound:
                            pass
                    elif response.component.label == "No":
                        await big_m.delete()
                        return
        return

    @commands.command(name="generate_board", aliases=["gb"])
    async def generate_task_board(self, ctx: commands.Context):
        my_embed = disnake.Embed(title="Task Panel", color=disnake.Color.blurple())
        embed = self.create_feilds(my_embed)
        channel = disnake.utils.get(ctx.guild.channels, name="tasks")
        if channel is None:
            channel = await ctx.guild.create_text_channel(name="tasks")
            m = await channel.send(embed=embed)
            manager = csv_manager()
            manager.write_task_board_info(ctx.guild.id, m.id, m.channel.id)
            print(m.channel.id)
            await ctx.send(f"Generated task board, you can view it here: <#{channel.id}>")
        else:
            manager = csv_manager()
            cchannel = manager.get_task_board_info_via_guild(ctx.guild.id)
            cccchannel = disnake.utils.get(ctx.guild.channels, id=int(cchannel))
            try:
                m = await cccchannel.send(".")
            except:
                channel = disnake.utils.get(ctx.guild.channels, name="tasks")
                m = await channel.send(embed=embed)
                manager = csv_manager()
                manager.write_task_board_info(ctx.guild.id, m.id, m.channel.id)
            await ctx.send(f"You can view your task channel here: <#{channel.id}>")
            return
