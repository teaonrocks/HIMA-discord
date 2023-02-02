import os
from urllib import response
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime
import random
import requests

load_dotenv()
TOKEN = os.getenv("ATTENDANCE_TOKEN")
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)
APIURL = os.getenv("APIURL")
# APIURL = "http://localhost:8000/api/"


@client.event
async def on_ready():
    print(
        f'{client.user} has connected to Discord at {datetime.utcnow().strftime("%H:%M:%S")}'
    )
    bgtask.start()


async def leaderboard():
    print("updating leaderboard")
    logs = client.get_channel(993366573718962256)
    log = discord.Embed(title="Updating leaderboard")
    timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
    log.add_field(name="time", value=f"{timenow}", inline=False)
    await logs.send(embed=log)
    leaderboard = requests.get(f"{APIURL}attendance_leaderboard").json()
    leaderboard_users = leaderboard["userid"]
    leaderboard_streaks = leaderboard["streaks"]
    channel = client.get_channel(980698781605560360)
    embed = discord.Embed(title="🏆 Leaderboard 🏆")
    if len(leaderboard_users) < 10:
        for x in range(len(leaderboard_users)):
            if x == 0:
                embed.add_field(
                    name=f"🥇{x+1}. {await client.fetch_user(int(leaderboard_users[x]))}",
                    value=f"currently has {leaderboard_streaks[x]} Days",
                    inline=False,
                )
            if x == 1:
                embed.add_field(
                    name=f"🥈{x+1}. {await client.fetch_user(int(leaderboard_users[x]))}",
                    value=f"currently has {leaderboard_streaks[x]} Days",
                    inline=False,
                )
            if x == 2:
                embed.add_field(
                    name=f"🥉{x+1}. {await client.fetch_user(int(leaderboard_users[x]))}",
                    value=f"currently has {leaderboard_streaks[x]} Days",
                    inline=False,
                )
            if x > 2:
                embed.add_field(
                    name=f"{x+1}. {await client.fetch_user(int(leaderboard_users[x]))}",
                    value=f"currently has {leaderboard_streaks[x]} Days",
                    inline=False,
                )
    else:
        for x in range(10):
            if x == 0:
                embed.add_field(
                    name=f"🥇{x+1}. {await client.fetch_user(int(leaderboard_users[x]))}",
                    value=f"currently has {leaderboard_streaks[x]} Days",
                    inline=False,
                )
            if x == 1:
                embed.add_field(
                    name=f"🥈{x+1}. {await client.fetch_user(int(leaderboard_users[x]))}",
                    value=f"currently has {leaderboard_streaks[x]} Days",
                    inline=False,
                )
            if x == 2:
                embed.add_field(
                    name=f"🥉{x+1}. {await client.fetch_user(int(leaderboard_users[x]))}",
                    value=f"currently has {leaderboard_streaks[x]} Days",
                    inline=False,
                )
            if x > 2:
                embed.add_field(
                    name=f"{x+1}. {await client.fetch_user(int(leaderboard_users[x]))}",
                    value=f"currently has {leaderboard_streaks[x]} Days",
                    inline=False,
                )
    await channel.send(embed=embed)


