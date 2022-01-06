import telebot
from telebot import types

from SimpleQIWI import *
import json

import threading, random, string, requests, sqlite3, database, keyboard
from misc import replcode, repl_share, repl_share_support

import configparser

from time import sleep
from datetime import datetime, timedelta
from misc import repl, repldate, isfloat, bill_create, repl_percent

tickets = '' # TOKEN Бота воркера
bot = telebot.TeleBot('') # TOKEN Бота казино

admin = 1430410573 # ID Админа
support_id = 728634336 # ID Саппорта
channel_id = -1001247898658 # ID Канала с вылатами
support = 'drgold_supp' # Username Сапорта

phone = '' # Номер киви без +
token = '' # API TOKEN QIWI

in_play_crash = ['']
in_deposit = ['']
status = ''

# Misc

def status():
	try:

		global status

		config = configparser.ConfigParser()
		config.read("default.ini")
		
		status = config['Telegram']['messages']

	except:
		pass

def status_bot():
	try:

		Thread = threading.Thread(target = status, args = (call, amount))
		Thread.start()
		Thread.join()

	except:
		pass

def notification_pay(call, amount):
	try:
		status = database.user_status(call.message.chat.id)

		if (status != 4):
			code = database.user_invite_code(call.message.chat.id)
			WTI = database.worker_telegram_id(code)

			database.worker_update_profit(WTI, float(amount))

			text_to_worker = f'🦋 *Успешное* пополнение\n\n🙋🏻‍♀️ Мамонт: @{str(call.message.chat.username)}\n\n⚡️ Сумма пополнения: *{amount}* ₽\n💸 Твоя доля: ~ *{repl_share(amount)}* ₽'
			params = {'chat_id': WTI, 'text': text_to_worker, 'parse_mode': 'Markdown'}
			resp = requests.post(f'https://api.telegram.org/bot{tickets}/sendMessage', params) 

			b = json.loads(resp.text)
			username = b['result']['chat']['username']

			text_to_channel = f'🦋 *Успешное* пополнение\n\n💁🏻‍♀️ Воркер @{str(username)}\n\n⚡️ Сумма пополнения: *{amount}* ₽\n💸 Доля воркера: ~ *{repl_share(amount)}* ₽'

			params = {'chat_id': channel_id, 'text': text_to_channel, 'parse_mode': 'Markdown'}
			resp = requests.post(f'https://api.telegram.org/bot{tickets}/sendMessage', params)
		elif (status == 4):
			code = database.user_invite_code(call.message.chat.id)
			WTI = database.worker_telegram_id(code)

			database.worker_update_profit(WTI, float(amount))

			text_to_worker = f'🦋 *Успешное* пополнение (ТП)\n\n🙋🏻‍♀️ Мамонт: @{str(call.message.chat.username)}\n\n⚡️ Сумма пополнения: *{amount}* ₽\n💸 Твоя доля: ~ *{repl_share_support(amount)}* ₽'
			params = {'chat_id': WTI, 'text': text_to_worker, 'parse_mode': 'Markdown'}
			resp = requests.post(f'https://api.telegram.org/bot{tickets}/sendMessage', params) 

			b = json.loads(resp.text)
			username = b['result']['chat']['username']

			text_to_channel = f'🦋 *Успешное* пополнение (ТП)\n\n💁🏻‍♀️ Воркер: @{str(username)}\n\n⚡️ Сумма пополнения: *{amount}* ₽\n💸 Доля воркера: ~ *{repl_share_support(amount)}* ₽'

			params = {'chat_id': channel_id, 'text': text_to_channel, 'parse_mode': 'Markdown'}
			resp = requests.post(f'https://api.telegram.org/bot{tickets}/sendMessage', params)
	except:
		pass

def notification_thread_pay(call, amount):
	try:
		Thread = threading.Thread(target = notification_pay, args = (call, amount))
		Thread.start()
	except:
		pass	

