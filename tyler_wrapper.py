# Packacge for commands in tyler ivtelli server
from package_util import *
from cog_core import *
from discord.ext import commands
import discord, random
import discord.app_commands
from datetime import datetime   

def get_wins(user_id):
    if not exists_json_db("gtn"):
        create_json_db("gtn")
    return get_json_db("gtn").get(str(user_id), [0,0])[1]
class Tyler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.number = None
        self.extra = None



    @app_commands.command(name="request", description="Request a role")
    @app_commands.choices(rn=[
    app_commands.Choice(name="RNG Manipulator", value="rng"),
    app_commands.Choice(name="Legacy Roles", value="legacy"),
    app_commands.Choice(name="Loyal Member", value="loyal"),
    ])
    async def request_cmd(self, ctx: discord.Interaction, rn=app_commands.Choice(str)):
        if rn == "rng":
            if get_wins(ctx.user.id) < 10:
                await ctx.response.send_message(f"You do not have enough *guess the number* wins for this role! You need {10-get_wins(ctx.user.id)} more wins!",ephemeral=True)
            else:
                role = await ctx.guild.fetch_role(1360666084599926824)
                await ctx.user.add_roles(role)
                await ctx.response.send_message("You got the RNG Manipulator role!")
        elif rn == "legacy":
            await ctx.response.send_message("Use my cool bot for this. This bot does not track messages")
        elif rn == "loyal":
            s = datetime.now() - datetime.timedelta(days=182)
            if ctx.user.joined_at < s:
                await ctx.response.send_message(f"You have to be in the server for more than 6 months! Days remaining: {ctx.user.joined_at-s}")
            else:
                r = await ctx.guild.fetch_role(1360665667078062144)
                await ctx.user.add_roles(r)
                await ctx.response.send_message("You got the Loyal member role!")
        else:
            await ctx.response.send_message("This error is not possible, report it")
        
    @app_commands.command("rule",description="checkout a rule!")
    async def rulecmd(self, ctx:discord.Interaction, number:app_commands.Range[int, 1, 15]):
        if ctx.channel.permissions_for(ctx.user).manage_messages:
            eph = False
        else:
            eph = True
        
        if number == 1:
            name = "No NSFW Content 🔞"
            rule = """
Any content that is not safe for work (NSFW) is strictly prohibited.

That includes:

- NSFW Remarks,
- Images,
- Drawings,

:warning: Not worth risking it over a joke :warning:
""" 
        elif number == 2:
            name = "No Toxicity to Members 💬"
            rule="""

Be respectful and kind to all members. Toxic behavior, harassment, or bullying will not be tolerated.

```ansi
[31mJaron: Stfu you skid[31m[0m
Aaron: bro what
[31mJaron: this is why no one likes you. like go get a life mf your a no one anyways[31m[0m
Aaron: im leaving this server. yall too toxic
[32mModerator: !!mute @jaron 2193712038y toxicity[32m[0m
```

Like you see in the above example, you will be punished for toxicity if you were toxic to a fello member. Not worth testing!

Instead of being toxic, just block them if you have issues.,
Moderators will take action if we find toxic attributes to your remarks,
And if you face punishment, just remember to control your anger/hate before it turning into something worse
"""
        elif number == 3:
            name = "No Doxxing"
            rule="""
Sharing personal information of others without their consent is forbidden.

Example:
```yml
Jaron: @wolf dis u?
IP: 240.69.156.420
Name: Arnold Daymond
Phone Number: +70 78634 45675
Address: 1206, 5th Tower, Blossom Apartments, 5th Cross Road, New York, US

Photo:
```

In this case, we will take action by deleting the message & giving a severe punishment.
"""
        elif number == 4:
            name = "No Discrimination of Any Sort 🚫"
            rule="""
Racism and hate speech are unacceptable in any form, any homophobia is not allowed too. Any sort of discimination at all will not be tolerated, everyone in this server has to feel welcomed, you are entitled to an opinion but if it breaks this rule please keep it to yourself!
"""
        elif number == 5:
            name = "Respect The Higher-Ups 🙇"
            rule = """
Staff with high roles have earned their positions with hard work. Show them the respect they deserve.
"""
        elif number ==6:
            name = "Use the channels for the right purposes"
            rule = """
Use a channel for its correct purposes ✅
If you wanna chat, go to #general, spam to the #spam channel, bot to #bots. Sometimes exceptions can be made like for example you can use ~grab & ~bal cmds in general but try your best to use a channel for its purposes. We don't want to clutter general

```js
Moderator: hello gng
Jaron: /help
BOT: HELP MENU
===== BIG EMBED =====



+++++++++++++++++++++
ufrrn530: @jaron stop spamming commands, i cant see messages
```

Not only commands but some topics or rants must belong in different channels such as vent and #suggestions
"""
        elif number == 7:
            name = "Keep the server PG-13 :pray:"
            rule = "I thought this was common sense but some people are just stupid. There are minors over here so let’s keep it safe for them."
        elif number == 8:
            name = "No Advertising in DMs ❌"
            rule = """
No Advertising (and in DMs) :x:
Basically don’t advertise your channel or server in stranger’s dms or you’ll get banned for 7 days.
```ansi
[31mJaron: JOIN MY COOL SERVER discord.gg/iokljdahsdkladlhald YOU'll GET COOL CAT PICS[31m[0m
messipro530: bro what
[BLOCKED & BANNED]
```
"""
        elif number == 9:
            name = "English Only :love_you_gesture:"
            rule = """
We have this rule because we have to understand everything your saying, usually other languages are used for bypasses. No languages other than english is allowed but this might change when we get moderators that can confidently translate other languages.

Believe me you wouldn't want someone speaking in german when none of us understand, it'll also be harder for us to moderate so we may/will delete messages (some moderators may kno the language or may convert it)
"""
        elif number == 10:
            name = "Controversial/Political Topics"
            rule = "No controversial topics at all, this rule is here because of the drama it usually stirs up, an example is the divide between the Israel-Palestine situation which can result in a bad end after a long conversation (Mostly turning into an angry and bad atmosphere)"
        elif number == 14:
            name = "Abide by Discord's Terms of Service 📜"
            rule = """
Follow all guidelines set by Discord's [TOS](https://discord.com/terms) & [guidelines](https://discord.com/guidelines)
"""
        elif number == 12:
            name = "Have Common Senses 🧠"
            rule = """
There are probably rules that aren’t mentioned over here like for example text walls and previous harassment in DMS, etc.. but we do still punish for them depending on how severe they are. Have common sense and know what’s right and not.

This sector can also include that you shouldn't be annoying anyone on purpose, ex. ragebaiting which is punishable if proven to ragebait on purpose.

Read [this](https://trouper.me/usebrain)
"""
        elif number == 11:
            name = "No Hate Speech 🗣️"
            rule = """
This is in 2 divisions, have respect for the members that you meet in the server and do not use any harsh slurs to insult people, some of you that are reading this might be used to using words like "retard" pretty often but those types of slurs are censored.
"""
        elif number == 13:
            name = "No Impersonation ❌"
            rule = """
Do NOT impersonate Tyler or any staffs in this server UNLESS you were excessively given permission to do so by either one of the owners or the person themselves, this rule was added to avoid confusion & misunderstanding.
"""
        elif number == 15:
            name = "Have Fun! 🎉"
            rule = """
Enjoy your time here and make the most out of our community. 
"""

        else:
            await ctx.response.send_message("You got a weird error!")

        embed = discord.Embed(title=name, description=rule)
        await ctx.response.send_message(embed=embed)





    
                


async def setup(bot):
    await bot.add_cog(Tyler(bot))