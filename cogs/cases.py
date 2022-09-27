import discord
import sys
from discord.ext import commands, bridge
import os
import random

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db
import helper

class Cases(commands.Cog):
    """Modul für die Casesfunktionen"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cases module loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if random.choices([True, False], weights=[5, 95])[0]:
            embed = discord.Embed(title="Simplistic - Cases", description=f"{message.author.name} hat eine Kiste gedroppt bekommen!", color=0x00ff00)
            db.database.add_case(message.author.id)
            await message.channel.send(embed=embed, delete_after=5)

    cases_group = discord.SlashCommandGroup("case", "Cases-Befehle")
    @cases_group.command()
    async def open(self, ctx):
        if db.database.get_case_amount(ctx.author.id) <= 0:
            await ctx.reply("Du hast keine Kiste zum öffnen...")
            return
        else:
            if db.database.get_key_amount(ctx.author.id) <= 0:
                await ctx.reply("Du hast keine Schlüssel um eine Kiste zu öffnen...")
                return
            rarity = random.choices(["Common", "Uncommon", "Rare", "Epic", "Mythical", "Legendary"], weights=[60, 25, 10, 3, 1.5, 0.5])[0]
            items = db.database.get_items_by_rarity(rarity.lower())
            item = random.choice(items)
            #db.database.remove_case(ctx.author.id)
            db.database.add_case_item(ctx.author.id, item[0])
            embed = discord.Embed(title="Simplistic - Cases", description=f"{ctx.author.name} hat eine Kiste geöffnet!", color=0x00ff00, fields=[
                discord.EmbedField(name="Item", value=item[1], inline=True),
                discord.EmbedField(name="Rarity", value=rarity, inline=True)
            ])
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Cases(bot))
