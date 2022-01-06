import telebot
from telebot import types
import requests
import json
import time
import sqlite3
import random
from datetime import datetime, datetime, timedelta
from coinbase.wallet.client import Client

from threading import Thread
import threading
from threading import Timer

import config
import menu
import func




bot = telebot.TeleBot(config.token2, parse_mode="HTML")
print("Бот запущен")

click = []
kk = 0
threads = list()

def start_bot():
	global kk 
	kk = 1
	x = threading.Thread(target=duble_click)
	threads.append(x)
	x.start()

	x = threading.Thread(target=autoposting)
	threads.append(x)
	x.start()

def autoposting():
	while True:
		a = str(datetime.today().strftime("%H-%M"))
		if a == "10-00":
			posting_in_chat()
			time.sleep(14000)
		elif a == "14-00":
			posting_in_chat()
			time.sleep(14000)
		elif a == "18-00":
			posting_in_chat()
			time.sleep(14000)
		elif a == "22-00":
			posting_in_chat()
			time.sleep(14000)
		elif a == "02-00":
			posting_in_chat()
			time.sleep(14000)
		elif a == "06-00":
			posting_in_chat()
			time.sleep(14000)
		
		time.sleep(60)

def posting_in_chat():
	try:
		conn = sqlite3.connect('main.db')
		cursor = conn.cursor()
		row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
		rows = cursor.execute(f'SELECT * FROM post').fetchone()
		conn.close()
		msg = rows[1]
		text = rows[0]
		msg = msg.split('\n')
		key = types.InlineKeyboardMarkup(row_width=1)
		for i in msg:
			i = i[1:len(i)-1].split("][")
			k = len(i)
			if k == 1:
				i = i[0].split('+')
				key.row(types.InlineKeyboardButton(text=i[0], url=i[1].replace(' ', '')))
			elif k == 2:
				i1 = i[0].split('+')
				i2 = i[1].split('+')
				key.row(
					types.InlineKeyboardButton(text=i1[0], url=i1[1].replace(' ', '')),
					types.InlineKeyboardButton(text=i2[0], url=i2[1].replace(' ', '')),
				)
			elif k == 3:
				i1 = i[0].split('+')
				i2 = i[1].split('+')
				i3 = i[2].split('+')
				key.row(
					types.InlineKeyboardButton(text=i1[0], url=i1[1].replace(' ', '')),
					types.InlineKeyboardButton(text=i2[0], url=i2[1].replace(' ', '')),
					types.InlineKeyboardButton(text=i3[0], url=i3[1].replace(' ', '')),
				)
			else:
				a = int(msg)
		try:
			with open('photo.jpg', 'rb') as photo:
				bot.send_photo(chat_id=row[5], photo=photo, caption=text, parse_mode="HTML", reply_markup=key)
		except:
			with open('video.mp4', 'rb') as photo:
				bot.send_document(chat_id=row[5], data=photo, caption=text, parse_mode="HTML", reply_markup=key)
	except:
		pass

def duble_click():
	global click
	while True:
		click = []
		time.sleep(1.3)

@bot.message_handler(content_types=['photo'])
def tesssst(message):
	file_id = message.json['photo'][0]['file_id']
	print(file_id)

@bot.message_handler(commands=['admin'])
def handler_admin(message):
	chat_id = message.chat.id
	conn = sqlite3.connect('main.db')
	cursor = conn.cursor()
	row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
	if str(chat_id) in row[3] or str(chat_id) in row[4]:
		bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	conn.close()


@bot.message_handler(commands=['start'])
def handler_start(message):
    if message.chat.type == 'private':
        chat_id = message.chat.id
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchall()
        if len(row) == 0:
        	username = message.chat.username
        	try:
        		cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username.lower()}", "User", "0", "0", "0", "0", "0")')
        	except:
        		cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username}", "User", "0", "0", "0", "0", "0")')
        	conn.commit()
        else:
        	try:
        		cursor.execute(f'UPDATE users SET name = "{message.chat.username.lower()}" WHERE user_id = "{chat_id}"')
        		conn.commit()
        	except:
        		pass
        bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
        conn.close()


