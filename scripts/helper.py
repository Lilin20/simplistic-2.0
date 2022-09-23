import discord
from discord.utils import get
import scripts.database as db

class DefaultConfig:
    profile_values = {'level': 1, 'xp': 0, 'growth': 0.25, 'messages': 0, 'warns': 0}
    economy_values = {'balance': 0, 'worked':0, 'worked_hours': 0,'got_robbed': 0, 'has_robbed': 0, 'rob_spree': 0}
    guild = None
    bot = None
    maintenance = True

class AchievementHandler:
    def __init__(self):
        self.text_achievements = []
        self.economy_work_achievements = []
        self.economy_rob_achievements = []
        self.economy_money_achievements = []
        self.economy_rob_spree_achievements = []

    def init(self):
        self.FetchTextAchievements()
        self.FetchEconomyWorkAchievements()
        self.FetchEconomyRobAchievements()
        self.FetchEconomyMoneyAchievements()
        self.FetchEconomyRobSpreeAchievements()

    def FetchTextAchievements(self):
        achievements = db.database.get_achievements('message')
        for achievement in achievements:
            self.text_achievements.append(achievement)

    def FetchEconomyWorkAchievements(self):
        achievements = db.database.get_achievements('economy_work')
        for achievement in achievements:
            self.economy_work_achievements.append(achievement)

    def FetchEconomyRobAchievements(self):
        achievements = db.database.get_achievements('economy_rob_success')
        for achievement in achievements:
            self.economy_rob_achievements.append(achievement)

    def FetchEconomyMoneyAchievements(self):
        achievements = db.database.get_achievements('economy_money')
        for achievement in achievements:
            self.economy_money_achievements.append(achievement)

    def FetchEconomyRobSpreeAchievements(self):
        achievements = db.database.get_achievements('economy_rob_spree')
        for achievement in achievements:
            self.economy_rob_spree_achievements.append(achievement)

    def FetchUserAchievements(self, member: discord.Member):
        return db.database.get_user_achievements(member.id)
        
    def TextAchievementHandler(self, member: discord.Member):
        messages = db.database.get_message_count(member.id)
        for achievement in self.text_achievements:
            if any(achievement[0] in x for x in self.FetchUserAchievements(member)):
                continue
            if messages == achievement[3]:
                db.database.cursor.execute(f"INSERT INTO user_achievements (users_id, achievements_id) VALUES ('{member.id}', '{achievement[0]}')")
                return (True, achievement[1], achievement[2])

    def EconomyWorkAchievementHandler(self, member: discord.Member):
        worked = db.database.get_worked(member.id)
        for achievement in self.economy_work_achievements:
            if any(achievement[0] in x for x in self.FetchUserAchievements(member)):
                continue
            if worked == achievement[3]:
                db.database.cursor.execute(f"INSERT INTO user_achievements (users_id, achievements_id) VALUES ('{member.id}', '{achievement[0]}')")
                return (True, achievement[1], achievement[2])

    def EconomyRobAchievementHandler(self, member: discord.Member):
        robbed = db.database.has_robbed(member.id)
        for achievement in self.economy_rob_achievements:
            if any(achievement[0] in x for x in self.FetchUserAchievements(member)):
                continue
            if robbed == achievement[3]:
                db.database.cursor.execute(f"INSERT INTO user_achievements (users_id, achievements_id) VALUES ('{member.id}', '{achievement[0]}')")
                return (True, achievement[1], achievement[2])

    def EconomyMoneyAchievementHandler(self, member: discord.Member):
        balance = db.database.get_balance(member.id)
        for achievement in self.economy_money_achievements:
            if any(achievement[0] in x for x in self.FetchUserAchievements(member)):
                continue
            if balance >= achievement[3]:
                db.database.cursor.execute(f"INSERT INTO user_achievements (users_id, achievements_id) VALUES ('{member.id}', '{achievement[0]}')")
                return (True, achievement[1], achievement[2])

    def EconomyRobSpreeAchievementHandler(self, member: discord.Member):
        rob_spree = db.database.get_rob_spree(member.id)
        for achievement in self.economy_rob_spree_achievements:
            if any(achievement[0] in x for x in self.FetchUserAchievements(member)):
                continue
            if rob_spree == achievement[3]:
                db.database.cursor.execute(f"INSERT INTO user_achievements (users_id, achievements_id) VALUES ('{member.id}', '{achievement[0]}')")
                return (True, achievement[1], achievement[2])

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