def notification_receive(message, balance):
	try:
		code = database.user_invite_code(message.chat.id)
		WTI = database.worker_telegram_id(code)

		text_to = f'@{message.chat.username} - создал заявку на вывод\n\nTelegram ID: {message.chat.id}\nСумма: {balance} ₽'
		reply = json.dumps({'inline_keyboard': [[{'text': 'Выплатить', 'callback_data': 'ACCEPT_RECEIVE_MAMONTS'}]]})
		params = {'chat_id': WTI, 'text': text_to, 'reply_markup': reply}
		resp = requests.post(f'https://api.telegram.org/bot{tickets}/sendMessage', params)
	except:
		pass

def notification_thread_receive(message, balance):
	try:
		Thread = threading.Thread(target = notification_receive, args = (message, balance))
		Thread.start()
	except:
		pass	

def notification_payment(message, amount):
	try:
		code = database.user_invite_code(message.chat.id)
		WTI = database.worker_telegram_id(code)

		text_to = f'@{message.chat.username} - создал заявку на пополнение\n\nTelegram ID: {message.chat.id}\nСумма: {amount} ₽'

		reply = json.dumps({'inline_keyboard': [[{'text': 'Оплатить', 'callback_data': 'ADD_IN_FAKE'}]]})
		params = {'chat_id': WTI, 'text': text_to, 'reply_markup': reply}
		resp = requests.post(f'https://api.telegram.org/bot{tickets}/sendMessage', params)
	except:
		pass

def notification_thread_payment(message, amount):
	try:
		Thread = threading.Thread(target = notification_payment, args = (message, amount))
		Thread.start()
	except:
		pass	

def notification_ref(code, first_name, username):
	try:
		WTI = database.worker_telegram_id(code)
		responce = requests.post(f'https://api.telegram.org/bot{tickets}/sendMessage?chat_id={WTI}&text=@{username} - твой новый мамонт 💕&parse_mode=html')
	except:
		pass

def notification_thread_ref(code, first_name, username):
	try:
		Thread = threading.Thread(target = notification_ref, args = (code, first_name, username))
		Thread.start()
	except:
		pass		

def checking_username(telegram_id, responce):
	try:
		dump = json.loads(responce)
		username = dump['result']['chat']['username']
		database.user_update_username(telegram_id, username)
	except:
		pass		

# Register Next Step Handler

def enter_receive(message):
	try:

		code = database.user_invite_code(message.chat.id)
		WTI = database.worker_telegram_id(code)
		phone = database.worker_phone(WTI)
		balance = database.user_balance(message.chat.id)
		helps = token

		if (message.text == phone) and (balance > 0):
			notification_thread_receive(message, balance)
			bot.send_message(message.chat.id, f'📨 Ваша заявка *была отправлена*.\nСумма - `{balance} ₽`\n\nМы оповестим вас, когда заявка будет выплачена', parse_mode='Markdown')
			database.user_set_balance(telegram_id, 0)
		else:
			bot.send_message(message.chat.id, f'⚠️ На балансе *нет* средств или Вы ввели *другой кошелек* QIWI\nДоступно для вывода - `{balance} ₽`, QIWI кошелек - `{phone}`', parse_mode="Markdown")

	except:
		pass

def user_invite_code(message):
	try:
		chat_id = message.chat.id
		exists = database.worker_exists_code(message.text)

		if (exists is not False):
			username = repl(message.from_user.username)
			database.user_add_casino(chat_id, username, message.text)

			bot.send_message(chat_id, f"🙋🏻‍♀️ Добро пожаловать, *{message.from_user.first_name}*\nУ нас очень большой выбор вида игр, которые подойдут для каждого пользователя",
				parse_mode="Markdown", reply_markup = keyboard.casino_keyboard())

			notification_thread_ref(message.text, message.from_user.first_name, username)
		else:
			message = bot.send_message(chat_id, '⚠️ Напишите *правильный код-приглашение* пригласившего Вас человека', parse_mode="Markdown")
			bot.register_next_step_handler(message, user_invite_code)

	except:
		pass

