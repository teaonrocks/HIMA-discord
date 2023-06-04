import os
from datetime import timedelta
from select import select
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
import json
import asyncio
import requests

APIURL = os.getenv("APIURL")
load_dotenv()
TOKEN = os.getenv("POINTS_TOKEN")
msgjson = open("message.json", "r")
messages = json.loads(msgjson.read())
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)
GENERAL_CHANNEL_ID = os.getenv("GENERAL_CHANNEL_ID")
HALLPASS_1_ROLE = os.getenv("HALLPASS_1_ROLE")
HALLPASS_2_ROLE = os.getenv("HALLPASS_2_ROLE")
HALLPASS_3_ROLE = os.getenv("HALLPASS_3_ROLE")
HALLPASS_4_ROLE = os.getenv("HALLPASS_4_ROLE")
HALLPASS_5_ROLE = os.getenv("HALLPASS_5_ROLE")
HALLPASS_6_ROLE = os.getenv("HALLPASS_6_ROLE")
HALLPASS_7_ROLE = os.getenv("HALLPASS_7_ROLE")
HALLPASS_8_ROLE = os.getenv("HALLPASS_8_ROLE")
HALLPASS_9_ROLE = os.getenv("HALLPASS_9_ROLE")
HALLPASS_10_ROLE = os.getenv("HALLPASS_10_ROLE")
SERVER_ID = os.getenv("SERVER_ID")
LOGS_CHANNEL = os.getenv("LOGS_CHANNEL")


@client.event
async def on_ready():
    newhour.start()
    print(f"{client.user} has connected to Discord!")


async def random_minute():
    minute = "%02d" % random.randrange(3, 8)
    return minute


@tasks.loop(minutes=10)
async def newhour():
    minute = await random_minute()
    time = datetime.utcnow() + timedelta(minutes=int(minute))
    time = time.strftime("%M")
    print(f"sending message at {time}:00")
    send_msg.start(time)


