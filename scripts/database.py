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

    def get_balance(self, id):
        self.cursor.execute(f"SELECT balance FROM economy WHERE users_id = '{id}'")
        return self.cursor.fetchall()[0][0]

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

    def add_user(self, id, username):
        self.cursor.execute(f"INSERT INTO users (id, username, level, xp, growth, messages, warns) VALUES ('{id}', '{username}', {helper.DefaultConfig.profile_values['level']}, {helper.DefaultConfig.profile_values['xp']}, {helper.DefaultConfig.profile_values['growth']}, {helper.DefaultConfig.profile_values['messages']}, {helper.DefaultConfig.profile_values['warns']})")
        self.cursor.execute(f"INSERT INTO economy (users_id, balance, worked,got_robbed, has_robbed) VALUES ('{id}', {helper.DefaultConfig.economy_values['balance']}, {helper.DefaultConfig.economy_values['worked']}, {helper.DefaultConfig.economy_values['got_robbed']}, {helper.DefaultConfig.economy_values['has_robbed']})")

database = Connector(host, user, password, db)
