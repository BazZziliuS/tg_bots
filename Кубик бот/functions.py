from utils.mydb import *
from utils.user import User

from aiogram import types

import datetime
import random
import texts
import menu
import config
import requests
import json
import time


buy_dict = {}

class Buy:
    def __init__(self, user_id):
        self.user_id = user_id
        self.product_code = None


async def first_join(user_id, first_name, username, code, bot):
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    row = cursor.fetchall()
    who_invite = code[7:]

    if who_invite == '':
        who_invite = 0

    if len(row) == 0:
        cursor.execute(f'INSERT INTO users VALUES ("{user_id}", "{first_name}", "@{username}", "0", "{who_invite}", "{datetime.datetime.now()}")')
        conn.commit()

        if who_invite != 0:
            try:
                User(who_invite).update_balance(config.config('ref_reward'))

                cursor.execute(f'SELECT * FROM stats WHERE user_id = "{who_invite}"')
                user = cursor.fetchall()

                if len(user) == 0:
                    cursor.execute(f'INSERT INTO stats VALUES("{user_id}", "0", "1", "{config.config("ref_reward")}")')
                    conn.commit()
                else:
                    cursor.execute(f'UPDATE stats SET ref_amount = {user[0][2] + 1} WHERE user_id = "{who_invite}"')
                    conn.commit()

                    cursor.execute(f'UPDATE stats SET ref_profit = {float(user[0][3]) + float(config.config("ref_reward"))} WHERE user_id = "{who_invite}"')
                    conn.commit()

                await bot.send_message(chat_id=who_invite, text=f'За приглашение {User(user_id).username} вам начислено {config.config("ref_reward")} ₽')
            except Exception as e:
                print(e)

        return True, who_invite
        
    return False, 0


def check_in_bd(user_id):
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    row = cursor.fetchall()

    if len(row) == 0:
        return False
    else:
        return True


def replenish_balance(user_id):
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM check_payment WHERE user_id = "{user_id}"')
    row = cursor.fetchall()
    
    if len(row) > 0:
        code = row[0][1]
    else:
        code = random.randint(1111, 9999)

        cursor.execute(f'INSERT INTO check_payment VALUES ("{user_id}", "{code}", "0")')
        conn.commit()

    msg = texts.replenish_balance.format(
        number=config.config("qiwi_number"),
        code=code,
    )
    url =  f'https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={config.config("qiwi_number")}&amountFraction=0&extra%5B%27comment%27%5D={code}&currency=643&&blocked[0]=account&&blocked[1]=comment'

    markup = menu.payment_menu(url)

    return msg, markup


def check_payment(user_id):
    try:
        conn, cursor = connect()
    
        session = requests.Session()
        session.headers['authorization'] = 'Bearer ' + config.config("qiwi_token")
        parameters = {'rows': '10'}
        h = session.get(
            'https://edge.qiwi.com/payment-history/v1/persons/{}/payments'.format(config.config("qiwi_number")),
            params=parameters)
        req = json.loads(h.text)

        cursor.execute(f'SELECT * FROM check_payment WHERE user_id = {user_id}')
        result = cursor.fetchone()
        comment = result[1]

        for i in range(len(req['data'])):
            if comment in str(req['data'][i]['comment']):
                if str(req['data'][i]['sum']['currency']) == '643':
                    User(user_id).update_balance(req["data"][i]["sum"]["amount"])
                    User(user_id).give_ref_reward(float(req["data"][i]["sum"]["amount"]))

                    cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
                    conn.commit()

                    rub = req["data"][i]["sum"]["amount"]

                    try:
                        cursor.execute(f'INSERT INTO deposit_logs VALUES ("{user_id}", "qiwi", "{rub}", "{datetime.datetime.now()}")')
                        conn.commit()
                    except:
                        pass



                    return 1, req["data"][i]["sum"]["amount"]

                    
    except Exception as e:
        print(e)

    return 0, 0


def profile(user_id):
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    row = cursor.fetchone()

    return row