async def daily_raffle():
    logs = client.get_channel(993366573718962256)
    heretoday = requests.get(f"{APIURL}present_today").json()
    raffle = heretoday["userid"]
    winnerid = random.choice(raffle)
    guild = client.get_guild(int(943173196490879009))
    channel = client.get_channel(986155177427992586)
    scholars = guild.get_role(980506731736100946)
    honor = guild.get_role(977092646763921439)
    winnerobj = await guild.fetch_member(int(winnerid))
    userrole = "student"
    for role in winnerobj.roles:
        if role.id == 977092646763921439:
            userrole = "honor"
        elif role.id == 980506731736100946:
            userrole = "scholar"
    if userrole == "scholar":
        response = requests.put(f"{APIURL}addrep/{winnerid}/15").json()
        print(
            f"{await client.fetch_user(int(winnerid))} Already has scholar, rewarding 15 Reps"
        )
        print(
            f"updating Rep for {await client.fetch_user(winnerid)} before:{response['before']} after:{response['after']}"
        )
        log = discord.Embed(title="Daily raffle")
        log.add_field(
            name=f"{winnerobj.name}",
            value="User already has scholar, awarding 15 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
        embed = discord.Embed(
            title=f"🎉 {winnerobj.name} 🎉", description="You won 15 Reps"
        )
        await channel.send(winnerobj.mention, embed=embed)

    elif userrole == "honor":
        if len(scholars.members) < 250:
            await winnerobj.add_roles(scholars)
            await winnerobj.remove_roles(honor)
            print(
                f"{await client.fetch_user(int(winnerid))} Already has Honor roll, Upgrading to scholar"
            )
            log = discord.Embed(title="Daily raffle")
            log.add_field(
                name=f"{winnerobj.name}",
                value="User already has Honor roll, Upgrading to scholar.",
                inline=False,
            )
            await logs.send(embed=log)
            embed = discord.Embed(
                title=f"🎉 {winnerobj.name} 🎉",
                description="You have been upgraded to a scholar",
            )
            await channel.send(winnerobj.mention, embed=embed)
        else:
            response = requests.put(f"{APIURL}addrep/{winnerid}/10").json()
            print(
                f"{await client.fetch_user(int(winnerid))} Already has Honor roll, Scholars are full, awarding 10 Rep"
            )
            log = discord.Embed(title="Daily raffle")
            log.add_field(
                name=f"{winnerobj.name}",
                value="User already has Honor roll, Scholars are full, awarding 10 Rep.",
                inline=False,
            )
            await logs.send(embed=log)
            print(
                f"updating Rep for {await client.fetch_user(winnerid)} before:{response['before']} after:{response['after']}"
            )
            embed = discord.Embed(
                title=f"🎉 {winnerobj.name} 🎉", description="You won 10 Reps"
            )
            await channel.send(winnerobj.mention, embed=embed)

    elif userrole == "student":
        if len(honor.members) < 400:
            await winnerobj.add_roles(honor)
            embed = discord.Embed(
                title=f"🎉 {winnerobj.name} 🎉",
                description="You have been upgraded to Honor Roll",
            )
            log = discord.Embed(title="Daily raffle")
            log.add_field(
                name=f"{winnerobj.name}",
                value="User upgraded to Honor roll.",
                inline=False,
            )
            await logs.send(embed=log)
            await channel.send(winnerobj.mention, embed=embed)
            print(f"{await client.fetch_user(int(winnerid))} Upgrading to Honor roll")

        else:
            response = requests.put(f"{APIURL}addrep/{winnerid}/10").json()
            print(
                f"{await client.fetch_user(int(winnerid))} Honor roll is full, rewarding 5 Reps"
            )
            print(
                f"updating Rep for {await client.fetch_user(winnerid)} before:{response['before']} after:{response['after']}"
            )
            log = discord.Embed(title="Daily raffle")
            log.add_field(
                name=f"{winnerobj.name}",
                value="Honor roll is full, awarding 5 Reps.",
                inline=False,
            )
            await logs.send(embed=log)
            embed = discord.Embed(
                title=f"🎉 {winnerobj.name} 🎉", description="You won 5 Reps"
            )
            await channel.send(winnerobj.mention, embed=embed)

    dayresponse = requests.get(f"{APIURL}getday").json()
    day = dayresponse["day"]
    if day == 7:
        raffle = []
        members = requests.get(f"{APIURL}get_members_above/week/{5/7}").json()
        winnerid = random.choice(members["members"])
        weeklywinner = await guild.fetch_member(int(winnerid))
        response = requests.put(f"{APIURL}addrep/{winnerid}/20").json()
        log = discord.Embed(title="Day 7 raffle")
        log.add_field(name=f"{winnerobj.name}", value="Awarding 20 Reps.", inline=False)
        await logs.send(embed=log)
        embed = discord.Embed(
            title=f"🎉 {weeklywinner.name} 🎉", description="You won 20 Reps"
        )
        await channel.send(weeklywinner.mention, embed=embed)
        print(f"{await client.fetch_user(winnerid)} won the weekly giveaway")
        print(
            f"updating Rep for {await client.fetch_user(winnerid)} before: {response['before']} after: {response['after']}"
        )


async def new_day():
    logs = client.get_channel(993366573718962256)
    response = requests.post(f"{APIURL}newday").json()
    print(f"New day, Week: {response['week']} Day: {response['day']}")
    guild = client.get_guild(int(943173196490879009))
    students = guild.get_role(943176594539827200)
    channel = client.get_channel(980367233253519360)
    embed = discord.Embed(
        title=f"⏰ Attention students ⏰", description="The school day has begun"
    )
    embed.add_field(name=f"!present", value=f"Mark attendance", inline=False)
    embed.add_field(name=f"!attendance", value=f"Check attendance", inline=False)
    await channel.send(students.mention, embed=embed)
    log = discord.Embed(title="New day")
    await logs.send(embed=log)


async def daily_rep():
    logs = client.get_channel(993366573718962256)
    guild = client.get_guild(int(943173196490879009))
    hp10 = guild.get_role(984905714860453928).members
    hp9 = guild.get_role(984905707751084032).members
    hp8 = guild.get_role(984905700692086834).members
    hp7 = guild.get_role(984905693628874762).members
    hp6 = guild.get_role(984905686536290304).members
    hp5 = guild.get_role(984905679607324672).members
    hp4 = guild.get_role(984905672699306025).members
    hp3 = guild.get_role(984905665778688020).members
    hp2 = guild.get_role(984905658929389628).members
    hp1 = guild.get_role(984905652054933584).members

    for member in hp10:
        response = requests.put(f"{APIURL}addrep/{member.id}/10").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 10 Hall Passes, awarding 10 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
    for member in hp9:
        response = requests.put(f"{APIURL}addrep/{member.id}/9").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 9 Hall Passes, awarding 9 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
    for member in hp8:
        response = requests.put(f"{APIURL}addrep/{member.id}/8").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 8 Hall Passes, awarding 8 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
    for member in hp7:
        response = requests.put(f"{APIURL}addrep/{member.id}/7").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 7 Hall Passes, awarding 7 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
    for member in hp6:
        response = requests.put(f"{APIURL}addrep/{member.id}/6").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 6 Hall Passes, awarding 6 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
    for member in hp5:
        response = requests.put(f"{APIURL}addrep/{member.id}/5").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 5 Hall Passes, awarding 5 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
    for member in hp4:
        response = requests.put(f"{APIURL}addrep/{member.id}/4").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 4 Hall Passes, awarding 4 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
    for member in hp3:
        response = requests.put(f"{APIURL}addrep/{member.id}/3").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 3 Hall Passes, awarding 3 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
    for member in hp2:
        response = requests.put(f"{APIURL}addrep/{member.id}/2").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 2 Hall Passes, awarding 2 Reps.",
            inline=False,
        )
        await logs.send(embed=log)
    for member in hp1:
        response = requests.put(f"{APIURL}addrep/{member.id}/1").json()
        print(
            f"Updating rep for {await client.fetch_user(member.id)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Daily Reps")
        log.add_field(
            name=f"{member.name}",
            value="User has 1 Hall Pass, awarding 1 Rep.",
            inline=False,
        )
        await logs.send(embed=log)


