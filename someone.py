# Wimp package for fake messages, \w rate limits!

from discord import app_commands
from discord.ext import commands
import discord, datetime, random
from package_util import *
from cog_core import *

rate_limits = {

}

create_package_config("someone",{"allowed_role":None})
class SomeoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="someone_setup",description="Setup the someone package")
    @owner_only()
    async def someone_setup_callback(self,ctx:discord.Interaction,role:discord.Role):
        change_settings("someone",{"allowed_role":role.id})
        await ctx.response.send_message(f"Someone package setup complete!")

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if "@someone" in message.content.lower():
            if get_package_config("someone")["allowed_role"] == None:
                await message.channel.send(f"Someone package is not setup! Please use `/someone_setup` to setup the package!",silent=True)
                return
            role = get_package_config("someone")["allowed_role"]
            role = await message.guild.fetch_role(role)
            if role not in message.author.roles:
                await message.channel.send(f"You are not allowed to use someone! You need the {role.mention} role to use someone!",silent=True,ephemeral=True)
                return
            if message.author.id not in rate_limits or rate_limits.get(message.author.id,datetime.datetime.now()) < datetime.datetime.now() - datetime.timedelta(seconds=60):
                embed = discord.Embed(title="This is a fake message",description=f"Sent by {message.author.mention}. This message was sent using @someone and didn't come from any server staffs and is mostly used to troll, please be cautious.")
                await message.channel.send(message.content.replace('@','').replace("@someone",random.choice(message.guild.members).mention),embed=embed)
                rate_limits[message.author.id] = datetime.datetime.now()
            else:
                await message.channel.send(f"You can only use someone every 60 seconds!",silent=True,ephemeral=True)

        
        

async def setup(bot: commands.Bot):
    await bot.add_cog(SomeoneCog(bot))