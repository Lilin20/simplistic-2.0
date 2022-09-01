import discord
import sys
from discord.ext import commands, bridge, pages
import os

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db


class Profile(commands.Cog):
    """Modul für die Profilfunktionen"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Profile module loaded.")

    @bridge.bridge_command()
    async def profile(self, ctx, member: discord.Member = None):
        """Zeigt das Profil des angegebenen Mitglieds"""
        if member is None:
            member = ctx.author

        self.pages = [
            discord.Embed(title="Simplistic - Perso", description=f"Profil von {member.name}", fields=[
                discord.EmbedField(name="Name", value=member.name, inline=True),
                discord.EmbedField(name="ID", value=member.id, inline=True)
            ]),
            [
                discord.Embed(title="Simplistic - Economy", description=f"Stats von {member.name}", fields=[
                    discord.EmbedField(name="Vermögen", value=db.database.get_balance(member.id), inline=True),
                    discord.EmbedField(name="Raubzüge", value=db.database.has_robbed(member.id), inline=True),
                    discord.EmbedField(name="Hops genommen", value=db.database.get_robbed(member.id), inline=True)
                ]),
            ],
            "Page Three",
            discord.Embed(title="Page Four"),
            discord.Embed(
                title="Page Five",
                fields=[
                    discord.EmbedField(name="Example Field", value="Example Value", inline=False),
                ],
            ),
            [
                discord.Embed(title="Page Six, Embed 1"),
                discord.Embed(title="Page Seven, Embed 2"),
            ],
        ]
        self.pages[0].set_thumbnail(url=member.avatar.url)
        self.pages[1][0].set_thumbnail(url=member.avatar.url)
        self.pages[3].set_image(url="https://c.tenor.com/pPKOYQpTO8AAAAAM/monkey-developer.gif")
        self.pages[4].add_field(name="Another Example Field", value="Another Example Value", inline=False)

        self.more_pages = [
            "Second Page One",
            discord.Embed(title="Second Page Two"),
            discord.Embed(title="Second Page Three"),
        ]

        self.even_more_pages = ["11111", "22222", "33333"]

        self.new_pages = [
            pages.Page(
                content="Page 1 Title!",
                embeds=[
                    discord.Embed(title="New Page 1 Embed Title 1!"),
                    discord.Embed(title="New Page 1 Embed Title 2!"),
                ],
            ),
            pages.Page(
                content="Page 2 Title!",
                embeds=[
                    discord.Embed(title="New Page 2 Embed Title 1!"),
                    discord.Embed(title="New Page 2 Embed Title 2!"),
                ],
            ),
        ]

        paginator = pages.Paginator(pages=self.pages)
        await paginator.respond(ctx.interaction, ephemeral=False)


    

def setup(bot):
    bot.add_cog(Profile(bot))