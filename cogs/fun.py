import discord
import sys
from discord.ext import commands, bridge
import os
import configparser

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
        c_parser.set("ChannelConfig", "countingChannel_ID", str(channel.id))
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.ini'), 'w') as configfile:
            c_parser.write(configfile)
        c_parser.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.ini'))
        await channel.send("Dieser Channel wird nun zum Zählen genutzt. Der Zähler wurde auf 0 zurückgesetzt.")
        db.database.reset_counter()

def setup(bot):
    bot.add_cog(Fun(bot))