@bot.message_handler(content_types=['text'])
def messages(message):
	chat_id = message.chat.id
	global kk
	if kk == 0:
		start_bot()
	msg = message.text

	if message.chat.type == 'private':
		conn = sqlite3.connect('main.db')
		cursor = conn.cursor()
		row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchall()
		if len(row) == 0:
			username = message.chat.username
			try:
				cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username.lower()}", "User", "0", "0", "0", "0", "0")')
			except:
				cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username}", "User", "0", "0", "0", "0", "0")')
			conn.commit()

		row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
		if message.chat.type == 'private':
			if str(chat_id) in row[3]  or str(chat_id) in row[4]:
				if msg == 'Статистика':
					bot.send_message(chat_id, 'Собираю информацию...')
					rows = cursor.execute(f'SELECT * FROM users').fetchall()
					bal1 = 0
					bal2 = 0
					bal3 = 0
					end_sale = 0 
					sum_sale = 0
					open_sale = 0
					disput_sale = 0
					for row in rows:
						bal1 += row[3]
						end_sale += row[4] + row[6]
						sum_sale += row[5] + row[7]
					rows = cursor.execute(f'SELECT * FROM sale').fetchall()
					for row in rows:
						bal2 += int(row[5])
						open_sale += 1
					rows = cursor.execute(f'SELECT * FROM dispute').fetchall()
					for row in rows:
						bal3 += row[5]
						disput_sale += 1
					open_sale -= 1
					rows = cursor.execute(f'SELECT * FROM donate').fetchall()
					count_donate = 0
					sum_donate = 0
					for row in rows:
						sum_donate += row[2]
						count_donate += 1
					users = cursor.execute(f'SELECT * FROM users').fetchall()
					bot.send_message(chat_id, f"Общее количество пользователей: {len(users)}\n\nБаланс пользователей: {bal1}\nСумма открытых сделок: {bal2}\nБаланс диспутов: {bal3}\n<b>Общий баланс бота: {bal1+bal2+bal3}</b>\n\nЗавершенных сделок: {end_sale}\nНа сумму: {sum_sale}\nОткрытых споров: {disput_sale}\n\nКол-во донатеров: {count_donate}\nСумма донатов: {sum_donate}")
				elif msg == 'Админы':
					if str(chat_id) in row[3] :
						bot.clear_step_handler_by_chat_id(chat_id)
						send = bot.send_message(chat_id, f"Первый админ: {row[3]}\nВторой админ: {row[4]}\nВыберите какого админа вы хотите поменять", reply_markup=menu.one_two)
						bot.register_next_step_handler(send, edit_admins)
					else:
						bot.send_message(chat_id, "Извините, но эта функция доступна только главному админу")
				elif msg == 'Рассылка':
					send = bot.send_message(chat_id, 'Введите текст рассылки', reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, mail)
				elif msg == 'Изменить баланс':
					send = bot.send_message(chat_id, "Введите id юзера которому надо изменить баланс", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_balance)

				elif msg == 'Токен':
					send = bot.send_message(chat_id, f"Токен: <b>{row[2]}</b>\nЕсли хотите сменить, то оправьте новый токен", parse_mode="HTML", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_qiwi, 'qiwi_api')

				elif msg == 'Номер':
					send = bot.send_message(chat_id, f"Номер: <b>{row[1]}</b>\nЕсли хотите сменить, то оправьте новый номер", parse_mode="HTML", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_qiwi, 'qiwi_num')

				elif msg == 'Токен p2p':
					send = bot.send_message(chat_id, f"Токен p2p: <b>{row[8]}</b>\nЕсли хотите сменить, то оправьте новый токен", parse_mode="HTML", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_qiwi, 'qiwi_p2p')

				elif msg == 'Api btc':
					send = bot.send_message(chat_id, f"Api btc: <b>{row[9]}</b>\nЕсли хотите сменить, то оправьте новый токен", parse_mode="HTML", reply_markup=menu.back)
					bot.clear_step_handler_by_chat_id(chat_id)
					bot.register_next_step_handler(send, edit_qiwi, 'api_key')

				elif msg == 'Api secret btc':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Api secret btc: <b>{row[10]}</b>\nЕсли хотите сменить, то оправьте новый токен", parse_mode="HTML", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_qiwi, 'api_secret')
				
				elif msg == 'Оплата':
					bot.send_message(chat_id, "<b>Настройки оплаты</b>", parse_mode="HTML", reply_markup=menu.qiwi_menu)

				elif msg == 'Назад':
					bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
				elif msg == 'Баланс':
					try:
						mylogin = row[1]
						api_access_token = row[2]
						balances = balance(mylogin,api_access_token)['accounts']
						rubAlias = [x for x in balances if x['alias'] == 'qw_wallet_rub']
						rubBalance = rubAlias[0]['balance']['amount']
						bot.send_message(chat_id, f'Баланс qiwi: {str(rubBalance)}р')
					except:
						bot.send_message(chat_id, f'Ошибка')
				elif msg == 'Канал':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Текущий канал: <b>{row[5]}</b>\nЕсли хотите сменить, то оправьте новую ссылку на канал в формате <b>@name</b>, либо в виде ссылки <b>https://t.me/joinchat/ABCDEabcde</b>", parse_mode="HTML", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_channal)
				elif msg == 'Описание':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Текущее описание: <b>{row[7]}</b>\nЕсли хотите сменить, то оправьте новый текст", parse_mode="HTML", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_help)
				elif msg == 'Комиссия':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Текущая комиссия: <b>{row[6]}</b>\nЕсли хотите сменить, то оправьте новое число от 0 до 50", parse_mode="HTML", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_commission)
				elif msg == 'Статус':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Если вы хотите сменить статус какого-либо юзера, то отправьте мне его ник в формате @name", reply_markup=menu.back)
					bot.register_next_step_handler(send, edit_stat)
				elif msg == 'Автопостинг':
					bot.clear_step_handler_by_chat_id(chat_id)
					send = bot.send_message(chat_id, f"Если хотите сменить, то создайте пост заного, сперва отправьте текст", reply_markup=menu.back)
					bot.register_next_step_handler(send, auto_post1)

				elif msg[:3] == '/id':
					try:
						id = msg[4:]
						row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{id}"').fetchone()
						bot.send_message(chat_id, f"🆔{id}\n🎩 Профиль: @{row[1]}\n\n➖Статус: {row[2]}\n\n💰Ваш баланс: {row[3]}₽\n🛒Покупки - шт | ₽ : {row[4]} | {row[5]}\n🎁Продажи - шт | ₽ : {row[6]} | {row[7]}")
					except:
						bot.send_message(chat_id, 'Юзер не найден')


			if msg == '💬 Помощь':
				bot.send_message(chat_id, row[7], reply_markup=menu.update_name)
			
			elif msg == '🎩Мой профиль':
				row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
				feedback = cursor.execute(f'SELECT * FROM feedback WHERE user_id = {row[0]}').fetchall()
				text = f"<b>🎩 Профиль:</b> @{message.chat.username}\n<b>📝 Статус:</b> {row[2]}\n<b>💰Ваш баланс:</b> {row[3]}₽\n<b>💬Кол-во Отзывов:</b> {len(feedback)}\n\n<b>🤝 Продаж:</b> {row[4]} шт.\n<b>🛒 Покупок:</b> {row[6]} шт.\n<b>💰 Сумма покупок:</b> {row[5]} руб.\n<b>🏦 Сумма продаж:</b> {row[7]} руб."
				bot.send_message(chat_id, text, reply_markup=menu.profile_menu)

			elif msg == '🤝 Мои сделки':
				rows = cursor.execute(f'SELECT * FROM sale WHERE user_id = "{chat_id}"').fetchall()
				a = 0
				if rows != []:
				    for row in rows:
				        text = f'Сделка №{row[0]}\nОт @{row[2]}\nДля @{row[4]}\nСумма: {row[5]}₽'
				        sales = types.InlineKeyboardMarkup(row_width=1)
				        sales.add(
				            types.InlineKeyboardButton(text='Завершить сделку', callback_data='sale_end '+str(row[0])),
				            types.InlineKeyboardButton(text='Открыть спор', callback_data='dispute '+str(row[0])),
				        )
				        bot.send_message(chat_id, text, reply_markup=sales)
				else:
				    a += 1
				rows = cursor.execute(f'SELECT * FROM sale WHERE user_id2 = "{chat_id}"').fetchall()
				if rows != []:
				    for row in rows:
				    	sales = types.InlineKeyboardMarkup(row_width=1)
				    	text = f'Сделка №{row[0]}\nОт @{row[2]}\nДля @{row[4]}\nСумма: {row[5]}₽'
				    	sales.add(
							types.InlineKeyboardButton(text='Отменить сделку', callback_data='sale_back '+str(row[0])),
							types.InlineKeyboardButton(text='Открыть спор', callback_data='dispute '+str(row[0])),
				    	)
				    	bot.send_message(chat_id, text, reply_markup=sales)
				else:
				    a += 1
				if a == 2:
				    bot.send_message(chat_id, 'У вас нет открытых сделок', reply_markup=menu.main_menu)

			elif msg == '🔍 Найти user':
				bot.send_message(chat_id, "Введите никнейм в формате @username")
			elif msg[:1] == "@":
				name = msg[1:]
				row = cursor.execute(f'SELECT * FROM users WHERE name = "{name.lower()}"').fetchone()
				try:
				    garant_user = types.InlineKeyboardMarkup(row_width=3)
				    garant_user.add(
				    	types.InlineKeyboardButton(text='Оформить сделку', callback_data='oplata '+row[0]),
				    	types.InlineKeyboardButton(text='Отзывы', callback_data='feed '+row[0])
				    	)
				    feedback = cursor.execute(f'SELECT * FROM feedback WHERE user_id = {row[0]}').fetchall()
				    text = f"<b>📝 Статус:</b> {row[2]}\n<b>🔎Юзер </b>{msg}\n<b>💬Кол-во Отзывов:</b> {len(feedback)}\n\n<b>🤝 Продаж:</b> {row[4]} шт.\n<b>🛒 Покупок:</b> {row[6]} шт.\n<b>💰 Сумма покупок:</b> {row[5]} руб.\n<b>🏦 Сумма продаж:</b> {row[7]} руб."
				    if row[0] != str(chat_id):
				        bot.send_message(chat_id, text, reply_markup=garant_user)
				    else:
				        bot.send_message(chat_id, text)
				except:
				    bot.send_message(chat_id, "Пользователь не найден")
			elif msg == 'Отмена' or msg == 'Вернуться в главное меню':
				bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
			elif msg == '🎁 Пожертвовать':
				text =  '<b>🎩Накинь монетку в сокровищницу Скруджа, не скупись</b>\n\n'
				text += '🔅<b>Все</b> пожертвования пойдут на Развитие Проекта, закуп рекламы и т.п.\n\n'
				text += '🔅В дальнейшем будут определенные привилегии для <b>Топ-5</b>\n\n'
				text += '🔅Благодарим за любую помощь проекту. Спасибо, что вы с нами!'
				bot.send_message(chat_id, text, reply_markup=menu.donate_menu)

		conn.close()


