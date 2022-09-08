import mysql.connector
import configparser
import os
import scripts.helper as helper

def getpath():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'config.ini')

c_parser = configparser.ConfigParser()
c_parser.read(getpath())

host = c_parser.get('Database', 'host')
user = c_parser.get('Database', 'user')
password = c_parser.get('Database', 'pass')
db = c_parser.get('Database', 'db')


class Connector:
    def __init__(self, host, user, password, db):
        self.database = mysql.connector.connect(host=host, user=user, password=password, autocommit=True)
        self.cursor = self.database.cursor()
        self.cursor.execute(f"USE {db}")

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, script):
        self.cursor.execute(script)

    def check_user(self, id):
        self.cursor.execute(f"SELECT id FROM users WHERE id = '{id}'")
        result = self.cursor.fetchall()
        if result:
            return True
        else:
            return False

    def get_last_achievement(self, id):
        self.cursor.execute(f"SELECT * FROM user_achievements WHERE users_id = '{id}' ORDER BY id DESC LIMIT 1")
        achievement_id = self.cursor.fetchall()[0][2]
        self.cursor.execute(f"SELECT * FROM achievements WHERE id = '{achievement_id}'")
        return self.cursor.fetchall()[0]

    def get_balance(self, id):
        self.cursor.execute(f"SELECT balance FROM economy WHERE users_id = '{id}'")
        return self.cursor.fetchall()[0][0]

    def add_balance(self, id, value):
        self.cursor.execute(f"UPDATE economy SET balance = balance + {value} WHERE users_id = '{id}'")

    def get_robbed(self, id):
        self.cursor.execute(f"SELECT got_robbed FROM economy WHERE users_id = '{id}'")
        return self.cursor.fetchall()[0][0]

    def has_robbed(self, id):
        self.cursor.execute(f"SELECT has_robbed FROM economy WHERE users_id = '{id}'")
        return self.cursor.fetchall()[0][0]

    def get_level(self, id):
        self.cursor.execute(f'SELECT level FROM users WHERE id = "{id}"')
        return self.cursor.fetchall()[0][0]

    def get_status(self, id):
        self.cursor.execute(f"SELECT status FROM users WHERE id = '{id}'")
        return self.cursor.fetchall()[0][0]

    def set_status(self, id, status):
        self.cursor.execute(f"UPDATE users SET status = '{status}' WHERE id = '{id}'")

    def get_server_var(self, var):
        self.cursor.execute(f"SELECT value FROM server_vars WHERE name = '{var}'")
        return self.cursor.fetchall()[0][0]

    def add_counter(self):
        self.cursor.execute(f"UPDATE server_vars SET value = value + 1 WHERE name = 'counting'")

    def reset_counter(self):
        self.cursor.execute(f"UPDATE server_vars SET value = 0 WHERE name = 'counting'")

    def get_counting_record(self):
        self.cursor.execute(f"SELECT value FROM server_vars WHERE name = 'counting_record'")
        return self.cursor.fetchall()[0][0]

    def set_counting_record(self, value):
        self.cursor.execute(f"UPDATE server_vars SET value = {value} WHERE name = 'counting_record'")
    
    def add_server_money(self, var, value):
        self.cursor.execute(f"UPDATE server_vars SET value = value + {value} WHERE name = '{var}'")

    def add_user(self, id, username):
        self.cursor.execute(f"INSERT INTO users (id, username, level, xp, growth, messages, warns) VALUES ('{id}', '{username}', {helper.DefaultConfig.profile_values['level']}, {helper.DefaultConfig.profile_values['xp']}, {helper.DefaultConfig.profile_values['growth']}, {helper.DefaultConfig.profile_values['messages']}, {helper.DefaultConfig.profile_values['warns']})")
        self.cursor.execute(f"INSERT INTO economy (users_id, balance, worked, worked_hours, got_robbed, has_robbed, rob_spree) VALUES ('{id}', {helper.DefaultConfig.economy_values['balance']}, {helper.DefaultConfig.economy_values['worked']}, {helper.DefaultConfig.economy_values['worked_hours']}, {helper.DefaultConfig.economy_values['got_robbed']}, {helper.DefaultConfig.economy_values['has_robbed']}, {helper.DefaultConfig.economy_values['rob_spree']})")

    def get_achievements(self, type):
        self.cursor.execute(f"SELECT * FROM achievements WHERE type = '{type}'")
        return self.cursor.fetchall()

    def get_achievement(self, id):
        self.cursor.execute(f"SELECT * FROM achievements WHERE id = '{id}'")
        return self.cursor.fetchall()[0]

    def get_user_achievements(self, id):
        self.cursor.execute(f"SELECT * FROM user_achievements WHERE users_id = '{id}'")
        return self.cursor.fetchall()

    def get_message_count(self, id):
        self.cursor.execute(f"SELECT messages FROM users WHERE id = '{id}'")
        return self.cursor.fetchall()[0][0]

    def add_message_count(self, id, value):
        self.cursor.execute(f"UPDATE users SET messages = messages + {value} WHERE id = '{id}'")

    def get_worked(self, id):
        self.cursor.execute(f"SELECT worked FROM economy WHERE users_id = '{id}'")
        return self.cursor.fetchall()[0][0]
    
    def get_worked_hours(self, id):
        self.cursor.execute(f"SELECT worked_hours FROM economy WHERE users_id = '{id}'")
        return self.cursor.fetchall()[0][0]

    def add_worked(self, id):
        self.cursor.execute(f"UPDATE economy SET worked = worked + 1 WHERE users_id = '{id}'")

    def add_worked_hours(self, id, value):
        self.cursor.execute(f"UPDATE economy SET worked_hours = worked_hours + {value} WHERE users_id = '{id}'")

    def add_has_robbed(self, id):
        self.cursor.execute(f"UPDATE economy SET has_robbed = has_robbed + 1 WHERE users_id = '{id}'")

    def get_rob_spree(self, id):
        self.cursor.execute(f"SELECT rob_spree FROM economy WHERE users_id = '{id}'")
        return self.cursor.fetchall()[0][0]

    def add_rob_spree(self, id):
        self.cursor.execute(f"UPDATE economy SET rob_spree = rob_spree + 1 WHERE users_id = '{id}'")

    def reset_rob_spree(self, id):
        self.cursor.execute(f"UPDATE economy SET rob_spree = 0 WHERE users_id = '{id}'")

    def add_xp(self, id, value):
        self.cursor.execute(f"UPDATE users SET xp = xp + {value} WHERE id = '{id}'")

    def get_leveling_info(self, id):
        self.cursor.execute(f"SELECT level, xp, growth FROM users WHERE id = '{id}'")
        return self.cursor.fetchall()[0]

    def level_up(self, id):
        self.cursor.execute(f"UPDATE users SET level = level + 1 WHERE id = '{id}'")
        self.cursor.execute(f"UPDATE users SET xp = 0 WHERE id = '{id}'")
        self.cursor.execute(f"UPDATE users SET growth = growth + 0.025 WHERE id = '{id}'")

    def get_leaderboard_level(self):
        self.cursor.execute(f"SELECT username, level FROM users ORDER BY level DESC")
        return self.cursor.fetchall()

    def get_leaderboard_money(self):
        self.cursor.execute(f"SELECT users.username, economy.balance FROM economy INNER JOIN users ON economy.users_id = users.id ORDER BY economy.balance DESC LIMIT 10")
        return self.cursor.fetchall()

    def get_leaderboard_rob(self):
        self.cursor.execute(f"SELECT users.username, economy.has_robbed FROM economy INNER JOIN users ON economy.users_id = users.id ORDER BY economy.has_robbed DESC LIMIT 10")
        return self.cursor.fetchall()

    def get_leaderboard_worked_hours(self):
        self.cursor.execute(f"SELECT users.username, economy.worked_hours FROM economy INNER JOIN users ON economy.users_id = users.id ORDER BY economy.worked_hours DESC LIMIT 10")
        return self.cursor.fetchall()

database = Connector(host, user, password, db)
