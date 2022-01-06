# -*- coding: utf-8 -*-
import telebot
import datetime
from telebot import types, apihelper
import sqlite3
import config
import random
import time
import json
from light_qiwi import Qiwi, OperationType
import keyboards
import requests
import transliterate
import sys
import time
from PIL import Image


bot = telebot.TeleBot(config.bot_token)
bot2 = telebot.TeleBot('токен второго бота')

@bot.message_handler(commands=['start'])
def start_message(message):
	userid = str(message.chat.id)
	username = str(message.from_user.username)
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	q = q.execute('SELECT * FROM user WHERE id IS '+str(userid))
	row = q.fetchone()
	if row is None:
		q.execute("INSERT INTO user (id,balance,ref,ref_colvo,win,game,luls,status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(userid,'0','0','0','0','0','0','Активен'))
		connection.commit()
		if message.text[7:] != '':
			if message.text[7:] != userid:
				sql = 'update user set ref = ? where id = ?'
				q.execute(sql, (message.text[7:], userid))
				connection.commit()
				sql = "update user set ref_colvo =ref_colvo + 1 where id = ?"
				q.execute(sql, (message.text[7:], ))
				connection.commit()
				bot.send_message(message.text[7:], f'Новый реферал! <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML')
		msg = bot.send_message(message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		if row[3] == '0':
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q = q.execute(f'SELECT status FROM user WHERE id = {message.chat.id}')
			botb = q.fetchone()
			#text = ''
			#keyboard = types.InlineKeyboardMarkup()
			#for i in row:
	#			text = f'{text}<a href="{i[2]}">{i[1]}</a>\n➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖\n'
#			keyboard.add(types.InlineKeyboardButton(text='💰 Купить ссылку',callback_data='buy_reklama'))
#			bot.send_message(message.chat.id, f'''<b>💎 Реклама:</b>

			if botb[0] == 'Активен':	
#''' ,parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)
				bot.send_message(message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)
			else:	
				pass

		else:
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q = q.execute(f'SELECT status FROM user WHERE id = {message.chat.id}')
			botb = q.fetchone()
			#text = ''
			#keyboard = types.InlineKeyboardMarkup()
			#for i in row:
				#text = f'{text}<a href="{i[2]}">{i[1]}</a>\n➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖\n'
			#keyboard.add(types.InlineKeyboardButton(text='💰 Купить ссылку',callback_data='buy_reklama'))
			#bot.send_message(message.chat.id, f'''<b>💎 Реклама:</b>

#{text}
#''' ,parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)
			if botb[0] == 'Активен':
				bot.send_message(message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)
			else:	
				pass

@bot.message_handler(content_types=['text'])
def send_text(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	q = q.execute(f'SELECT status FROM user WHERE id = {message.chat.id}')
	botb = q.fetchone()
	if botb[0] == 'Активен':
		if message.text.lower() == '/admin':
			if message.chat.id == config.admin:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text=f'🏆 Топ 10 Игры',callback_data='топигры'),types.InlineKeyboardButton(text=f'🏆 Топ 10 Рефералов',callback_data='топигры'))
				bot.send_message(message.chat.id, '<b>Привет, админ!</b>',parse_mode='HTML', reply_markup=keyboard)
				msg = bot.send_message(message.chat.id, '<b>Привет, админ!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
		
		elif message.text.lower() == 'пользователи':
			if message.chat.id == config.admin:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Найти пользователя по @username',callback_data='admin_search_user'))
				keyboard.add(types.InlineKeyboardButton(text='Найти пользователя по ID',callback_data='asdasdasdasdasd'))
				bot.send_message(message.chat.id, '<b>Нажми на кнопку</b>',parse_mode='HTML', reply_markup=keyboard)

		elif message.text.lower() == 'статистика':
			if message.chat.id == config.admin:
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				count_users = q.execute(f"SELECT count(id) from user").fetchone()[0]
				balans_users = q.execute("select sum(balance) from user").fetchone()[0]
				q.execute("SELECT balance FROM winers where id is " + str(1))
				winers = q.fetchone()
				dohod = int(balans_users) / 100 * 5
				
				bot.send_message(message.chat.id, f'''<i>Всего пользователей:</i> <code>{count_users}</code>

	<b>Баланс пользователей:</b> <code>{balans_users}</code>
	<b>Прибыль:</b> <code>{winers[0]}</code>

	''',parse_mode='HTML')
				q.close()
				connection.close()

		elif message.text.lower() == 'настройки':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, 'Введите id игры')
				bot.register_next_step_handler(msg, editgame2)

		elif message.text.lower() == 'рассылка':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, 'Введите текст рассылки')
				bot.register_next_step_handler(msg, send_photoorno)



		elif message.text.lower() == 'отмена':
			bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)


		elif message.text.lower() == '📜 информация':
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			balans_users = q.execute("select sum(game) from user").fetchone()[0]
			game_summas = q.execute("select sum(summa) from game").fetchone()[0]
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text=f'🏆 Топ 10 игроков',callback_data='топигры'))
			keyboard.add(types.InlineKeyboardButton(text=f'💬 Чат',url='https://t.me/G21_CHAT'),types.InlineKeyboardButton(text=f'🔧 Поддержка',url=f'https://t.me/G21ROBOT_SUPPORT'))
			keyboard.add(types.InlineKeyboardButton(text=f'♻️ Логи',url='https://t.me/G21_LOG'),types.InlineKeyboardButton(text=f'💸 Выплаты',url='https://t.me/joinchat/AAAAAEkD4du-oepTVNDRjA'))
			keyboard.add(types.InlineKeyboardButton(text=f'📕 Правила игры',url='https://telegra.ph/Dvadcat-odno-21Ochko--Pravila-08-22'))
			doc = open('info.jpg', 'rb')
			bot.send_photo(message.chat.id,doc, f'''На данный момент пользователи сыграли {balans_users} игр на сумму {game_summas} рублей.''' ,parse_mode='HTML', reply_markup=keyboard)

		elif message.text.lower() == '🃏 играть':
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT * FROM game where status = '1'")
			row = q.fetchall()
			keyboard = types.InlineKeyboardMarkup()
			for i in row:
				print('111')
				keyboard.add(types.InlineKeyboardButton(text=f'🔹 #Game_{i[0]} | Сумма {i[1]}р',callback_data=f'game_{i[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='🗂 Мои игры',callback_data='моиигры'),types.InlineKeyboardButton(text='♻️ Обновить',callback_data='обновить'))
			keyboard.add(types.InlineKeyboardButton(text='✔️ Создать игру',callback_data='newgame'))
			doc = open('game.jpg', 'rb')
			bot.send_photo(message.chat.id,doc, f'''♻️ Доступные игры:''' ,parse_mode='HTML', reply_markup=keyboard)


		elif message.text.lower() == '/top':
			if message.chat.id == message.chat.id:
						ids = []
						game = []
						win = []
						luls = []
						connection = sqlite3.connect('database.sqlite')
						with connection:
							cur = connection.cursor()
							keyboard = types.InlineKeyboardMarkup()
							cur.execute("SELECT * FROM user ORDER BY game DESC")
							row = cur.fetchall()
							for i in row:
									game.append(i[5])
									ids.append(i[0])
									win.append(i[4])
									luls.append(i[6])
							x = 0
							for ro,ror,rooo,roooo  in zip(ids,game,win,luls):
								x += 1
								if x <= 10:
									userid = ro
									UsrInfo = bot.get_chat_member(userid, userid).user
									keyboard.add(types.InlineKeyboardButton(text = f'ℹ️ {str(UsrInfo.first_name)} |🕹 {str(ror)} |🏆 {str(rooo)} |☹️ {str(roooo)}', url = f"t.me/{str(UsrInfo.username)}"))
						keyboard.add(types.InlineKeyboardButton(text = f'⬅️ Назад', callback_data = f"назадинфо"))			
						bot.send_message(message.chat.id, "ℹ️ Имя |🕹 Игры |🏆 Победы |☹️ Проигрыши ", reply_markup = keyboard)
						
		elif message.text.lower() == '🖥 кабинет':
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT balance FROM user where id is " + str(message.chat.id))
			balanss = q.fetchone()
			q.execute("SELECT ref_colvo FROM user where id is " + str(message.chat.id))
			ref_colvo = q.fetchone()
			q.execute("SELECT win FROM user where id is " + str(message.chat.id))
			win = q.fetchone()
			q.execute("SELECT luls FROM user where id is " + str(message.chat.id))
			luls = q.fetchone()
			q.execute("SELECT game FROM user where id is " + str(message.chat.id))
			game = q.fetchone()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='⚜️ Пополнить баланс',callback_data='awhat_oplata'),types.InlineKeyboardButton(text='⚜️ Вывод средств',callback_data='выводбаланса'))
			keyboard.add(types.InlineKeyboardButton(text='👥 Реферальная система',callback_data='рефсистема'))
			doc = open('cab.jpg', 'rb')
			bot.send_photo(message.chat.id,doc, f'''🧟‍♂ id: <code>{message.chat.id}</code>
💰 Баланс: <code>{balanss[0]}</code>

📊 Статистика:

➖ Игры: <code>{game[0]}</code>
➖ Победы: <code>{win[0]}</code>
➖ Прогрыши: <code>{luls[0]}</code>


''',parse_mode='HTML', reply_markup=keyboard)

		elif message.text.lower() == 'назад':
			msg = bot.send_message(message.chat.id, '<b>Вернулись назад</b>',parse_mode='HTML', reply_markup=keyboards.main)
	else:	
		pass