def auto_post1(message):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена':
			text = "<b>Отправьте ссылку(и) в формате:</b>\n[Текст кнопки + ссылка]\n<pre>Пример:</pre>\n[TGLab + https://t.me/TGLab]\n\n<b>Чтобы добавить несколько кнопок в один ряд, "
			text += "пишите ссылки рядом с предыдущими, не более трех.</b>\n<pre>Формат:</pre>\n[Первый текст + первая ссылка][Второй текст + вторая ссылка]\n\n"
			text += "<b>Чтобы добавить несколько кнопок в строчку, пишите новые ссылки с новой строки.</b>\n<pre>Формат:</pre>\n[Первый текст + первая ссылка]\n[Второй текст + вторая ссылка]"

			send = bot.send_message(chat_id, text, reply_markup=menu.back)
			bot.register_next_step_handler(send, auto_post2, message.text)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def auto_post2(message, text):
	chat_id = message.chat.id
	try:
		msg = message.text
		if msg == 'Отмена':
			bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
		else:
			save = msg
			msg = msg.split('\n')
			key = types.InlineKeyboardMarkup(row_width=1)
			for i in msg:
				i = i[1:len(i)-1].split("][")
				k = len(i)
				if k == 1:
					i = i[0].split('+')
					key.row(types.InlineKeyboardButton(text=i[0], url=i[1].replace(' ', '')))
				elif k == 2:
					i1 = i[0].split('+')
					i2 = i[1].split('+')
					key.row(
						types.InlineKeyboardButton(text=i1[0], url=i1[1].replace(' ', '')),
						types.InlineKeyboardButton(text=i2[0], url=i2[1].replace(' ', '')),
					)
				elif k == 3:
					i1 = i[0].split('+')
					i2 = i[1].split('+')
					i3 = i[2].split('+')
					key.row(
						types.InlineKeyboardButton(text=i1[0], url=i1[1].replace(' ', '')),
						types.InlineKeyboardButton(text=i2[0], url=i2[1].replace(' ', '')),
						types.InlineKeyboardButton(text=i3[0], url=i3[1].replace(' ', '')),
					)
				else:
					a = int(msg)
			
			bot.send_message(chat_id, text, reply_markup=key)

			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			try:
				cursor.execute(f'DELETE FROM post')
			except:
				pass
			cursor.execute(f'INSERT INTO post VALUES ("{text}", "{save}")')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "<b>Главное меню</b>", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def edit_stat(message):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена' and message.text[0] == '@':
			send = bot.send_message(chat_id, f"Хорошо, отправьте теперь его новый статус, не длинее 10 символов", reply_markup=menu.back)
			bot.register_next_step_handler(send, edit_stat2, message.text[1:])
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_stat2(message, name):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена' and len(message.text) <= 10:
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			cursor.execute(f'UPDATE users SET status = "{message.text}" WHERE name = "{name}"')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Статус успешно обновлен", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_commission(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		if msg != 'Отмена' and int(msg) >= 0 and int(msg) <= 50:
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			i = int(message.text)
			cursor.execute(f'UPDATE settings SET commission = {i} WHERE id = 1')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Комиссия успешно обновлена", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_help(message):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена':
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			cursor.execute(f'UPDATE settings SET help = "{message.text}" WHERE id = 1')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Описание успешно обновлено", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)


