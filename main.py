from ast import Not
import discord
from discord.ext import commands, bridge
from discord.ext.pages import Paginator, Page
import os
import configparser
import scripts.database as db
import scripts.helper as helper

c_parser = configparser.ConfigParser()
c_parser.read(os.path.dirname(os.path.realpath(__file__))+"/config/config.ini")

# Information zum Bot
description = """ Simplistic 2.0 - Kranker Discord-Bot """
version = "0.1"
maintenance = False

# Intents
intents = discord.Intents.all()

# Object
bot = bridge.Bot(command_prefix="-", case_insensitive=True, description=description, intents=intents, activity=discord.Streaming(name="WIP", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

# Load Achievement Handler
a_handler = helper.AchievementHandler()
a_handler.init()

# Event - Startup
@bot.event
async def on_ready():
    print("""
         _______  _______  _______  _          _______     _______ 
        (  ____ \(       )(  ____ )( \        / ___   )   (  __   )
        | (    \/| () () || (    )|| (        \/   )  |   | (  )  |
        | (_____ | || || || (____)|| |            /   )   | | /   |
        (_____  )| |(_)| ||  _____)| |          _/   /    | (/ /) |
              ) || |   | || (      | |         /   _/     |   / | |
        /\____) || )   ( || )      | (____/\  (   (__/\ _ |  (__) |
        \_______)|/     \||/       (_______/  \_______/(_)(_______)
    """)

    guild = None
    for guilds in bot.guilds:
        guild = guilds
        helper.DefaultConfig.guild = guild
        helper.DefaultConfig.bot = bot

    # Check for new members ##########################################
    print("Checking for new users...")
    async for member in guild.fetch_members(limit=None):
        if not db.database.check_user(member.id):
            db.database.add_user(member.id, member.name)
            print(f"{member.name} has been added to the database.")
    print("Done")
    ##################################################################

@bot.event
async def on_member_join(member):
    if not db.database.check_user(member.id):
        db.database.add_user(member.id, member.name)
        print(f"{member.name} has been added to the database.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    db.database.add_message_count(message.author.id, 1)
    ach_values = a_handler.TextAchievementHandler(message.author)
    if ach_values is not None:
        if ach_values[0]:
            embed = discord.Embed(title="Achievement freigeschaltet!", description=f"{message.author.mention} hat folgendes Achievement freigeschaltet:", color=0x00ff00, fields=[
                discord.EmbedField(name=ach_values[1], value=ach_values[2], inline=False)
            ])
            await message.channel.send(embed=embed)

@bot.listen()
async def on_application_command(ctx):
    ach_values_list = [a_handler.EconomyWorkAchievementHandler(ctx.author), a_handler.EconomyMoneyAchievementHandler(ctx.author)]
    for ach_values in ach_values_list:
        if ach_values is not None:
            print(ach_values)
            if ach_values[0]:
                embed = discord.Embed(title="Achievement freigeschaltet!", description=f"{ctx.author.mention} hat folgendes Achievement freigeschaltet:", color=0x00ff00, fields=[
                    discord.EmbedField(name=ach_values[1], value=ach_values[2], inline=False)
                ])
                await ctx.send(embed=embed)

@bot.slash_command()
async def test_msg(ctx):
    embed = discord.Embed(title="Simplistic", description=" ", color=0x00ff00)
    embed.add_field(name="Willkommen", value="auf dem inoffiziellen Discord-Server der TBS1. Bitte wähle unten im Selector eine passende Rolle. Bitte wähle die Rolle die auch zu deiner Klasse passt. Falls du kein Schüler der TBS1 bist, dann nimm bitte die Rolle 'Gast'. Falls du ein Schüler der TBS1 bist, bitten wir dich die Rolle zu nehmen mit der richtigen Klassenbezeichnung. Viel spaß auf unserem Discord-Server!", inline=False)
    await ctx.author.send(embed=embed)
    await ctx.author.send("Simplistic - Role Selector", view=helper.RoleSelectorView())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embedVar = discord.Embed(title="404 - Befehl nicht gefunden.", description=f'**{ctx.message.content}**', color=0xff1c1c)
        await ctx.send(embed=embedVar)

@bot.slash_command(help="Lädt ein Modul neu.")
async def reload(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"Successfully reloaded the '{extension}' module!")

@bot.slash_command(help="Lädt ein Modul.")
async def load(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"Successfully loaded the '{extension}' module!")

for filename in os.listdir(os.path.dirname(os.path.realpath(__file__))+"/cogs"):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#@bot.event
#async def on_member_join(member):
#    db.database.execute(f'SELECT d_id FROM userdata WHERE d_id = "{member.id}"')
#    result = db.database.fetchall()
#    joined = member.joined_at.strftime("%d.%m.%Y")
#    if not result:
#        db.database.execute(f'INSERT INTO userdata (d_id, lvl, warns, msg, join_date, xp, growth) VALUES ({member.id}, 0, 0, 0, "{joined}", 0, 0.25)')
#        db.database.execute(f'INSERT INTO economy (d_id) VALUES ({member.id})')

bot.run(c_parser.get('Bot', 'token'))