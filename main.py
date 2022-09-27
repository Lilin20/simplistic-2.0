import asyncio
import discord
from discord.ext import commands, bridge, tasks
from discord.ext.pages import Paginator, Page
import os
import configparser
import scripts.database as db
import scripts.helper as helper

c_parser = configparser.ConfigParser()
c_parser.read(os.path.dirname(os.path.realpath(__file__))+"/config/config.ini")

# Information zum Bot
description = """ Simplistic 2.0 - Kranker Discord-Bot """
version = "2.0"
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
            try:
                db.database.add_user(member.id, member.name)
            except:
                pass
            print(f"{member.name} has been added to the database.")
    print("Done")
    ##################################################################

@tasks.loop(count=None)
async def keep_db_connection():
    db.database.cursor.execute("SELECT 1")
    asyncio.sleep(1800)

@bot.event
async def on_member_join(member):
    if not db.database.check_user(member.id):
        db.database.add_user(member.id, member.name)
        print(f"{member.name} has been added to the database.")
    embed = discord.Embed(title="Simplistic", description=" ", color=0x00ff00)
    embed.add_field(name="Willkommen", value="auf dem inoffiziellen Discord-Server der TBS1. Bitte wähle unten im Selector eine passende Rolle. Bitte wähle die Rolle die auch zu deiner Klasse passt. Falls du kein Schüler der TBS1 bist, dann nimm bitte die Rolle 'Gast'. Falls du ein Schüler der TBS1 bist, bitten wir dich die Rolle zu nehmen mit der richtigen Klassenbezeichnung. Viel spaß auf unserem Discord-Server!", inline=False)
    await member.send(embed=embed)
    await member.send("Simplistic - Role Selector", view=helper.RoleSelectorView())

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
            embed.set_thumbnail(url="https://opengameart.org/sites/default/files/gif_3.gif")
            await message.channel.send(embed=embed)

@bot.listen()
async def on_application_command(ctx):
    ach_values_list = [a_handler.EconomyWorkAchievementHandler(ctx.author), a_handler.EconomyMoneyAchievementHandler(ctx.author)]
    for ach_values in ach_values_list:
        if ach_values is not None:
            if ach_values[0]:
                embed = discord.Embed(title="Achievement freigeschaltet!", description=f"{ctx.author.mention} hat folgendes Achievement freigeschaltet:", color=0x00ff00, fields=[
                    discord.EmbedField(name=ach_values[1], value=ach_values[2], inline=False)
                ])
                embed.set_thumbnail(url="https://opengameart.org/sites/default/files/gif_3.gif")
                await ctx.send(embed=embed)

@bot.slash_command()
async def info(ctx):
    dev_user = await bot.fetch_user(232109327626797056)
    embed = discord.Embed(title="Simplistic 2.0", description=" ", color=0x00ff00)
    embed.add_field(name="Version", value=version, inline=False)
    embed.add_field(name="Entwickler", value="Lilin#1343", inline=False)
    if maintenance:
        embed.add_field(name="Status", value="Wartungsarbeiten", inline=False)
    else:
        embed.add_field(name="Status", value="Online", inline=False)
    embed.set_thumbnail(url=dev_user.avatar.url)
    await ctx.reply(embed=embed)

@bot.slash_command()
@commands.has_permissions(administrator=True)
async def change_status(ctx, status):
    await bot.change_presence(activity=discord.Game(name=status))



@bot.slash_command()
@commands.has_permissions(administrator=True)
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
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"Successfully reloaded the '{extension}' module!")

@bot.slash_command(help="Lädt ein Modul.")
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"Successfully loaded the '{extension}' module!")

if maintenance == False:
    for filename in os.listdir(os.path.dirname(os.path.realpath(__file__))+"/cogs"):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
else:
    print("Bot is in maintenance mode!")

bot.run(c_parser.get('Bot', 'token'))
