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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content.startswith(self.bot.command_prefix):
            return
        if message.content.startswith("https") or message.content.startswith("http"):
            return
        
        xp_to_give = len(message.content) - message.content.count(" ")
        db.database.add_xp(message.author.id, xp_to_give)
        leveling_info = db.database.get_leveling_info(message.author.id)

        calculate_xp = 50 * (1 + leveling_info[2]) ** int(leveling_info[0])
        if leveling_info[1] >= calculate_xp:
            db.database.level_up(message.author.id)
            embed = discord.Embed(title="Simplistic - Level UP", description=f"{message.author.mention} hat Level {leveling_info[0] + 1} erreicht!", color=0x00ff00)
            embed.set_thumbnail(url="https://monophy.com/media/aQu0Douf5MM8nhZBy9/monophy.gif")
            embed.set_footer(text="Keep grinding!")
            await message.channel.send(embed=embed, delete_after=5)

    status = discord.SlashCommandGroup('status', "Bearbeite deinen Status")
    @status.command()
    async def set(self, ctx, status):
        """Setze deinen Status"""
        if len(status) > 50:
            await ctx.respond("Dein Status darf nicht länger als 50 Zeichen sein.", ephemeral=True)
            return
        db.database.set_status(ctx.author.id, f"{status}")
        await ctx.respond("Status wurde geändert.", ephemeral=True)

    @status.command()
    async def reset(self, ctx):
        """Setze deinen Status zurück"""
        db.database.set_status(ctx.author.id, " ")
        await ctx.respond("Dein Status wurde zurückgesetzt.", ephemeral=True)

    @discord.slash_command()
    async def profile(self, ctx, member: discord.Member = None):
        """Zeigt das eigene Profil oder das Profil des angegebenen Users an"""
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
                discord.EmbedField(name="SMPL-Coins", value=db.database.get_balance(member.id), inline=True),
                discord.EmbedField(name="Raubzüge", value=db.database.has_robbed(member.id), inline=True),
                discord.EmbedField(name="Hops genommen", value=db.database.get_robbed(member.id), inline=True),
                discord.EmbedField(name="Arbeitstage", value=db.database.get_worked(member.id), inline=True),
                discord.EmbedField(name="Arbeitsstunden", value=db.database.get_worked_hours(member.id), inline=True)
            ]),
        ]
        self.pages[0].set_thumbnail(url=member.avatar.url)
        self.pages[0].set_footer(text=f"Join date: {member.joined_at.date()}\nAccount created: {member.created_at.date()}")
        self.pages[1].set_thumbnail(url=member.avatar.url)

        paginator = pages.Paginator(pages=self.pages)
        await paginator.respond(ctx.interaction, ephemeral=False)

    achievement_group = discord.SlashCommandGroup('achievement', "Alle Befehle zu Achievements")
    @achievement_group.command()
    async def list(self, ctx, hide: bool = False):
        """Zeigt alle deine Achievements an"""
        achievement_list = []
        self.pages = []
        # Show all user achievements in a page
        all_user_achievements = db.database.get_user_achievements(ctx.author.id)
        for user_achievement in all_user_achievements:
            achievement_list.append(db.database.get_achievement(user_achievement[2]))

        embed = discord.Embed(title="Simplistic - Achievements", description="Deine Achievements", fields=[
            discord.EmbedField(name="Name", value="".join([f"{achievement[1]}\n" for achievement in achievement_list]), inline=True),
            discord.EmbedField(name="Beschreibung", value="".join([f"{achievement[2]}\n" for achievement in achievement_list]), inline=True),
        ])

        self.pages.append(embed)
        paginator = pages.Paginator(pages=self.pages)
        await paginator.respond(ctx.interaction, ephemeral=hide)
        
    @achievement_group.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, member: discord.Member, achievement_id: int):
        """Fügt dem User ein Achievement hinzu"""
        db.database.cursor.execute(f"INSERT INTO user_achievements (users_id, achievements_id) VALUES ('{member.id}', '{achievement_id}')")
        await ctx.respond(f"Das Achievement {db.database.get_achievement(achievement_id)[1]} wurde dem Benutzer {member.name} hinzugefügt.", ephemeral=True)
        await member.send("Psst... Eine höhere Macht hat dir ein Achievement hinzugefügt. Schau mal in deinem Profil nach.")


def setup(bot):
    bot.add_cog(Profile(bot))