async def streak_rep():
    logs = client.get_channel(993366573718962256)
    response = requests.get(f"{APIURL}get_10_streak").json()
    members = response["members"]
    for member in members:
        response = requests.put(f"{APIURL}addrep/{member}/10").json()
        print(
            f"Updating rep for {await client.fetch_user(member)} before: {response['before']} after: {response['after']}"
        )
        log = discord.Embed(title="Streak Reps")
        log.add_field(
            name=f"{await client.fetch_user(member)}",
            value="User has 10 streak, awarding 10 Reps.",
            inline=False,
        )
        await logs.send(embed=log)


@tasks.loop(seconds=1)
async def bgtask():
    if datetime.utcnow().strftime("%H:%M:%S") == "15:55:00":
        await leaderboard()
        await streak_rep()
        await daily_raffle()

    if datetime.utcnow().strftime("%H:%M:%S") == "16:00:00":
        await new_day()
        await daily_rep()


@client.command()
async def streakleaderboard(ctx):
    if ctx.message.author.guild_permissions.manage_messages:
        leaderboard()
        embed = discord.Embed(
            title=f"✅ Success ✅", description="Leaderboard has been updated"
        )
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title=f"❌ Nice try ❌",
            description="You do not have permission for this command",
        )
        await ctx.reply(embed=embed)


