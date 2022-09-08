import discord
import sys
from discord.ext import commands, bridge
import os

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')

sys.path.insert(1, getpath())
import database as db

class Moderation(commands.Cog):
    """Modul für die Moderationfunktionen"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation module loaded.")

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount: int):
        """Löscht die angegebene Anzahl an Nachrichten"""
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"{amount} Nachrichten wurden gelöscht.", delete_after=5)

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kickt den angegebenen User"""
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} wurde gekickt.", delete_after=5)

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bant den angegebenen User"""
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} wurde gebannt.", delete_after=5)

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        """Entbannt den angegebenen User"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} wurde entbannt.", delete_after=5)
                return

def setup(bot):
    bot.add_cog(Moderation(bot))