def admin_info():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM users')
    row = cursor.fetchall()

    d = datetime.timedelta(days=1)
    h = datetime.timedelta(hours=1)
    date = datetime.datetime.now()

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    for i in row:
        amount_user_all += 1

        if date - datetime.datetime.fromisoformat(i[5]) <= d:
            amount_user_day += 1
        if date - datetime.datetime.fromisoformat(i[5]) <= h:
            amount_user_hour += 1

    cursor.execute(f'SELECT * FROM deposit_logs')
    row = cursor.fetchall()

    qiwi = 0
    all_qiwi = 0

    for i in row:
        if i[1] == 'qiwi':
            if date - datetime.datetime.fromisoformat(i[3]) <= d:
                qiwi += i[2]

            all_qiwi += i[2]

    cursor.execute(f'SELECT * FROM withdraw_logs')
    row = cursor.fetchall()

    withdraw = 0
    all_withdraw = 0

    for i in row:
        if date - datetime.datetime.fromisoformat(i[2]) <= d:
            withdraw += i[1]

        all_withdraw += i[1]

    cursor.execute(f'SELECT * FROM profit_logs')
    row = cursor.fetchall()

    profit = 0
    all_profit = 0

    for i in row:
        if date - datetime.datetime.fromisoformat(i[2]) <= d:
            profit += i[1]

        all_profit += i[1]

    msg = f"""
❕ Информаци о пользователях:

❕ За все время - <b>{amount_user_all}</b>
❕ За день - <b>{amount_user_day}</b>
❕ За час - <b>{amount_user_hour}</b>

❕ Пополнений за 24 часа
❕ QIWI: <b>{qiwi} ₽</b>

❕ Выводы за 24 часа
❕ <b>{withdraw} ₽</b>

❕ Прибыль за 24 часа
❕ <b>{profit} ₽</b>

⚠️ Ниже приведены данные за все время
❕ Пополнения QIWI: <b>{all_qiwi} ₽</b>
❕ Выводы: <b>{all_withdraw} ₽</b>
❕ Прибыль: <b>{all_profit} ₽</b>
"""

    return msg


def give_balance(balance, user_id):
    conn, cursor = connect()
    
    cursor.execute(f'UPDATE users SET balance = "{balance}" WHERE user_id = "{user_id}"')
    conn.commit()


def get_users_list():
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM users')
    users = cursor.fetchall()

    return users


def add_sending(info):
    conn, cursor = connect()
    
    d = (int(info['date'].split(':')[0]) - int(time.strftime('%d', time.localtime()))) * 86400
    h = (int(info['date'].split(':')[1]) - int(time.strftime('%H', time.localtime()))) * 3600
    m = (int(info['date'].split(':')[2]) - int(time.strftime('%M', time.localtime()))) * 60
    
    date = float(time.time()) + d + h + m

    cursor.execute(f'INSERT INTO sending VALUES ("{info["type_sending"]}", "{info["text"]}", "{info["photo"]}", "{date}")')
    conn.commit()


def sending_check():
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM sending')
    row = cursor.fetchall()

    for i in row:
        if float(i[3]) <= time.time():
            cursor.execute(f'DELETE FROM sending WHERE photo = "{i[2]}"')
            conn.commit()

            return i

    return False


def add_withdraw(user_id, withdraw_sum, info):
    conn, cursor = connect()
    
    user = User(user_id)

    if float(withdraw_sum) <= user.balance:
        user.update_balance(-float(withdraw_sum))

        cursor.execute(f'INSERT INTO withdraw VALUES ("{random.randint(1, 9999999)}", "{user_id}", "{withdraw_sum}", "{info}", "{datetime.datetime.now()}")')
        conn.commit()

        return True


def withdrawal_requests():
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM withdraw')
    withdraw_list = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=2)

    for i in withdraw_list:
        markup.add( 
            types.InlineKeyboardButton(text=f'{i[0]} | {i[2]} RUB', callback_data=f'withdraw:{i[0]}')
        )

    return markup


def get_info_withdraw(code):
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM withdraw WHERE id = "{code}"')
    withdraw_list = cursor.fetchone()

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add( 
        types.InlineKeyboardButton(text=f'Удалить', callback_data=f'withdraw_del:{code}'),
        types.InlineKeyboardButton(text=f'Выйти', callback_data=f'back_to_admin_menu'),
    )

    msg = f"""
ID: {withdraw_list[0]}
USER_ID: {withdraw_list[1]}
LINK: {User(withdraw_list[1]).username}
SUM: {withdraw_list[2]}
INFO: {withdraw_list[3]}
DATE: {withdraw_list[4]}
    """

    return msg, markup
    

async def withdraw_del(code, bot):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM withdraw WHERE id = "{code}"')
    withdraw = cursor.fetchone()
    
    cursor.execute(f'DELETE FROM withdraw WHERE id = "{code}"')
    conn.commit()

    try:
        cursor.execute(f'INSERT INTO withdraw_logs VALUES ("{withdraw[1]}", "{withdraw[2]}", "{datetime.datetime.now()}")')
        conn.commit()
    except:
        pass

    user = User(withdraw[1])

    msg = f"""
❕ Вывод | #{withdraw[0]}
❕ {user.first_name}/{user.username}/{user.user_id}
❕ Дата: {datetime.datetime.now()}

💸 Сумма {withdraw[2]} ₽
❕ Реквизиты: {withdraw[3]}
"""


async def check_user_data(bot, user_id):
    chat = await bot.get_chat(user_id)
    user = User(user_id)

    conn, cursor = connect()

    if user.username != f'@{chat.username}':
        cursor.execute(f'UPDATE users SET username = "@{chat.username}" WHERE user_id = "{user_id}"')
        conn.commit()
    if user.first_name != chat.first_name:
        cursor.execute(f'UPDATE users SET first_name = "@{chat.first_name}" WHERE user_id = "{user_id}"')
        conn.commit()
