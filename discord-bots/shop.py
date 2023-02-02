import discord
from discord import default_permissions
from discord.ext import commands, tasks
from discord.ui import Button, View
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
import requests
import os

APIURL = "http://164.68.109.113/api/"
# APIURL = "http://localhost:8000/api/"
load_dotenv()
TOKEN = os.getenv("SHOP_TOKEN")
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)


class Item:
    def __init__(self, name, price, callback):
        self.name = name
        self.price = price
        self.callback = callback


async def ml_day_callback(interaction):
    embed = discord.Embed(title="Confirm your transaction")
    embed.add_field(name="Medical leave (1 Day)", value="20 Reps", inline=False)
    confirm = Button(label="✅ Confirm", style=discord.ButtonStyle.green)
    cancel = Button(label="❌ Cancel", style=discord.ButtonStyle.red)

    async def confirm_callback(interaction):
        account = requests.get(f"{APIURL}userdata/{interaction.user.id}").json()
        if account["reps"] < 20:
            embed = discord.Embed(title="❌ Error")
            embed.add_field(
                name="Error",
                value="You dont have enough Reps to purchase this item",
            )
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            transaction = requests.put(
                f"{APIURL}minusrep/{interaction.user.id}/20"
            ).json()
            response = requests.put(
                f"{APIURL}medical_leave/{interaction.user.id}/1"
            ).json()
            updated = response["updated"]
            embed = discord.Embed(title="✅ Success")
            for update in updated:
                embed.add_field(name="updated", value=f"{update}", inline=False)
            embed.add_field(
                name="before", value=f"{transaction['before']} Reps", inline=False
            )
            embed.add_field(
                name="after", value=f"{transaction['after']} Reps", inline=False
            )
            logs = client.get_channel(993366573718962256)
            log = discord.Embed(title="Purchase")
            log.add_field(
                name=f"{interaction.user}",
                value="Purchased medical leave (1 Day).",
                inline=False,
            )
            log.add_field(
                name="Before: ", value=f"{transaction['before']} Reps", inline=False
            )
            log.add_field(
                name="After: ", value=f"{transaction['after']} Reps", inline=False
            )
            timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
            log.add_field(name="time", value=f"{timenow}", inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
            await logs.send(embed=log)

    async def cancel_callback(interaction):
        embed = discord.Embed(title="✅ Cancelled")
        await interaction.response.edit_message(embed=embed, view=None)

    confirm.callback = confirm_callback
    cancel.callback = cancel_callback
    view = View(confirm, cancel)
    await interaction.response.edit_message(embed=embed, view=view)


async def ml_week_callback(interaction):
    embed = discord.Embed(title="Confirm your transaction")
    embed.add_field(name="Medical leave (7 Days)", value="80 Reps", inline=False)
    confirm = Button(label="✅ Confirm", style=discord.ButtonStyle.green)
    cancel = Button(label="❌ Cancel", style=discord.ButtonStyle.red)

    async def confirm_callback(interaction):
        account = requests.get(f"{APIURL}userdata/{interaction.user.id}").json()
        if account["reps"] < 80:
            embed = discord.Embed(title="❌ Error")
            embed.add_field(
                name="Error",
                value="You dont have enough Reps to purchase this item",
            )
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            transaction = requests.put(
                f"{APIURL}minusrep/{interaction.user.id}/80"
            ).json()
            response = requests.put(
                f"{APIURL}medical_leave/{interaction.user.id}/7"
            ).json()
            updated = response["updated"]
            embed = discord.Embed(title="✅ Success")
            for update in updated:
                embed.add_field(name="updated", value=f"{update}", inline=False)
            embed.add_field(
                name="before", value=f"{transaction['before']} Reps", inline=False
            )
            embed.add_field(
                name="after", value=f"{transaction['after']} Reps", inline=False
            )
            logs = client.get_channel(993366573718962256)
            log = discord.Embed(title="Purchase")
            log.add_field(
                name=f"{interaction.user}",
                value="Purchased medical leave (7 Days).",
                inline=False,
            )
            log.add_field(
                name="Before: ", value=f"{transaction['before']} Reps", inline=False
            )
            log.add_field(
                name="After: ", value=f"{transaction['after']} Reps", inline=False
            )
            timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
            log.add_field(name="time", value=f"{timenow}", inline=False)
            await interaction.response.edit_message(embed=embed, view=None)
            await logs.send(embed=log)

    async def cancel_callback(interaction):
        embed = discord.Embed(title="✅ Cancelled")
        await interaction.response.edit_message(embed=embed, view=None)

    confirm.callback = confirm_callback
    cancel.callback = cancel_callback
    view = View(confirm, cancel)
    await interaction.response.edit_message(embed=embed, view=view)


async def honor_roll_callback(interaction):
    embed = discord.Embed(title="Confirm your transaction")
    embed.add_field(name="Honor roll", value="100 Reps", inline=False)
    confirm = Button(label="✅ Confirm", style=discord.ButtonStyle.green)
    cancel = Button(label="❌ Cancel", style=discord.ButtonStyle.red)

    async def confirm_callback(interaction):
        userrole = "student"
        for role in interaction.user.roles:
            if role.id == 977092646763921439:
                userrole = "honor"
            elif role.id == 980506731736100946:
                userrole = "scholar"
        if userrole == "honor" or userrole == "scholar":
            embed = discord.Embed(title="❌ Error")
            embed.add_field(
                name="Error",
                value="If you have Honor roll or Scholar you are not able to purchase this item",
            )
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            account = requests.get(f"{APIURL}userdata/{interaction.user.id}").json()
            if account["reps"] < 100:
                embed = discord.Embed(title="❌ Error")
                embed.add_field(
                    name="Error",
                    value="You dont have enough Reps to purchase this item",
                )
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                transaction = requests.put(
                    f"{APIURL}minusrep/{interaction.user.id}/100"
                ).json()
                guild = client.get_guild(int(943173196490879009))
                honor = guild.get_role(977092646763921439)
                user_obj = await guild.fetch_member(int(interaction.user.id))
                await user_obj.add_roles(honor)
                embed = discord.Embed(title="✅ You have been upgraded to honor role")
                embed.add_field(
                    name="before",
                    value=f"{transaction['before']} Reps",
                    inline=False,
                )
                embed.add_field(
                    name="after", value=f"{transaction['after']} Reps", inline=False
                )
                logs = client.get_channel(993366573718962256)
                log = discord.Embed(title="Purchase")
                log.add_field(
                    name=f"{interaction.user}",
                    value="Purchased Honor roll.",
                    inline=False,
                )
                log.add_field(
                    name="Before: ", value=f"{transaction['before']} Reps", inline=False
                )
                log.add_field(
                    name="After: ", value=f"{transaction['after']} Reps", inline=False
                )
                timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
                log.add_field(name="time", value=f"{timenow}", inline=False)
                await interaction.response.edit_message(embed=embed, view=None)
                await logs.send(embed=log)

    async def cancel_callback(interaction):
        embed = discord.Embed(title="✅ Cancelled")
        await interaction.response.edit_message(embed=embed, view=None)

    confirm.callback = confirm_callback
    cancel.callback = cancel_callback
    view = View(confirm, cancel)
    await interaction.response.edit_message(embed=embed, view=view)


async def scholar_callback(interaction):
    embed = discord.Embed(title="Confirm your transaction")
    embed.add_field(name="Scholarship", value="120 Reps", inline=False)
    confirm = Button(label="✅ Confirm", style=discord.ButtonStyle.green)
    cancel = Button(label="❌ Cancel", style=discord.ButtonStyle.red)

    async def confirm_callback(interaction):
        userrole = "student"
        for role in interaction.user.roles:
            if role.id == 977092646763921439:
                userrole = "honor"
            elif role.id == 980506731736100946:
                userrole = "scholar"
        if userrole == "student":
            embed = discord.Embed(title="❌ Error")
            embed.add_field(
                name="Error",
                value="You must have Honor roll to purchase this item",
            )
            await interaction.response.edit_message(embed=embed, view=None)

        elif userrole == "scholar":
            embed = discord.Embed(title="❌ Error")
            embed.add_field(name="Error", value="You already have Scholar")
            await interaction.response.edit_message(embed=embed, view=None)
        elif userrole == "honor":
            account = requests.get(f"{APIURL}userdata/{interaction.user.id}").json()
            if account["reps"] < 120:
                embed = discord.Embed(title="❌ Error")
                embed.add_field(
                    name="Error",
                    value="You dont have enough Reps to purchase this item",
                )
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                transaction = requests.put(
                    f"{APIURL}minusrep/{interaction.user.id}/120"
                ).json()
                guild = client.get_guild(int(943173196490879009))
                scholar = guild.get_role(980506731736100946)
                honor = guild.get_role(977092646763921439)
                user_obj = await guild.fetch_member(int(interaction.user.id))
                await user_obj.add_roles(scholar)
                await user_obj.remove_roles(honor)
                embed = discord.Embed(title="✅ You have been upgraded to Scholar")
                embed.add_field(
                    name="before",
                    value=f"{transaction['before']} Reps",
                    inline=False,
                )
                embed.add_field(
                    name="after", value=f"{transaction['after']} Reps", inline=False
                )
                logs = client.get_channel(993366573718962256)
                log = discord.Embed(title="Purchase")
                log.add_field(
                    name=f"{interaction.user}", value="Purchased Scholar", inline=False
                )
                log.add_field(
                    name="Before: ", value=f"{transaction['before']} Reps", inline=False
                )
                log.add_field(
                    name="After: ", value=f"{transaction['after']} Reps", inline=False
                )
                timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
                log.add_field(name="time", value=f"{timenow}", inline=False)
                await interaction.response.edit_message(embed=embed, view=None)
                await logs.send(embed=log)

    async def cancel_callback(interaction):
        embed = discord.Embed(title="✅ Cancelled")
        await interaction.response.edit_message(embed=embed, view=None)

    confirm.callback = confirm_callback
    cancel.callback = cancel_callback
    view = View(confirm, cancel)
    await interaction.response.edit_message(embed=embed, view=view)


async def mint_ticket_callback(interaction):
    embed = discord.Embed(title="Confirm your transaction")
    embed.add_field(name="Mint ticket", value="200 Reps", inline=False)
    confirm = Button(label="✅ Confirm", style=discord.ButtonStyle.green)
    cancel = Button(label="❌ Cancel", style=discord.ButtonStyle.red)

    async def confirm_callback(interaction):
        guild = client.get_guild(int(943173196490879009))
        ticketrole = guild.get_role(990950779802255401)
        user_obj = await guild.fetch_member(int(interaction.user.id))
        ticket = False
        for role in interaction.user.roles:
            if role.id == 990950779802255401:
                ticket = True
        if ticket:
            embed = discord.Embed(title="❌ Error")
            embed.add_field(name="Error", value="You already own a mint ticket")
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            account = requests.get(f"{APIURL}userdata/{interaction.user.id}").json()
            if account["reps"] < 200:
                embed = discord.Embed(title="❌ Error")
                embed.add_field(
                    name="Error",
                    value="You dont have enough Reps to purchase this item",
                )
                await interaction.response.edit_message(embed=embed, view=None)
            else:
                if len(ticketrole.members) < 100:
                    transaction = requests.put(
                        f"{APIURL}minusrep/{interaction.user.id}/200"
                    ).json()
                    await user_obj.add_roles(ticketrole)
                    embed = discord.Embed(title="✅ Success")
                    embed.add_field(
                        name="before",
                        value=f"{transaction['before']} Reps",
                        inline=False,
                    )
                    embed.add_field(
                        name="after",
                        value=f"{transaction['after']} Reps",
                        inline=False,
                    )
                    logs = client.get_channel(993366573718962256)
                    log = discord.Embed(title="Purchase")
                    log.add_field(
                        name=f"{interaction.user}",
                        value="Purchased Mint ticket.",
                        inline=False,
                    )
                    log.add_field(
                        name="Before: ",
                        value=f"{transaction['before']} Reps",
                        inline=False,
                    )
                    log.add_field(
                        name="After: ",
                        value=f"{transaction['after']} Reps",
                        inline=False,
                    )
                    timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
                    log.add_field(name="time", value=f"{timenow}", inline=False)
                    await interaction.response.edit_message(embed=embed, view=None)
                    await logs.send(embed=log)
                else:
                    embed = discord.Embed(title="❌ Error")
                    embed.add_field(
                        name="Error", value="Sorry mint tickets are sold out"
                    )
                    await interaction.response.edit_message(embed=embed, view=None)

    async def cancel_callback(interaction):
        embed = discord.Embed(title="✅ Cancelled")
        await interaction.response.edit_message(embed=embed, view=None)

    confirm.callback = confirm_callback
    cancel.callback = cancel_callback
    view = View(confirm, cancel)
    await interaction.response.edit_message(embed=embed, view=view)


async def raffle_callback(interaction):
    embed = discord.Embed(title="Confirm your transaction")
    embed.add_field(name="raffle ticket", value="10 Reps", inline=False)
    confirm = Button(label="✅ Confirm", style=discord.ButtonStyle.green)
    cancel = Button(label="❌ Cancel", style=discord.ButtonStyle.red)

    async def confirm_callback(interaction):
        guild = client.get_guild(int(943173196490879009))
        ticketrole = guild.get_role(991763573737009172)
        user_obj = await guild.fetch_member(int(interaction.user.id))
        account = requests.get(f"{APIURL}userdata/{interaction.user.id}").json()
        first_time = True
        if account["reps"] < 10:
            embed = discord.Embed(title="❌ Error")
            embed.add_field(
                name="Error",
                value="You dont have enough Reps to purchase this item",
            )
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            for role in user_obj.roles:
                if role.id == 991763573737009172:
                    first_time = False
            if first_time:
                await user_obj.add_roles(ticketrole)
                transaction = requests.put(
                    f"{APIURL}minusrep/{interaction.user.id}/10"
                ).json()
                embed = discord.Embed(title="✅ Success")
                embed.add_field(
                    name="before", value=f"{transaction['before']} Reps", inline=False
                )
                embed.add_field(
                    name="after", value=f"{transaction['after']} Reps", inline=False
                )
                logs = client.get_channel(993366573718962256)
                log = discord.Embed(title="Purchase")
                log.add_field(
                    name=f"{interaction.user}",
                    value="Purchased Raffle ticket.",
                    inline=False,
                )
                log.add_field(
                    name="Before: ", value=f"{transaction['before']} Reps", inline=False
                )
                log.add_field(
                    name="After: ", value=f"{transaction['after']} Reps", inline=False
                )
                timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
                log.add_field(name="time", value=f"{timenow}", inline=False)
                await interaction.response.edit_message(embed=embed, view=None)
                await logs.send(embed=log)
            else:
                embed = discord.Embed(title="❌ Error")
                embed.add_field(
                    name="Error",
                    value="You only can purchase this item once",
                )
                await interaction.response.edit_message(embed=embed, view=None)

    async def cancel_callback(interaction):
        embed = discord.Embed(title="✅ Cancelled")
        await interaction.response.edit_message(embed=embed, view=None)

    confirm.callback = confirm_callback
    cancel.callback = cancel_callback
    view = View(confirm, cancel)
    await interaction.response.edit_message(embed=embed, view=view)


ml_day = Item("Medical leave (1 Day)", 20, ml_day_callback)
ml_week = Item("Medical leave (7 Days)", 80, ml_week_callback)
honor_roll_role = Item("Honor roll", 100, honor_roll_callback)
scholar_role = Item("Scholarship", 120, scholar_callback)
mint_ticket = Item("Mint ticket", 200, mint_ticket_callback)
raffle_ticket = Item("Raffle ticket", 10, raffle_callback)
shop_items = [
    ml_day,
    ml_week,
    honor_roll_role,
    scholar_role,
    mint_ticket,
]


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


@client.slash_command(
    guild_ids=[943173196490879009, 943841709106819092],
    description="🛒 Rep shop",
)
async def shop(ctx):
    embed = discord.Embed(title="🛒 Rep Shop ")
    shopview = View()
    btns = []
    for index, item in enumerate(shop_items):
        embed.add_field(
            name=f"{index+1}. {item.name}", value=f"{item.price} Reps", inline=False
        )
        btn = Button(label=f"{index+1}", style=discord.ButtonStyle.green)
        btns.append(btn)

    for btn, item in zip(btns, shop_items):
        btn.callback = item.callback
        shopview.add_item(btn)

    await ctx.respond(embed=embed, view=shopview, ephemeral=True)


@client.slash_command(
    guild_ids=[943173196490879009, 943841709106819092],
    description="Set up raffle in shop",
)
@default_permissions(manage_messages=True)
async def raffle(
    ctx,
    duration: discord.Option(int, description="Duration in HOURS"),
    prize: discord.Option(str, description="Prize"),
):
    embed = discord.Embed(title="✅ Confirm")
    embed.add_field(name="Duration", value=f"{duration} Hours", inline=False)
    embed.add_field(name="Price", value="10 Reps", inline=False)
    embed.add_field(name="prize", value=f"{prize}")
    confirm = Button(label="Confirm", style=discord.ButtonStyle.green)
    cancel = Button(label="Cancel", style=discord.ButtonStyle.red)

    async def confirm_callback(interaction):
        embed = discord.Embed(title="✅ Success")
        shop_items.append(raffle_ticket)
        now = datetime.utcnow()
        time = now + timedelta(hours=duration)
        raffle_timer.start(time.strftime("%Y/%m/%d %H:%M:%S"), prize)
        print(time.strftime("%Y/%m/%d %H:%M:%S"))
        channel = client.get_channel(991779150723547227)
        announcement = discord.Embed(
            title="Raffle tickets are available in the Rep Shop!"
        )
        announcement.add_field(name="Price", value="10 Reps")
        announcement.add_field(name="Prize", value=f"{prize}")
        announcement.add_field(name="Ends in", value=f"{duration} Hours")
        await channel.send(embed=announcement)
        logs = client.get_channel(993366573718962256)
        log = discord.Embed(title="Raffle set up")
        log.add_field(name=f"{interaction.user}", value="Set up raffle.", inline=False)
        log.add_field(name="prize: ", value=f"{prize}", inline=False)
        log.add_field(name="Duration: ", value=f"{duration}", inline=False)
        timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
        log.add_field(name="time", value=f"{timenow}", inline=False)
        await logs.send(embed=log)
        await interaction.response.edit_message(embed=embed, view=None)

    async def cancel_callback(interaction):
        embed = discord.Embed(title="❌ Cancelled")
        await interaction.response.edit_message(embed=embed, view=None)

    confirm.callback = confirm_callback
    cancel.callback = cancel_callback
    view = View(confirm, cancel)
    await ctx.respond(embed=embed, view=view, ephemeral=True)


@client.slash_command(
    guild_ids=[943173196490879009, 943841709106819092],
    description="End the raffle",
)
@default_permissions(manage_messages=True)
async def end_raffle(ctx, prize: discord.Option(str, description="Prize")):
    shop_items.remove(raffle_ticket)
    guild = client.get_guild(int(943173196490879009))
    ticketrole = guild.get_role(991763573737009172)
    channel = client.get_channel(991779150723547227)
    logs = client.get_channel(993366573718962256)
    log = discord.Embed(title="Raffle ended")
    log.add_field(name=f"{ctx.message.author}", value="Ended the raffle.", inline=False)
    log.add_field(name="prize: ", value=f"{prize}", inline=False)
    if len(ticketrole.members) < 1:
        embed = discord.Embed(title="No winner")
        await channel.send(embed=embed)
        log.add_field(name="Winner", value="None", inline=False)
        for member in ticketrole.members:
            member_obj = await guild.fetch_member(member.id)
            await member_obj.remove_roles(ticketrole)
    else:
        winner = random.choice(ticketrole.members)
        embed = discord.Embed(title=f"🏆 You won {prize} 🏆")
        await channel.send(winner.mention, embed=embed)
        log.add_field(name="Winner", value=f"{winner.name}", inline=False)
        for member in ticketrole.members:
            member_obj = await guild.fetch_member(member.id)
            await member_obj.remove_roles(ticketrole)
    timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
    log.add_field(name="time", value=f"{timenow}", inline=False)
    await logs.send(embed=log)
    raffle_timer.stop()


@tasks.loop(seconds=1)
async def raffle_timer(time, prize):
    if datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S") == f"{time}":
        shop_items.remove(raffle_ticket)
        guild = client.get_guild(int(943173196490879009))
        ticketrole = guild.get_role(991763573737009172)
        channel = client.get_channel(991779150723547227)
        logs = client.get_channel(993366573718962256)
        log = discord.Embed(title="Raffle ended")
        log.add_field(name="prize: ", value=f"{prize}", inline=False)
        if len(ticketrole.members) < 1:
            embed = discord.Embed(title="No winner")
            await channel.send(embed=embed)
            log.add_field(name="Winner", value="None", inline=False)
            for member in ticketrole.members:
                member_obj = await guild.fetch_member(member.id)
                await member_obj.remove_roles(ticketrole)
        else:
            winner = random.choice(ticketrole.members)
            embed = discord.Embed(title=f"🏆 You won {prize} 🏆")
            await channel.send(winner.mention, embed=embed)
            log.add_field(name="Winner", value=f"{winner.name}", inline=False)
            for member in ticketrole.members:
                member_obj = await guild.fetch_member(member.id)
                await member_obj.remove_roles(ticketrole)
            timenow = datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S")
            log.add_field(name="time", value=f"{timenow}", inline=False)
            await logs.send(embed=log)
        raffle_timer.stop()


client.run(TOKEN)
