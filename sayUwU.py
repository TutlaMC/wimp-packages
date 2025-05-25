# ~UwU~ Fun & Troll commands, some from Tutla Assistance

from discord import app_commands
from discord.ext import commands
import discord
from package_util import *
from cog_core import *
import requests
from io import BytesIO

create_package_config("sayUwU",{"fake_admin_role":None,"action_role":None})
class SayUwUCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="uwu_setup",description="Setup the uwu package")
    @owner_only()
    async def uwu_setup_callback(self,ctx:discord.Interaction,fake_admin_role:discord.Role=None,action_role:discord.Role=None):
        if fake_admin_role != None:
            data = get_package_config("sayUwU")
            data["fake_admin_role"] = fake_admin_role.id
            change_settings("sayUwU",data)
        if action_role != None:
            data = get_package_config("sayUwU")
            data["action_role"] = action_role.id
            change_settings("sayUwU",data)
        await ctx.response.send_message(f"UwU package setup complete!")

    @app_commands.command(name="beatup",description="Beat up a user")
    async def beatup_callback(self,ctx:discord.Interaction,user:discord.Member):
        role = await ctx.guild.fetch_role(get_package_config("sayUwU")["action_role"])
        if role not in ctx.user.roles:
            await ctx.response.send_message(f"You need the {role.mention} role to use this command!",ephemeral=True)
            return
        await ctx.response.send_message(f"**{ctx.user.mention}** beats up **{user.mention}**!\nhttps://tenor.com/view/foghorn-leghorn-spank-beat-beating-gif-12866723695374477811",silent=True)

    @app_commands.command(name="slap",description="Slap a user")
    async def slap_callback(self,ctx:discord.Interaction,user:discord.Member):
        role = await ctx.guild.fetch_role(get_package_config("sayUwU")["action_role"])
        if role not in ctx.user.roles:
            await ctx.response.send_message(f"You need the {role.mention} role to use this command!",ephemeral=True)
            return
        await ctx.response.send_message(f"**{ctx.user.mention}** slaps **{user.mention}**!\nhttps://tenor.com/view/shut-up-stfu-shut-your-mouth-slap-slapping-gif-8050553153066707611",silent=True)

    @app_commands.command(name="bon",description="Fake ban")
    async def bon_callback(self,ctx:discord.Interaction,user:discord.Member):
        if get_package_config("sayUwU")["fake_admin_role"] == None:
            await ctx.response.send_message(f"Fake Admin Role is not set! Please use `/uwu_setup` to setup the package!",silent=True)
            return
        role = await ctx.guild.fetch_role(get_package_config("sayUwU")["fake_admin_role"])
        if role in ctx.user.roles:
            e = await ctx.response.send_message(f"Banning **{user.mention}**!\nhttps://tenor.com/view/banned-one-wrong-move-ban-server-aint-no-playground-gif-11464951596714631122",silent=True)
        else:
            await ctx.response.send_message(f"You need the {role.mention} role to use this command!",ephemeral=True)

    @app_commands.command(name="kiiick",description="Fake kick")
    async def kiiick_callback(self,ctx:discord.Interaction,user:discord.Member):
        if get_package_config("sayUwU")["fake_admin_role"] == None:
            await ctx.response.send_message(f"Fake Admin Role is not set! Please use `/uwu_setup` to setup the package!",silent=True)
            return
        role = await ctx.guild.fetch_role(get_package_config("sayUwU")["fake_admin_role"])
        if role in ctx.user.roles:
            e = await ctx.response.send_message(f"Kicking **{user.mention}**!\nhttps://tenor.com/view/asdf-movie-punt-kick-donewiththis-gif-26537188",silent=True)
        else:
            await ctx.response.send_message(f"You need the {role.mention} role to use this command!",ephemeral=True)

    @app_commands.command(name="kat",description="Random cat image")
    async def kat_callback(self,ctx:discord.Interaction):
        if get_package_config("sayUwU")["action_role"] == None:
            await ctx.response.send_message(f"Action Role is not set! Please use `/uwu_setup` to setup the package!",silent=True)
            return
        role = await ctx.guild.fetch_role(get_package_config("sayUwU")["action_role"])
        if role not in ctx.user.roles:
            await ctx.response.send_message(f"You need the {role.mention} role to use this command!",ephemeral=True)
            return
        res = requests.get("https://api.thecatapi.com/v1/images/search")
        res = requests.get(res.json()[0]["url"])
        await ctx.response.send_message("Kitty ❣️",file=discord.File(fp=BytesIO(res.content),filename="kat.jpg"))

    @app_commands.command(name="xxod", description="Prank a user with fun facts about them")
    async def doxx(self, ctx: discord.Interaction, user: discord.User):
        if get_package_config("sayUwU")["fake_admin_role"] == None:
            await ctx.response.send_message(f"Fake Admin Role is not set! Please use `/uwu_setup` to setup the package!",silent=True)
            return
        role = await ctx.guild.fetch_role(get_package_config("sayUwU")["fake_admin_role"])
        if role not in ctx.user.roles:
            await ctx.response.send_message(f"You need the {role.mention} role to use this command!",ephemeral=True)
            return
        await ctx.response.send_message("Finding more about user 🔍...", ephemeral=True)
        gender = requests.get(f'https://api.genderize.io?name={user.display_name}').json()['gender']
        await ctx.followup.send(f"More about {user.mention}:\n- Age: ||Above 0||\n- Location: ||Milkyway Galaxy, Earth||\n- Gender: ||{gender}||\n- email: ||hosted by sum email service like gmail or sum||\n- Skin Color: ||black, yellow, white, or brown||")
    

async def setup(bot:commands.Bot):
    await bot.add_cog(SayUwUCog(bot))
    await bot.tree.sync()