def editgame2(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM game where id = '{message.text}'")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML', reply_markup=keyboards.admin)
		if row != None:
			keyboard = types.InlineKeyboardMarkup()
			userid = row[2]
			UsrInfo = bot.get_chat_member(userid, userid).user
			userid1 = row[3]
			UsrInfo1 = bot.get_chat_member(userid1, userid1).user
			keyboard.add(types.InlineKeyboardButton(text=f'Изменить банк',callback_data=f'изменитьбанк_{row[0]}'),types.InlineKeyboardButton(text=f'Изменить противник',callback_data=f'изменитьпротивник_{row[0]}'))
			bot.send_message(message.chat.id, f'''@{UsrInfo.username} (банк):{row[14]} vs @{UsrInfo1.username} :{row[16]}
Cумма: {row[1]}''',parse_mode='HTML', reply_markup=keyboard)
		else:
			print('2')	

	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def add_money1(message):
   if message.text != 'Отмена':
      global textt
      textt = message.text
      msg = bot.send_message(message.chat.id, 'Введи сумму: ',parse_mode='HTML')
      bot.register_next_step_handler(msg, add_money2)
   else:
      bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def add_money2(message):
   if message.text != 'Отмена':
      connection = sqlite3.connect('database.sqlite')
      q = connection.cursor()
      q.execute("update user set balance = balance +" + str( message.text ) +  " where id =" + str(id_user_edit_bal1))
      connection.commit()
      msg = bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
   else:
      bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_phone(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set qiwi_phone = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_token(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set qiwi_token = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def editgame(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update game set bank_summa = '"+str(message.text)+f"' where id = '{idgames}'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def editgames(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update game set protivnik_summa = '"+str(message.text)+f"' where id = '{idgames1}'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def idviplatauser(message):
	if message.text != 'Отмена':
		bot.send_message(idviplata, f'''<b>#выплата</b>

{message.text}''',parse_mode='HTML', reply_markup=keyboards.admin)
		bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def qiwi_viplata(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	if message.text.isdigit() == True:
		q = q.execute("SELECT balance FROM user WHERE id = "+str(message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(message.text):
				ref_prozent = '5'
				add_ref_money = int(message.text)/100*int(ref_prozent)
				sum_vivod = int(message.text) - int(add_ref_money)
				q.execute("update user set balance = balance - "+str(message.text)+" where id = " + str(message.chat.id))
				connection.commit()
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Выплатить',callback_data=f'выплата_{message.chat.id}'))
				bot.send_message(config.admin, f'#Вывод\n\nЗаказана выплата!\n\nПользовать: <a href="tg://user?id={message.chat.id}">{message.from_user.first_name}</a>\nИд: <code>'+str(message.chat.id)+'</code>\nСумма: <code>'+str(sum_vivod)+' </code>руб',parse_mode='HTML',reply_markup=keyboard)
				bot.send_message(message.chat.id, f'''<b>✅ Выплата успешно заказана, ожидайте перевод !</b>

<b>ℹ️ Информация:</b>

<b>➖ Сумма выплаты:</b> <code>{sum_vivod}</code> <b>RUB (с учетом комиссии)</b>
''',reply_markup=keyboards.main, parse_mode='HTML')

def send_photoorno(message):
	global text_send_all
	text_send_all = message.text
	msg = bot.send_message(message.chat.id, '<b>Введите нужны аргументы в таком виде:\n\nСсылка куда отправит кнопка\nСсылка на картинку</b>\n\nЕсли что-то из этого не нужно, то напишите "Нет"',parse_mode='HTML')
	bot.register_next_step_handler(msg, admin_send_message_all_text_rus)

def admin_send_message_all_text_rus(message):
		global photoo
		global keyboar
		global v
		try:
			photoo = message.text.split('\n')[1]
			keyboar = message.text.split('\n')[0]
			v = 0
			if str(photoo.lower()) != 'Нет'.lower():
				v = v+1
				
			if str(keyboar.lower()) != 'Нет'.lower():
				v = v+2

			if v == 0:
				msg = bot.send_message(message.chat.id, "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML')
				bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
			
			elif v == 1:
				msg = bot.send_photo(message.chat.id,str(photoo), "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML')
				bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

			elif v == 2:
				keyboard = types.InlineKeyboardMarkup(row_width=1)
				keyboard.add(types.InlineKeyboardButton(text='Перейти',url=f'{keyboar}'))
				msg = bot.send_message(message.chat.id, "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML',reply_markup=keyboard)
				bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

			elif v == 3:
				keyboard = types.InlineKeyboardMarkup(row_width=1)
				keyboard.add(types.InlineKeyboardButton(text='Перейти',url=f'{keyboar}'))
				msg = bot.send_photo(message.chat.id,str(photoo), "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML',reply_markup=keyboard)
				bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
		except:
			bot.send_message(message.chat.id, 'Аргументы указаны неверно!')	


def admin_send_message_all_text_da_rus(message):
	otvet = message.text
	colvo_send_message_users = 0
	colvo_dont_send_message_users = 0
	if message.text.lower() == 'Да'.lower():
		connection = sqlite3.connect('database.sqlite')
		with connection:	
			q = connection.cursor()
			bot.send_message(message.chat.id, 'Начинаем отправлять!')
			if v == 0:
				q.execute("SELECT * FROM user")
				row = q.fetchall()
				for i in row:
					jobid = i[0]
					time.sleep(0.2)
					response = requests.post(
						url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendMessage"),
						data={'chat_id': jobid, 'text': str(text_send_all),'parse_mode': 'HTML'}
					).json()
					if response['ok'] == False:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1
					else:
						colvo_send_message_users = colvo_send_message_users + 1;
				bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	
			elif v == 1:
				q.execute("SELECT * FROM user")
				row = q.fetchall()
				for i in row:
					jobid = i[0]


					time.sleep(0.1)
					response = requests.post(
						url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendPhoto"),
						data={'chat_id': jobid,'photo': str(photoo), 'caption': str(text_send_all),'parse_mode': 'HTML'}
					).json()
					if response['ok'] == False:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1
					else:
						colvo_send_message_users = colvo_send_message_users + 1;
				bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	

			elif v == 2:
				q.execute("SELECT * FROM user")
				row = q.fetchall()
				for i in row:
					jobid = i[0]

					time.sleep(0.1)
					reply = json.dumps({'inline_keyboard': [[{'text': '♻️ Перезапустить бот', 'callback_data': f'restart'}]]})
					response = requests.post(
						url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendMessage"),
						data={'chat_id': jobid, 'text': str(text_send_all), 'reply_markup': str(reply),'parse_mode': 'HTML'}
					).json()
					if response['ok'] == False:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1
					else:
						colvo_send_message_users = colvo_send_message_users + 1;
				bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	
			elif v == 3:
				q.execute("SELECT * FROM user")
				row = q.fetchall()
				for i in row:
					jobid = i[0]

					time.sleep(0.1)
					reply = json.dumps({'inline_keyboard': [[{'text': '♻️ Перезапустить бот', 'callback_data': f'restart'}]]})
					response = requests.post(
						url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendPhoto"),
						data={'chat_id': jobid,'photo': str(photoo), 'caption': str(text_send_all),'reply_markup': str(reply),'parse_mode': 'HTML'}
					).json()
					if response['ok'] == False:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1
					else:
						colvo_send_message_users = colvo_send_message_users + 1;
				bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	


	elif message.text == 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("delete from dep WHERE id_user = " + str(message.chat.id))
		connection.commit()
		q.close()
		connection.close()
		bot.send_message(message.chat.id, "Вернулись на главную", reply_markup=keyboards.main)


def adminsendmessage(message):
	if message.text.lower() != 'отмена':
		bot.send_message(iduserasend, str(message.text),parse_mode='HTML')
		bot.send_message(message.chat.id, '<b>Отправленно</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.admin)

def btc_oplata(message):
	if message.text != 'Отмена':
		try:
			price = int(message.text)
			if str(price).isdigit() == True:
				if int(price) < 100:
					msg = bot.send_message(message.chat.id, 'Cумма пополнения меньше 100 руб')
					bot.register_next_step_handler(msg, btc_oplata)
				else:
					msg = bot.send_message(message.chat.id, f"<b>ℹ️ Отправьте BTC ЧЕК на сумму:{message.text}</b>", reply_markup=keyboards.main, parse_mode='HTML')
					bot.register_next_step_handler(msg, btc_oplata_1)

			else:
				msg = bot.send_message(message.chat.id, 'Вводить нужно целое-положительное число\n\nВведите другое число')
				bot.register_next_step_handler(msg, btc_oplata)
		except ValueError:
			msg = bot.send_message(message.chat.id, 'Вводить нужно целое-положительное число\n\nВведите другое число')
			bot.register_next_step_handler(msg, btc_oplata)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)

def searchuser(message):
	if message.text.lower() != 'отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM user where name = '{message.text}'")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML', reply_markup=keyboards.admin)
		if row != None:
			
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='✉ Написать',callback_data=f'написатьюзеру_{row[0]}'),types.InlineKeyboardButton(text='✔️ Изменить прайс',callback_data=f'изменитьпрайс_{row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='🔒 Заблокировать',callback_data=f'заблокировать_{row[0]}'),types.InlineKeyboardButton(text='🔓 Раблокировать',callback_data=f'разблокировать_{row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='➕ Добавить баланс',callback_data=f'добавитьбаланс_{row[0]}'),types.InlineKeyboardButton(text='➖ Снять баланс',callback_data=f'снятьбаланс_{row[0]}'))
			msg = bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

<b>username:</b> <b>@{row[1]}</b>
<b>Ид:</b> <code>{row[0]}</code>
<b>Рефералов:</b> <code>{row[4]}</code>
<b>Баланс:</b> <code>{row[2]}</code>
<b>Отправил:</b> <code>{vsegosms[0]}</code>
<b>Прайс смс:</b> <code>{row[5]}</code>
<b>Прайс прозвона:</b> <code>{row[6]}</code>
<b>Статус:</b> <code>{row[7]}</code>
''',parse_mode='HTML',reply_markup=keyboard)
		else:
			bot.send_message(message.chat.id, '<b>Нет такого пользователя</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.admin)

def qiwi_viplata11111(message):
	qiwi_user = message.text
	if message.text != '🔶 Отменить':
		if qiwi_user[:1] == '7' and len(qiwi_user) == 11 or qiwi_user[:3] == '380' and len(qiwi_user[3:]) == 9 or qiwi_user[:3] == '375' and len(qiwi_user) <= 12:
			if qiwi_user.isdigit() == True:
				global numberphone
				numberphone = message.text
				msg = bot.send_message(message.chat.id, 'Введите сумму для выплаты')
				bot.register_next_step_handler(msg, summa_vilata_qiwi)
			else:
				bot.send_message(message.chat.id, '📛 Неверно указан кошелек!',reply_markup=keyboards.main)
		else:
			msg = bot.send_message(message.chat.id, '📛 Неверно указан кошелек!')

	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def summa_vilata_qiwi(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	if message.text.isdigit() == True:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balance FROM user WHERE id = "+str(message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(message.text):
				ref_prozent = '5'
				add_ref_money = int(message.text)/100*int(ref_prozent)
				sum_vivod = int(message.text) - int(add_ref_money)
				print(sum_vivod)
				q.execute("update user set balance = balance - "+str(message.text)+" where id = " + str(message.chat.id))
				connection.commit()
				rand = random.randint(1,999999999)
				q.execute("INSERT INTO viplata (id,summa,user,qiwi) VALUES ('%s','%s', '%s', '%s')"%(rand,sum_vivod,message.chat.id,numberphone))
				connection.commit()

				bot.send_message(-1001428771225, f'''<b>ℹ️ Информация:</b>

<b>💰 Сумма выплаты:</b> <code>{sum_vivod}</code>
<b>👤 Пользователь:</b> <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>''', parse_mode='HTML')


				bot.send_message(message.chat.id, f'''<b>✅ Выплата успешно прошла, ожидайте перевод !</b>

<b>ℹ️ Информация:</b>

<b>➖ Сумма выплаты:</b> <code>{sum_vivod}</code> <b>RUB (с учетом комиссии)</b>

<b>➖ Реквизиты:</b>  <code>{numberphone}</code>


''',reply_markup=keyboards.main, parse_mode='HTML')
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Выплатить',callback_data=f'выплатить_{rand}'))
				bot.send_message(config.admin, f'''<b>✅ Выплата успешно прошла, ожидайте перевод !</b>

<b>👤 Пользователь:</b> <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>

<b>➖ Сумма выплаты:</b> <code>{sum_vivod}</code> <b>RUB (с учетом комиссии)</b>

<b>➖ Реквизиты:</b>  <code>{numberphone}</code>

<code>{message.chat.id}</code>


''',reply_markup=keyboard, parse_mode='HTML')

def searchuser_id(message):
	if message.text.lower() != 'отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM user where id = '{message.text}'")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML', reply_markup=keyboards.admin)
		if row != None:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='✉ Написать',callback_data=f'написатьюзеру_{row[0]}'),types.InlineKeyboardButton(text='✔️ Изменить прайс',callback_data=f'изменитьпрайс_{row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='🔒 Заблокировать',callback_data=f'заблокировать_{row[0]}'),types.InlineKeyboardButton(text='🔓 Раблокировать',callback_data=f'разблокировать_{row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='➕ Добавить баланс',callback_data=f'добавитьбаланс_{row[0]}'),types.InlineKeyboardButton(text='➖ Снять баланс',callback_data=f'снятьбаланс_{row[0]}'))
			msg = bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

<b>Ид:</b> <code>{row[0]}</code>
<b>Рефералов:</b> <code>{row[3]}</code>
<b>Баланс:</b> <code>{row[1]}</code>
<b>Игры:</b> <code>{row[5]}</code>
<b>Выйграл:</b> <code>{row[4]}</code>
<b>Проиграл:</b> <code>{row[6]}</code>
<b>Статус:</b> <code>{row[7]}</code>
''',parse_mode='HTML',reply_markup=keyboard)
		else:
			bot.send_message(message.chat.id, '<b>Нет такого пользователя</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.admin)


def btc_oplata_1(message):
	if message.text != 'Отмена':
		if "https://telegram.me/BTC_CHANGE_BOT?" in str(message.text):
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='Подтвердить',callback_data=f'good_oplata_btc_{message.chat.id}'))
			bot.send_message(message.chat.id, '♻️ Платеж проверяется, время зачисления 5-30 минут')
			bot.send_message(config.admin, f'#НОВЫЙЧЕК \n<a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a> \n {message.text}',parse_mode='HTML', reply_markup=keyboard)

		else:
			bot.send_message(message.chat.id, f'⚒ Чек указан неверно!',parse_mode='HTML', reply_markup=keyboards.main)

	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)

def user_id_balance11(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		print(user_id_balance)
		q.execute(f"update user set balance = balance + {message.text} where id = {user_id_balance}")
		connection.commit()
		today = datetime.datetime.today()
		bot.send_message(message.chat.id, 'Готово', reply_markup=keyboards.admin)
		bot.send_message(user_id_balance, 'Ваш баланс пополнен', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.admin)

def newgame(message):
	summagame = message.text
	if message.text != 'Отмена':
		try:
			if int(summagame) >= int(10):
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q = q.execute("SELECT balance FROM user WHERE id = "+str(message.chat.id))
				check_balans = q.fetchone()
				if float(check_balans[0]) >= int(summagame):
					q.execute("update user set balance = balance - "+str(summagame)+" where id = " + str(message.chat.id))
					connection.commit()
					rand = random.randint(1,999999999)
					q.execute("INSERT INTO game (id,summa,bank,protivnik,k2,k3,k4,k7,k8,k9,k10,k11,status,bank_colvo,bank_summa,protivnik_colvo,protivnik_summa,rezultat) VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(rand,summagame,message.chat.id,'0','4','4','4','4','4','4','4','4','1','0','0','0','0','0'))
					connection.commit()
					dohodss = int(summagame) / 100 * 4
					q.execute("update winers set balance = balance + "+str(dohodss)+" where id = " + str(1))
					connection.commit()
					bot2.send_message(-1001386797138, f'♻️ Новая игра на {summagame}р.', parse_mode='HTML')
					bot.send_message(message.chat.id, '🃏 Игра успешно создана, ждите соперника.', parse_mode='HTML', reply_markup=keyboards.main)
				else:
					bot.send_message(message.chat.id, '⚠ Недостаточно средств', reply_markup=keyboards.main)
			else:
				bot.send_message(message.chat.id, 'Сумма игры должна быть больше 10 рублей', reply_markup=keyboards.main)	
		except:
			bot.send_message(message.chat.id, 'Ошибка', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)
@bot.callback_query_handler(func=lambda call:True)
def podcategors(call):

	if call.data[:12] == 'awhat_oplata':
		what_oplata = types.InlineKeyboardMarkup(row_width=2)
		what_oplata_qiwi = types.InlineKeyboardButton(text='🥝 Qiwi', callback_data='Depoziit_qiwi')
		what_oplataa_crypta = types.InlineKeyboardButton(text='💲 Криптовалюта', callback_data='crypt_oplata')
		what_oplataa_btc = types.InlineKeyboardButton(text='🎁 BTC ЧЕК', callback_data='btc_oplata')
		what_oplata.add(what_oplataa_crypta,what_oplata_qiwi,what_oplataa_btc)
		bot.send_message(call.message.chat.id, 'Выбери способ для депозита', reply_markup=what_oplata)

	if call.data == 'crypt_oplata':
		bot.send_message(call.from_user.id,  '👁‍🗨 Временно не доступно')

	if call.data[:12] == 'btc_oplata':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.from_user.id,  '👁‍🗨 Введите сумму для пополнения\n💵 Минимальный депозит - 100 руб', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, btc_oplata)


	if call.data[:13] == 'Depoziit_qiwi':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✅ Проверить',callback_data='Check_Depozit_qiwi_'))
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT qiwi_phone FROM config where id = '1'")
		qiwi_phone = q.fetchone()
		qiwi_oplata_url = "https://qiwi.com/payment/form/99?extra['account']="+str(qiwi_phone[0])+"&extra['comment']="+str(call.message.chat.id)+"&amountInteger=50&amountFraction=0&currency=643&blocked[1]=account&blocked[2]=comment"
		keyboard.add(types.InlineKeyboardButton(text='💳 Перейти к оплате',url=qiwi_oplata_url))
		bot.send_message(call.message.chat.id, "📥 <b>Для совершения пополнения через QIWI кошелёк, переведите нужную сумму средств (минимум </b><code>50</code><b> руб) на номер кошелька указанный ниже, оставив при этом индивидуальный комментарий перевода:\n\n💳 Номер кошелька:</b> <code>%s</code>\n💬 <b>Коментарий к переводу:</b> <code>%s</code>" % (str(qiwi_phone[0]), str(call.message.chat.id)),parse_mode='HTML', reply_markup=keyboard)
		bot.send_message(call.message.chat.id, '⚠️  Депозит меньше 50р = подарок проекту !, после оплаты нажмите "✅ Проверить" ')

	if call.data[:19] == 'Check_Depozit_qiwi_':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT qiwi_phone FROM config where id = 1")
		qiwi_phone = str(q.fetchone()[0])
		q.execute("SELECT qiwi_token FROM config where id = 1")
		qiwi_token = str(q.fetchone()[0])
		for payment in Qiwi(qiwi_token,qiwi_phone).get_payments(10, operation=OperationType.IN):
			q = q.execute('SELECT id FROM temp_pay WHERE txnid = ' + str(payment.raw['txnId']))
			temp_pay = q.fetchone()
			if 'RUB' in str(payment.currency) and str(payment.comment) == str(call.message.chat.id) and temp_pay == None and float(payment.amount) >= 50:
				q.execute("INSERT INTO temp_pay (txnid) VALUES ('%s')"%(payment.raw['txnId']))
				connection.commit()
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("update user set balance = balance + "+str(payment.amount)+" where id = " + str(call.message.chat.id))
				connection.commit()
				
				today = datetime.datetime.today()
				q.execute("select ref from user where Id = " + str(call.message.chat.id))
				ref_user1 = q.fetchone()[0]
				if ref_user1 != '':
					add_deposit = int(payment.amount) / 100 * 0.1
					bot.send_message(ref_user1, f'Реферал пополнил баланс и вам зачислинно {add_deposit} RUB',parse_mode='HTML')

				bot.send_message(config.admin, "<b>Новый депозит!</b>\nId Пользователя: " + str(call.message.chat.id)+"\nСумма: " + str(payment.amount),parse_mode='HTML')
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ На ваш баланс зачислено "+str(payment.amount) +' руб')
				break
			else:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Оплата не найдена!")

	elif call.data == 'edit_praces':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT rules FROM user  where id = "+str(call.message.chat.id))
		sms_prace = q.fetchone()
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()

		keyboard.add(types.InlineKeyboardButton(text=f'VIP | 1000р',callback_data='vip_1'),types.InlineKeyboardButton(text=f'Premium | 10000р',callback_data='vip_3'))
		keyboard.add(types.InlineKeyboardButton(text=f'VIP+ | 5000р',callback_data='vip_2'),types.InlineKeyboardButton(text=f'Premium+ | 30000р',callback_data='vip_4'))
		bot.send_message(call.message.chat.id, f'''➖ VIP: цена смс 12р
➖ VIP+: цена смс 10р
➖ Premium: цена смс 7р
➖ Premium+: цена смс 5р

⚠️ Все тарифы подключатся бесплатно, необходимо только наличие баланса на счету.''' ,parse_mode='HTML', reply_markup=keyboard)

	elif call.data == 'vip_1':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(1000):
			q.execute("update user set rules = " + str(12) +  " where id =" + str(call.message.chat.id))
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ Вы успешно сменили тариф")

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Недостаточно средств")

	elif call.data == 'vip_2':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(5000):
			q.execute("update user set rules = " + str(10) +  " where id =" + str(call.message.chat.id))
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ Вы успешно сменили тариф")

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Недостаточно средств")

	elif call.data == 'vip_3':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(10000):
			q.execute("update user set rules = " + str(7) +  " where id =" + str(call.message.chat.id))
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ Вы успешно сменили тариф")

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Недостаточно средств")

	elif call.data == 'vip_4':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(30000):
			q.execute("update user set rules = " + str(5) +  " where id =" + str(call.message.chat.id))
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ Вы успешно сменили тариф")

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Недостаточно средств")

	elif call.data == 'шаблоны':
			bot.send_message(call.message.chat.id, f'''Авито.ру ссылка прямого оформления:

Ваш товар оплачен! Ссылка для подтверждения сделки:

Подтвердите сделку с покупателем:

Укажите реквизиты для дальнейшего перевода д/с:

Ваш товар оплачен! Ссылка безопасной сделки:

Оплата заказа:

Оформление заказа:

Покупка через безопасную сделку:

На Ваше имя зарегистрировано отправление №7542916.
Подтверждение и оплата:

Произошла ошибка платежа! Ссылка для возврата средств:

Ваш товар оплачен! Получите деньги с продажи:''' ,parse_mode='HTML')


	elif call.data == 'сократить_ссылку':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(types.InlineKeyboardButton(text='🔸 Life | 0р',callback_data=f'сократить_ссылку_лифе'),types.InlineKeyboardButton(text='🔹 Premium | 5р',callback_data=f'сократить_ссылку_премиум'))
		bot.send_message(call.message.chat.id, '''<b>♻️ Примеры ссылок:</b> 

🔹 Premium:		
<code>0️⃣ https://oplata.uno/2ywn1
1️⃣ https://oplata.live/l559d
2️⃣ https://dostavim.live/ssgkw
2️⃣ https://dostavim.world/ssgkw</code>
🔸 Life:
<code>⚠ НЕ ДОСТУПНО</code>
''',parse_mode='HTML', reply_markup=keyboard)
		#bot.answer_callback_query(callback_query_id=call.id, text="⚠ НЕ ДОСТУПНО")

	elif call.data == 'сократить_ссылку_лифе':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте ссылку:\n\nПример:</b> <code>https://yandex.ru/</code>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,generator_url)

	elif call.data == 'сократить_ссылку_премиум':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(5):
			msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте ссылку:\n\nПример:</b> <code>https://yandex.ru/</code>',parse_mode='HTML', reply_markup=keyboards.otmena)
			bot.register_next_step_handler(msg,generator_url_1)
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data[:14] == 'написатьюзеру_':
		global iduserasend
		iduserasend = call.data[14:]
		msg=bot.send_message(call.message.chat.id, f'<b>Введи текст сообщения:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, adminsendmessage)

	elif call.data == 'svoi_text':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте текст сообщения:</b> \n\nМаксимум 120 символов',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,svoi_text)

	elif call.data == 'svoi_textvip':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте текст сообщения:</b> \n\nМаксимум 160 символов',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,svoi_textvip)

	elif call.data == 'рефсистема':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT balance FROM user where id is " + str(call.message.chat.id))
		balanss = q.fetchone()
		q.execute("SELECT ref_colvo FROM user where id is " + str(call.message.chat.id))
		ref_colvo = q.fetchone()
		q.execute("SELECT win FROM user where id is " + str(call.message.chat.id))
		win = q.fetchone()
		q.execute("SELECT luls FROM user where id is " + str(call.message.chat.id))
		luls = q.fetchone()
		q.execute("SELECT game FROM user where id is " + str(call.message.chat.id))
		game = q.fetchone()
		doc = open('ref.jpg', 'rb')
		bot.send_photo(call.message.chat.id,doc, f'''👥Реферальная система

▫️Что это?
Наша уникальная реферальная система позволит вам заработать крупную сумму без вложений. Вам необходимо лишь приглашать друзей и вы будете получать пожизненно 5% от их пополнений в боте

📯Ваша реферальная ссылка:
https://t.me/{config.bot_name}?start={call.message.chat.id}

Всего рефералов {ref_colvo[0]}''',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data == 'svoi_text_prozvon':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте текст сообщения:</b> \n\nМаксимум 500 символов',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,svoi_text_prozvon)

	elif call.data == 'узнать_статус':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте id звонка:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,poisk_status)

	elif call.data == 'узнать_статус_sms':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте id смс:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,poisk_status_sms)

	elif call.data[:16] == 'good_oplata_btc_':
		global user_id_balance
		user_id_balance = call.data[16:]
		#bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Введите сумму:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,user_id_balance11)

	elif call.data == "vau":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='➕ Создать',callback_data=f'vau_add'),types.InlineKeyboardButton(text=' ✔️ Активировать',callback_data=f'vau_good'))
		bot.send_message(call.message.chat.id, "<b>Что вы бы хотели сделать?</b>",parse_mode='HTML', reply_markup=keyboard)


	elif call.data == "vau_add":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT balans FROM user where id is " + str(call.message.chat.id))
		balanss = q.fetchone()
		msg = bot.send_message(call.message.chat.id, f'''На какую сумму RUB выписать Ваучер ? (Его сможет обналичить любой пользователь, знающий код).

Доступно: {balanss[0]} RUB''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, vau_add)

	elif call.data == "vau_good":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '''Для активации ваучера отправьте его код:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, vau_good)

	elif call.data == "пробить_номер":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '''<b>ℹ️ Отправьте номер:\n\nПример:</b> <code>79999999999</code>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, probiv_number)

	elif call.data[:16] == 'restart':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		bot.send_message(call.message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)


	elif call.data == 'buy_reklama':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'✔️ Согласен, купить| 500 RUB',callback_data=f'yes_buy_reklama'))
		bot.send_message(call.message.chat.id, '''<b>В витрине отображается 5 добавленных ссылок.
Добавленная ссылка, будет отображена первой, а последняя будет удалена.

Ссылку увидят:
➖В приветствие. 
➖При депозите. 
➖После отправки сообщений. 
➖В выборе сервиса отправки.</b>''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data == 'yes_buy_reklama':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Введите текст ссылки:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, yes_buy_reklama)

	elif call.data == "авито_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=av&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data == "телеграм_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=tg&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data == "ватсап_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=wa&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')


	if call.data[:15] == 'разблокировать_':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT status FROM user where id = "+ str(call.data[15:]))
		roww = q.fetchone()[0]
		if roww == 'Заблокирован':
			q.execute(f"update user set status = 'Активен' where id = {call.data[15:]}")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Разблокирован")
			connection.close()

		else:
			bot.answer_callback_query(callback_query_id=call.id, text="⚠ Пользователь не заблокирован")

	if call.data[:14] == 'заблокировать_':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT status FROM user where id = "+ str(call.data[14:]))
		roww = q.fetchone()[0]
		if roww == 'Активен':
			q.execute(f"update user set status = 'Заблокирован' where id = {call.data[14:]}")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Заблокирован")
			connection.close()

		else:
			bot.answer_callback_query(callback_query_id=call.id, text="⚠ Пользователь уже заблокирован")

	elif call.data == "вибер_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=vi&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data == "юла_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=ym&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data[:14] == 'проверить_смс_':
		id_sms_number = call.data[14:]
		r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getStatus&id={id_sms_number}')
		ok_number = r.text
		pracesms = 5
		if str(ok_number.split(':')[0]) == 'STATUS_OK':
			smsgoodnumber = ok_number.split(':')[1]
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT rules FROM config  where id = "+str(1))
			prace_smska = q.fetchone()
			q.execute(f"update user set balans = balans - {prace_smska[0]} where id = {call.message.chat.id}")
			connection.commit()
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getBalance')
			balance_sms = r.text
			bot.send_message(-1001147741701, f'''#СМСАКТИВАЦИЯ: #{call.message.chat.id} <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a>

{balance_sms}''', parse_mode='HTML')
			bot.send_message(call.message.chat.id, f'<b>Успешная активация:</b> <code>{smsgoodnumber}</code>',parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Ожидание смс")

	elif call.data[:13] == 'отменить_смс_':
		id_sms_number = call.data[13:]
		r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=setStatus&status=8&id={id_sms_number}')
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Номер добавлен в черный список")

	elif call.data[:17] == 'admin_search_user':
		msg = bot.send_message(call.message.chat.id, f'<b>Введи username пользователя\n(Вводить нужно без @)</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,searchuser)

	elif call.data == 'asdasdasdasdasd':
		msg = bot.send_message(call.message.chat.id, f'<b>Введи id пользователя</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,searchuser_id)


	elif call.data == 'fead_10':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '''<b>✔️ Напишите отзыв:

⚠️ Минимум 50 символов.</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,fead_10)

	elif call.data == 'прокси':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🔹 http',callback_data=f'http'))
		keyboard.add(types.InlineKeyboardButton(text=f'🔹 socks4',callback_data=f'socks4'))
		keyboard.add(types.InlineKeyboardButton(text=f'🔹 socks5',callback_data=f'socks5'))
		bot.send_message(call.message.chat.id, '''<b>Выберите тип прокси:</b>''',parse_mode='HTML', reply_markup=keyboard)


	elif call.data == 'авитоакк':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		count_users = q.execute(f"SELECT count(id) from shopa").fetchone()[0]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'Купить | 15р',callback_data=f'авито_50'))
		bot.send_message(call.message.chat.id, f'''<b>Подтвержденные по SMS и по почте аккаунты Avito.ru Сим-карты: Россия. Города и IP - Россия. Формат: логин:пароль;Имя; почта:пароль . Покупать только тем, кто умеет и знает как пользоваться, замена товара не производится ни в каком случае, валидность 100% при загрузке в магазин, купите 1 шт на тест.</b>

<b>Осталось:</b> <code>{count_users}</code>''',parse_mode='HTML', reply_markup=keyboard)


	elif call.data == 'авито_50':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(15):
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT * FROM shopa DESC LIMIT 1")
			row = q.fetchall()
			for i in row:
				bot.send_message(call.message.chat.id, f'''Спасибо за покупку
{i[0]}''',parse_mode='HTML', reply_markup=keyboards.main)
				bot.send_message(config.admin, f'Покупка avito юзер: <code>{call.message.chat.id}</code>',parse_mode='HTML')
				q.execute('DELETE FROM shopa WHERE id = '+ str(i[1]))
				connection.commit()
				q.execute("update user set balans = balans - "+str(15)+" where id = " + str(call.message.chat.id))
				connection.commit()

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Недостаточно средств")

	elif call.data == 'киви':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		count_users = q.execute(f"SELECT count(id) from shop").fetchone()[0]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'Купить | 50р',callback_data=f'киви_50'))
		bot.send_message(call.message.chat.id, f'''<b>ОСНОВНОЙ - ЛОГИН:ПАРОЛЬ + CARD VIZA (номер карты. дата.код) + API key</b>
<b>Осталось:</b> <code>{count_users}</code>''',parse_mode='HTML', reply_markup=keyboard)


	elif call.data == 'киви_50':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(50):
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT * FROM shop DESC LIMIT 1")
			row = q.fetchall()
			for i in row:
				bot.send_message(call.message.chat.id, f'''Спасибо за покупку
{i[0]}''',parse_mode='HTML', reply_markup=keyboards.main)
				bot.send_message(config.admin, f'Покупка qiwi юзер: <code>{call.message.chat.id}</code>',parse_mode='HTML')
				q.execute('DELETE FROM shop WHERE id = '+ str(i[1]))
				connection.commit()
				q.execute("update user set balans = balans - "+str(50)+" where id = " + str(call.message.chat.id))
				connection.commit()

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Недостаточно средств")


	elif call.data == 'авитоакк':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🔹 http',callback_data=f'http'))
		keyboard.add(types.InlineKeyboardButton(text=f'🔹 socks4',callback_data=f'socks4'))
		keyboard.add(types.InlineKeyboardButton(text=f'🔹 socks5',callback_data=f'socks5'))
		bot.send_message(call.message.chat.id, '''<b>Выберите тип прокси:</b>''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data == 'http':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		pr1 = 'RU:http'
		pr2 = 'UA:http'
		pr3 = ':http'
		pr11 = requests.get("https://proxy1337.com/proxy.php?type=http&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=RU")
		colvo_ru = len(pr11.text.splitlines())
		pr22 = requests.get("https://proxy1337.com/proxy.php?type=http&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=UA")
		colvo_ua = len(pr22.text.splitlines())
		pr33 = requests.get("https://proxy1337.com/proxy.php?type=http&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=")
		colvo = len(pr33.text.splitlines())
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🇷🇺 Россия | {colvo_ru} шт',callback_data=f'скачать_прокси_{pr1}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🇺🇦 Украина | {colvo_ua} шт',callback_data=f'скачать_прокси_{pr2}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🌐 Весь мир | {colvo} шт',callback_data=f'скачать_прокси_{pr3}'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'прокси'))
		bot.send_message(call.message.chat.id, '''<b>Выберите страну прокси для скачивания:
			
💸 Стоимость 1 выкачки: 10р

♻️ Обновление каждый час</b>''',parse_mode='HTML', reply_markup=keyboard)


	elif call.data == 'socks4':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		pr1 = 'RU:socks4'
		pr2 = 'UA:socks4'
		pr3 = ':socks4'
		pr11 = requests.get("https://proxy1337.com/proxy.php?type=socks4&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=RU")
		colvo_ru = len(pr11.text.splitlines())
		pr22 = requests.get("https://proxy1337.com/proxy.php?type=socks4&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=UA")
		colvo_ua = len(pr22.text.splitlines())
		pr33 = requests.get("https://proxy1337.com/proxy.php?type=socks4&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=")
		colvo = len(pr33.text.splitlines())
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🇷🇺 Россия | {colvo_ru} шт',callback_data=f'скачать_прокси_{pr1}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🇺🇦 Украина | {colvo_ua} шт',callback_data=f'скачать_прокси_{pr2}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🌐 Весь мир | {colvo} шт',callback_data=f'скачать_прокси_{pr3}'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'прокси'))
		bot.send_message(call.message.chat.id, '''<b>Выберите страну прокси для скачивания:
			
💸 Стоимость 1 выкачки: 10р

♻️ Обновление каждый час</b>''',parse_mode='HTML', reply_markup=keyboard)


	elif call.data == 'socks5':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		pr1 = 'RU:socks5'
		pr2 = 'UA:socks5'
		pr3 = ':socks5'
		pr11 = requests.get("https://proxy1337.com/proxy.php?type=socks5&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=RU")
		colvo_ru = len(pr11.text.splitlines())
		pr22 = requests.get("https://proxy1337.com/proxy.php?type=socks5&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=UA")
		colvo_ua = len(pr22.text.splitlines())
		pr33 = requests.get("https://proxy1337.com/proxy.php?type=socks5&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=")
		colvo = len(pr33.text.splitlines())
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🇷🇺 Россия | {colvo_ru} шт',callback_data=f'скачать_прокси_{pr1}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🇺🇦 Украина | {colvo_ua} шт',callback_data=f'скачать_прокси_{pr2}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🌐 Весь мир | {colvo} шт',callback_data=f'скачать_прокси_{pr3}'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'прокси'))
		bot.send_message(call.message.chat.id, '''<b>Выберите страну прокси для скачивания:

💸 Стоимость 1 выкачки: 10р

♻️ Обновление каждый час</b>''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:15] == 'скачать_прокси_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(10):
			keyboard = types.InlineKeyboardMarkup()
			try:
				zapros_proxy = call.data[15:]
				print(zapros_proxy.split(':')[0])
				print(zapros_proxy.split(':')[1])
				proxyyy = requests.get(f"https://proxy1337.com/proxy.php?type={zapros_proxy.split(':')[1]}&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country={zapros_proxy.split(':')[0]}")
				proxy = proxyyy.text
				doc = open(f'{call.message.chat.id}proxi_@{config.bot_name}.txt', 'w', encoding='utf8')
				doc.write(f'{proxy}\n')
				doc.close()
				doc = open(f'{call.message.chat.id}proxi_@{config.bot_name}.txt', 'rb')
				bot.send_document(call.from_user.id, doc)
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute(f"update user set balans = balans - 10 where id = {call.message.chat.id}")
				connection.commit()
				bot.send_message(call.message.chat.id, '❤️ Спасибо за покупку !', reply_markup=keyboards.main)
				bot.send_message(-1001147741701, f'''#ПОКУПКАПРОКСИ: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a>''', parse_mode='HTML')
			except:
				bot.send_message(call.message.chat.id, '⚠ Ошибка', reply_markup=keyboards.main)
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств', reply_markup=keyboards.main)

	elif call.data[:14] == 'game_':
		global id_user_edit
		id_user_edit = call.data[14:]
		msg = bot.send_message(call.message.chat.id, 'Введи сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, edit_prace_2)

	elif call.data[:12] == 'снятьбаланс_':
		global id_user_edit_bal1111
		id_user_edit_bal1111 = call.data[12:]
		msg = bot.send_message(call.message.chat.id, 'Введи сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, add_money2)

	elif call.data[:15] == 'добавитьбаланс_':
		global id_user_edit_bal1
		id_user_edit_bal1 = call.data[15:]
		msg = bot.send_message(call.message.chat.id, 'Введи сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, add_money2)

	elif call.data == 'изменитьтокен_':
		msg = bot.send_message(call.message.chat.id, 'Введи новый токен киви: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_token)

	elif call.data == 'изменитьномер_':
		msg = bot.send_message(call.message.chat.id, 'Введи новый номер: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_phone)

	elif call.data == 'изменитьценапрозвон_':
		msg = bot.send_message(call.message.chat.id, 'Введи новую сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_prace_prozvon)

	elif call.data == 'изменитьценасмс_':
		msg = bot.send_message(call.message.chat.id, 'Введи новую сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_prace_sms)

	elif call.data == 'изменитьпрайсприемасмс':
		msg = bot.send_message(call.message.chat.id, 'Введи новую сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_prace_sms_ppp)

	elif call.data == 'изменить_api_prozvon':
		msg = bot.send_message(call.message.chat.id, '<b>Введите нужны аргументы в таком виде:\n\nИД КАМПАНИЙ\nАПИ КАМПАНИЙ</b>',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_prace_apii)

	elif call.data == "получить_токен_апи":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= float(14000):
			chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
			number = 1
			length = 25
			for n in range(number):
				token =''
				for i in range(length):
					token += random.choice(chars)
					print(token)
					q.execute(f"update user set api_token = {token} where id = {call.message.chat.id}")
					connection.commit()
					q.execute(f"update user set balans = balans - 14000 where id = {call.message.chat.id}")
					connection.commit()
					bot.send_message(call.message.chat.id, 'Успешно купленно ! ')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')


	elif call.data == 'newgame':
		msg = bot.send_message(call.message.chat.id, '💵 Укажите сумму игры:',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, newgame)

	elif call.data[:5] == 'game_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		idgame = call.data[5:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
		bank = q.fetchone()
		q = q.execute("SELECT protivnik FROM game WHERE id = "+str(idgame))
		protivnik = q.fetchone()
		q = q.execute("SELECT summa FROM game WHERE id = "+str(idgame))
		summa = q.fetchone()
		q = q.execute("SELECT status FROM game WHERE id = "+str(idgame))
		statusgame = q.fetchone()
		q = q.execute("SELECT balance FROM user WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(statusgame[0]) == float(1):
			if float(protivnik[0]) <= float(1):
				if float(check_balans[0]) >= float(summa[0]):
					if float(bank[0]) != float(call.message.chat.id):
						q.execute(f"update game set status = '0' where id = {idgame}")
						connection.commit()
						q.execute(f"update game set protivnik = '{call.message.chat.id}' where id = {idgame}")
						connection.commit()
						q.execute(f"update user set balance = balance - '{summa[0]}' where id = '{call.message.chat.id}'")
						connection.commit()

						card = ['2', '3', '4', '10', '7', '8', '9', '11']
						card1 = random.choice(card)
						card2 = random.choice(card)
						q.execute(f"update game set k{card1} = k{card1} - '1' where id = '{idgame}'")
						connection.commit()
						q.execute(f"update game set k{card2} = k{card2} - '1' where id = '{idgame}'")
						connection.commit()
						q.execute(f"update game set bank_colvo = bank_colvo + '1' where id = '{idgame}'")
						connection.commit()
						q.execute(f"update game set protivnik_colvo = protivnik_colvo + '1' where id = '{idgame}'")
						connection.commit()
						q.execute(f"update game set bank_summa = bank_summa + '{card1}' where id = '{idgame}'")
						connection.commit()
						q.execute(f"update game set protivnik_summa = protivnik_summa + '{card2}' where id = '{idgame}'")
						connection.commit()
						q = q.execute("SELECT protivnik_colvo FROM game WHERE id = "+str(idgame))
						protivnik_colvo = q.fetchone()
						q = q.execute("SELECT protivnik_summa FROM game WHERE id = "+str(idgame))
						protivnik_summa = q.fetchone()
						q = q.execute("SELECT summa FROM game WHERE id = "+str(idgame))
						game_summa = q.fetchone()


						keyboard = types.InlineKeyboardMarkup()
						keyboard.add(types.InlineKeyboardButton(text=f'➕ Взять еще карту',callback_data=f'addcard_{idgame}'))
						keyboard.add(types.InlineKeyboardButton(text=f'✔️ Хватит, пусть играет',callback_data=f'goodcard_{idgame}'))
						bot.send_message(call.message.chat.id, f'''✅ Вы успешно присоединились к игре № <code>{idgame}</code> на сумму <code>{game_summa[0]}</code>''',parse_mode='HTML')
						bot.send_message(bank[0], f'''✅ <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> присоединился к игре № <code>{idgame}</code> на сумму <code>{game_summa[0]}</code>р , ожидайте свой ход. ''',parse_mode='HTML')
						bot.send_message(call.message.chat.id, f'''ℹ️ Количество карт: {protivnik_colvo[0]}


		🔄 Количество очков: {protivnik_summa[0]}''',parse_mode='HTML', reply_markup=keyboard)
					else:
						bot.send_message(call.message.chat.id, '⚠ Вы не можете играть в свою игру', reply_markup=keyboards.main)
				else:
					bot.send_message(call.message.chat.id, '⚠ Недостаточно средств', reply_markup=keyboards.main)
			else:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='♻️ Обновить',callback_data='обновить'))
				bot.send_message(call.message.chat.id, '⚠ Игра уже идет', reply_markup=keyboard)
		else:
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='♻️ Обновить',callback_data='обновить'))
			bot.send_message(call.message.chat.id, '⚠ Игра уже идет', reply_markup=keyboard)
						
	elif call.data[:8] == 'addcard_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		idgame = call.data[8:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		card = ['2', '3', '4', '10', '7', '8', '9', '11']
		card1 = random.choice(card)
		q.execute(f"update game set k{card1} = k{card1} - '1' where id = '{idgame}'")
		connection.commit()
		
		q.execute(f"update game set protivnik_summa = protivnik_summa + '{card1}' where id = '{idgame}'")
		connection.commit()
		q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
		bank = q.fetchone()
		q = q.execute("SELECT protivnik_colvo FROM game WHERE id = "+str(idgame))
		protivnik_colvo = q.fetchone()
		q = q.execute("SELECT rezultat FROM game WHERE id = "+str(idgame))
		rezultat = q.fetchone()
		q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
		bank = q.fetchone()
		q = q.execute("SELECT protivnik_summa FROM game WHERE id = "+str(idgame))
		protivnik_summa = q.fetchone()
		if float(rezultat[0]) != float(2):

			if float(protivnik_summa[0]) <= float(21):
				if float(protivnik_summa[0]) == float(21):
					q.execute(f"update game set protivnik_colvo = protivnik_colvo + '1' where id = '{idgame}'")
					connection.commit()
					q = q.execute("SELECT summa FROM game WHERE id = "+str(idgame))
					summa = q.fetchone()
					summawin = int(summa[0]) * int(2)
					dohod = int(summawin) / 100 * 4
					summawin = int(summawin) - int(dohod)
					q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
					bank = q.fetchone()
					q.execute(f"update user set balance = balance + '{summawin}' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update game set rezultat = rezultat + '2' where id = '{idgame}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{bank[0]}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update user set win = win + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update user set luls = luls + '1' where id = '{bank[0]}'")
					connection.commit()
					bot.send_message(bank[0], f'''🃏 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> взял(а) карту. ''',parse_mode='HTML')
					bot.send_message(call.message.chat.id, f'🎉 Победа <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>',parse_mode='HTML', reply_markup=keyboards.main)
					bot.send_message(bank[0], f'😡  Вы проиграли: {summawin}р  тк <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> набрал 21',parse_mode='HTML', reply_markup=keyboards.main)
					
				else:
					q.execute(f"update game set protivnik_colvo = protivnik_colvo + '1' where id = '{idgame}'")
					connection.commit()
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text=f'➕ Взять еще карту',callback_data=f'addcard_{idgame}'))
					keyboard.add(types.InlineKeyboardButton(text=f'✔️ Хватит, пусть играет',callback_data=f'goodcard_{idgame}'))
					bot.send_message(bank[0], f'''🃏 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> взял(а) карту. ''',parse_mode='HTML')
					bot.send_message(call.message.chat.id, f'''ℹ️ Количество карт: {protivnik_colvo[0]}


	🔄 Количество очков: {protivnik_summa[0]}''',parse_mode='HTML', reply_markup=keyboard)
			else:
				if protivnik_colvo[0] == '1' and card1 == '11':
					q.execute(f"update game set protivnik_colvo = protivnik_colvo + '1' where id = '{idgame}'")
					connection.commit()
					q = q.execute("SELECT summa FROM game WHERE id = "+str(idgame))
					summa = q.fetchone()
					summawin = int(summa[0]) * int(2)
					dohod = int(summawin) / 100 * 4
					summawin = int(summawin) - int(dohod)
					q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
					bank = q.fetchone()
					q.execute(f"update user set balance = balance + '{summawin}' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update game set rezultat = rezultat + '2' where id = '{idgame}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{bank[0]}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update user set win = win + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update user set luls = luls + '1' where id = '{bank[0]}'")
					connection.commit()
					bot.send_message(bank[0], f'''🃏 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> взял(а) карту. ''',parse_mode='HTML')
					bot.send_message(call.message.chat.id, f'😡 Победа <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>',parse_mode='HTML', reply_markup=keyboards.main)
					bot.send_message(bank[0], f'🎉  Вы проиграли: {summawin}р  тк <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> набрал золотои сет',parse_mode='HTML', reply_markup=keyboards.main)
				else:	

					q = q.execute("SELECT summa FROM game WHERE id = "+str(idgame))
					summa = q.fetchone()
					summawin = int(summa[0]) * int(2)
					dohod = int(summawin) / 100 * 4
					summawin = int(summawin) - int(dohod)
					q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
					bank = q.fetchone()
					q.execute(f"update user set balance = balance + '{summawin}' where id = '{bank[0]}'")
					connection.commit()

					q.execute(f"update game set rezultat = rezultat + '2' where id = '{idgame}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{bank[0]}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update user set win = win + '1' where id = '{bank[0]}'")
					connection.commit()
					q.execute(f"update user set luls = luls + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					bot.send_message(bank[0], f'''🃏 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> взял(а) карту. ''',parse_mode='HTML')
					bot.send_message(call.message.chat.id, f'😡 Перебор и победа <a href="tg://user?id={bank[0]}">{bank[0]}</a>',parse_mode='HTML', reply_markup=keyboards.main)
					bot.send_message(bank[0], f'🎉  Вы выиграли: {summawin}р  тк <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> перебрал очков',parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.send_message(call.message.chat.id, f'Cосать',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:9] == 'goodcard_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		idgame = call.data[9:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
		bank = q.fetchone()
		q = q.execute("SELECT protivnik_colvo FROM game WHERE id = "+str(idgame))
		protivnik_colvo = q.fetchone()
		q = q.execute("SELECT bank_colvo FROM game WHERE id = "+str(idgame))
		bank_colvo = q.fetchone()
		q = q.execute("SELECT bank_summa FROM game WHERE id = "+str(idgame))
		bank_summa = q.fetchone()
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'➕ Взять еще карту',callback_data=f'addcardb_{idgame}'))
		keyboard.add(types.InlineKeyboardButton(text=f'✔️ Хватит, вскрываемся',callback_data=f'goodcardb_{idgame}'))
		bot.send_message(call.message.chat.id, f'''✅ Вы закончили игру, теперь играет <a href="tg://user?id={bank[0]}">{bank[0]}</a> ожидайте результатов. ''',parse_mode='HTML')
		bot.send_message(bank[0], f'''✔️ <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> закончил играть и у него {protivnik_colvo[0]} карт, банкуй''',parse_mode='HTML')
		bot.send_message(bank[0], f'''ℹ️ Количество карт: {bank_colvo[0]}


🔄 Количество очков: {bank_summa[0]}''',parse_mode='HTML', reply_markup=keyboard)


	elif call.data[:9] == 'addcardb_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		idgame = call.data[9:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		card = ['2', '3', '4', '10', '7', '8', '9', '11']
		card1 = random.choice(card)
		q.execute(f"update game set k{card1} = k{card1} - '1' where id = '{idgame}'")
		connection.commit()

		q.execute(f"update game set bank_summa = bank_summa + '{card1}' where id = '{idgame}'")
		connection.commit()

		q = q.execute("SELECT protivnik FROM game WHERE id = "+str(idgame))
		protivnik = q.fetchone()
		q = q.execute("SELECT bank_colvo FROM game WHERE id = "+str(idgame))
		bank_colvo = q.fetchone()
		q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
		bank = q.fetchone()
		q = q.execute("SELECT bank_summa FROM game WHERE id = "+str(idgame))
		bank_summa = q.fetchone()
		q = q.execute("SELECT rezultat FROM game WHERE id = "+str(idgame))
		rezultat = q.fetchone()
		if float(rezultat[0]) != float(2):

			if float(bank_summa[0]) <= float(21):
					q.execute(f"update game set bank_colvo = bank_colvo + '1' where id = '{idgame}'")
					connection.commit()
					keyboard = types.InlineKeyboardMarkup()
					keyboard.add(types.InlineKeyboardButton(text=f'➕ Взять еще карту',callback_data=f'addcardb_{idgame}'))
					keyboard.add(types.InlineKeyboardButton(text=f'✔️ Хватит, вскрываемся',callback_data=f'goodcardb_{idgame}'))
					bot.send_message(protivnik[0], f'''🃏 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> взял(а) карту. ''',parse_mode='HTML')
					bot.send_message(call.message.chat.id, f'''ℹ️ Количество карт: {bank_colvo[0]}


	🔄 Количество очков: {bank_summa[0]}''',parse_mode='HTML', reply_markup=keyboard)

			else:
				if bank_colvo[0] == '1' and card1 == '11':
					q.execute(f"update game set bank_colvo = bank_colvo + '1' where id = '{idgame}'")
					connection.commit()
					q = q.execute("SELECT summa FROM game WHERE id = "+str(idgame))
					summa = q.fetchone()
					summawin = int(summa[0]) * int(2)
					dohod = int(summawin) / 100 * 4
					summawin = int(summawin) - int(dohod)
					q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
					bank = q.fetchone()
					q.execute(f"update user set balance = balance + '{summawin}' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update game set rezultat = rezultat + '2' where id = '{idgame}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{bank[0]}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update user set win = win + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update user set luls = luls + '1' where id = '{bank[0]}'")
					connection.commit()
					bot.send_message(bank[0], f'''🃏 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> взял(а) карту. ''',parse_mode='HTML')
					bot.send_message(call.message.chat.id, f'😡 Победа <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a>',parse_mode='HTML', reply_markup=keyboards.main)
					bot.send_message(protivnik[0], f'🎉  Вы проиграли: {summawin}р  тк <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> набрал золотои сет',parse_mode='HTML', reply_markup=keyboards.main)
				else:	

					q = q.execute("SELECT summa FROM game WHERE id = "+str(idgame))
					summa = q.fetchone()
					q = q.execute("SELECT protivnik FROM game WHERE id = "+str(idgame))
					protivnik = q.fetchone()
					summawin = int(summa[0]) * int(2)
					dohod = int(summawin) / 100 * 4
					summawin = int(summawin) - int(dohod)
					q.execute(f"update user set balance = balance + '{summawin}' where id = '{protivnik[0]}'")
					connection.commit()
					q.execute(f"update game set rezultat = rezultat + '2' where id = '{idgame}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update user set game = game + '1' where id = '{protivnik[0]}'")
					connection.commit()
					q.execute(f"update user set win = win + '1' where id = '{protivnik[0]}'")
					connection.commit()
					q.execute(f"update user set luls = luls + '1' where id = '{call.message.chat.id}'")
					connection.commit()
					bot.send_message(protivnik[0], f'''🃏 <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> взял(а) карту. ''',parse_mode='HTML')
					bot.send_message(call.message.chat.id, f'😡 Перебор и победа <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a>',parse_mode='HTML', reply_markup=keyboards.main)
					bot.send_message(protivnik[0], f'🎉  Вы выиграли: {summawin}р  тк <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a> перебрал очков',parse_mode='HTML', reply_markup=keyboards.main)
		else:		
			bot.send_message(call.message.chat.id, f'Cосать',parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data[:10] == 'goodcardb_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		idgame = call.data[10:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT protivnik_summa FROM game WHERE id = "+str(idgame))
		protivnik_summa = q.fetchone()
		q.execute(f"update game set rezultat = rezultat + '2' where id = '{idgame}'")
		connection.commit()
		q = q.execute("SELECT bank_summa FROM game WHERE id = "+str(idgame))
		bank_summa = q.fetchone()
		q = q.execute("SELECT bank FROM game WHERE id = "+str(idgame))
		bank = q.fetchone()
		q = q.execute("SELECT protivnik FROM game WHERE id = "+str(idgame))
		protivnik = q.fetchone()
		q = q.execute("SELECT summa FROM game WHERE id = "+str(idgame))
		summa = q.fetchone()
		summawin = int(summa[0]) * int(2)
		dohod = int(summawin) / 100 * 4
		summawin = int(summawin) - int(dohod)
		if float(bank_summa[0]) >= float(protivnik_summa[0]):
			bot.send_message(protivnik[0], f'''
⚔️ <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a>: {protivnik_summa[0]}  VS <a href="tg://user?id={bank[0]}">{bank[0]}</a>: {bank_summa[0]}

🎉  Победитель:  <a href="tg://user?id={bank[0]}">{bank[0]}</a> выиграл: {summawin}р''',parse_mode='HTML', reply_markup=keyboards.main)
			bot.send_message(bank[0], f'''
⚔️ <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a>: {protivnik_summa[0]}  VS <a href="tg://user?id={bank[0]}">{bank[0]}</a>: {bank_summa[0]}

🎉  Победитель:  <a href="tg://user?id={bank[0]}">{bank[0]}</a> выиграл: {summawin}р''',parse_mode='HTML', reply_markup=keyboards.main)
			q.execute(f"update user set balance = balance + '{summawin}' where id = '{bank[0]}'")
			connection.commit()
			q.execute(f"update user set game = game + '1' where id = '{bank[0]}'")
			connection.commit()
			q.execute(f"update user set game = game + '1' where id = '{protivnik[0]}'")
			connection.commit()
			q.execute(f"update user set win = win + '1' where id = '{bank[0]}'")
			connection.commit()
			q.execute(f"update user set luls = luls + '1' where id = '{protivnik[0]}'")
			connection.commit()
			bot2.send_message(-1001386797138, f'''
⚔️ <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a>: {protivnik_summa[0]}  VS <a href="tg://user?id={bank[0]}">{bank[0]}</a>: {bank_summa[0]}

🎉  Победитель:  <a href="tg://user?id={bank[0]}">{bank[0]}</a> выиграл: {summawin}р''',parse_mode='HTML')
			


		else:
			bot.send_message(protivnik[0], f'''
⚔️ <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a>: {protivnik_summa[0]}  VS <a href="tg://user?id={bank[0]}">{bank[0]}</a>: {bank_summa[0]}

🎉  Победитель:  <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a> выиграл: {summawin}р''',parse_mode='HTML', reply_markup=keyboards.main)
			bot.send_message(bank[0], f'''
⚔️ <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a>: {protivnik_summa[0]}  VS <a href="tg://user?id={bank[0]}">{bank[0]}</a>: {bank_summa[0]}

🎉  Победитель:  <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a> выиграл: {summawin}р''',parse_mode='HTML', reply_markup=keyboards.main)
			q.execute(f"update user set balance = balance + '{summawin}' where id = '{protivnik[0]}'")
			connection.commit()
			q.execute(f"update user set game = game + '1' where id = '{protivnik[0]}'")
			connection.commit()
			q.execute(f"update user set game = game + '1' where id = '{bank[0]}'")
			connection.commit()
			q.execute(f"update user set win = win + '1' where id = '{protivnik[0]}'")
			connection.commit()
			q.execute(f"update user set luls = luls + '1' where id = '{bank[0]}'")
			connection.commit()
			bot2.send_message(-1001386797138, f'''
⚔️ <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a>: {protivnik_summa[0]}  VS <a href="tg://user?id={bank[0]}">{bank[0]}</a>: {bank_summa[0]}

🎉  Победитель:  <a href="tg://user?id={protivnik[0]}">{protivnik[0]}</a> выиграл: {summawin}р''',parse_mode='HTML')

	elif call.data == "выводбаланса":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='🥝 QIWI',callback_data=f'QIWI'))
		keyboard.add(types.InlineKeyboardButton(text='🎁 BTC ЧЕК',callback_data=f'БТКЧЕК'))
		bot.send_message(call.message.chat.id, "<b>📤 Выберите платежную систему:</b>",parse_mode='HTML', reply_markup=keyboard)
	
	elif call.data == "QIWI":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>📤 Введите ваш Qiwi Кошелек (Без +):</b>",parse_mode='HTML')
		bot.register_next_step_handler(msg, qiwi_viplata11111)

	elif call.data == "БТКЧЕК":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, "<b>📤 Введите сумму (МИНИМУМ 400Р):</b>",parse_mode='HTML')
		bot.register_next_step_handler(msg, qiwi_viplata)

	elif call.data[:8] == 'выплата_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		global idviplata
		idviplata = call.data[8:]
		msg = bot.send_message(call.message.chat.id, "<b>📤 отправьте чек:</b>",parse_mode='HTML')
		bot.register_next_step_handler(msg, idviplatauser)

	elif call.data == "обновить":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT * FROM game where status = '1'")
		row = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		for i in row:
			keyboard.add(types.InlineKeyboardButton(text=f'🔹 #Game_{i[0]} | Сумма {i[1]}р',callback_data=f'game_{i[0]}'))
		keyboard.add(types.InlineKeyboardButton(text='🗂 Мои игры',callback_data='моиигры'),types.InlineKeyboardButton(text='♻️ Обновить',callback_data='обновить'))
		keyboard.add(types.InlineKeyboardButton(text='✔️ Создать игру',callback_data='newgame'))
		bot.send_message(call.message.chat.id, f'''♻️ Доступные игры:''' ,parse_mode='HTML', reply_markup=keyboard)

	elif call.data == "моиигры":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM game where status = '1' and bank = '{call.message.chat.id}'")
		row = q.fetchall()
		keyboard = types.InlineKeyboardMarkup()
		for i in row:
			keyboard.add(types.InlineKeyboardButton(text=f'Сумма {i[1]}р | ❌ Отмена',callback_data=f'отменаигры_{i[0]}'))
		keyboard.add(types.InlineKeyboardButton(text='⬅️ Назад',callback_data='обновить'))
		doc = open('mygame.jpg', 'rb')
		bot.send_photo(call.message.chat.id,doc, f'''♻️ Ваши игры:''' ,parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:11] == 'отменаигры_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		idgame = call.data[11:]
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT status FROM game WHERE id = "+str(idgame))
		status = q.fetchone()
		if status[0] != '0':
			q = q.execute("SELECT summa FROM game WHERE id = "+str(idgame))
			summa = q.fetchone()
			q.execute(f"update user set balance = balance + '{summa[0]}' where id = '{call.message.chat.id}'")
			connection.commit()
			q.execute(f"update game set status = '0' where id = {idgame}")
			connection.commit()
			bot.send_message(call.message.chat.id, f'''❌ Отменили''' ,parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.send_message(call.message.chat.id, f'''❌ Игру отменить нельзя''' ,parse_mode='HTML', reply_markup=keyboards.main)

	elif call.data == "назадинфо":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		balans_users = q.execute("select sum(game) from user").fetchone()[0]
		game_summas = q.execute("select sum(summa) from game").fetchone()[0]
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🏆 Топ 10 игроков',callback_data='топигры'))
		keyboard.add(types.InlineKeyboardButton(text=f'💬 Чат',url='https://t.me/g21chat'),types.InlineKeyboardButton(text=f'🔧 Поддержка',url=f'https://t.me/G21ROBOT_SUPPORT'))
		keyboard.add(types.InlineKeyboardButton(text=f'♻️ Логи',url='https://t.me/G21LOG'),types.InlineKeyboardButton(text=f'💸 Выплаты',url='https://t.me/joinchat/AAAAAEkD4du-oepTVNDRjA'))
		doc = open('info.jpg', 'rb')
		bot.send_photo(call.message.chat.id,doc, f'''На данный момент пользователи сыграли {balans_users} игр на сумму {game_summas} рублей.''' ,parse_mode='HTML', reply_markup=keyboard)


	elif call.data == "топигры":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		ids = []
		game = []
		win = []
		luls = []
		connection = sqlite3.connect('database.sqlite')
		with connection:
			cur = connection.cursor()
			keyboard = types.InlineKeyboardMarkup()
			cur.execute("SELECT * FROM user ORDER BY game DESC")
			row = cur.fetchall()
			for i in row:
					game.append(i[5])
					ids.append(i[0])
					win.append(i[4])
					luls.append(i[6])
			x = 0
			for ro,ror,rooo,roooo  in zip(ids,game,win,luls):
				x += 1
				if x <= 10:
					userid = ro
					UsrInfo = bot.get_chat_member(userid, userid).user
					keyboard.add(types.InlineKeyboardButton(text = f'ℹ️ {str(UsrInfo.first_name)} |🕹 {str(ror)} |🏆 {str(rooo)} |☹️ {str(roooo)}', url = f"t.me/{str(UsrInfo.username)}"))
		keyboard.add(types.InlineKeyboardButton(text = f'⬅️ Назад', callback_data = f"назадинфо"))			
		doc = open('topgame.jpg', 'rb')
		bot.send_photo(call.message.chat.id,doc, "ℹ️ Имя |🕹 Игры |🏆 Победы |☹️ Проигрыши ", reply_markup = keyboard)

	elif call.data[:13] == 'изменитьбанк_':
		global idgames
		idgames = call.data[13:]
		msg = bot.send_message(call.message.chat.id, "<b>Введите сумму:</b>",parse_mode='HTML')
		bot.register_next_step_handler(msg, editgame)

	elif call.data[:18] == 'изменитьпротивник_':
		global idgames1
		idgames1 = call.data[18:]
		msg = bot.send_message(call.message.chat.id, "<b>Введите сумму:</b>",parse_mode='HTML')
		bot.register_next_step_handler(msg, editgames)

	elif call.data[:10] == 'выплатить_':
		idviplataaa = call.data[10:]
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM viplata where id = '{idviplataaa}'")
		row = q.fetchone()
		if row != None:
			api = Qiwi('', '')
			account = f"{row[3]}"
			amount = f'{row[1]}'
			comment = f"Выплата @G21ROBOT | Пользователь #{row[2]}"
			response = api.pay(account, amount, comment)
			bot.send_message(1031811029, response)
			bot.send_message(row[2], '💸 Платеж успешно прошел,проверяйте QIWI')
			#q.execute("delete from viplata WHERE id = " + str(idviplataaa))
			#connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Выплата успешно прошла")

while True:				
	try:
		bot.polling(True)
	except Exception as ex:
		bot.send_message(1031811029, f'Появилась ошибка: \n\n' +  str(ex))
		time.sleep(0.1)