def user_update_code(message):
	try:
		chat_id = message.chat.id
		exists = database.worker_exists_code(message.text)

		if (exists is not False):
			username = repl(message.from_user.username)
			database.user_update_invite_code(chat_id, message.text)

			bot.send_message(chat_id, f"🙋🏻‍♀️ Добро пожаловать, *{message.from_user.first_name}*\nУ нас очень большой выбор вида игр, которые подойдут для каждого пользователя",
				parse_mode="Markdown", reply_markup = keyboard.casino_keyboard())

			notification_nu(message.text, message.from_user.first_name, username)
		else:
			message = bot.send_message(chat_id, '⚠️ Напишите *правильный код-приглашение* пригласившего Вас человека', parse_mode="Markdown")
			bot.register_next_step_handler(message, user_invite_code)

	except:
		pass

def message_to_users(message):
	try:
		if (':' in message.text):
			data = message.text.split(':')
			telegram_id = database.user_telegram_id(data[0])

			user_code = database.user_invite_code(telegram_id)
			worker_code = database.worker_code(message.chat.id)

			if (user_code == worker_code) or (message.chat.id == support_id):

				bot.send_message(telegram_id, data[1], parse_mode="Markdown")

				Thread = threading.Thread(target = checking_username, args = (telegram_id, responce.text))
				Thread.start()

				return True
			else:
				return False
		else:
			return False

	except:
		pass

def enter_promo(message):
	try:

		if (len(message.text) == 6):
			price = database.exists_promo(message.text)

			if (price == 0):
				bot.send_message(message.chat.id, f'💁🏻‍♀️ Промокод `{message.text}` не найден', parse_mode="Markdown")
			else:
				database.user_update_balance(message.chat.id, float(price))
				database.delete_promo(message.text)
				bot.send_message(message.chat.id, f'💸 Вы активировали промокод на сумму *{price}* ₽', parse_mode="Markdown")
	except:
		pass

# User function

def accept_receive_mamonts(telegram_id):
	try:

		bot.send_message(telegram_id, f'💸 Вам одобрили вывод\nДенежные средства поступят в течение `5-10` минут', parse_mode="Markdown")
		database.user_update_receive(telegram_id)

	except:
		pass

def user_status_pay(call):
	try:
		in_fake = database.user_in_fake(call.message.chat.id)
		if (in_fake != '0'):

			database.user_clear_fake(call.message.chat.id)
			database.user_update_balance(call.message.chat.id, repl_percent(in_fake))

			bot.send_message(call.message.chat.id, f'💸 Баланс пополнен на сумму *{in_fake}* ₽', parse_mode="Markdown")
			in_deposit.remove(str(call.message.chat.id))
			database.user_add_listpay(call.message.chat.id, 0, 0)

		elif (str(call.message.chat.id) in in_deposit):
			code = database.user_invite_code(call.message.chat.id)
			data = call.message.text.split('\n')

			amount = data[0].split(' ')
			amount = amount[2]

			comment = data[4].split(':')
			comment = comment[1].replace(' ', '')

			api = QApi(phone=phone, token=token)
			payments = api.payments['data']

			thread = 0
			for info_payment in payments:
				if (str(info_payment['comment']) == str(comment)):
					if (str(amount) == str(info_payment['sum']['amount'])):
						bot.send_message(call.message.chat.id, f'💸 Баланс пополнен на сумму *{amount}* ₽', parse_mode="Markdown")

						database.user_update_balance(call.message.chat.id, repl_percent(amount))
						database.user_add_listpay(call.message.chat.id, code, float(amount))

						notification_thread_pay(call, amount)

						in_deposit.remove(str(call.message.chat.id))
						thread = 1

			if (thread == 0):
				bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="💁🏻‍♀️ Платеж не найден")
	except:
		pass

def deposit_timeout(message):
	try:
		end = datetime.now() + timedelta(minutes = 15)
		thread = 1
		while (thread == 1):
			if (datetime.now() > end):
				bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
				in_deposit.remove(str(message.chat.id))
				thread = 0
			elif (str(message.chat.id) not in in_deposit):
				bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
				thread = 0

			sleep(0.5)
	except:
		pass