@tasks.loop(seconds=1)
async def send_msg(minute):
    if datetime.utcnow().strftime("%M:%S") == f"{minute}:00":
        selector = random.randrange(0, 10)
        channel = client.get_channel(GENERAL_CHANNEL_ID)
        logs = client.get_channel(LOGS_CHANNEL)
        guild = client.get_guild(int(SERVER_ID))
        index = random.randrange(0, len(messages["scenario"]))
        scenario = messages["scenario"][index]
        answer = messages["answer"][index]
        if selector == 0 or selector == 1 or selector == 2 or selector == 3:
            embed = discord.Embed(title="🚨Alert🚨", color=0x0000FF)
            embed.add_field(name=f"{scenario}", value=f"{answer}", inline=False)
            await channel.send(embed=embed)
            print(f"sending message {datetime.utcnow()}")
            log = discord.Embed(title=f"Bento's bot sending message (Normal)")
            timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
            log.add_field(name="time", value=f"{timenow}", inline=False)
            await logs.send(embed=log)
            try:
                msg = await client.wait_for(
                    "message",
                    check=lambda x: x.content.lower() == answer
                    and x.channel.id == GENERAL_CHANNEL_ID,
                    timeout=60,
                )
                print(f"reply recieved at {msg.created_at}")
                print(msg.channel.id)
                user = await guild.fetch_member(int(msg.author.id))
                base = 1
                multiplier = 0
                for role in user.roles:
                    if role.id == HALLPASS_1_ROLE:
                        multiplier = 0.2
                    elif role.id == HALLPASS_2_ROLE:
                        multiplier = 0.4
                    elif role.id == HALLPASS_3_ROLE:
                        multiplier = 0.6
                    elif role.id == HALLPASS_4_ROLE:
                        multiplier = 0.8
                    elif role.id == HALLPASS_5_ROLE:
                        multiplier = 1
                    elif role.id == HALLPASS_6_ROLE:
                        multiplier = 1.2
                    elif role.id == HALLPASS_7_ROLE:
                        multiplier = 1.4
                    elif role.id == HALLPASS_8_ROLE:
                        multiplier = 1.6
                    elif role.id == HALLPASS_9_ROLE:
                        multiplier = 1.8
                    elif role.id == HALLPASS_10_ROLE:
                        multiplier = 2
                response = requests.put(
                    f"{APIURL}addrep/{msg.author.id}/{base + multiplier}"
                ).json()
                embed = discord.Embed(title="🎉 Congratulations 🎉")
                embed.add_field(
                    name=f"{msg.author}",
                    value=f"fast fingers 👀\nYou currently have {response['after']} Rep",
                    inline=False,
                )
                log = discord.Embed(title=f"Replied to Bento's bot (Normal)")
                log.add_field(
                    name=f"{msg.author}",
                    value=f"awarded {base + multiplier} Reps",
                    inline=False,
                )
                timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
                log.add_field(name="time", value=f"{timenow}", inline=False)
                await logs.send(embed=log)
                await msg.reply(embed=embed)
                print(
                    f"updating Rep for {msg.author}, before: {response['before']} after: {response['after']}"
                )
            except asyncio.TimeoutError:
                embed = discord.Embed(title="⏰ Timed out ⏰")
                await channel.send(embed=embed)
        elif (
            selector == 4
            or selector == 5
            or selector == 6
            or selector == 7
            or selector == 8
        ):
            embed = discord.Embed(title="🚨Alert🚨", color=0x00FF00)
            embed.add_field(name=f"{scenario}", value=f"{answer}", inline=False)
            await channel.send(embed=embed)
            print(f"sending message {datetime.utcnow()}")
            log = discord.Embed(title=f"Bento's bot sending message (Beginner)")
            timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
            log.add_field(name="time", value=f"{timenow}", inline=False)
            await logs.send(embed=log)
            try:
                msg = await client.wait_for(
                    "message",
                    check=lambda x: x.content.lower() == answer
                    and requests.get(f"{APIURL}userdata/{x.author.id}").json()["reps"]
                    < 100
                    and x.channel.id == GENERAL_CHANNEL_ID,
                    timeout=90,
                )
                print(f"reply recieved at {msg.created_at}")
                user = await guild.fetch_member(int(msg.author.id))
                base = 2
                multiplier = 0
                for role in user.roles:
                    if role.id == HALLPASS_1_ROLE:
                        multiplier = 0.2
                    elif role.id == HALLPASS_2_ROLE:
                        multiplier = 0.4
                    elif role.id == HALLPASS_3_ROLE:
                        multiplier = 0.6
                    elif role.id == HALLPASS_4_ROLE:
                        multiplier = 0.8
                    elif role.id == HALLPASS_5_ROLE:
                        multiplier = 1
                    elif role.id == HALLPASS_6_ROLE:
                        multiplier = 1.2
                    elif role.id == HALLPASS_7_ROLE:
                        multiplier = 1.4
                    elif role.id == HALLPASS_8_ROLE:
                        multiplier = 1.6
                    elif role.id == HALLPASS_9_ROLE:
                        multiplier = 1.8
                    elif role.id == HALLPASS_10_ROLE:
                        multiplier = 2
                response = requests.put(
                    f"{APIURL}addrep/{msg.author.id}/{base + multiplier}"
                ).json()
                embed = discord.Embed(title="🎉 Congratulations 🎉")
                embed.add_field(
                    name=f"{msg.author}",
                    value=f"fast fingers 👀\nYou currently have {response['after']} Rep",
                    inline=False,
                )
                log = discord.Embed(title=f"Replied to Bento's bot (Beginner)")
                log.add_field(
                    name=f"{msg.author}",
                    value=f"awarded {base + multiplier} Reps",
                    inline=False,
                )
                timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
                log.add_field(name="time", value=f"{timenow}", inline=False)
                await logs.send(embed=log)
                await msg.reply(embed=embed)
                print(
                    f"updating Rep for {msg.author}, before: {response['before']} after: {response['after']}"
                )
            except asyncio.TimeoutError:
                embed = discord.Embed(title="⏰ Timed out ⏰")
                await channel.send(embed=embed)
        elif selector == 9:
            embed = discord.Embed(title="🚨Alert🚨", color=0xFF0000)
            embed.add_field(name=f"{scenario}", value=f"{answer}", inline=False)
            await channel.send(embed=embed)
            print(f"sending message {datetime.utcnow()}")
            log = discord.Embed(title=f"Bento's bot sending message (Evil)")
            timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
            log.add_field(name="time", value=f"{timenow}", inline=False)
            await logs.send(embed=log)
            try:
                msg = await client.wait_for(
                    "message",
                    check=lambda x: x.content.lower() == answer
                    and x.channel.id == GENERAL_CHANNEL_ID,
                    timeout=60,
                )
                print(f"reply recieved at {msg.created_at}")
                base = 1
                response = requests.put(
                    f"{APIURL}minusrep/{msg.author.id}/{base}"
                ).json()
                embed = discord.Embed(title="😈 MUAHAHAHAH thanks for the Rep 😈")
                embed.add_field(
                    name=f"{msg.author}",
                    value=f"Be careful 👀\nYou currently have {response['after']} Rep",
                    inline=False,
                )
                await msg.reply(embed=embed)
                log = discord.Embed(title=f"Replied to Bento's bot (Evil)")
                log.add_field(
                    name=f"{msg.author}", value=f"Deducted 1 Rep", inline=False
                )
                timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
                log.add_field(name="time", value=f"{timenow}", inline=False)
                await logs.send(embed=log)
                print(
                    f"updating Rep for {msg.author}, before: {response['before']} after: {response['after']}"
                )
            except asyncio.TimeoutError:
                embed = discord.Embed(title="⏰ Timed out ⏰")
                await channel.send(embed=embed)
        send_msg.stop()


