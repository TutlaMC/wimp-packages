# Package for Guess the Number game
from package_util import *
from cog_core import *
from discord.ext import commands
import discord, random
import discord.app_commands


global number
number = random.randint(0, 100)

def get_points(user_id):
    if not exists_json_db("gtn"):
        create_json_db("gtn")
    return get_json_db("gtn").get(str(user_id), 0)

def change_points(user_id, points):
    if not exists_json_db("gtn"):
        create_json_db("gtn")
    data = get_json_db("gtn")
    data[str(user_id)] = points
    change_json_db("gtn", data)

def get_leaderboard():
    if not exists_json_db("gtn"):
        create_json_db("gtn")
    data = get_json_db("gtn")
    return sorted(data.items(), key=lambda x: x[1], reverse=True)

create_package_config("gtn", {"channel_id": None})


class HintView(discord.ui.View):
    def __init__(self, number):
        self.number = number
        super().__init__(timeout=None)

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_callback(self, ctx: discord.Interaction, button: discord.ui.Button):
        if get_points(ctx.user.id) < 10:
            await ctx.response.send_message("You do not have enough points to get a hint!",ephemeral=True)
            self.stop()
            return
        await ctx.response.send_message(f"You lost 10 points, hint: {self.number-random.randint(5,10)} - {self.number+random.randint(5,10)}",ephemeral=True)
        change_points(ctx.user.id, get_points(ctx.user.id) - 10)
        await ctx.followup.send(f"You have {get_points(ctx.user.id)} points",ephemeral=True)
        self.stop()
    
    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_callback(self, ctx: discord.Interaction, button: discord.ui.Button):
        await ctx.response.send_message("You did not want a hint",ephemeral=True)
        self.stop()

class ChangePointsModal(discord.ui.Modal):
    def __init__(self, user_id, points,add=True):
        self.user_id = user_id
        self.points = points
        super().__init__(title="Change Points", timeout=None)
        self.add_item(discord.ui.TextInput(label="Points", style=discord.TextStyle.short, placeholder="10"))
    
    async def on_submit(self, interaction: discord.Interaction):
        if self.children[0].value.isdigit():
            points = int(self.children[0].value)
            if self.add:
                change_points(self.user_id, self.points + points)
                await interaction.response.send_message(f"Added {points} points to {self.user_id}")
            else:
                change_points(self.user_id, self.points - points)
                await interaction.response.send_message(f"Removed {points} points from {self.user_id}")
        else:
            await interaction.response.send_message("Invalid points",ephemeral=True)
    
    

class ChangePointsView(discord.ui.View):
    def __init__(self, user_id, points):
        self.user_id = user_id
        self.points = points
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Add", style=discord.ButtonStyle.green)
    async def add_callback(self, ctx: discord.Interaction, button: discord.ui.Button):
        if ctx.user.id in get_config()["owners"]:
            change_points(self.user_id, self.points + 10)
            await ctx.response.send_message(f"Added 10 points to {self.user_id}")
        else:
            await ctx.response.send_message("You are not the owner of the bot")
    
    @discord.ui.button(label="Remove", style=discord.ButtonStyle.red)
    async def remove_callback(self, ctx: discord.Interaction, button: discord.ui.Button):
        if ctx.user.id in get_config()["owners"]:
            await ctx.response.send_message(f"Removed 10 points from {self.user_id}",view=ChangePointsModal(self.user_id, self.points,add=False),ephemeral=True)
        else:
            await ctx.response.send_message("You are not the owner of the bot")
    
