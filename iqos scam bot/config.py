import telebot, sqlite3, random, string, csv, os
from SimpleQIWI import *
from telebot import types

curdir = os.curdir

bot = telebot.TeleBot('1621985834:AAF25Dq-yVRsjvzlcZPpvySWcsj58LlLQR0') #токен бота

admins = [304746706] #айди админов

phone = '' #номер киви

token = '' #токен киви с первыми 3 галочками

price24 = 2990 #цена 2.4+ версии

price3duo = 4990 #цена 3дуо версии

pricemulti = 2490 #цена 3мульти версии

pricestick = 150 #цена за 1 пачку стиков

telegram = '@faulmit' #никнейм телеграмм

id1 = []

def add_message(message):
        if (message.text != 'Назад'):
            rows = get_usersId_banker()

            for row in rows:
                try:
                    bot.send_message(row, message.text)
                except Exception as e:
                    print(e)
                    continue

def get_usersId_banker():
    try:
        array = []

        with sqlite3.connect("users.db") as con:
            cur = con.cursor()
            rows = cur.execute("SELECT user_id FROM user").fetchall()

            for row in rows:
                array.append(row[0])

        return array
    except Exception as e:
        print(e)


def bill_create(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def deposit(chat_id, price):
    try:
        chat_id = chat_id
        global amount
        amount = price
        billId = str(f'{bill_create(6)}_{random.randint(10000, 999999)}')

        inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
        inline_1 = types.InlineKeyboardButton(text="Проверить оплату",
                                                  callback_data=f'STATUS-{billId}-{amount}')
        inline_keyboard.add(inline_1)
        message = bot.send_message(chat_id,
                                       f'💁🏻‍♀️ *Переведите* {str(amount)} ₽ на QIWI\nСчет действителен *10* минут\n\nНомер: `+{phone}`\nКомментарий: `{billId}`\n\n_Нажмите на реквизиты и комментарий чтобы их скопировать_',
                                       parse_mode="Markdown",
                                       reply_markup=inline_keyboard)


    except Exception as e:
        print(e)


def user_status_pay(call, billId, amount):
    chat_id = call.message.chat.id
    api = QApi(phone=phone, token=token)
    payments = api.payments['data']
    for info_payment in payments:
        if info_payment['comment'] == billId:
            if str(amount) == str(info_payment['sum']['amount']):
                bot.send_message(chat_id, '✅Оплата прошла успешно!✅')
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            else:
                bot.answer_callback_query(callback_query_id=call.message.id, show_alert=False,
                                          text="💁🏻‍♀️ Платеж не найден")