@client.command()
async def startloop(ctx, minute):
    send_msg.start("%02d" % int(minute))


@client.command()
async def rep(ctx):
    response = requests.get(f"{APIURL}userdata/{ctx.message.author.id}").json()
    reps = response["reps"]
    embed = discord.Embed(title="💯 Rep 💯")
    embed.add_field(
        name=f"{ctx.message.author}",
        value=f"You currently have {reps} Rep",
        inline=False,
    )
    await ctx.reply(embed=embed)
    print(f"fetching Rep for {ctx.author}")


@client.command()
async def leaderboard(ctx):
    response = requests.get(f"{APIURL}reps_leaderboard").json()
    users = response["userid"]
    reps = response["reps"]
    embed = discord.Embed(title="🏆 Leaderboard 🏆")
    if len(users) < 10:
        for x in range(len(users)):
            if x == 0:
                embed.add_field(
                    name=f"🥇{x+1}. {await client.fetch_user(users[x])}",
                    value=f"currently has {reps[x]} Rep",
                    inline=False,
                )
            if x == 1:
                embed.add_field(
                    name=f"🥈{x+1}. {await client.fetch_user(users[x])}",
                    value=f"currently has {reps[x]} Rep",
                    inline=False,
                )
            if x == 2:
                embed.add_field(
                    name=f"🥉{x+1}. {await client.fetch_user(users[x])}",
                    value=f"currently has {reps[x]} Rep",
                    inline=False,
                )
            if x > 2:
                embed.add_field(
                    name=f"{x+1}. {await client.fetch_user(users[x])}",
                    value=f"currently has {reps[x]} Rep",
                    inline=False,
                )
    else:
        for x in range(10):
            if x == 0:
                embed.add_field(
                    name=f"🥇{x+1}. {await client.fetch_user(users[x])}",
                    value=f"currently has {reps[x]} Rep",
                    inline=False,
                )
            if x == 1:
                embed.add_field(
                    name=f"🥈{x+1}. {await client.fetch_user(users[x])}",
                    value=f"currently has {reps[x]} Rep",
                    inline=False,
                )
            if x == 2:
                embed.add_field(
                    name=f"🥉{x+1}. {await client.fetch_user(users[x])}",
                    value=f"currently has {reps[x]} Rep",
                    inline=False,
                )
            if x > 2:
                embed.add_field(
                    name=f"{x+1}. {await client.fetch_user(users[x])}",
                    value=f"currently has {reps[x]} Rep",
                    inline=False,
                )
    await ctx.reply(embed=embed)
    print("fetching leaderboard")