class GTN(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.number = None
        self.extra = None


    group = app_commands.Group(name="gtn", description="Guess the Number")
    @group.command(name="reload", description="Reload the GTN config")
    @owner_only()
    async def reload_gtn_config(self, ctx: discord.Interaction):
        if ctx.user.id in get_config()["owners"]:
            create_package_config("gtn", {"channel_id": None})
            await ctx.response.send_message("GTN config reloaded")
        else:
            await ctx.response.send_message("You are not the owner of the bot")


    @group.command(name="start", description="Start the GTN game")
    async def start_callback(self, ctx: discord.Interaction,range_start:int=0,range_end:int=100):
        if range_start > range_end:
            await ctx.response.send_message("Range start cannot be greater than range end!",ephemeral=True)
            return
        if range_start < 0 or range_end < 0:
            await ctx.response.send_message("Range start and end cannot be negative!",ephemeral=True)
            return
        if range_end - range_start < 100:
            await ctx.response.send_message("Range start and end cannot be less than 100!",ephemeral=True)
            return
        if range_end - range_start != 100:
            self.extra = ((range_end-range_start)-(range_end-range_start))/10
        else:
            self.extra = 0
        if ctx.channel.id != get_package_config("gtn")["channel_id"]:
            await ctx.response.send_message(f"This command can only be used in <#{get_package_config('gtn')['channel_id']}>! GTN May not have been setup on this server!")
            return
        if self.number == None:
            await ctx.response.send_message("Starting Guess the Number!")
            self.number = random.randint(0, 100) 
            await ctx.followup.send(f"Guess the number between {range_start} and {range_end}")
        else:
            await ctx.response.send_message("Guess the number is already running!")

    @group.command(name="hint", description="Get a hint for the GTN game")
    async def hint_callback(self, ctx: discord.Interaction):
        if self.number == None:
            await ctx.response.send_message("Guess the number is not running!")
            return
        
        await ctx.response.send_message(f"Are you sure you want a hint? It will cost you 10 points",view=HintView(self.number),ephemeral=True)

    @group.command(name="points", description="View your points")
    async def points_callback(self, ctx: discord.Interaction, user: discord.Member=None):
        if user == None:
            await ctx.response.send_message(f"You have {get_points(ctx.user.id)} points",ephemeral=True)
        else:
            await ctx.response.send_message(f"{user.mention} has {get_points(user.id)} points",view=ChangePointsView(user.id, get_points(user.id)),ephemeral=True)

    @group.command(name="stop", description="Stop the GTN game")
    async def stop_callback(self, ctx: discord.Interaction):
        if ctx.channel.permissions_for(ctx.user).moderate_members:
            self.reset_game()
            await ctx.response.send_message("Guess the number has been stopped")
        else:
            await ctx.response.send_message("You do not have permission to stop the game!")

    @group.command(name="leaderboard", description="View the GTN leaderboard")
    async def leaderboard_callback(self, ctx: discord.Interaction):
        leaderboard = get_leaderboard()
        embed = discord.Embed(title="Guess the Number Leaderboard", description="Top 10 players")
        for i in range(10):
            if i < len(leaderboard):
                embed.add_field(name=f"{i+1}. {leaderboard[i][1]} Points", value=f"<@{leaderboard[i][0]}>", inline=False)
        await ctx.response.send_message(embed=embed,ephemeral=True)

    @group.command(name="set_channel", description="Set the channel for the GTN game")
    async def set_channel_callback(self, ctx: discord.Interaction, channel: discord.TextChannel):
        if ctx.user.id in get_config()["owners"]:
            change_settings("gtn", {"channel_id": channel.id})
            await ctx.response.send_message(f"GTN channel set to {channel.mention}")
        else:
            await ctx.response.send_message("You are not the owner of the bot")

    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == get_package_config("gtn")["channel_id"]:

            if message.content.isdigit():
                if int(message.content) == self.number:
                    points = 2+self.extra
                    if self.number == 69:
                        points = 10
                    await message.reply(f"You guessed the number! You got {points} points")
                    
                    change_points(message.author.id, get_points(message.author.id) + points)
                    self.reset_game()

    def reset_game(self):
        self.number = None
        self.extra = None
    
                


async def setup(bot):
    await bot.add_cog(GTN(bot))