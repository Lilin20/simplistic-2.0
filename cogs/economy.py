from ast import main
import discord
import sys
from discord.ext import commands
import os
import random
import time
import asyncio

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db
import helper

class Economy(commands.Cog):
    """Modul für die Economyfunktionen"""
    def __init__(self, bot):
        self.bot = bot
        self.a_handler = helper.AchievementHandler()
        self.a_handler.init()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy module loaded.")

    @commands.slash_command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        hours = random.randint(1, 8) 
        money = (50 * hours)
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
        db.database.add_worked(ctx.author.id)
        db.database.add_worked_hours(ctx.author.id, hours)
        # WORKED_HOURS NOCH HOCH ZÄHLEN
        await ctx.reply(embed=embed)

    @work.error
    async def work_error(self, ctx, error):
        # cooldown anzeigen mit stunden und minuten und sekunden
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("Versuch es erneut in <t:{}:R>".format(int(time.time() + error.retry_after)), ephemeral=True)
        else:
            raise error

    @commands.slash_command()
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member):
        if member == self.bot.user:
            await ctx.respond("Naaaaaaaa HÖR MAL! Noch son Ding Augenring.", ephemeral=True)
            return
        if member == ctx.author:
            await ctx.respond("Du kannst dich nicht selber ausrauben.", ephemeral=True)
            return
        if db.database.get_balance(member.id) < 100:
            await ctx.respond("Dein gewähltes Opfer hat nicht mal Geld um sich was zum Essen zu holen... Such dir jemand anderes.", ephemeral=True)
            return
        if db.database.get_balance(ctx.author.id) < 100:
            await ctx.respond("Du hast kein Geld um dir eine Ski-Maske zu leisten... Geh ein bisschen arbeiten...", ephemeral=True)
            return

        embed = discord.Embed(title="Simplistic - Diebstahl", color=discord.Colour.orange(), fields=[
            discord.EmbedField(name="Ausrauben", value=f"Du versuchst {member.name} ausfindig zu machen...", inline=True)
        ])
        saved_embed = await ctx.reply(embed=embed)
        await asyncio.sleep(3)
        await saved_embed.edit_original_message(embed=discord.Embed(title="Simplistic - Diebstahl", color=discord.Colour.orange(), fields=[
            discord.EmbedField(name="Ausrauben", value=f"Du planst deinen Raub...", inline=True)
        ]))
        await asyncio.sleep(random.randrange(3, 6))
        await saved_embed.edit_original_message(embed=discord.Embed(title="Simplistic - Diebstahl", color=discord.Colour.orange(), fields=[
            discord.EmbedField(name="Ausrauben", value=f"Du versuchst {member.name} auszurauben...", inline=True)
        ]))

        choice = random.choices([True, False], weights=[0.99, 0.01])[0]
        if choice:
            await asyncio.sleep(random.randrange(3, 6))
            await saved_embed.edit_original_message(embed=discord.Embed(title="Simplistic - Diebstahl", color=discord.Colour.green(), fields=[
                discord.EmbedField(name="Ausrauben", value=f"Du hast {member.mention} erfolgreich ausgeraubt!", inline=True)
            ]))
            robbed_money = int(db.database.get_balance(member.id) * 0.1)
            db.database.add_balance(ctx.author.id, robbed_money)
            db.database.add_has_robbed(ctx.author.id)
            db.database.add_rob_spree(ctx.author.id)
            ach_values_list = [self.a_handler.EconomyRobAchievementHandler(ctx.author), self.a_handler.EconomyRobSpreeAchievementHandler(ctx.author)]
            print(ach_values_list)
            for ach_values in ach_values_list:
                if ach_values is not None:
                    print(ach_values)
                    if ach_values[0]:
                        embed = discord.Embed(title="Achievement freigeschaltet!", description=f"{ctx.author.mention} hat folgendes Achievement freigeschaltet:", color=0x00ff00, fields=[
                            discord.EmbedField(name=ach_values[1], value=ach_values[2], inline=False)
                        ])
                        await ctx.send(embed=embed)

            db.database.add_balance(member.id, -robbed_money)
        else:
            if (random.choices([True, False], weights=[0.1, 0.9])[0]):
                await asyncio.sleep(random.randrange(3, 6))
                await saved_embed.edit_original_message(embed=discord.Embed(title="Simplistic - Diebstahl", color=discord.Colour.red(), fields=[
                    discord.EmbedField(name="Ausrauben", value=f"{member.mention} ist entkommen!", inline=True)
                ]))
                db.database.reset_rob_spree(ctx.author.id)
            else:
                penalty = int(db.database.get_balance(ctx.author.id) * 0.05)
                await asyncio.sleep(random.randrange(3, 6))
                await saved_embed.edit_original_message(embed=discord.Embed(title="Simplistic - Diebstahl", color=discord.Colour.red(), fields=[
                    discord.EmbedField(name="Ausrauben", value=f"Die Polizei hat deinen Raubversuch mitbekommen.\nDie freundlichen Beamten erleichtern dich um 5% deines Vermögens!", inline=True),
                    discord.EmbedField(name="Strafe", value=f"{penalty}", inline=False)
                ]).set_thumbnail(url="https://purepng.com/public/uploads/large/purepng.com-jail-prisonprisonjailgaoldetention-center-14215265523662mbuy.png"))
                db.database.add_server_money("server_money", penalty)
                db.database.add_balance(ctx.author.id, -penalty)
                db.database.reset_rob_spree(ctx.author.id)

    @rob.error
    async def rob_error(self, ctx, error):
        # cooldown anzeigen mit stunden und minuten und sekunden
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("Versuch es erneut in <t:{}:R>".format(int(time.time() + error.retry_after)), ephemeral=True)
        else:
            raise error
    


def setup(bot):
    bot.add_cog(Economy(bot))
