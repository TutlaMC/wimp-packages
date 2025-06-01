# Wimp package based on Tutla Assistance's help command

from discord import app_commands
from discord.ext import commands
import discord, datetime

afks = {}
def is_safe(message):
    if len(message) > 80:
        return False
    if "http" in message:
        return False
    if "<@" in message:
        return False
    return True

class AFKCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="afk",description="Set your AFK status")
    async def afk_callback(self,ctx: discord.Interaction, message: str = ""):
        if not is_safe(message):
            await ctx.response.send_message("Message is too long or contains links!",ephemeral=True)
            return
        if message == "":
            await ctx.response.send_message(f"You are now AFK!",delete_after=4)
        else:
            await ctx.response.send_message(f"You are now AFK: {message}",delete_after=4)
            afks[ctx.user.id] = f"{message} - <t:{datetime.datetime.now().timestamp()}>"
        if ctx.user.id in afks:
            afks.pop(ctx.user.id)
            await ctx.response.send_message("You are no longer AFK",delete_after=4)
    
    @app_commands.command(name="removeafk",description="Admin command to remove restricted AFK statuses")
    async def removeafk_callback(self,ctx: discord.Interaction, user: discord.Member):
        if ctx.channel.permissions_for(ctx.user).manage_messages:
            if user.id in afks:
                afks[user.id] = ""
                await ctx.response.send_message(f"AFK status removed for {user.mention}!")
            else:
                await ctx.response.send_message("User is not AFK!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id in afks:
            afks.pop(message.author.id)
            await message.channel.send(f"{message.author.mention} is no longer AFK!",delete_after=4)
        for i in message.mentions:
            if i.id in afks:
                await message.channel.send(f"{i.mention} is AFK: {afks[i.id]}",delete_after=4,silent=True)

        if message.content.startswith("!afk"):
            if not is_safe(message.content[4:]):
                await message.channel.send("Message is too long or contains links!",ephemeral=True)
                return
            if message.content[4:] == "":
                await message.channel.send(f"You are now AFK!")
            else:
                await message.channel.send(f"You are now AFK: {message.content[4:]}")
                afks[message.author.id] = message.content[4:]

        
        

async def setup(bot: commands.Bot):
    await bot.add_cog(AFKCog(bot))