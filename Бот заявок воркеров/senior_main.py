from senior_config import bot, admin_chat, admin_1, workers_chat_link, hello
from senior_buttons import main_keyboard, second_keyboard, admin_chat_keyboard, admin_menu_keyboard, chat_keyboard
import sqlite3

@bot.message_handler(commands=['start'])
def send_welcome(message):
	chat_id = message.chat.id
	if chat_id > 0:
		user = get_user(chat_id)
		if user == None:			
			try:
				add_to_db(chat_id)
			except:
				pass
		user = get_user(chat_id)
		if user != None:
			if user[4] == "True":
				bot.send_message(chat_id, "<b>Ваша заявка находится на расмотрении. Ожидайте решения</b>",
											parse_mode="HTML")
			elif user[1] == None:
				bot.send_message(chat_id, "<b>Привет! Воспользуйся кнопками.</b>",
											reply_markup=main_keyboard(),
											parse_mode="HTML")
			
			elif user[1] == "True":
				bot.send_message(chat_id, f"<b>❗️Ты уже в команде переходи в чат воркеров.</b>",
									 reply_markup=chat_keyboard(),
									 parse_mode="HTML")
			elif user[1] == "False":
				bot.send_message(chat_id, "<b>Вы забанены в боте</b>",
											parse_mode="HTML")
			

@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
	bot.send_message(message.chat.id, hello, parse_mode="HTML", disable_web_page_preview=True)

@bot.message_handler(commands=['ban'])
def ban(message):
	if message.chat.id < 0:
		if get_admin(message.from_user.id) != None:
			if message.reply_to_message == None:
				bot.send_message(message.chat.id, f"Нет реплая")
			else:
				user_to_ban = message.reply_to_message.from_user
				if bot.get_chat_member(chat_id=message.chat.id,user_id=user_to_ban.id).status != 'administrator':
					bot.kick_chat_member(chat_id=message.chat.id, user_id=user_to_ban.id)
					bot.send_message(chat_id=message.chat.id, text=f"{user_to_ban.first_name} - Забанен", reply_to_message_id=message.message_id)
				else:
					bot.send_message(chat_id=message.chat.id, text=f"Он админ, дибил", reply_to_message_id=message.message_id)
		else:
			bot.send_message(chat_id=message.chat.id, text=f"У вас нет доступа к данной команде", reply_to_message_id=message.message_id)

@bot.message_handler(commands=['unban'])
def unban(message):
	if message.chat.id < 0:
		if get_admin(message.from_user.id) != None:
			if message.reply_to_message == None:
				bot.send_message(message.chat.id, f"Нет реплая")
			else:
				user_to_unban = message.reply_to_message.from_user
				if bot.get_chat_member(chat_id=message.chat.id,user_id=user_to_unban.id).status != 'administrator':
					bot.unban_chat_member(chat_id=message.chat.id, user_id=user_to_unban.id)
					bot.send_message(chat_id=message.chat.id, text=f"{user_to_unban.first_name} - Разбанен", reply_to_message_id=message.message_id)
				else:
					bot.send_message(chat_id=message.chat.id, text=f"Он админ, дибил", reply_to_message_id=message.message_id)
		else:
			bot.send_message(chat_id=message.chat.id, text=f"У вас нет доступа к данной команде", reply_to_message_id=message.message_id)

@bot.message_handler(commands=['admin'])
def admin(message):
	if message.chat.id > 0:
		if message.from_user.id == admin_1:
			bot.send_message(chat_id=message.from_user.id, text="Нажмите на одну из кнопок", reply_markup=admin_menu_keyboard())
		else:
			pass

