import discord
import sys
from discord.ext import commands
import os
from PIL import Image, ImageChops, ImageDraw, ImageFont
from io import BytesIO

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db

def circle(pfp, size = (200,200)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert('RGBA')
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

class Profile(commands.Cog):
    """Modul für die Profilfunktionen"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Profile module loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('.'):
            return
        if message.author == self.bot.user:
            return
        if message.content.startswith("https") or message.content.startswith("http"):
            return
        else:
            xp_to_give = len(message.content) - message.content.count(" ")
            db.database.execute(f'UPDATE userdata SET xp = xp + {xp_to_give} WHERE d_id = {message.author.id}')
            db.database.execute(f'SELECT * FROM userdata WHERE d_id = {message.author.id}')
            result = db.database.fetchall()
            try:
              fetched_xp, fetched_growth, fetched_level = result[0][5], result[0][6], result[0][1]
            except IndexError:
              print(result)
              print("Unknown Error")
            calculate_xp = 50 * (1+fetched_growth) ** int(fetched_level)
            if fetched_xp >= calculate_xp:
                db.database.execute(f'UPDATE userdata SET lvl = lvl + 1 WHERE d_id = {message.author.id}')
                db.database.execute(f'UPDATE userdata SET xp = 0 WHERE d_id = {message.author.id}')
                db.database.execute(f'UPDATE userdata SET growth = growth + 0.025 WHERE d_id = {message.author.id}')
                embedVar = discord.Embed(title="Level Up!", description=f'{message.author.name} hat ein neues Level erreicht!', color=0x0000CD)
                embedVar.set_thumbnail(url="https://i.redd.it/5ej93xbz1jo51.gif")
                embedVar.set_author(name=message.author, url=" ",icon_url=message.author.avatar_url)
                await message.channel.send(embed=embedVar, delete_after=5)

    @commands.command(help="Zeigt das eigene Profil oder das eines anderen Users an.")
    async def profile(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        db.database.cursor.execute(f'SELECT * FROM userdata WHERE d_id = {user.id}')
        result_userdata = db.database.fetchall()

        db.database.cursor.execute(f"SELECT * FROM economy WHERE d_id = %s;", (user.id,))
        result_economy = db.database.cursor.fetchall()

        #Get latest achievement from user_achievements
        db.database.cursor.execute(f"SELECT * FROM user_achievements WHERE d_id = %s ORDER BY achievement_id DESC LIMIT 1;", (user.id,))
        result_achievements = db.database.cursor.fetchall()

        #Get achievement from achievements using result_achievement[0][1]
        db.database.cursor.execute(f"SELECT * FROM achievements WHERE id = %s;", (result_achievements[0][1],))
        result_achievement = db.database.cursor.fetchall()

        base = Image.open("profile.png").convert("RGBA")
        
        pfp = user.avatar_url
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert("RGBA")

        name = user.display_name
        if len(name) >= 11:
            name = f"{name[:11]}..."

        draw = ImageDraw.Draw(base)
        pfp = circle(pfp, (200,200))
        font = ImageFont.truetype("04B_30__.ttf", 38)
        akafont = ImageFont.truetype("04B_30__.ttf", 30)

        draw.text((275, 185), name, font=font, fill=(0, 0, 0, 255))

        #Message Text
        draw.text((180, 455), f"{result_userdata[0][3]}", font=akafont, fill=(230, 229, 227, 255), anchor="mm")

        #Level Text
        draw.text((535, 455), f"{result_userdata[0][1]}", font=akafont, fill=(230, 229, 227, 255), anchor="mm")

        #Money Text
        draw.text((180, 605), f"{result_economy[0][2]}", font=akafont, fill=(230, 229, 227, 255), anchor="mm")

        #Got Robbed Text
        draw.text((535, 605), f"{result_economy[0][6]}", font=akafont, fill=(230, 229, 227, 255), anchor="mm")

        #Has Robbed Text
        draw.text((180, 755), f"{result_economy[0][3]}", font=akafont, fill=(230, 229, 227, 255), anchor="mm")

        #Worked Text
        draw.text((535, 755), f"{result_economy[0][5]}", font=akafont, fill=(230, 229, 227, 255), anchor="mm")

        #Latest Achievement Text
        draw.text((360, 900), f"{result_achievement[0][1]}", font=akafont, fill=(230, 229, 227, 255), anchor="mm")

        #Status Text
        draw.text((485, 280), f"{result_userdata[0][7]}", font=akafont, fill=(0, 0, 0, 255), anchor="mm")


        base.paste(pfp, (63, 102), pfp)

        with BytesIO() as a:
            base.save(a, "PNG")
            a.seek(0)
            await ctx.send(file=discord.File(a, "profile_test.png"))


        

    @commands.command(help="Setzt einen beliebigen Status für dein Profil.")
    async def set_status(self, ctx, *args):
        string = ""
        user_id = ctx.author.id

        if len(args) > 0:
            for word in args:
                string += word+" "

        if len(string) >= 17:
            await ctx.send("Dein Status darf nicht länger als 15 Zeichen sein.")
            return

        db.database.execute(f'UPDATE userdata SET description = "{string}" WHERE d_id = "{user_id}"')


def setup(bot):
    bot.add_cog(Profile(bot))