@client.command()
async def addrep(ctx, userid, points):
    if ctx.message.author.guild_permissions.manage_messages:
        response = requests.put(f"{APIURL}addrep/{userid}/{points}").json()
        embed = discord.Embed(
            title=f"📝 Updated Rep for {await client.fetch_user(userid)} 📝"
        )
        embed.add_field(
            name=f"Before:", value=f"{response['before']} Rep", inline=False
        )
        embed.add_field(name=f"After:", value=f"{response['after']} Rep", inline=False)
        await ctx.reply(embed=embed)
        print(
            f"updating Rep for {await client.fetch_user(userid)}, before: {response['before']} after: {response['after']} - done by {ctx.message.author}"
        )
        logs = client.get_channel(LOGS_CHANNEL)
        log = discord.Embed(title=f"Rep added for {await client.fetch_user(userid)}")
        log.add_field(name="Done by", value=f"{ctx.message.author}", inline=False)
        log.add_field(name="Before: ", value=f"{response['before']}", inline=False)
        log.add_field(name="After: ", value=f"{response['after']}", inline=False)
        timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        log.add_field(name="time", value=f"{timenow}", inline=False)
        await logs.send(embed=log)
    else:
        embed = discord.Embed(
            title=f"❌ Nice try ❌",
            description="You do not have permission for this command",
        )
        await ctx.reply(embed=embed)


@client.command()
async def minusrep(ctx, userid, points):
    if ctx.message.author.guild_permissions.manage_messages:
        response = requests.put(f"{APIURL}minusrep/{userid}/{points}").json()
        embed = discord.Embed(
            title=f"📝 Updated Rep for {await client.fetch_user(userid)} 📝"
        )
        embed.add_field(
            name=f"Before:", value=f"{response['before']} Rep", inline=False
        )
        embed.add_field(name=f"After:", value=f"{response['after']} Rep", inline=False)
        await ctx.reply(embed=embed)
        print(
            f"updating Rep for {await client.fetch_user(userid)}, before: {response['before']} after: {response['after']} - done by {ctx.message.author}"
        )
        logs = client.get_channel(LOGS_CHANNEL)
        log = discord.Embed(title=f"Rep deducted for {await client.fetch_user(userid)}")
        log.add_field(name="Done by", value=f"{ctx.message.author}", inline=False)
        log.add_field(name="Before: ", value=f"{response['before']}", inline=False)
        log.add_field(name="After: ", value=f"{response['after']}", inline=False)
        timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        log.add_field(name="time", value=f"{timenow}", inline=False)
        await logs.send(embed=log)
    else:
        embed = discord.Embed(
            title=f"❌ Nice try ❌",
            description="You do not have permission for this command",
        )
        await ctx.reply(embed=embed)


@client.command()
async def checkrep(ctx, userid):
    if ctx.message.author.guild_permissions.manage_messages:
        response = requests.get(f"{APIURL}userdata/{userid}").json()
        reps = response["reps"]
        embed = discord.Embed(title="💯 Rep 💯")
        embed.add_field(
            name=f"{await client.fetch_user(userid)}",
            value=f"You currently have {reps} Rep",
            inline=False,
        )
        await ctx.reply(embed=embed)
        print(
            f"fetching Rep for {await client.fetch_user(userid)} -done by {ctx.message.author}"
        )
    else:
        embed = discord.Embed(
            title=f"❌ Nice try ❌",
            description="You do not have permission for this command",
        )
        await ctx.reply(embed=embed)


client.run(TOKEN)