def edit_channal(message):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена':
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			cursor.execute(f'UPDATE settings SET channal = "{message.text}" WHERE id = 1')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Канал успешно обновлен", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_qiwi(message, what):
	chat_id = message.chat.id
	try:
		if message.text != 'Отмена':
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			cursor.execute(f'UPDATE settings SET {what} = "{message.text}" WHERE id = 1')
			conn.commit()
			conn.close()
			bot.send_message(chat_id, "Настройки оплаты успешно обновлены", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)


def edit_balance(message):
	chat_id = message.chat.id
	try:
		m = message.text
		send = bot.send_message(chat_id, "Введите число, на него поменяется баланс", reply_markup=menu.back)
		bot.register_next_step_handler(send, edit_balance2, m)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)
    		
    		
def edit_balance2(message, user_id):
	chat_id = message.chat.id
	try:
		conn = sqlite3.connect("main.db")
		cursor = conn.cursor()
		cursor.execute(f"UPDATE users SET balance = {int(message.text)} WHERE user_id = {user_id}")
		conn.commit()
		bot.send_message(chat_id, "Баланс успешно обновлен", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def mail(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		if msg == 'Отмена':
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)
		else:
			bot.send_message(chat_id, msg)
			send = bot.send_message(chat_id, 'Отправьте "ПОДТВЕРДИТЬ" для подтверждения', reply_markup=menu.back)
			bot.register_next_step_handler(send, mail_true, msg)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def mail_true(message, text):
	chat_id = message.chat.id
	try:
		if message.text.lower() == 'подтвердить':
			bot.send_message(chat_id, "Рассылка началась", reply_markup=menu.admin_menu)
			time.sleep(1)
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			k = 0
			rows = cursor.execute(f'SELECT * FROM users').fetchall()
			for row in rows:
				try:
					bot.send_message(row[0], text)
				except:
					pass
				time.sleep(1)
				k += 1
			bot.send_message(chat_id, f"Рассылку получило {str(k)} человек")
			conn.close()
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)

	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_admins(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		if msg == 'Первый':
			send = bot.send_message(chat_id, f"Введите id нового админа", reply_markup=menu.back)
			bot.register_next_step_handler(send, edit_admin, 1)
		elif msg == 'Второй':
			send = bot.send_message(chat_id, f"Введите id нового админа", reply_markup=menu.back)
			bot.register_next_step_handler(send, edit_admin, 2)
		else:
			bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)

	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.admin_menu)

def edit_admin(message, who):
	chat_id = message.chat.id
	try:
		id = int(message.text)
		conn = sqlite3.connect('main.db')
		cursor = conn.cursor()
		if who == 1:
			cursor.execute(f'UPDATE settings SET admin = "{str(id)}" WHERE id = 1')
			conn.commit()
		else:
			cursor.execute(f'UPDATE settings SET admin2 = "{str(id)}" WHERE id = 1')
			conn.commit()
		conn.close()
		bot.send_message(chat_id, "Админ успешно установлен", reply_markup=menu.admin_menu)
	except:
		bot.send_message(chat_id, "<b>Меню админа</b>", parse_mode="HTML", reply_markup=menu.admin_menu)

