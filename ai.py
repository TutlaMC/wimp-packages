# AI Package

import discord
from discord.ext import commands
import google.generativeai as genai
import json
import os, subprocess
from datetime import datetime, timedelta

# Install packages
subprocess.run(["pip", "install", "google-generativeai"])
create_package_config("ai", {"gemini_api_key": None,"ekitten_name": "TutlaMC","model": "gemini-2.0-flash"})
if get_package_config("ai")["gemini_api_key"] is None:
    gemini_api_key = input("Enter your Gemini API key: ")
    change_package_config("ai", {"gemini_api_key": gemini_api_key})

class AITraining(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.training_data = []
        self.data_file = "database/training_data.json"
        self.load_training_data()
        
        genai.configure(api_key=get_package_config("ai")["gemini_api_key"])
        self.model = genai.GenerativeModel(get_package_config("ai")["model"])

    def load_training_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.training_data = json.load(f)

    def save_training_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.training_data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        """Collect messages for training"""
        if message.author.id == self.bot.user.id:
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
        if self.bot.user in message.mentions:
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

    GIFS when:
    Someone pisses you off: https://tenor.com/view/cat-meme-kitten-caption-tweaking-gif-6559128694419360571
    Someone attempts to ragebait: https://cdn.discordapp.com/attachments/1336784263734886450/1358145931144331506/togif.gif
    Spam pinging: https://cdn.discordapp.com/attachments/1164968710356861121/1351708502888022100/image0.gif
    Someone tells u to do something bad: https://media.discordapp.net/attachments/867858042141409312/1102306122561503232/kill.gif
    Against rules: https://cdn.discordapp.com/attachments/1273254831074840651/1361963482999951390/image0.gif
    Append these gifs to the message in most cases.

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
                    await message.reply("Error")
                elif "pussy" in response.text.lower():
                    await message.reply("Error")
                elif "shit" in response.text.lower():
                    await message.reply("Error")
                elif "nigga" in response.text.lower():
                    await message.reply("Error")
                elif "nigger" in response.text.lower():
                    await message.reply("Error")
                elif "niggers" in response.text.lower():
                    await message.reply("Error")
                elif "niggas" in response.text.lower():
                    await message.reply("Error")
                elif "kys" in response.text.lower():
                    await message.reply("Error")
                elif "kill yourself" in response.text.lower():
                    await message.reply("Error")
                elif "suicide" in response.text.lower():
                    await message.reply("Error")
                elif "faggot" in response.text.lower():
                    await message.reply("Error")
                elif "dickhead" in response.text.lower():
                    await message.reply("Error")
                elif "cum" in response.text.lower():
                    await message.reply("Error")
                await message.reply(f"{response.text}")
            except Exception as e:
                pass
        else:
            
            self.training_data.append(message_data)
            self.save_training_data()



    @commands.command()
    @commands.is_owner()
    async def clear_training(self, ctx):
        """Clear all collected training data"""
        self.training_data = []
        self.save_training_data()
        await ctx.send("Training data cleared!")

async def setup(bot):
    await bot.add_cog(AITraining(bot)) 