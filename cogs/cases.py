import discord
import sys
from discord.ext import commands, bridge
import os

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db

class Cases(commands.Cog):
    """Modul für die Casesfunktionen"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cases module loaded.")

def setup(bot):
    bot.add_cog(Cases(bot))
