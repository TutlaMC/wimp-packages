# Wimp package based on Tutla Assistance's help command

from discord import app_commands
from discord.ext import commands
import discord


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="help",description="List commands or get info about a command")
    async def help_callback(self,ctx: discord.Interaction, page: int = 1, command: str = None):
        pages = []

        def append_page(content, new_line=False):
            if new_line:
                content += '\n'
            if pages:
                if len(pages[-1].description) <= 200:
                    pages[-1].description += content
                else:
                    new_embed = discord.Embed(description=content,color=discord.Color.blue())
                    pages.append(new_embed)
            else:
                new_embed = discord.Embed(description=content)
                pages.append(new_embed)

        def commandify(cmd, sub=False):
            if isinstance(cmd, discord.app_commands.Group): 
                return f'### {cmd.name.upper()}'

            final = f"**/{cmd.name}"
            if hasattr(cmd, "parent") and cmd.parent is not None:
                final = f"/{cmd.parent.name} {cmd.name}"

            for i in cmd.parameters:
                final += f" `[{'' if i.required else 'Optional: '}{i.name}]`"
            
            final += f"**\n {cmd.description}\n"
            return final
        
        def collect_cog_commands(bot):
            cog_commands = []
            for cog in bot.cogs.values():
                if isinstance(cog, commands.Cog):
                    for app_cmd in cog.__cog_app_commands__:
                        cog_commands.append(app_cmd)
            return cog_commands
        epic_list = collect_cog_commands(ctx.client)
        for cmd in list(ctx.client.tree.walk_commands()): epic_list.append(cmd)
        for cmd in epic_list:
            if isinstance(cmd, app_commands.Group):
                append_page(commandify(cmd), new_line=True)
            elif hasattr(cmd,"parent"):
                
                append_page(commandify(cmd), new_line=True)
            else:
                append_page(commandify(cmd), new_line=True)

        nmessage = f"Hi, I'm {ctx.client.user.name} and can run the following {len(list(ctx.client.tree.walk_commands()))} Commands:"
        if command == None:
            if len(pages) < page:
                await ctx.response.send_message(f'No page found with number {str(page)}')
            else:
                nmessage += f'\n\n------------------------ PAGE {str(page)}/{len(pages)} ------------------------\n'
                await ctx.response.send_message(nmessage, embed=pages[page-1])
        else:
            cmd = ctx.client.tree.get_command(command)
            if cmd:
                await ctx.response.send_message(commandify(cmd))
            else:
                await ctx.response.send_message(f'Command "{command}" is not found!')
    
async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))