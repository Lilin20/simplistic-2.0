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

    @commands.command(help="Zeigt das eigene Profil oder das eines anderen Users an.")
    async def profile(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author

        result_userdata = [["test", "test", "test", "test", "test", "test", "test"]]
        result_achievement = [["testachievement","testachievement","testachievement","testachievement","testachievement",]]
        result_economy = [[0, 0, 0,0,0,0,0,0,0,0,0,]]
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

def setup(bot):
    bot.add_cog(Profile(bot))