@bot.message_handler(content_types="text")
def get_text_message(message, *args):
	chat_id = message.chat.id
	if chat_id > 0:
		user = get_user(chat_id)
		if user == None:			
			try:
				add_to_db(chat_id)
			except:
				pass
		user = get_user(chat_id)
		if user != None:
			if user[4] == "True":
				bot.send_message(chat_id, "<b>Ваша заявка находится на расмотрении. Ожидайте решения</b>",
											parse_mode="HTML")
			elif user[1] == None:
				bot.send_message(chat_id, "<b>Привет! Воспользуйся кнопками.</b>",
											reply_markup=main_keyboard(),
											parse_mode="HTML")
			
			elif user[1] == "True":
				bot.send_message(chat_id, f"<b>❗️Ты уже в команде переходи в чат воркеров.</b>",
									 reply_markup=chat_keyboard(),
									 parse_mode="HTML")
			elif user[1] == "False":
				bot.send_message(chat_id, "<b>Вы забанены в боте</b>",
											parse_mode="HTML")
	else:
		if message.text.lower() == 'кинь кубик':
			dice = bot.send_dice(chat_id=message.chat.id)
			while dice.dice.value < 6 and message.from_user.id == admin_1:
				bot.delete_message(chat_id=message.chat.id, message_id=dice.message_id)
				dice = bot.send_dice(chat_id=message.chat.id)
			bot.send_message(message.chat.id, f"У @{message.from_user.username} выпало: {dice.dice.value}")

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	id = call.message.chat.id
	message_id = call.message.message_id
	if call.data == "to_team":
		user = get_user(id)
		if user[4] == "True":
			bot.send_message(id, "<b>Ваша заявка находится на расмотрении. Ожидайте решения</b>",
											parse_mode="HTML")
		else:
			bot.edit_message_text(chat_id=id,message_id=message_id, text='Откуда вы о нас узнали?')
			bot.register_next_step_handler(call.message, to_team1)
	
	if call.data == "add_admin":
		bot.send_message(chat_id=id, text='Введите id пользователя кому вы хотите выдать администратора')
		bot.register_next_step_handler(call.message, add_admin1)

	if call.data == "del_admin":
		bot.send_message(chat_id=id, text='Введите id пользователя у кого вы хотите забрать администратора')
		bot.register_next_step_handler(call.message, del_admin1)

	if call.data.startswith("send"):
		user_id = call.data.split("-")[1]
		username = call.data.split("-")[2]
		user = get_user(user_id)
		update_send(user_id)
		bot.delete_message(chat_id=id, message_id=message_id)
		bot.send_message(chat_id=user_id, text='Заявка успешно отправлена')
		bot.send_message(chat_id=admin_chat, text=f'Новая заявка!\n\nОпыт: {user[2]}\n\nОткуда: {user[3]}\n\nID: {user_id}\n\nUsername: @{username}', reply_markup=admin_chat_keyboard(user_id, username))
			
	if call.data.startswith("accept"):
		bot.edit_message_reply_markup(chat_id=id, message_id=message_id)
		info = call.data.split('-')
		set_true(info[1])
		bot.send_message(chat_id=info[1], text=f'<b>🎉Поздравляем! Вы приняты в нашу команду. Для работы зайдите в наш чат.</b>',
											reply_markup=chat_keyboard(),
											parse_mode="HTML")
		bot.send_message(chat_id=id, text=f'Заявка пользователя @{info[2]} принята')

	if call.data.startswith("reject"):
		bot.edit_message_reply_markup(chat_id=id, message_id=message_id)
		info = call.data.split('-')
		set_false(info[1])
		bot.send_message(chat_id=info[1], text='😔Ваша заявка на вступление в команду отклонена.')
		bot.send_message(chat_id=id, text=f'Заявка пользователя @{info[2]} отклонена')


def to_team1(message):
	from_info = message.text
	bot.send_message(chat_id=message.chat.id, text='Был ли у вас опыт в сфере скама?')
	bot.register_next_step_handler(message, to_team2, from_info)

def to_team2(message, from_info):
	work = message.text
	username = message.chat.username
	update_from_info(message.chat.id, from_info)
	update_work(message.chat.id, work)
	bot.send_message(chat_id=message.chat.id, text=f'Заявка сформирована. Проверьте её.\n\nОпыт: {work}', reply_markup=second_keyboard(message.chat.id, username))

def add_to_db(id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""INSERT INTO users(id) VALUES('{id}') """)
	db.commit()

def get_user(id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""SELECT * FROM users WHERE id = '{id}' """)
	row = cursor.fetchone()
	return row

def set_true(id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""UPDATE users SET accepted = 'True' WHERE id = '{id}' """)
	db.commit()

def update_send(id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""UPDATE users SET send = 'True' WHERE id = '{id}' """)
	db.commit()

def update_work(id, work):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""UPDATE users SET work = '{work}' WHERE id = '{id}' """)
	db.commit()

def update_from_info(id, from_info):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""UPDATE users SET from_info = '{from_info}' WHERE id = '{id}' """)
	db.commit()

def get_admin(id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""SELECT id FROM admins WHERE id = '{id}' """)
	row = cursor.fetchone()
	return row

def add_admin(id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""INSERT INTO admins(id) VALUES('{id}') """)
	db.commit()

def del_admin(id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""DELETE FROM admins WHERE id = '{id}' """)
	db.commit()

def set_false(id):
	db = sqlite3.connect('database.db')
	cursor = db.cursor()
	cursor.execute(f"""UPDATE users SET accepted = 'False' WHERE id = '{id}' """)
	db.commit()

def add_admin1(message):
	try:
		id = int(message.text)
		bot.send_message(chat_id=message.from_user.id, text="Пользователю были выданы права администратора.")
		add_admin(id)
	except:
		bot.send_message(chat_id=message.from_user.id, text="Вводите цифрами!")

def del_admin1(message):
	try:
		id = int(message.text)
		bot.send_message(chat_id=message.from_user.id, text="У пользователя отняты права администратора.")
		del_admin(id)
	except:
		bot.send_message(chat_id=message.from_user.id, text="Вводите цифрами!")


if __name__ == '__main__':
	try:
		bot.polling(none_stop = True, interval = 0)
	except Exception as e:
		bot.send_message(admin_chat, text=f"<b>Возникла ошибка</b>\n\n{e}", parse_mode="HTML")
		while True:
			try:
				bot.polling(none_stop = True, interval = 0)
			except Exception as e:
				bot.send_message(admin_chat, text=f"<b>Возникла ошибка!</b>\n\n{e}", parse_mode="HTML")