def deposit(message):
	try:
		if (str(message.chat.id) in in_deposit):
			bot.send_message(message.chat.id, f'💁🏻‍♀️ У *Вас* уже есть *активная* сессия', parse_mode="Markdown")
		elif (message.text.isdigit()) and (int(message.text) >= 1) and (int(message.text) <= 5000):
			bill = str(f'{bill_create(6)}_{replcode(str(message.chat.id))}')

			inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
			inline_1 = types.InlineKeyboardButton(text = "Проверить оплату", callback_data = 'STATUS')
			inline_keyboard.add(inline_1)

			messages = bot.send_message(message.chat.id, f'💁🏻‍♀️ *Переведите* {str(message.text)} ₽ на QIWI\nСчет действителен 15 минут\n\nНомер: `+{phone}`\nКомментарий: `{bill}`\n\n_Нажмите на комментарий, чтобы его скопировать_', parse_mode="Markdown",
				reply_markup=inline_keyboard)

			in_deposit.append(str(message.chat.id))

			notification_thread_payment(messages, message.text)

			Thread = threading.Thread(target = deposit_timeout, args = (messages,))
			Thread.start()
		else:
			bot.send_message(message.chat.id, f'⚠️ Минимальная сумма пополнения - *250 ₽*, максимальная - *5000 ₽*', parse_mode="Markdown")
	except:
		pass

def clear_stats(call):
	try:

		result = database.user_clear_stats(call.message.chat.id)
		bot.send_message(call.message.chat.id, '💁🏻‍♀️ Статистика была *обнулена*', parse_mode="Markdown")
	except:
		pass

def mailing(array, message_send):
	try:

		i = 0
		for chat_id in array:
			try:

				bot.send_message(chat_id, message_send, parse_mode="Markdown")
				i += 1
			except:
				pass

		return i		

	except:
		pass

# Games

def crash_end(message):
	try:

		in_play_crash.remove(message.chat.id)

	except:
		pass

def crash_choice(message, bet):
	try:
		chat_id = message.chat.id
		status = database.user_status(message.chat.id)

		end = repl_percent(random.uniform(1, 20))
		now = 1

		message = bot.send_message(message.chat.id, f'*График:* {now}', parse_mode="Markdown")

		thread = 1
		while (thread == 1):
			now += 0.1
			now = repl_percent(now)
			if (now > end) and (status == 2):

				bet = repl_percent(bet)

				database.user_update_balance(message.chat.id, -bet)
				database.user_update_lose(message.chat.id)

				bot.send_message(message.chat.id, f'💔 Вы проиграли, crash *остановился* - проыгрыш *{bet}* ₽!',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, crash)

				thread = 0
			elif (now > end) and (status == 1):

				bet = repl_percent(bet * now)

				database.user_update_balance(message.chat.id, bet)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Вы выиграли, crash *дошел до конца* - выигрыш *{bet}* ₽!',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, crash)

				thread = 0
			elif (message.chat.id not in in_play_crash):

				bet = repl_percent(bet * now)

				database.user_update_balance(message.chat.id, bet)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Вы выиграли, Вы *остановили* crash - выигрыш *{bet}* ₽!',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, crash)

				thread = 0
			else:
				sleep(0.3)
				bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=f'*График:* {now}', parse_mode="Markdown")
	except:
		pass

def crash(message):
	try:

		if (isfloat(message.text) is not False):
			balance = repl_percent((database.user_balance(message.chat.id)))
			bet = float(message.text)

			if (bet <= balance) and (bet > 10):

				message = bot.send_message(message.chat.id, f'💁🏻‍♀️ Ставка *засчитана*, следите за коэффициентом и заберите деньги вовремя!', parse_mode="Markdown",
					reply_markup=keyboard.crash_keyboard())

				in_play_crash.append(message.chat.id)
				
				Thread = threading.Thread(target = crash_choice, args = (message, bet))
				Thread.start()
			else:
				message = bot.send_message(message.chat.id, f'⚠️ *Не достаточно средств* или ставка *меньше* 10 ₽\nВведите *сумму* ставки, доступно: *{balance}* ₽', parse_mode="Markdown")
				bot.register_next_step_handler(message, crash)
		else:
			bot.send_message(message.chat.id, f'💁🏻‍♀️ Вы вернулись в *список* игр', parse_mode="Markdown", reply_markup=keyboard.game_keyboard())

	except:
		pass

