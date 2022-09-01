import discord
import sys
from discord.ext import commands
from discord.commands import SlashCommandGroup
from discord.ext import commands, pages
import os

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db

class Test(commands.Cog):
    """Modul für die Testfunktionen"""
    def __init__(self, bot):
        self.bot = bot
        self.pages = [
            "Page 1",
            [
                discord.Embed(title="Page 2, Embed 1"),
                discord.Embed(title="Page 2, Embed 2"),
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


    @commands.Cog.listener()
    async def on_ready(self):
        print("Test module loaded.")

    def get_pages(self):
        return self.pages

    pagetest = SlashCommandGroup("pagetest", "Commands for testing ext.pages.")

    @pagetest.command(name="default")
    async def pagetest_default(self, ctx: discord.ApplicationContext):
        """Demonstrates using the paginator with the default options."""
        paginator = pages.Paginator(pages=self.get_pages())
        await paginator.respond(ctx.interaction, ephemeral=False)

def setup(bot):
    bot.add_cog(Test(bot))
