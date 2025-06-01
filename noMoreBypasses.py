# NoMoreBypasses - NWord detection
from package_util import *
from cog_core import *
from discord.ext import commands
import discord, re
import discord.app_commands


    
class NoMoreBypasses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.number = None
        self.extra = None

    @commands.Cog.listener()
    async def on_message(self, message):
        pattern = r"([nN]?[iI1]+[gG6]+[eE3aA@#]+[rR]+|[nN]+[iI1]+[gG6]+[aA4@]+)"
        matches = re.findall(pattern, message.content)
        matched_text = ''.join(matches)
        if len(matched_text) > 0:
            await message.delete()
            await message.channel.send(f"{message.author.mention} NWORD DETECTED! **ACTIVE MODERATORS, please check the message.**", delete_after=8)
            return

    
                


async def setup(bot):
    await bot.add_cog(NoMoreBypasses(bot))