@client.command()
async def present(ctx):
    logs = client.get_channel(993366573718962256)
    userid = ctx.message.author.id
    response = requests.put(f"{APIURL}present/{userid}").json()
    if response["first"]:
        embed = discord.Embed(
            title=f"{ctx.message.author}", description="Attendance taken 📝"
        )
        log = discord.Embed(title="Attendance")
        log.add_field(
            name=f"{ctx.message.author}",
            value="User has taken attendance",
            inline=False,
        )
        timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        log.add_field(name="time", value=f"{timenow}", inline=False)
        await logs.send(embed=log)
        await ctx.reply(embed=embed)
        print(f"Attendance updated for {ctx.message.author}")
    else:
        embed = discord.Embed(
            title=f"{ctx.message.author}", description="Attendance already taken 📝"
        )
        await ctx.reply(embed=embed)
        print(f"{ctx.message.author} has already marked attendance for today")


@client.command()
async def attendance(ctx):
    userid = ctx.message.author.id
    response = requests.get(f"{APIURL}userdata/{userid}").json()
    weekly_attendance = response["weekly_attendance"]
    full_attendance = response["full_attendance"]
    streak = response["streak"]
    date = requests.get(f"{APIURL}getday").json()
    week = date["week"]
    day = date["day"]
    print(f"fetching attendance for {ctx.message.author}")
    userid = ctx.message.author.id
    embed = discord.Embed(title=f"📝 Attendance for {ctx.message.author} 📝")
    embed.add_field(
        name=f"Current day", value=f"Day {day} of week {week}", inline=False
    )
    embed.add_field(
        name=f"Attendance for current week", value=f"{weekly_attendance}%", inline=False
    )
    embed.add_field(name=f"Full attendance", value=f"{full_attendance}%", inline=False)
    embed.add_field(name=f"Streak", value=f"{streak} Days", inline=False)
    await ctx.reply(embed=embed)


@client.command()
async def check(ctx, userid):
    if ctx.message.author.guild_permissions.manage_messages:
        user = await client.fetch_user(int(userid))
        print(f"fetching attendance for {user}")
        response = requests.get(f"{APIURL}userdata/{userid}").json()
        weekly_attendance = response["weekly_attendance"]
        full_attendance = response["full_attendance"]
        streak = response["streak"]
        date = requests.get(f"{APIURL}getday").json()
        week = date["week"]
        day = date["day"]
        embed = discord.Embed(title=f"📝 Attendance for {user} 📝")
        embed.add_field(
            name=f"Current day", value=f"Day {day} of week {week}", inline=False
        )
        embed.add_field(
            name=f"Attendance for current week",
            value=f"{weekly_attendance}%",
            inline=False,
        )
        embed.add_field(
            name=f"Full attendance", value=f"{full_attendance}%", inline=False
        )
        embed.add_field(name=f"Streak", value=f"{streak} Days", inline=False)
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title=f"❌ Nice try ❌",
            description="You do not have permission for this command",
        )
        await ctx.reply(embed=embed)


@client.command()
async def dailyrep(ctx):
    if ctx.message.author.guild_permissions.manage_messages:
        await daily_rep()
        embed = discord.Embed(
            title=f"✅ Success ✅", description="Daily Rep has been awarded"
        )
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title=f"❌ Nice try ❌",
            description="You do not have permission for this command",
        )
        await ctx.reply(embed=embed)


@client.command()
async def newday(ctx):
    if ctx.message.author.guild_permissions.manage_messages:
        await new_day()
        embed = discord.Embed(title=f"✅ Success ✅", description="Day has cycled")
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title=f"❌ Nice try ❌",
            description="You do not have permission for this command",
        )
        await ctx.reply(embed=embed)


@client.command()
async def daily(ctx):
    if ctx.message.author.guild_permissions.manage_messages:
        await daily_raffle()
        embed = discord.Embed(
            title=f"✅ Success ✅", description="Daily raffle has been executed"
        )
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(
            title=f"❌ Nice try ❌",
            description="You do not have permission for this command",
        )
        await ctx.reply(embed=embed)


client.run(TOKEN)
