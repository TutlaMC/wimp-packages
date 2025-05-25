# NoMoreBypasses - No more fonts and NWord detection
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
        pattern = r"[a-zA-Z0-9!@#$‘%’”…“’^&*()-=}{\]\[\\|;:'\",_‘.<>/?`~\s]|[\U0001F300-\U0001F9FF\U00002600-\U000026FF\U00002700-\U000027BF\U0001F000-\U0001F02F\U0001F0A0-\U0001F0FF\U0001F100-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF\U00002700-\U000027BF\U000024C2-\U0001F251\U0001F004\U0001F0CF\U0001F170-\U0001F171\U0001F17E-\U0001F17F\U0001F18E\U0001F191-\U0001F19A\U0001F1E6-\U0001F1FF\U0001F201-\U0001F202\U0001F21A\U0001F22F\U0001F232-\U0001F23A\U0001F250-\U0001F251\U0001F300-\U0001F321\U0001F324-\U0001F393\U0001F396-\U0001F397\U0001F399-\U0001F39B\U0001F39E-\U0001F3F0\U0001F3F3-\U0001F3F5\U0001F3F7-\U0001F3FA\U0001F400-\U0001F4FD\U0001F4FF-\U0001F53D\U0001F549-\U0001F54E\U0001F550-\U0001F567\U0001F56F-\U0001F570\U0001F573-\U0001F57A\U0001F57A-\U0001F5A4\U0001F5A5-\U0001F5FA\U0001F5FB-\U0001F64F\U0001F680-\U0001F6C5\U0001F6CB-\U0001F6D2\U0001F6D5\U0001F6E0-\U0001F6E5\U0001F6E9\U0001F6EB-\U0001F6EC\U0001F6F0\U0001F6F3-\U0001F6FA\U0001F7E0-\U0001F7EB\U0001F90D-\U0001F93A\U0001F93C-\U0001F945\U0001F947-\U0001F971\U0001F973-\U0001F976\U0001F97A-\U0001F9A2\U0001F9A5-\U0001F9AA\U0001F9AE-\U0001F9CA\U0001F9CD-\U0001F9FF\U0001FA70-\U0001FA73\U0001FA78-\U0001FA7A\U0001FA80-\U0001FA82\U0001FA90-\U0001FA95]"
        matches = re.findall(pattern, message.content)
        
        matched_text = ''.join(matches)
        if len(matched_text) != len(message.content):
            unmatched = []
            for i, char in enumerate(message.content):
                if i >= len(matched_text) or char != matched_text[i]:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Please do not use fonts, fonts aren't allowed.", delete_after=3)
                    return
                
        pattern = r"([nN]?[iI1]+[gG6]+[eE3aA@#]+[rR]+|[nN]+[iI1]+[gG6]+[aA4@]+)"
        matches = re.findall(pattern, message.content)
        matched_text = ''.join(matches)
        if len(matched_text) > 0:
            await message.delete()
            await message.channel.send(f"{message.author.mention} NWORD DETECTED! **ACTIVE MODERATORS, please check the message.**", delete_after=8)
            return

    
                


async def setup(bot):
    await bot.add_cog(NoMoreBypasses(bot))