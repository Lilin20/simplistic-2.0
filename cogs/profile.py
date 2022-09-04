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

    status = discord.SlashCommandGroup('status', "Bearbeite deinen Status")
    @status.command()
    async def set(self, ctx, status):
        if len(status) > 50:
            await ctx.respond("Dein Status darf nicht länger als 50 Zeichen sein.", ephemeral=True)
            return
        db.database.set_status(ctx.author.id, f"{status}")
        await ctx.respond("Status wurde geändert.", ephemeral=True)

    @status.command()
    async def reset(self, ctx):
        db.database.set_status(ctx.author.id, " ")
        await ctx.respond("Dein Status wurde zurückgesetzt.", ephemeral=True)

    @discord.slash_command()
    async def profile(self, ctx, member: discord.Member = None):
        """Zeigt das Profil des angegebenen Mitglieds"""
        if member is None:
            member = ctx.author

        try:
            fetched_achievement = (db.database.get_last_achievement(member.id)[1], db.database.get_last_achievement(member.id)[2])
        except:
            fetched_achievement = ('None', 'Noch kein Achievement freigeschaltet.')

        self.pages = [
            discord.Embed(title=f"Simplistic - Perso", description=f"{db.database.get_status(member.id)}", fields=[
                discord.EmbedField(name="Name", value=member.name, inline=True),
                discord.EmbedField(name="Level", value=db.database.get_level(member.id), inline=True),
                discord.EmbedField(name="ID", value=member.id, inline=True),
                discord.EmbedField(name="Nachrichten", value=db.database.get_message_count(member.id), inline=True),
                discord.EmbedField(name="Letztes Achievement", value=f'{fetched_achievement[0]}\n{fetched_achievement[1]}', inline=True),
            ]), # {db.database.get_last_achievement(member.id)[1]}\n{db.database.get_last_achievement(member.id)[2]}
            discord.Embed(title="Simplistic - Economy", description=f"Stats von {member.name}", fields=[
                discord.EmbedField(name="Vermögen", value=db.database.get_balance(member.id), inline=True),
                discord.EmbedField(name="Raubzüge", value=db.database.has_robbed(member.id), inline=True),
                discord.EmbedField(name="Hops genommen", value=db.database.get_robbed(member.id), inline=True)
            ]),
        ]
        self.pages[0].set_thumbnail(url=member.avatar.url)
        self.pages[0].set_footer(text=f"Join date: {member.joined_at.date()}\nAccount created: {member.created_at.date()}")
        self.pages[1].set_thumbnail(url=member.avatar.url)

        paginator = pages.Paginator(pages=self.pages)
        await paginator.respond(ctx.interaction, ephemeral=False)

    

def setup(bot):
    bot.add_cog(Profile(bot))