@bot.callback_query_handler(func=lambda call: True)
def handler_call(call):
	chat_id = call.message.chat.id
	message_id = call.message.message_id	
	global click
	if chat_id in click:
		bot.send_message(chat_id, 'Не так быстро')
	else:
		try:
			print(call.data)
			click.append(chat_id)
			a = call.data.split()
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchall()
			if len(row) == 0:
				username = message.chat.username
				try:
					cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username.lower()}", "User", "0", "0", "0", "0", "0")')
				except:
					cursor.execute(f'INSERT INTO users VALUES ("{chat_id}", "{username}", "User", "0", "0", "0", "0", "0")')
				conn.commit()

			row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()

			if a[0] == 'how':
				text = '<b>Краткая инструкция:</b>\nДля начала необходимо пополнить баланс\nДалее нажимаете "🔍 Найти user"\nВводите @username продавца\nЗатем снизу появится кнопка "Оформить сделку"\nПосле получения и проверки товара Вы можете отправить деньги и закрыть сделку\n\n'
				text += 'В случае если Вам дали невалидный товар и продавец отказывается заменять или отклонять сделку\nВы можете открыть спор и решить вопрос через Тех.Поддержку\n\nЕсли вы изменили свой @username, то нажмите /start'

				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=text,
					parse_mode="HTML",
					reply_markup=menu.clear_inline
				)

			elif a[0] == 'input':
				bot.send_message(chat_id, "Выберите платежную систему: ", reply_markup=menu.input_menu)

			elif a[0] == 'input_qiwi':
				send = bot.send_message(chat_id, "Введите сумму пополнения(от 10 руб)")
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, input_qiwi)

			elif a[0] == 'donate':
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					reply_markup=menu.donate
				)

			elif a[0] == 'donate_balance':
				send = bot.send_message(chat_id, "Введите сумму доната")
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, donate_balance)

			elif a[0] == 'donate_qiwi':
				send = bot.send_message(chat_id, "Введите сумму доната(от 10 руб)")
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, donate_qiwi)

			elif a[0] == 'input_btc':
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					parse_mode="HTML",
					reply_markup=menu.clear_inline
				)
				text = 'Введите сумму пополнения\nМинимальная сумма - 1000р'
				send = bot.send_message(chat_id, text, reply_markup=menu.back)
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, input_btc)

			elif a[0] == 'check_btc':
				r = requests.get('https://blockchain.info/q/addressbalance/' + a[1])
				s = r.text
				if float(s) >= float(a[2]):
					try:
						bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Баланс успешно пополнен на {a[2]}btc!', reply_markup=menu.clear_inline)
					except:
						pass
					balance = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
					balance = balance[3] + int(a[3])
					cursor.execute(f'UPDATE users SET balance = {balance} WHERE user_id = "{chat_id}"')
					conn.commit()
				else:
					bot.send_message(chat_id, 'Оплата не найдена')

			elif a[0] == 'top_donate':
				text = f"<b>🏆Топ донатеров:\n\n"
				rows = cursor.execute(f'SELECT * FROM donate ORDER BY sum DESC').fetchall()
				premium = ['🥇', '🥈', '🥉', '🏅', '🏅']
				l = len(rows)
				if l > 10:
					l = 10
				for i in range(l):
					if i <= len(premium)-1:
						text += f"{premium[i]}{i+1}) @{rows[i][1]} {rows[i][2]}₽\n"
					else:
						text += f"🎗{i+1}) @{rows[i][1]} {rows[i][2]}₽\n"
				text += '\n⚠️ОСТОРОЖНО!</b>\nЖертвуя в данный Проект, ты автоматически становишься частью <b>Утиной Империи.</b>'
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=text
				)

			elif a[0] == 'check_qiwi_donate':
				try:
					rowss = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
					headers={'Authorization': 'Bearer '+rows[8],
						'Accept': 'application/json',
						'Content-Type': 'application/json',
					}

					g = requests.get('https://api.qiwi.com/partner/bill/v1/bills/'+a[1], headers=headers)
					res = g.json()['status']['value']
					if res == 'PAID':
						row = cursor.execute(f'SELECT * FROM donate WHERE user_id = "{chat_id}"').fetchone()
						if row != None:
							cursor.execute(f'UPDATE donate SET sum = {row[2]+int(a[2])} WHERE user_id = "{chat_id}"')
						else:
							cursor.execute(f'INSERT INTO donate VALUES ({chat_id}, "{call.message.chat.username}", {a[2]})')
						rows = cursor.execute(f'SELECT * FROM donate ORDER BY sum DESC').fetchall()
						k = 0 
						for i in range(len(rows)):
							if rows[i][0] == chat_id:
								k = i+1
								break
						conn.commit()
						bot.delete_message(chat_id, message_id)
						text = f"<b>🎉Поступил донат!\n\n🔑 Частью Утиной Империи становится: @{call.message.chat.username}\n💰 Сумма: </b>{a[2]} руб.\n<b>🏅 Он занимает №{k} место в топе Донатеров</b>\n\n🎩Скрудж лично снимает шляпу перед тобой."
						text2 = "<b>🎩Добро пожаловать в Утиную Империю\n\n▪️*цзиньк*</b>, Монета упала в хранилище с золотом\n\n▪️ Благодарю тебя за донат, и снимаю перед тобой шляпу\n\n🖤 Эти средства пойдут на <b>Развитие Проекта!</b>"
						bot.send_message(chat_id, text2)
						try:
							bot.send_message(rowss[5], text, reply_markup=menu.donat_keyboard)
						except:
							try:
								bot.send_message(rowss[3], f'Канал {rowss[5]} недействителен')
								bot.send_message(rowss[4], f'Канал {rowss[5]} недействителен')
							except:
								pass
					elif res == 'WAITING':
						bot.send_message(chat_id, "❌ Счёт не оплачен")
					else:
						bot.delete_message(chat_id, message_id)
						bot.send_message(chat_id, "⌛️ Время ожидания истекло")
				except:
					bot.delete_message(chat_id, message_id)

			elif a[0] == 'check_qiwi':
				try:
					rows = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
					headers={'Authorization': 'Bearer '+rows[8],
						'Accept': 'application/json',
						'Content-Type': 'application/json',
					}

					g = requests.get('https://api.qiwi.com/partner/bill/v1/bills/'+a[1], headers=headers)
					res = g.json()['status']['value']
					if res == 'PAID':
						row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
						cursor.execute(f'UPDATE users SET balance = {row[3]+int(a[2])} WHERE user_id = "{chat_id}"')
						conn.commit()
						bot.delete_message(chat_id, message_id)
						bot.send_message(chat_id, f"Баланс успешно пополнен на {a[2]}р")
					elif res == 'WAITING':
						bot.send_message(chat_id, "❌ Счёт не оплачен")
					else:
						bot.delete_message(chat_id, message_id)
						bot.send_message(chat_id, "⌛️ Время ожидания истекло")
				except:
					bot.delete_message(chat_id, message_id)

			elif a[0] == 'output':
				send = bot.send_message(chat_id, 'Введите сумму Вывода\nМинимальная сумма - 100р', reply_markup=menu.back)
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, output_sum)

			elif a[0] == 'output_true':
				try:
					api_access_token = row[2]
					row = cursor.execute(f'SELECT * FROM output WHERE id = {int(a[1])}').fetchone()
					num = row[2]
					sum = row[3]
					cursor.execute(f'DELETE FROM output WHERE id = {int(a[1])}')
					conn.commit()
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text,
						reply_markup=menu.clear_inline
					)
					send_p2p(api_access_token, num, str(int(int(sum)*0.98)))
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text+"\n\nВывод выполнен!",
						reply_markup=menu.clear_inline
					)
					try:
						bot.send_message(row[1], "Заявка на вывод подтвержена, деньги поступят в течении 2 минут")
					except:
						pass
				except:
					bot.send_message(chat_id, 'Ошибка вывода киви:(')
			elif a[0] == 'update':
				try:
					cursor.execute(f'UPDATE users SET name = "{message.chat.username}" WHERE user_id = "{chat_id}"')
					conn.commit()
				except:
					pass
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					reply_markup=menu.clear_inline
				)
				bot.send_message(chat_id, 'Никнейм успешно обновлен')
			elif a[0] == 'output_false':
				try:
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text+"\n\nВывод отменен!",
						reply_markup=menu.clear_inline
					)
					cursor.execute(f'DELETE FROM output WHERE id = {int(a[1])}')
					conn.commit()
				except:
					pass

			elif a[0] == 'check':
				check = func.check_payment(chat_id, a[1])
				if check > 0:
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text,
						reply_markup=menu.clear_inline
					)
					text = f'✅ Оплата прошла\nСумма: {check}р'
					bot.send_message(chat_id, text, reply_markup=menu.main_menu)
				else:
					bot.send_message(chat_id, 'Оплата не найдена')

			elif a[0] == 'oplata':
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					reply_markup=menu.clear_inline
				)
				send = bot.send_message(chat_id, 'Введите сумму сделки\nМинимальная сумма - 10р', reply_markup=menu.back)
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, open_sell, a[1])

			elif a[0] == 'sale_back' or a[0] == 'dispute' or a[0] == 'sale_end':
				sales = types.InlineKeyboardMarkup(row_width=2)
				sales.add(
					types.InlineKeyboardButton(text='Да', callback_data='1'+call.data),
					types.InlineKeyboardButton(text='Нет', callback_data='back'),
				)

				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text+'\nУверены?',
					reply_markup=sales
				)

			elif call.data == 'back':
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					reply_markup=menu.clear_inline
				)
				bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
				
			elif a[0] == '1dispute':
				b = func.dispute(a[1], chat_id)
				if b != 'Ошибка':
					msg = f'Сделка №{a[1]}\nОт @{b[1]} для @{b[3]}\nСумма: {b[4]}₽\nСтатус: <b>Запрос на возврат средств</b>'
					bot.edit_message_text(
					    chat_id=chat_id,
					    message_id=message_id,
					    text=msg,
					    reply_markup=menu.clear_inline,
					    parse_mode="HTML"
					)
					sales = types.InlineKeyboardMarkup(row_width=2)
					sales.add(
					    types.InlineKeyboardButton(text='@'+b[1], callback_data='@0 '+a[1]),
					    types.InlineKeyboardButton(text='@'+b[3], callback_data='@1 '+a[1]),
					)
					try:
					    bot.send_message(row[3], msg+'\nКому уйдут деньги?', reply_markup=sales, parse_mode="HTML")
					    bot.send_message(row[4], msg+'\nКому уйдут деньги?', reply_markup=sales, parse_mode="HTML")
					except:
						pass

					try:
					    bot.send_message(b[2], msg, parse_mode="HTML")
					except:
					    pass
					b = 0
					try:
						bot.send_message(row[5], msg, parse_mode="HTML")
					except:
						b = 10
					if b == 10:
						try:
							bot.send_message(row[3], f'Канал {row[5]} недействителен')
							bot.send_message(row[4], f'Канал {row[5]} недействителен')
						except:
							pass
				else:
					bot.edit_message_text(
					    chat_id=chat_id,
					    message_id=message_id,
					    text=call.message.text+'\nОшибка',
					    reply_markup=menu.clear_inline
					)
			elif a[0] == '@0' or a[0] == '@1':
				who = a[0]
				bot.edit_message_text(
				    chat_id=chat_id,
				    message_id=message_id,
				    text=call.message.text,
				    reply_markup=menu.clear_inline
				)
				info = func.cancel_dispute(a[1], int(who[1:]))
				try:
				    bot.send_message(info[0], info[2], parse_mode="HTML")
				except:
				    pass
				try:
				    bot.send_message(info[2], info[2], parse_mode="HTML")
				except:
				    pass
				bot.send_message(chat_id, info[2], parse_mode="HTML") 
				b = 0
				try:
					bot.send_message(row[5], info[2], parse_mode="HTML")
				except:
					b = 10
				if b == 10:
					try:
						bot.send_message(row[3], f'Канал {row[5]} недействителен')
						bot.send_message(row[4], f'Канал {row[5]} недействителен')
					except:
						pass

			elif a[0] == '1sale_end':
				text = func.sale_end(a[1])
				if text[0] == 'Ошибка':
					bot.edit_message_text(
					    chat_id=chat_id,
					    message_id=message_id,
					    text=text[0],
					    reply_markup=menu.clear_inline,
					    parse_mode="HTML"
					)
				else:
					sales = types.InlineKeyboardMarkup(row_width=2)
					sales.add(
					    types.InlineKeyboardButton(text='Оставить отзыв', callback_data='feedback '+str(text[1])),
					    types.InlineKeyboardButton(text='Скрыть', callback_data='back'),
					)
					bot.edit_message_text(
					    chat_id=chat_id,
					    message_id=message_id,
					    text=text[0],
					    reply_markup=sales,
					    parse_mode="HTML"
					)
					b = 0
					try:
						bot.send_message(row[5], text[0], parse_mode="HTML")
					except:
						b = 10
					if b == 10:
						try:
							bot.send_message(row[3], f'Канал {row[5]} недействителен')
							bot.send_message(row[4], f'Канал {row[5]} недействителен')
						except:
							pass
					try:
					    bot.send_message(text[1], text[0], parse_mode="HTML")
					except:
					    pass
			elif a[0] == 'feedback':
				bot.edit_message_text(
					chat_id=chat_id,
					message_id=message_id,
					text=call.message.text,
					reply_markup=menu.clear_inline
					)
				send = bot.send_message(chat_id, 'Введите текст отзыва', reply_markup=menu.back)
				bot.clear_step_handler_by_chat_id(chat_id)
				bot.register_next_step_handler(send, feedback, a[1])

			elif a[0] == 'feed':
				rows = cursor.execute(f'SELECT * FROM feedback WHERE user_id = {a[1]}').fetchall()
				text = '🗣\n<b>Отзывы:</b>\n\n'
				k = 1
				for row in rows:
					text += f'<b>✅ Отзыв №{k}</b> от @{row[2]}\n└{row[3]}\n\n'
					#text += f'<b>От</b> @{row[2]} <b>для</b> @{row[1]}\n<pre>{row[3]}</pre>'
					k += 1
				bot.send_message(chat_id, text, parse_mode="HTML")

			elif a[0] == '1sale_back':
				text = func.sale_back(int(a[1]))
				if text[0] == '❌Ошибка':
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=call.message.text+"\n\n"+text[0],
						reply_markup=menu.clear_inline
					)
				else:
					bot.edit_message_text(
						chat_id=chat_id,
						message_id=message_id,
						text=text[0],
						reply_markup=menu.clear_inline,
						parse_mode="HTML"
					)
					b = 0
					try:
						bot.send_message(row[5], text[0], parse_mode="HTML")
					except:
						b = 10
					if b == 10:
						try:
							bot.send_message(row[3], f'Канал {row[5]} недействителен')
							bot.send_message(row[4], f'Канал {row[5]} недействителен')
						except:
							pass
					try:
						bot.send_message(text[1], text[0], parse_mode="HTML")
					except:
						pass
			conn.close()
		except Exception as e:
			print(repr(e))

