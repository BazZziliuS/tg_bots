import sqlite3
import telebot
import requests
import json

def open_sell(chat_id, chat_id2, summ):
	conn = sqlite3.connect('main.db')
	cursor = conn.cursor()
	row = cursor.execute(f'SELECT * FROM sale WHERE user_id = "0"').fetchone()
	id = row[0]
	cursor.execute(f'UPDATE sale SET id = "{id+1}" WHERE user_id = "0"')

	row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
	balance = row[3]
	name = row[1]
	row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id2}"').fetchone()
	name2 = row[1]
	row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
	comsa = int(summ*row[6]//100)
	
	cursor.execute(f'UPDATE users SET balance = {balance-summ} WHERE user_id = "{chat_id}"')

	cursor.execute(f'INSERT INTO sale VALUES ({id}, "{chat_id}", "{name}", "{chat_id2}", "{name2}", "{str(summ-comsa)}")')
	conn.commit()

	return str(id), name2 

def check_balance(user_id, price):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    row = cursor.fetchone()

    if row[3] >= price:
        return 1
    else:
        return 0

def sale_back(id):
	try:
		conn = sqlite3.connect('main.db')
		cursor = conn.cursor()
		row = cursor.execute(f'SELECT * FROM sale WHERE id = "{id}"').fetchone()
		chat_id = row[1]
		chat_id2 = row[3]
		summ = row[5]
		name = row[2]
		name2 = row[4]
		text = f'Сделка №{id}\nОт @{name} Для @{name2}\nСумма: {summ}₽\nСтатус: <b>Отмена</b>'
		cursor.execute(f'DELETE FROM sale WHERE id = "{id}"')

		row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
		balance = float(row[3])

		cursor.execute(f'UPDATE users SET balance = {balance+int(summ)} WHERE user_id = "{chat_id}"')
		conn.commit()

	except:
		text = "❌Ошибка"
		chat_id = 0
		
	return text, chat_id

def dispute(id, chat_id):
	try:
		conn = sqlite3.connect('main.db')
		cursor = conn.cursor()
		row = cursor.execute(f'SELECT * FROM sale WHERE id = {int(id)}').fetchone()
		chat_id = row[1]
		chat_id2 = row[3]
		summ = row[5]
		name = row[2]
		name2 = row[4]

		cursor.execute(f'DELETE FROM sale WHERE id = {int(id)}')

		cursor.execute(f'INSERT INTO dispute VALUES ({id}, "{chat_id}", "{name}", "{chat_id2}", "{name2}", {int(summ)})')
		conn.commit()
		msg = [chat_id, name, chat_id2, name2, summ]
	except:
		msg = "Ошибка"

	return msg


def sale_end(id):
	try:
		conn = sqlite3.connect('main.db')
		cursor = conn.cursor()
		row = cursor.execute(f'SELECT * FROM sale WHERE id = "{id}"').fetchone()
		chat_id = row[1]
		chat_id2 = row[3]
		summ = row[5]
		name = row[2]
		name2 = row[4]

		text = f'Сделка №{id}\nОт @{name} Для @{name2}\nСумма: {summ}₽\nСтатус: <b>Завершена</b>'
		cursor.execute(f'DELETE FROM sale WHERE id = {id}')

		row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
		cursor.execute(f'UPDATE users SET buy = {row[4]+1} WHERE user_id = "{chat_id}"')
		cursor.execute(f'UPDATE users SET buy_sum = {row[5]+int(summ)} WHERE user_id = "{chat_id}"')


		row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id2}"').fetchone()
		cursor.execute(f'UPDATE users SET sell = {row[6]+1} WHERE user_id = "{chat_id2}"')
		cursor.execute(f'UPDATE users SET sell_sum = {row[7]+int(summ)} WHERE user_id = "{chat_id2}"')
		cursor.execute(f'UPDATE users SET balance = {row[3]+int(summ)} WHERE user_id = "{chat_id2}"')
		conn.commit()

	except:
		text = "Ошибка"
		chat_id2 = 0

	return text, chat_id2

def feedback(chat_id, name2, text):
	conn = sqlite3.connect('main.db')
	cursor = conn.cursor()
	row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id}"').fetchone()
	cursor.execute(f'INSERT INTO feedback VALUES ("{chat_id}", "{row[1]}", "{name2}", "{text}")')
	conn.commit()
	msg = f"<b>Отзыв\nОт </b>@{name2} <b>Для </b>@{row[1]}\n<pre>{text}</pre>"
	return msg

def cancel_dispute(id, who):
	chat_id = ['1', '1']
	name = ['1', '1']
	conn = sqlite3.connect('main.db')
	cursor = conn.cursor()
	row = cursor.execute(f'SELECT * FROM dispute WHERE id = {int(id)}').fetchone()
	chat_id[0] = row[1]
	chat_id[1] = row[3]
	name[0] = row[2]
	name[1] = row[4]
	summ = row[5]

	cursor.execute(f'DELETE FROM dispute WHERE id = "{id}"')

	row = cursor.execute(f'SELECT * FROM users WHERE user_id = "{chat_id[who]}"').fetchone()
	balance = row[3]

	cursor.execute(f'UPDATE users SET balance = {balance+int(summ)} WHERE user_id = "{chat_id[who]}"')
	conn.commit()

	msg = f'Сделка №{id}\nОт @{name[0]} Для @{name[1]}\nСумма: {summ}₽\nСтатус: <b>Завершена (Спор)</b>'
	info = [chat_id[0], chat_id[1], msg]
	return info

def check_payment(user_id, code):
    conn = sqlite3.connect('main.db')
    cursor = conn.cursor()
    a = 0
    row = cursor.execute(f'SELECT * FROM settings WHERE id = 1').fetchone()
    try:
        session = requests.Session()
        session.headers['authorization'] = 'Bearer ' + row[2]
        parameters = {'rows': '5'}
        h = session.get(
            'https://edge.qiwi.com/payment-history/v1/persons/{}/payments'.format(row[1]),
            params=parameters)
        req = json.loads(h.text)

        for i in range(len(req['data'])):
            if code in str(req['data'][i]['comment']):
                if req["data"][i]["sum"]["currency"] == 643 and int(req["data"][i]["sum"]["amount"]) >= 10:
                    balance = cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"').fetchone()

                    balance = balance[3] + int(req["data"][i]["sum"]["amount"])

                    cursor.execute(f'UPDATE users SET balance = {balance} WHERE user_id = "{user_id}"')

                    conn.commit()
                    
                    a = int(req["data"][i]["sum"]["amount"])

    except Exception as e:
        pass

    return a

