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

class Casino(commands.Cog):
    """Modul für die Casinofunktionen"""
    def __init__(self, bot):
        self.bot = bot
        self.max_bet = 250
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Casino module loaded.") 

    @commands.slash_command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def hol(self, ctx, amount: int):
        user_balance = db.database.get_balance(ctx.author.id)
        if amount > self.max_bet:
            await ctx.reply(f"{ctx.author.name}, du kannst nicht mehr als 500 SMPL-Coins setzen!")
            return
        if amount <= 0:
            await ctx.reply(f"{ctx.author.name}, du kannst nicht weniger als 1 SMPL-Coin setzen!")
            return
        if user_balance < amount:
            await ctx.reply(f"{ctx.author.name}, du hast nicht genug SMPL-Coins!")
            return
        
        bot_number = random.randint(1, 50)
        player_number = random.randint(1, 50)

        while bot_number == player_number:
            bot_number = random.randint(1, 50)
        
        embed = discord.Embed(title="Simplistic - Casino", description=f"{ctx.author.name} hat eine Runde HoL gestartet!", color=0x00ff00, fields=[
            discord.EmbedField(name="Deine Zahl", value=player_number, inline=True)])
        await ctx.reply(embed=embed)

        while True:
            try:
                message = await self.bot.wait_for('message', timeout=30.0)
            except:
                await ctx.reply("Zeit abgelaufen!")
                return
            
            if message.author == ctx.author:
                if message.content == "higher" or message.content == "Higher":
                    if player_number > bot_number:
                        print("test")
                        embed = discord.Embed(title="Simplistic - Casino", description=f"{ctx.author.name} hat die Runde HoL verloren!", color=0x00ff00, fields=[
                            discord.EmbedField(name="Deine Zahl", value=player_number, inline=True),
                            discord.EmbedField(name="Bot Zahl", value=bot_number, inline=True)])
                        embed.set_thumbnail(url="https://preview.redd.it/6k4sujr5u7m81.jpg?auto=webp&s=c2af0d2ee9f8dfa3cc3af90d24927f3f4bfdb16a")
                        await ctx.send(embed=embed)
                        db.database.add_balance(ctx.author.id, -amount)
                        return
                    else:
                        embed = discord.Embed(title="Simplistic - Casino", description=f"{ctx.author.name} hat die Runde HoL gewonnen!", color=0x00ff00, fields=[
                            discord.EmbedField(name="Deine Zahl", value=player_number, inline=True),
                            discord.EmbedField(name="Bot Zahl", value=bot_number, inline=True),
                            discord.EmbedField(name="Gewinn", value=amount, inline=True)])
                        embed.set_thumbnail(url="https://i.ytimg.com/vi/if-2M3K1tqk/maxresdefault.jpg")
                        await ctx.send(embed=embed)
                        db.database.add_balance(ctx.author.id, amount)
                        return

                elif message.content == "lower" or message.content == "Lower":
                    if player_number < bot_number:
                        embed = discord.Embed(title="Simplistic - Casino", description=f"{ctx.author.name} hat die Runde HoL verloren!", color=0x00ff00, fields=[
                            discord.EmbedField(name="Deine Zahl", value=player_number, inline=True),
                            discord.EmbedField(name="Bot Zahl", value=bot_number, inline=True)])
                        embed.set_thumbnail(url="https://preview.redd.it/6k4sujr5u7m81.jpg?auto=webp&s=c2af0d2ee9f8dfa3cc3af90d24927f3f4bfdb16a")
                        await ctx.send(embed=embed)
                        db.database.add_balance(ctx.author.id, -amount)
                        return
                    else:
                        embed = discord.Embed(title="Simplistic - Casino", description=f"{ctx.author.name} hat die Runde HoL gewonnen!", color=0x00ff00, fields=[
                            discord.EmbedField(name="Deine Zahl", value=player_number, inline=True),
                            discord.EmbedField(name="Bot Zahl", value=bot_number, inline=True),
                            discord.EmbedField(name="Gewinn", value=amount, inline=True)])
                        embed.set_thumbnail(url="https://i.ytimg.com/vi/if-2M3K1tqk/maxresdefault.jpg")
                        await ctx.send(embed=embed)
                        db.database.add_balance(ctx.author.id, amount)
                        return

    @hol.error
    async def hol_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("Versuch es erneut in <t:{}:R>".format(int(time.time() + error.retry_after)), ephemeral=True)
        else:
            raise error

    @commands.slash_command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def tower(self, ctx, amount: int):
        multiplier = 1
        etage = 1
        user_balance = db.database.get_balance(ctx.author.id)
        if amount > self.max_bet:
            await ctx.reply(f"{ctx.author.name}, du kannst nicht mehr als 500 SMPL-Coins setzen!")
            return
        if amount <= 0:
            await ctx.reply(f"{ctx.author.name}, du kannst nicht weniger als 1 SMPL-Coin setzen!")
            return
        if user_balance < amount:
            await ctx.reply(f"{ctx.author.name}, du hast nicht genug SMPL-Coins!")
            return

        embed = discord.Embed(title="Simplistic - Casino", description=f"{ctx.author.name} hat eine Runde Tower gestartet!", color=0x00ff00, fields=[
            discord.EmbedField(name="Tower of God", value="Der Turm startet bei Etage 1!", inline=True)])
        embed.set_thumbnail(url="https://www.freeiconspng.com/uploads/tower-icon-24.png")
        await ctx.reply(embed=embed)

        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=30.0)
            except:
                await ctx.reply("Zeit abgelaufen!")
                return

            if msg.author == ctx.author:
                if msg.content == "stop" or msg.content == "Stop":
                    winnings = int(amount * multiplier)
                    embed = discord.Embed(title="Simplistic - Tower of God", description=f"{ctx.author.name} hat den Turm abgebrochen!", color=0x00ff00, fields=[
                        discord.EmbedField(name="Etage", value=f"{str(etage)}", inline=True),
                        discord.EmbedField(name="Multiplikator", value=str(multiplier), inline=False),
                        discord.EmbedField(name="Gewinn", value=winnings, inline=False)])
                    embed.set_thumbnail(url="https://www.freeiconspng.com/uploads/tower-icon-24.png")
                    await ctx.respond(embed=embed)
                    db.database.add_balance(ctx.author.id, amount * multiplier)
                    return
                elif msg.content == "weiter" or msg.content == "Weiter":
                    choice = random.choices([True, False], weights=[0.7, 0.3])[0]
                    if choice:
                        etage += 1
                        multiplier += .25
                        embed = discord.Embed(title="Simplistic - Tower of God", description=f"{ctx.author.name} hat sich gewagt eine Etage höher zu gehen!\nGehst du weiter oder nicht?", color=0x00ff00, fields=[
                            discord.EmbedField(name="Etage", value=f"{str(etage)}", inline=True)])
                        embed.set_thumbnail(url="https://www.freeiconspng.com/uploads/tower-icon-24.png")
                        await ctx.respond(embed=embed)
                    else:
                        embed = discord.Embed(title="Simplistic - Tower of God", description=f"{ctx.author.name} ist mit dem Turm begraben worden!", color=0x00ff00, fields=[
                            discord.EmbedField(name="Etage", value=f"{str(etage)}", inline=True),
                            discord.EmbedField(name="Eigentlicher Multiplikator", value=str(multiplier), inline=False),
                            discord.EmbedField(name="Resultat", value="Du hast alles verloren!", inline=False)])
                        embed.set_thumbnail(url="https://www.freeiconspng.com/uploads/tower-icon-24.png")
                        await ctx.respond(embed=embed)
                        db.database.add_balance(ctx.author.id, -amount)
                        return

def setup(bot):
    bot.add_cog(Casino(bot))
