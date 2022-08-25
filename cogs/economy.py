import discord
import sys
from discord.ext import commands
import os
import random
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
        self.message = None
        self.vote_channel = None
        self.time = None

    def leadingZero(self, time: str):
        if len(time) > 1:
            return time

        return "0" + time

    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy module loaded.")

    @commands.command(help="Gibt dir die Möglichkeit einen User auszurauben.")
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member):
        if member.id == ctx.message.author.id:
            await ctx.send("Du kannst dich nicht selbst ausrauben.")
            return

        if member.id == self.bot.user.id:
            await ctx.send("Der Bot ist pleite versuchs erst gar nicht!")
            return

        db.database.execute(f'SELECT * FROM economy WHERE d_id = {member.id}')
        result = db.database.fetchall()
        money = result[0][2]
        if money <= 0:
            await ctx.send("Ausgewählter User hat zu wenig Geld.")
            return

        db.database.execute(f'SELECT * FROM economy WHERE d_id = {ctx.author.id}')
        result = db.database.fetchall()
        money_robber = result[0][2]

        # Embed wich shows the progress of robbing someone
        embed = discord.Embed(title="Simplistic - Economy", color=discord.Colour.green())
        embed.add_field(name="Ausrauben", value="Du versuchst " + member.name + " ausfindig zu machen...", inline=True)
        embed_saved = await ctx.send(embed=embed)

        # After a random amount of time, the user is robbed
        await asyncio.sleep(6)
        embed = discord.Embed(title="Simplistic - Economy", color=discord.Colour.green())
        embed.add_field(name="Ausrauben", value="Du näherst dich dein Opfer...", inline=True)
        await embed_saved.edit(embed=embed)

        await asyncio.sleep(random.randrange(5, 10))
        embed = discord.Embed(title="Simplistic - Economy", color=discord.Colour.green())
        embed.add_field(name="Ausrauben", value="Du versuchst dein Opfer zu beklauen...", inline=True)
        await embed_saved.edit(embed=embed)
        
        await asyncio.sleep(random.randrange(5, 10))

        chance = random.randrange(1, 100)
        if chance <= 10:
            money = (money / 100) * 10
            db.database.execute(f'UPDATE economy SET money = money - {money} WHERE d_id = {member.id}')
            db.database.execute(f'UPDATE economy SET got_robbed = robbed_success + 1 WHERE d_id = {member.id}')
            db.database.execute(f'UPDATE economy SET robbed_success = robbed_success + 1 WHERE d_id = {ctx.author.id}')
            db.database.execute(f'UPDATE economy SET money = money + {money} WHERE d_id = {ctx.message.author.id}')

            embed_second = discord.Embed(title="Simplistic - Economy", color=discord.Colour.green())
            embed_second.add_field(name="Geschafft!", value="Du konntest erfolgreich dein Opfer beklauen!", inline=False)
            embed_second.add_field(name="Räuber", value=ctx.message.author.mention, inline=True)
            embed_second.add_field(name="Opfer", value=member.mention, inline=True)
            embed_second.add_field(name="Erbeuteter Betrag", value=int(money), inline=True)
            await embed_saved.edit(embed=embed_second)

        elif chance == 1 and money_robber > 0:
            money_robber = (money_robber / 100) * 5

            embed_second = discord.Embed(title="Simplistic - Economy", color=discord.Colour.red())
            embed_second.add_field(name="Verdammt!", value="Die Polizei hat gesehen wie du versucht hast jemanden zu beklauen... Du musstest 5% von deinem Vermögen an die Polizei abdrücken...", inline=False)
            embed_second.add_field(name="Zu zahlender Betrag", value=int(money_robber), inline=True)
            await embed_saved.edit(embed=embed_second)
            db.database.execute(f'UPDATE economy SET money = money - {money_robber} WHERE d_id = {ctx.author.id}')

        else:
            embed_second = discord.Embed(title="Simplistic - Economy", color=discord.Colour.red())
            embed_second.add_field(name="Verdammt...", value="Dein Ziel hat den Raubversuch bemerkt und ist entkommen...", inline=False)
            await embed_saved.edit(embed=embed_second)

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Cooldown", color=discord.Color.red())

            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)

            embed.add_field(name="Achtung", value=f"Deine kriminelle Energie ist zu schwach für den nächsten Raubzug.\nMach erstmal eine Pause:\n \n {self.leadingZero(minutes)}:{self.leadingZero(seconds)}.")
            await ctx.send(embed=embed)

    def leadingZero(self, time: str):
        if len(time) > 1:
            return time

        return "0" + time


    @commands.command(help="Gibt dir einen Daily-Reward.")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        db.database.execute(f'UPDATE economy SET money = money + 150 WHERE d_id = {ctx.message.author.id}')
        embedVar = discord.Embed(title='Simplistic - Economy', description='Daily Reward abgeholt!', color=discord.Colour.green())
        embedVar.add_field(name='Erhaltenes Geld', value=150, inline=True)
        await ctx.send(embed=embedVar)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Cooldown", color=discord.Color.red())

            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)

            embed.add_field(name="Achtung",
                            value=f"Du hast bereits deine tägliche Summe an Geld abgeholt.\nBitte warte:\n \n {self.leadingZero(minutes)}:{self.leadingZero(seconds)}")
            await ctx.send(embed=embed)

    @commands.command(help="Gibt dir Geld für gearbeitete Stunden.")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def work(self, ctx):
        calculated_money = random.randrange(10, 150, 10)
        worked_hours = int(calculated_money / 10)
        db.database.execute(f'UPDATE economy SET worked_hours = worked_hours + {worked_hours} WHERE d_id = {ctx.message.author.id}')
        db.database.execute(f'UPDATE economy SET money = money + {calculated_money} WHERE d_id = {ctx.message.author.id}')
        embedVar = discord.Embed(title='Simplistic - Economy', description='Deine Arbeit wird entlohnt!', color=discord.Colour.green())
        embedVar.add_field(name='Erhaltenes Geld', value=calculated_money, inline=True)
        embedVar.add_field(name="Gearbeitete Stunden", value=worked_hours, inline=True)
        await ctx.send(embed=embedVar)
        

    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title="Cooldown", color=discord.Color.red())

            cd = round(error.retry_after)
            minutes = str(cd // 60)
            seconds = str(cd % 60)

            embed.add_field(name="Achtung",
                            value=f"Du brauchst erstmal eine Pause. Die Arbeit war anstrengend.\nMach erstmal eine Pause:\n \n {self.leadingZero(minutes)}:{self.leadingZero(seconds)}")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))