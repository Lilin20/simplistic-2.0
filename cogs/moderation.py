import discord
import sys
from discord.ext import commands, bridge
import os

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db

class Moderation(commands.Cog):
    """Modul für die Moderationfunktionen"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation module loaded.")

    @commands.slash_command()
    async def purge(self, ctx, amount: int):
        """Löscht die angegebene Anzahl an Nachrichten"""
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"{amount} Nachrichten wurden gelöscht.", delete_after=5)

def setup(bot):
    bot.add_cog(Moderation(bot))
