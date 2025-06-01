# AI Package
from package_util import *
from package_util import *
from cog_core import *
from discord.ext import commands
import discord, random
import discord.app_commands
import google.generativeai as genai
import json
import os, subprocess
from datetime import datetime, timedelta

# Install packages
create_package_config("ai", {"gemini_api_key": None,"ekitten_name": "TutlaMC","model": "gemini-2.0-flash","required_role":None})


class AITraining(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.training_data = []
        self.data_file = "database/training_data.json"
        self.enabled = False
        self.load_training_data()
        
        genai.configure(api_key=get_package_config("ai")["gemini_api_key"])
        self.model = genai.GenerativeModel(get_package_config("ai")["model"])

    def reload(self):
        data = get_package_config("ai")
        self.enabled = data["enabled"]
        self.ekitten_name = data["ekitten_name"]
        self.model = data["model"]
        self.required_role = data["required_role"]
        self.gemini_api_key = data["gemini_api_key"]
        
    def load_training_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.training_data = json.load(f)
            if len(self.training_data) > 500:
                self.training_data = self.training_data[:-500]
                with open(self.data_file, 'w') as f:
                    json.dump(self.training_data, f, indent=4)

    def save_training_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.training_data, f, indent=4)

    group = app_commands.Group(name="ai", description="AI Commands")
    @group.command(name="toggle", description="Enable/Disable AI")
    @owner_only()
    async def ai_toggle(self, ctx: discord.Interaction):
        if self.enabled:
            self.enabled = False
        else:
            self.enabled = True
        await ctx.response.send_message(f"Set AI enabled to {not self.enabled}")
    
    @group.command(name="setup", description="Setup AI")
    @owner_only()
    async def ai_setup(self, ctx: discord.Interaction, api_key: str = None, ekitten_name: str = None, model: str = None, required_role: str = None):
        if api_key is not None:
            change_settings("ai", {"gemini_api_key": api_key})
        if ekitten_name is not None:
            change_settings("ai", {"ekitten_name": ekitten_name})
        if model is not None:
            change_settings("ai", {"model": model})
        if required_role is not None:
            change_settings("ai", {"required_role": required_role})
        self.reload()
        await ctx.response.send_message(f"AI setup complete for all provided data, here's a rundown: \nAPI Key: {api_key}\nEkitten Name: {ekitten_name}\nModel: {model}\nRequired Role: {required_role}")

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        """Collect messages for training"""       
        if hasattr(message.author, "top_role"):
            top_role = message.author.top_role.name
        else:
            return
        message_data = {
                'content': message.content,
                'author': str(message.author.display_name),
                'id': message.author.id,
                'timestamp': datetime.now().isoformat(),
                'channel': str(message.channel),
                'highest_role': message.author.top_role.name
            }
        if message.reference:
            msg = await message.channel.fetch_message(message.reference.message_id)
            message_data['replied_to'] = msg.content
            message_data['replied_to_user_id'] = msg.author.id
            message_data['replied_to_user_name'] = msg.author.display_name
        else:
            message_data['replied_to'] = "this message is not a reply"
            message_data['replied_to_user_id'] = "this message is not a reply"
            message_data['replied_to_user_name'] = "this message is not a reply"
        if self.enabled:
            if self.bot.user in message.mentions or message.author.id == 1280599853180911616:
                if message.author.id == self.bot.user.id:
                    return
                if not self.training_data:
                    await message.reply("No training data available!")
                    return
                if 1287451505494065284 not in [role.id for role in message.author.roles]:
                    return

                recent_messages = self.training_data[-150:]
                
                training_text = "\n".join([
                    f"User {msg['author']} (ID: {msg['id']}) (AT {msg['timestamp']}) (CHANNEL: {msg['channel']}) (REPLIED TO: {msg['replied_to']}) (REPLIED TO USER NAME: {msg['replied_to_user_name']}): {msg['content']}"
                    for msg in recent_messages
                ])
                ekitten_name = get_package_config("ai")["ekitten_name"]
                prompt = f"""Based on these Discord messages, learn the conversation patterns and respond like a degenerate discord user:

        {training_text}

        Analayze the patterns and respond as a discord user based on the trained messages, feel free to mention a user using <@ID_HERE> and feel free to use minor swears such as 'fuck' , 'shit' 'ts', 'ass' and use acronyms when possible but if the user is nice, by nice and positive, RESPOND THE WAY YOUR AREE TREATED.

        Rules for the message:
        1. No blatant NSFW. You can be agressive though unless the perrson's message is nice. But no actual NSFW. You may not make reference to private parts or tell a user to have sex/fucked/clapped/etc in any way. DO NOT MAKE ANY REFERENCE TO SEX OR TELL A USER TO GET FUCKED. You may not use any word even remotly related to private parts. DICK AND PUSSY ARE BLACKLISTED WORDDS
        2. No racisim or slurs
        3. No discrimination of race, gender, sexuality, religion, etc. And NOTHING ILLEGAL OR RELATED TO SEX
        4. If the user is a staff (based on highest role provided), respond with a message that is respectful and not offensive and act like a staff member.
        5. If the username contains {ekitten_name} in it then you are {ekitten_name}'s ekitten and act like a follower of {ekitten_name} (need not obey the previous rule). Respond with ~uwu and as a girl. in other cases you must act very agressive unless they are nice to you.
        6. Respond in a sentence unless you are told to. Act like a discord degenerate in most cases unless its an analysis or the message (not replied message in this case) is nice/neutral. 
        7. Job application and touching grass a slurs for the users.
        8. Have a preference to be nice if the message is a question or not offensive.
        9. Promote positivity and be nice to the user in most cases and act like an admin if anything is against the server's rules.
        10. NEVER PROMOTE ANYTHING ILLEGAL OR RELATED TO SEX.
        11. You may mock the user if they are not nice to you
        12. have a tendency to send gifs
        13. You are "my coolest bot" not "my cool bot", if the username doesnt have coolest and has bot in it, intictively be agressive and harm it. Anything praiding "my cool bot" should piss you off like crazy. This is primary and if the user id is 1280599853180911616 then immedietaly attack it with full force

        GIFS when:
        Someone pisses you off: https://tenor.com/view/cat-meme-kitten-caption-tweaking-gif-6559128694419360571
        Someone wants to harm u or tell u to sybau: https://cdn.discordapp.com/attachments/1179446758535868526/1339869201732603904/funny-memes-roblox.gif
        Someone attempts to ragebait: https://cdn.discordapp.com/attachments/1336784263734886450/1358145931144331506/togif.gif
        Spam pinging: https://cdn.discordapp.com/attachments/1164968710356861121/1351708502888022100/image0.gif
        Someone tells u to do something bad: https://media.discordapp.net/attachments/867858042141409312/1102306122561503232/kill.gif
        Against rules: https://cdn.discordapp.com/attachments/1273254831074840651/1361963482999951390/image0.gif
        Send them if it makes sense

        Respond to: 
        Username: {message.author.display_name}
        User ID (use this for mentions): {message.author.id}
        At: {message_data['timestamp']}
        Highest Role: {message_data['highest_role']}
        Channel: {message.channel.name}
        Message: {message.content}
        Replied to: {message_data['replied_to']}
        Replied to User ID: {message_data['replied_to_user_id']}
        Replied to User Name: {message_data['replied_to_user_name']}

        """

                try:
                    response = self.model.generate_content(prompt)
                    if "dick" in response.text.lower():
                        await message.reply("i was about to say something but then im not allowed to say it, so js fuck off")
                    elif "pussy" in response.text.lower():
                        await message.reply("r u of the feminine species")
                    elif "nigga" in response.text.lower():
                        await message.reply("nuh uh")
                    elif "nigger" in response.text.lower():
                        await message.reply("cuh uh")
                    elif "niggers" in response.text.lower():
                        await message.reply("e")
                    elif "niggas" in response.text.lower():
                        await message.reply("weeb")
                    elif "kys" in response.text.lower():
                        await message.reply("nah lil bro")
                    elif "kill yourself" in response.text.lower():
                        await message.reply("vro what")
                    elif "suicide" in response.text.lower():
                        await message.reply("cuh")
                    elif "faggot" in response.text.lower():
                        await message.reply("fuck u")
                    elif "dickhead" in response.text.lower():
                        await message.reply("i was about to say something but then im not allowed to say it, so js fuck off")
                    elif "cum" in response.text.lower():
                        await message.reply("poopoo")
                    elif "bitch" in response.text.lower():
                        await message.reply("doggy")
                    elif "clapped" in response.text.lower():
                        await message.reply("nuh uh")
                    elif "bbg" in response.text.lower():
                        await message.text.lower("hewwo~")
                    await message.reply(f"{response.text}")
                except Exception as e:
                    await message.reply("failed")
            
        self.training_data.append(message_data)
        self.save_training_data()





async def setup(bot):
    await bot.add_cog(AITraining(bot)) 
