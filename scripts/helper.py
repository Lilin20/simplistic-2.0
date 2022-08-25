import scripts.database as db

def build_user_stat_dict(d_id):
	db.database.cursor.execute(f"SELECT * FROM userdata WHERE d_id = %s;", (d_id,))
	user_stats = db.database.cursor.fetchall()
	user_stat_dict = {
		'd_id': user_stats[0][0],
		'lvl': user_stats[0][1],
		'warns': user_stats[0][2],
		'messages': user_stats[0][3],
		'join_date': user_stats[0][4],
		'xp': user_stats[0][5],
		'growth': user_stats[0][6],
		'description': user_stats[0][7]
	}
	return user_stat_dict

def build_economy_dict(d_id):
	db.database.cursor.execute(f"SELECT * FROM economy WHERE d_id = %s;", (d_id,))
	economy_stats = db.database.cursor.fetchall()
	economy_stat_dict = {
		'd_id': economy_stats[0][1],
		'money': economy_stats[0][2],
		'robbed_success': economy_stats[0][3],
		'robbed_fail': economy_stats[0][4],
		'worked_hours': economy_stats[0][5]
		}
	return economy_stat_dict

def money_check(d_id, amount):
	db.database.cursor.execute(f"SELECT money FROM economy WHERE d_id = %s;", (d_id,))
	money = db.database.cursor.fetchall()
	if money[0][2] >= amount:
		return True
	else:
		return False

def money_add(d_id, amount):
	db.database.cursor.execute(f"SELECT money FROM economy WHERE d_id = %s;", (d_id,))
	money = db.database.cursor.fetchall()
	db.database.cursor.execute(f"UPDATE economy SET money = %s WHERE d_id = %s;", (money[0][2] + amount, d_id))
	db.database.connection.commit()

def money_remove(d_id, amount):
	db.database.cursor.execute(f"SELECT money FROM economy WHERE d_id = %s;", (d_id,))
	money = db.database.cursor.fetchall()
	db.database.cursor.execute(f"UPDATE economy SET money = %s WHERE d_id = %s;", (money[0][2] - amount, d_id))
	db.database.connection.commit()

def check_for_achievement(d_id, achievement_type):
	if achievement_type == "messages":
		#Get user stats
		user_stats = build_user_stat_dict(d_id)

		#Get all achievements with type messages
		db.database.cursor.execute(f"SELECT * FROM achievements WHERE type = %s;", ("messages",))
		achievements = db.database.cursor.fetchall()
		
		#get all achievements from the user and type messages
		db.database.cursor.execute(f"SELECT * FROM user_achievements WHERE d_id = %s AND achievement_type = %s;", (d_id, "messages"))
		user_achievements = db.database.cursor.fetchall()

		print(achievements)
		print("-----\n")
		print(user_achievements)
		for achievement in achievements:
			if not user_achievements:
				if user_stats["messages"] >= achievement[3]:
					db.database.cursor.execute(f"INSERT INTO user_achievements (d_id, achievement_type, achievement_id) VALUES (%s, %s, %s);", (d_id, "messages", achievement[0]))
					print(f"Achievement {achievement[0]} unlocked for {d_id}")
					return achievement
			for user_achievement in user_achievements:
				if achievement[0] not in user_achievement or not user_achievement:
					if user_stats["messages"] >= achievement[3]:
						db.database.cursor.execute(f"INSERT INTO user_achievements (d_id, achievement_type, achievement_id) VALUES (%s, %s, %s);", (d_id, "messages", achievement[0]))
						print(f"Achievement {achievement[0]} unlocked for {d_id}")
						return achievement