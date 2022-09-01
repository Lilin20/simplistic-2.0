import discord
from discord.utils import get

class DefaultConfig:
    profile_values = {'level': 0, 'xp': 0, 'growth': 0, 'messages': 0, 'warns': 0}
    economy_values = {'balance': 0, 'got_robbed': 0, 'has_robbed': 0}
    guild = None
    bot = None

class RoleSelectorView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Wähle eine Rolle!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="ITA21a",
                description="Für Schüler der ITA21a",
            ),
            discord.SelectOption(
                label="ITA21b",
                description="Für Schüler der ITA21b",
            ),
            discord.SelectOption(
                label="ITA22a",
                description="Für Schüler der TA22a",
            ),
            discord.SelectOption(
                label="ITA22b",
                description="Für Schüler der ITA22b",
            ),
            discord.SelectOption(
                label="ITF22a",
                description="Für Schüler der ITF22a",
            ),
            discord.SelectOption(
                label="ITF22d",
                description="Für Schüler der ITF22d",
            ),
            discord.SelectOption(
                label="Gast",
                description="Für Gäste",
            )
        ]
    )
    async def select_callback(self, select, interaction):
        await interaction.response.send_message(f"Perfekt. Du hast die Rolle {select.values[0]} bekommen!")
        select.disabled = True

        role = get(DefaultConfig.guild.roles, name=select.values[0])
        # Get Member
        member = get(DefaultConfig.guild.members, id=interaction.user.id)
        await member.add_roles(role)

        await interaction.message.edit(view=self)