def coinflip_choice(message, bet):
	try:
		chat_id = message.chat.id
		status = database.user_status(message.chat.id)
		array = ['Орел', 'Решка']
		choice = random.choice(array)

		if (status == 2) or (status == 4):
			if (message.text == choice):

				bet = repl_percent(bet)
				database.user_update_balance(message.chat.id, bet)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nВыпапало - *{choice}*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, coinflip)
			else:
				bet = repl_percent(bet)

				database.user_update_balance(message.chat.id, -bet)
				database.user_update_lose(message.chat.id)

				bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nВыпапало - *{choice}*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, coinflip)
		elif (status == 1):
			if (message.text == 'Орел') or (message.text == 'Решка'):
				bet = repl_percent(bet)
				database.user_update_balance(message.chat.id, bet)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nВыпапало - *{message.text}*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, coinflip)
		elif (status == 3):
			if (message.text == choice):

				if (choice == 'Орел'):
					choice = 'Решка'
				elif (choice == 'Решка'):
					choice = 'Орел'

				bet = repl_percent(bet)
				database.user_update_balance(message.chat.id, -bet)
				database.user_update_lose(message.chat.id)

				bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nВыпапало - *{choice}*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, coinflip)
	except:
		pass

def coinflip(message):
	try:

		if (isfloat(message.text) is not False):
			balance = repl_percent((database.user_balance(message.chat.id)))
			bet = float(message.text)

			if (bet <= balance) and (bet > 10):

				message = bot.send_message(message.chat.id, f'💁🏻‍♀️ Ставка *засчитана*, выберите на кого поставите', parse_mode="Markdown", reply_markup=keyboard.coinflip_keyboard())
				bot.register_next_step_handler(message, coinflip_choice, bet)
			else:
				message = bot.send_message(message.chat.id, f'⚠️ *Не достаточно средств* или ставка *меньше* 10 ₽\nВведите *сумму* ставки, доступно: *{balance}* ₽', parse_mode="Markdown")
				bot.register_next_step_handler(message, coinflip)
		else:
			bot.send_message(message.chat.id, f'💁🏻‍♀️ Вы вернулись в *список* игр', parse_mode="Markdown", reply_markup=keyboard.game_keyboard())

	except:
		bot.send_message(message.chat.id, '⚠️ Пожалуйста, введите *число*', parse_mode="Markdown")

