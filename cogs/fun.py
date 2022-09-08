import re
import discord
import sys
from discord.ext import commands, bridge
import os
import configparser
import random
import asyncio
import time

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db

c_parser = configparser.ConfigParser()
c_parser.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.ini'))

class Fun(commands.Cog):
    """Modul für die Funfunktionen"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun module loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # counting
        if message.channel.id == int(c_parser.get('ChannelConfig', 'countingChannel_ID')):
            if message.author.id == self.bot.user.id:
                return
            # Check if message is only a number
            if message.content.isdigit():
                # Check if message is the next number
                if int(message.content) == db.database.get_server_var('counting') + 1:
                    #Add reaction to message
                    await message.add_reaction('✅')
                    db.database.add_counter()
                    return
                else:
                    if db.database.get_server_var('counting_record') < db.database.get_server_var('counting'):
                        db.database.set_counting_record(db.database.get_server_var('counting'))

                    embed = discord.Embed(title="Simplisitc - Counting", description=f"{message.author.mention} hat verkackt! Fangt von vorne an! Zähler zurückgesetzt auf 0.", color=0xff0000, fields=[
                        discord.EmbedField(name="Rekord", value=db.database.get_server_var('counting_record'), inline=False),
                    ])
                    await message.channel.send(embed=embed)

                    await message.delete()
                    db.database.reset_counter()

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def counting_channel(self, ctx, channel: discord.TextChannel):
        """Setzt den Counting Channel"""
        c_parser.set("ChannelConfig", "countingChannel_ID", str(channel.id))
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.ini'), 'w') as configfile:
            c_parser.write(configfile)
        c_parser.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.ini'))
        await channel.send("Dieser Channel wird nun zum Zählen genutzt. Der Zähler wurde auf 0 zurückgesetzt.")
        db.database.reset_counter()

    @commands.slash_command()
    async def dice(self, ctx):
        """Wirft einen Würfel"""
        await ctx.send(f"Du hast eine {random.randint(1, 6)} gewürfelt.")

    @commands.slash_command()
    async def eightball(self, ctx, question):
        """Stellt eine Frage an den 8ball"""
        embed = discord.Embed(title="Simplistic - 8ball", description=f"Frage: {question}", color=0x00ff00, fields=[
            discord.EmbedField(name="Antwort", value=random.choice(["Ja", "Nein", "Vielleicht", "Ich weiß es nicht"]), inline=False),
        ])
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def vote(self, ctx, *, question):
        """Erstellt eine Umfrage"""
        embed = discord.Embed(title="Simplistic - Vote", description=f"{question}", color=0x00ff00)
        message = await ctx.reply(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❌')

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, *, time_limit: int, what, desc, from_who: discord.Member):
        """Startet ein Giveaway"""
        embed = discord.Embed(title="Simplistic - Giveaway", description=f"Giveaway von {from_who.mention}", color=0x00ff00, fields=[
            discord.EmbedField(name=what, value=desc, inline=False),
            discord.EmbedField(name="Dauer", value="<t:{}:R>".format(int(time.time() + time_limit)))
            ])
        message = await ctx.respond(embed=embed)
        await message.add_reaction('🎉')

        await asyncio.sleep(int(time_limit))
        # Fetch message
        message = await ctx.fetch_message(message.id)
        reactions = message.reactions
        users = await reactions[0].users().flatten()
        print(users)
        users.pop(users.index(self.bot.user))
        winner = random.choice(users)
        embed = discord.Embed(title="Simplistic - Giveaway", description=f"{desc}", color=0x00ff00, fields=[
            discord.EmbedField(name="Gewinner", value=f"{winner.mention}", inline=False),
        ])
        embed.set_thumbnail(url="https://cdn.edu.buncee.com/assets/ff9d3f82f68e785d6695db3704879d8d/animation-birthdays070517-01.gif?timestamp=1512494314")
        await message.edit(embed=embed)

    leaderboard_group = discord.SlashCommandGroup("leaderboard", "Zeigt die Leaderboards an")

    @leaderboard_group.command()
    async def level(self, ctx):
        """Zeigt das Level Leaderboard an"""
        embed = discord.Embed(title="Simplistic - Leaderboard", description="Level Leaderboard", color=0x00ff00)
        for id, user in enumerate(db.database.get_leaderboard_level()):
            embed.add_field(name=f'{id+1} - {user[0]}', value=f'Aktuelles Level: **{user[1]}**', inline=False)
        await ctx.send(embed=embed)

    @leaderboard_group.command()
    async def money(self, ctx):
        """Zeigt das Geld Leaderboard an"""
        embed = discord.Embed(title="Simplistic - Leaderboard", description="Geld Leaderboard", color=0x00ff00)
        for id, user in enumerate(db.database.get_leaderboard_money()):
            embed.add_field(name=f'{id+1} - {user[0]}', value=f'Aktuelles Vermögen: **{user[1]}**', inline=False)
        await ctx.send(embed=embed)

    @leaderboard_group.command()
    async def rob(self, ctx):
        """Zeigt das Räuber Leaderboard an"""
        embed = discord.Embed(title="Simplistic - Leaderboard", description="Räuber Leaderboard", color=0x00ff00)
        for id, user in enumerate(db.database.get_leaderboard_rob()):
            embed.add_field(name=f'{id+1} - {user[0]}', value=f'Erfolgreiche Raubzüge: **{user[1]}**', inline=False)
        await ctx.send(embed=embed)

    @leaderboard_group.command()
    async def work(self, ctx):
        """Zeigt das Arbeitsstunden Leaderboard an"""
        embed = discord.Embed(title="Simplistic - Leaderboard", description="Arbeitsstunden Leaderboard", color=0x00ff00)
        for id, user in enumerate(db.database.get_leaderboard_worked_hours()):
            embed.add_field(name=f'{id+1} - {user[0]}', value=f'Arbeitsstunden: **{user[1]}**', inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
