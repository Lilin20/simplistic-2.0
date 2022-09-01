import discord
import sys
from discord.ext import commands
import os
import random
import time

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db

class Economy(commands.Cog):
    """Modul für die Economyfunktionen"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy module loaded.")

    @commands.slash_command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        hours = random.randint(1, 8) 
        money = (100 * hours)
        tax = (db.database.get_server_var("steuer") / 100) * money
        money = money - tax
        embed = discord.Embed(title="Simplistic - Lohnabrechnung", description=f"Du hast Geld erhalten!", fields=[
            discord.EmbedField(name="Gehalt", value=f"{money}", inline=True),
            discord.EmbedField(name="Steuern", value=f"{tax}", inline=True),
            discord.EmbedField(name="Arbeitsstunden", value=f"{hours}", inline=False)
            ])
        embed.set_thumbnail(url="https://www.iconpacks.net/icons/1/free-coin-icon-794-thumb.png")
        embed.set_footer(text="Du kannst in einer Stunde wieder arbeiten.\nDie Steuern werden für Events verwendet.")
        db.database.add_server_money("server_money", tax)
        db.database.add_balance(ctx.author.id, money)
        await ctx.send(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        # cooldown anzeigen mit stunden und minuten und sekunden
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("Versuch es erneut in <t:{}:R>".format(int(time.time() + error.retry_after)), ephemeral=True)
        else:
            raise error

    


def setup(bot):
    bot.add_cog(Economy(bot))