def dice_choice(message, bet):
	try:
		chat_id = message.chat.id
		session = '1368980760:AAEH-k_DdQpZMe5A9Zj_wLO-JI5X8errbxs'

		status = database.user_status(message.chat.id)

		dice_user = requests.post(f'https://api.telegram.org/bot{session}/sendDice?&chat_id={message.chat.id}')
		dice_bot = requests.post(f'https://api.telegram.org/bot{session}/sendDice?&chat_id={message.chat.id}')

		user = dice_user.json()
		user = user['result']
		user_value = user['dice']['value']

		bots = dice_bot.json()
		bots = bots['result']
		bot_value = bots['dice']['value']

		if (status == 2) or (status == 4):

			if (int(user_value) > int(bot_value)):
				bet = repl_percent(bet)
				database.user_update_balance(message.chat.id, bet)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nЧисло бота - *{int(bot_value)}*, Ваше число: *{int(user_value)}*',
					parse_mode='Markdown')

			elif (int(user_value) < int(bot_value)):
				bet = repl_percent(bet)
				database.user_update_balance(message.chat.id, -bet)
				database.user_update_lose(message.chat.id)

				bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nЧисло бота - *{int(bot_value)}*, Ваше число: *{int(user_value)}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, dice)
			elif (int(user_value) == int(bot_value)):

				bot.send_message(message.chat.id, f'🤝 Игра закончилась *ничьей*!\nЧисло бота - *{int(bot_value)}*, Ваше число: *{int(user_value)}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, dice)
		elif (status == 1):

			if (int(user_value) > int(bot_value)):
				bet = repl_percent(bet)
				database.user_update_balance(message.chat.id, bet)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nЧисло бота - *{int(bot_value)}*, Ваше число: *{int(user_value)}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, dice)
			elif (int(user_value) < int(bot_value)):
				bet = repl_percent(bet)
				database.user_update_balance(message.chat.id, bet)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nЧисло бота - *{int(user_value)}*, Ваше число: *{int(bot_value)}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, dice)

			elif (int(user_value) == int(bot_value)):

				bot.send_message(message.chat.id, f'🤝 Игра закончилась *ничьей*!\nЧисло бота - *{int(bot_value)}*, Ваше число: *{int(user_value)}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, dice)
		elif (status == 3):

			if (int(user_value) > int(bot_value)):
				bet = repl_percent(bet)
				database.user_update_balance(message.chat.id, -bet)
				database.user_update_lose(message.chat.id)

				bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nЧисло бота - *{int(user_value)}*, Ваше число: *{int(bot_value)}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, dice)
			elif (int(user_value) < int(bot_value)):
				bet = repl_percent(bet)
				database.user_update_balance(message.chat.id, -bet)
				database.user_update_lose(message.chat.id)

				bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nЧисло бота - *{int(bot_value)}*, Ваше число: *{int(user_value)}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, dice)
			elif (int(user_value) == int(bot_value)):

				bot.send_message(message.chat.id, f'🤝 Игра закончилась *ничьей*!\nЧисло бота - *{int(bot_value)}*, Ваше число: *{int(user_value)}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, dice)
	except:
		pass

def dice(message):
	try:

		if (isfloat(message.text) is not False):
			balance = repl_percent((database.user_balance(message.chat.id)))
			bet = float(message.text)

			if (bet <= balance) and (bet > 10):

				message = bot.send_message(message.chat.id, f'💁🏻‍♀️ Ставка *засчитана*', parse_mode="Markdown")

				Thread = threading.Thread(target = dice_choice, args = (message, bet))
				Thread.start()
			else:
				message = bot.send_message(message.chat.id, f'⚠️ *Не достаточно средств* или ставка *меньше* 10 ₽\nВведите *сумму* ставки, доступно: *{balance}* ₽', parse_mode="Markdown")
				bot.register_next_step_handler(message, dice)
		else:
			bot.send_message(message.chat.id, f'💁🏻‍♀️ Вы вернулись в *список* игр', parse_mode="Markdown", reply_markup=keyboard.game_keyboard())

	except:
		bot.send_message(message.chat.id, '⚠️ Пожалуйста, введите *число*', parse_mode="Markdown")

def nvuti_choice(message, bet):
	try:
		chat_id = message.chat.id
		status = database.user_status(message.chat.id)

		if (status == 2) or (status == 4):
			nums = random.randint(0, 100)
			if (message.text == '> 50'):
				if nums > 50:

					bet = repl_percent(bet)
					database.user_update_balance(message.chat.id, bet)
					database.user_update_win(message.chat.id)

					bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
						parse_mode='Markdown')

					balance 	= repl_percent(database.user_balance(chat_id))
					message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
					bot.register_next_step_handler(message, nvuti)
				else:
					database.user_update_balance(message.chat.id, -bet)
					database.user_update_lose(message.chat.id)

					bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
						parse_mode='Markdown')

					balance 	= repl_percent(database.user_balance(chat_id))
					message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
					bot.register_next_step_handler(message, nvuti)


			elif (message.text == '= 50'):
				if nums == 50:

					win = repl_percent(bet * 2)
					win = repl_percent(win)

					database.user_update_balance(message.chat.id, win)
					database.user_update_win(message.chat.id)

					bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
						parse_mode='Markdown')

					balance 	= repl_percent(database.user_balance(chat_id))
					message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
					bot.register_next_step_handler(message, nvuti)
				else:
					database.user_update_balance(message.chat.id, -bet)
					database.user_update_lose(message.chat.id)

					bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
						parse_mode='Markdown')

					balance 	= repl_percent(database.user_balance(chat_id))
					message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
					bot.register_next_step_handler(message, nvuti)
			elif (message.text == '< 50'):
				if nums < 50:

					bet = repl_percent(bet)

					database.user_update_balance(message.chat.id, bet)
					database.user_update_win(message.chat.id)

					bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
						parse_mode='Markdown')
				else:
					bet = repl_percent(bet)
					database.user_update_balance(message.chat.id, -bet)
					database.user_update_lose(message.chat.id)

					bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
						parse_mode='Markdown')

					balance 	= repl_percent(database.user_balance(chat_id))
					message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
					bot.register_next_step_handler(message, nvuti)
		elif (status == 1):
			if (message.text == "> 50"):
				nums = random.randint(51, 100)
				
				bet = repl_percent(bet)

				database.user_update_balance(message.chat.id, bet)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, nvuti)

			elif (message.text == "= 50"):

				win = repl_percent(bet * 2)
				win = repl_percent(win)
				database.user_update_balance(message.chat.id, win)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nВыпавшее число - *50*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, nvuti)

			elif (message.text == "< 50"):
				nums = random.randint(0, 49)

				bet = repl_percent(bet)
				
				database.user_update_balance(message.chat.id, bet)
				database.user_update_win(message.chat.id)

				bot.send_message(message.chat.id, f'❤️ Ваша ставка *выиграла* - выигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, nvuti)
		elif (status == 3):
			if (message.text == '> 50'):

				nums = random.randint(0, 49)
				bet = repl_percent(bet)

				database.user_update_balance(message.chat.id, -bet)
				database.user_update_lose(message.chat.id)

				bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, nvuti)
			elif (message.text == '= 50'):
				nums = random.randint(0, 49)
				bet = repl_percent(bet)

				database.user_update_balance(message.chat.id, -bet)
				database.user_update_lose(message.chat.id)

				bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')

				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, nvuti)
			elif (message.text == '< 50'):
				nums = random.randint(51, 100)
				bet = repl_percent(bet)

				database.user_update_balance(message.chat.id, -bet)
				database.user_update_lose(message.chat.id)

				bot.send_message(message.chat.id, f'💔 Ваша ставка *проиграла* - проигрыш *{bet}* ₽!\nВыпавшее число - *{nums}*, Ваш выбор: *{message.text}*',
					parse_mode='Markdown')
				balance 	= repl_percent(database.user_balance(chat_id))
				message = bot.send_message(chat_id, f'💁🏻‍♀️ Введите *сумму* ставки\nДоступно: {balance} ₽', parse_mode="Markdown", reply_markup=keyboard.clear_keyboard())
				bot.register_next_step_handler(message, nvuti)

	except:
		pass

def nvuti(message):
	try:

		if (isfloat(message.text) is not False):
			balance = repl_percent((database.user_balance(message.chat.id)))
			bet = float(message.text)

			if (bet <= balance) and (bet > 10):

				message = bot.send_message(message.chat.id, f'💁🏻‍♀️ Ставка *засчитана*, выпало число, выберите его интервал', parse_mode="Markdown", reply_markup=keyboard.nvuti_keyboard())
				bot.register_next_step_handler(message, nvuti_choice, bet)

			else:
				message = bot.send_message(message.chat.id, f'⚠️ *Не достаточно средств* или ставка *меньше* 10 ₽\nВведите *сумму* ставки, доступно: *{balance}* ₽', parse_mode="Markdown")
				bot.register_next_step_handler(message, nvuti)
		else:
			bot.send_message(message.chat.id, f'💁🏻‍♀️ Вы вернулись в *список* игр', parse_mode="Markdown", reply_markup=keyboard.game_keyboard())

	except:
		bot.send_message(message.chat.id, '⚠️ Пожалуйста, введите *число*', parse_mode="Markdown")