def input_btc(message):
	chat_id = message.chat.id
	try:
		sum = int(message.text)
		if sum >= 1000:
			create_bill_btc(chat_id, str(sum))
		else:
			bot.send_message(chat_id, "Минимальная сумма пополнения 1000р", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def create_bill_btc(chat_id, summ):
	conn = sqlite3.connect('main.db')
	cursor = conn.cursor()
	row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
	api_key = row[9]
	api_secret = row[10]
	if len(api_key) > 5 and len(api_secret) > 5:
		client = Client(api_key, api_secret)
		account_id = client.get_primary_account()['id']
		sum = int(summ) + 100
		btc_price = round(float((client.get_buy_price(currency_pair='BTC-RUB')["amount"])))
		sum = float(str(sum / btc_price)[:10]) 
		address_for_tranz = client.create_address(account_id)['address']
		key = types.InlineKeyboardMarkup()
		key.add(types.InlineKeyboardButton(text='Проверить оплату', callback_data=f'check_btc {str(address_for_tranz)} {str(sum)} {str(summ)}'))
		key.add(types.InlineKeyboardButton(text = '⏪ Назад', callback_data = 'back'))
		bot.send_message(chat_id, f'🏛 Отправьте {str(sum)} BTC на данный кошелек\n\n<b><pre>{str(address_for_tranz)}</pre></b>\n\nЗачисление производится после 3 подтверждений', parse_mode="HTML", reply_markup=key)
	else:
		bot.send_message(chat_id, 'Оплата в btc временно недоступна', reply_markup=menu.main_menu)
	conn.close()

def donate_balance(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		s = int(msg)
		if s >= 1:
			check = func.check_balance(chat_id, s)
			if check == 1:
				conn = sqlite3.connect('main.db')
				cursor = conn.cursor()
				row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
				cursor.execute(f'UPDATE users SET balance = {row[3]-s} WHERE user_id = "{chat_id}"')
				
				row = cursor.execute(f'SELECT * FROM donate WHERE user_id = "{chat_id}"').fetchone()
				if row != None:
					cursor.execute(f'UPDATE donate SET sum = {row[2]+s} WHERE user_id = "{chat_id}"')
				else:
					cursor.execute(f'INSERT INTO donate VALUES ({chat_id}, "{message.chat.username}", {s})')
				rowss = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
				rows = cursor.execute(f'SELECT * FROM donate ORDER BY sum DESC').fetchall()
				k = 0 
				for i in range(len(rows)):
					if rows[i][0] == chat_id:
						k = i+1
						break
				conn.commit()
				conn.close()
				text = f"<b>🎉Поступил донат!\n\n🔑 Частью Утиной Империи становится: @{message.chat.username}\n💰 Сумма: </b>{s} руб.\n<b>🏅 Он занимает №{k} место в топе Донатеров</b>\n\n🎩Скрудж лично снимает шляпу перед тобой."
				text2 = "<b>🎩Добро пожаловать в Утиную Империю\n\n▪️*цзиньк*</b>, Монета упала в хранилище с золотом\n\n▪️ Благодарю тебя за донат, и снимаю перед тобой шляпу\n\n🖤 Эти средства пойдут на <b>Развитие Проекта!</b>"
				bot.send_message(chat_id, text2)
				try:
					bot.send_message(rowss[5], text, reply_markup=menu.donat_keyboard)
				except:
					try:
						bot.send_message(rowss[3], f'Канал {rowss[5]} недействителен')
						bot.send_message(rowss[4], f'Канал {rowss[5]} недействителен')
					except:
						pass
			else:
				bot.send_message(chat_id, 'Недостаточно средств')
		else:
			bot.send_message(chat_id, "Минимальная сумма доната - 1р", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def donate_qiwi(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		i = int(msg)
		if i >= 10 :
			a = datetime.now() + timedelta(minutes=15) + timedelta(hours=12)
			a = str(a.strftime("%Y-%m-%dT%H:%M:%S+03:00"))

			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()

			headers={'Authorization': 'Bearer '+row[8],
				'Accept': 'application/json',
				'Content-Type': 'application/json',
			}
			
			params={'amount': {'value': float(msg), 'currency': 'RUB'},
				'comment': '', 
				'expirationDateTime': a, 
				'customer': {}, 
				'customFields': {},        
				}
			id = random.randint(1, 999999999)
			params = json.dumps(params)
			g = requests.put('https://api.qiwi.com/partner/bill/v1/bills/'+str(id),
				headers=headers,
				data=params)
			url = g.json()['payUrl']
			

			oplata = types.InlineKeyboardMarkup(row_width=1)
			oplata.add(
				types.InlineKeyboardButton(text='🥝 Оплатить', url=url),
				types.InlineKeyboardButton(text='🔎 Проверить оплату', callback_data='check_qiwi_donate '+str(id)+' '+msg),
				types.InlineKeyboardButton(text='🚫 Отменить', callback_data='back'),
			)
			conn.close()
			bot.send_message(chat_id, "Оплатите счет ниже", reply_markup=oplata)
		else:
			bot.send_message(chat_id, "Минимальная сумма доната - 10р", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def input_qiwi(message):
	chat_id = message.chat.id
	try:
		msg = message.text
		i = int(msg)
		if i >= 10 :
			a = datetime.now() + timedelta(minutes=15) + timedelta(hours=12)
			a = str(a.strftime("%Y-%m-%dT%H:%M:%S+03:00"))

			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()

			headers={'Authorization': 'Bearer '+row[8],
				'Accept': 'application/json',
				'Content-Type': 'application/json',
			}
			
			params={'amount': {'value': float(msg), 'currency': 'RUB'},
				'comment': '', 
				'expirationDateTime': a, 
				'customer': {}, 
				'customFields': {},        
				}
			id = random.randint(1, 999999999)
			params = json.dumps(params)
			g = requests.put('https://api.qiwi.com/partner/bill/v1/bills/'+str(id),
				headers=headers,
				data=params)
			url = g.json()['payUrl']
			

			oplata = types.InlineKeyboardMarkup(row_width=1)
			oplata.add(
				types.InlineKeyboardButton(text='🥝 Оплатить', url=url),
				types.InlineKeyboardButton(text='🔎 Проверить оплату', callback_data='check_qiwi '+str(id)+' '+msg),
				types.InlineKeyboardButton(text='🚫 Отменить', callback_data='back'),
			)
			conn.close()
			bot.send_message(chat_id, "Оплатите счет ниже", reply_markup=oplata)
		else:
			bot.send_message(chat_id, "Минимальная сумма пополнения - 10р", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def output_sum(message):
	chat_id = message.chat.id
	try:
		sum = int(message.text)
		if sum >= 100:
			sum = str(sum)
			send = bot.send_message(chat_id, 'Введите Qiwi кошелек в формате 79876543210, номер карты или биткоин адрес', reply_markup=menu.back)
			bot.register_next_step_handler(send, output_num, sum)
		else:
			send = bot.send_message(chat_id, 'Минимальная сумма - 100р', reply_markup=menu.back)
			bot.register_next_step_handler(send, output_sum)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def output_num(message, sum):
	chat_id = message.chat.id
	try:
		num = message.text
		if num != 'Отмена':
			check = func.check_balance(chat_id, int(sum))
			if check == 1:
				conn = sqlite3.connect('main.db')
				cursor = conn.cursor()
				
				row = cursor.execute(f'SELECT * FROM output WHERE chat_id = "0"').fetchone()
				id = row[0]
				cursor.execute(f'UPDATE output SET id = {id+1} WHERE chat_id = "0"')
				cursor.execute(f'INSERT INTO output VALUES ({id}, "{chat_id}", "{num}", "{sum}")')

				balance = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
				balance = balance[3] - int(sum)
				cursor.execute(f'UPDATE users SET balance = {balance} WHERE user_id = "{chat_id}"')
				conn.commit()

				row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
				key = types.InlineKeyboardMarkup(row_width=2)
				key.add(
					types.InlineKeyboardButton(text='Подтвердить', callback_data='output_true '+str(id)),
					types.InlineKeyboardButton(text='Отменить', callback_data='output_false '+str(id)),
				)
				try:
					bot.send_message(row[3], f'Вывод\nid {chat_id}\nUser: @{message.chat.username}\nСумма: {sum}\nРеквизиты: {num}\nПодтвердить?', reply_markup=key)
				except:
					pass
				bot.send_message(chat_id, f"Заявка на вывод успешно оставлена\nСумма: {sum}\nНомер: {num}", reply_markup=menu.main_menu)

			else:
				bot.send_message(chat_id, "Недостаточно средств", reply_markup=menu.main_menu)
		else:
			bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)

def feedback(message, chat_id2):
	chat_id = message.chat.id
	try:
		msg = message.text
		if msg != 'Отмена' or msg != '/start':
			if len(msg) < 70:
				text = func.feedback(chat_id2, message.chat.username, msg)
				bot.send_message(chat_id, text, reply_markup=menu.main_menu)
				conn = sqlite3.connect('main.db')
				cursor = conn.cursor()
				row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
				try:
					bot.send_message(row[5], text, parse_mode="HTML")
				except:
					b = 10
				if b == 10:
					try:
						bot.send_message(row[3], f'Канал {row[5]} недействителен')
						bot.send_message(row[4], f'Канал {row[5]} недействителен')
					except:
						pass
				try:
					bot.send_message(chat_id2, text, parse_mode="HTML")
				except:
					pass
				
				else:
					send = bot.send_message(chat_id, 'Введите текст отзыва короче', reply_markup=menu.back)
					bot.register_next_step_handler(send, feedback, chat_id2)
		else:
			bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "Ошибка", reply_markup=menu.main_menu)
	
def open_sell(message, id):
	chat_id = message.chat.id
	time.sleep(0.1)
	try:
		summ = int(message.text)
		name = message.chat.username
		if summ >= 10:
			conn = sqlite3.connect('main.db')
			cursor = conn.cursor()
			row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
			comsa = int(summ*row[6]//100)
			check = func.check_balance(chat_id, summ)
			if check == 1:
				a = func.open_sell(chat_id, id, summ)
				bot.send_message(chat_id, f"Сделка №{a[0]}\nСумма: {summ-comsa}₽\nОт @{name} Для @{a[1]}\nСтатус: <b>В работе</b>", parse_mode="HTML", reply_markup=menu.main_menu)
				try:
					bot.send_message(id, f"Сделка №{a[0]}\nСумма: {summ-comsa}₽\nОт @{name} Для @{a[1]}\nСтатус: <b>В работе</b>", parse_mode="HTML")
				except:
					pass
				try:
					bot.send_message(row[5], f"Сделка №{a[0]}\nСумма: {summ-comsa}₽\nОт @{name} Для @{a[1]}\nСтатус: <b>В работе</b>", parse_mode="HTML")
				except:
					a = 10
				if a == 10:
					try:
						bot.send_message(row[3], f'Канал {row[5]} недействителен')
						bot.send_message(row[4], f'Канал {row[5]} недействителен')
					except:
						pass
			else:
				bot.send_message(chat_id, "Недостаточно средств", reply_markup=menu.main_menu)
		else:
			bot.send_message(chat_id, "Минимальная сумма сделки - 10р", reply_markup=menu.main_menu)
	except:
		bot.send_message(chat_id, "<b>Главное меню</b>", parse_mode="HTML", reply_markup=menu.main_menu)



def balance(login, api_access_token):
    s = requests.Session()
    s.headers['Accept']= 'application/json'
    s.headers['authorization'] = 'Bearer ' + api_access_token  
    b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + login + '/accounts')
    return b.json()
# Перевод на QIWI Кошелек
def send_p2p(api_access_token, to_qw, sum_p2p):
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + api_access_token
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept'] = 'application/json'
    postjson = {"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"},"fields":{"account":""}}
    postjson['id'] = str(int(time.time() * 1000))
    postjson['sum']['amount'] = sum_p2p
    postjson['sum']['currency'] = '643'
    postjson['fields']['account'] = to_qw
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments',json = postjson)
    return res.json()
bot.polling(none_stop=True)
"""
while True:
	try:
		bot.polling(none_stop=True)
	except:
		time.sleep(10)

"""