import numpy, datetime
import sqlite3, random, requests, string, time
import threading

from misc import repl, repl_percent, repl_share

# Misc

def project_all_payments():
	try:
		a = 0
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * FROM payments").fetchall()
			for row in rows:
				a += 1
		return a
	except:
		return 0

def project_all_rub():
	try:
		a = 0
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * FROM payments").fetchall()
			for row in rows:
				a += float(row[2])

		return round(float(a))
	except:
		return 0		

def project_all_id():
	try:
		array = []
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute("SELECT * FROM users").fetchall()
			for row in rows:
				array.append(row[1])

		return array
	except:
		return 0

# Регистрация пользователя
def user_exists_ticket(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `ticket` WHERE `user_id` = ?', (user_id,)).fetchall()
			return bool(len(result))
	except:
		return False

def user_add_ticket(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `ticket` (`user_id`, `merchant_id`) VALUES(?,?)", (user_id, 0))
	except:
		pass

def user_exists_casino(user_id):
	try:

		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			return bool(len(result))

	except:
		return False

def user_add_casino(user_id, username, invite_code):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `users` (`user_id`, `user_name`, `balance`, `invite_code`, `win`, `lose`, `all`, `receive`, `status`) VALUES(?,?,?,?,?,?,?,?,?)", (user_id, username, 0, invite_code,
				0, 0, 0, 0, 2))
	except:
		pass

# Информация о воркере
def worker_receive(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[7]
	except:
		pass

def worker_payments(code):
	try:
		array = []
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `payments` WHERE `code` = ?', (code,)).fetchall()
			for row in result:
				username = repl(row[2])
				array.append(f"({row[0]}) - {row[2]} ₽")
			
			return array
	except:
		return 0

def worker_merchant_id(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `ticket` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[1]
	except:
		pass

def worker_code(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[1]
	except:
		pass		

def worker_phone(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[2]
	except:
		pass	

def worker_telegram_id(code):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `code` = ?', (code,)).fetchall()
			for row in result:
				return row[0]
	except:
		pass	

def worker_balance(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[3]
	except:
		pass

def worker_allpayments(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[4]
	except:
		pass

def worker_all_along(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[5]
	except:
		pass

def worker_middlepayments(user_id):
	try:
		array = []
		code = worker_code(user_id)
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `payments` WHERE `code` = ?', (code,)).fetchall()
			for row in result:
				array.append(row[2])
			
		if (len(array) > 0):	
			middle = numpy.mean(array)
			return repl_percent(middle)
		else:
			return 0

	except:
		return 0

def worker_exists_code(code):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `code` = ?', (code,)).fetchall()
			return bool(len(result))
	except:
		return False		

def worker_mamonts(invite_code):
	try:
		array = []
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `invite_code` = ?', (invite_code,)).fetchall()
			for row in result:
				username = repl(row[2])
				array.append(f"({row[0]}) - @{row[2]} - {row[3]} ₽ - {row[9]}")
			
			return array
	except:
		return 0		

# Информация о пользователях казино
def user_num(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[0]
	except:
		pass

def user_in_fake(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[7]
	except:
		pass	

def user_telegram_id(num):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `id` = ?', (num,)).fetchall()
			for row in result:
				return row[1]
	except:
		return '0'

def user_username(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[2]
	except:
		return '0'		

def user_invite_code(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[4]
	except:
		return '0'

def user_userid_mamonts(invite_code):
	try:
		array = []
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `invite_code` = ?', (invite_code,)).fetchall()
			for row in result:
				array.append(row[1])
			
			return array
	except:
		return 0

def user_username_mamonts(invite_code):
	try:
		array = []
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `invite_code` = ?', (invite_code,)).fetchall()
			for row in result:
				array.append(row[2])
			
			return array
	except:
		return 0		

def user_balance(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[3]
	except:
		pass	

def user_win(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[5]
	except:
		pass	

def user_lose(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[6]
	except:
		pass	

def user_receives(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[8]
	except:
		pass							

def user_status(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[9]
	except:
		pass			

def user_count_payments(user_id):
	try:
		a = 0
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute('SELECT * FROM `payments` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in rows:
				a += 1

		return a
	except:
		pass

# Работа с воркерами
def worker_update_profit(worker_id, amount):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `payments` = payments + ? WHERE `user_id` = ?", (1, worker_id))
			cur.execute("UPDATE `workers` SET `all_along` = all_along + ? WHERE `user_id` = ?", (amount, worker_id))
			cur.execute("UPDATE `workers` SET `balance` = balance + ? WHERE `user_id` = ?", (amount, worker_id))
	except:
		pass


def user_add_promo(name, price):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `promocode` (`name`, `price`) VALUES(?,?)", (name, price))

		return 1
	except:
		return 0

def user_add_workers(user_id, code, phone):
	try:

		time = datetime.date.today()

		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `workers` (`user_id`, `code`, `phone`, `balance`, `payments`, `all_along`, `date`, `receive`) VALUES(?,?,?,?,?,?,?,?)", (user_id, code, phone, 0, 0, 0, time, 0))
	except:
		pass

def user_update_merchant_id(user_id, merchant_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `ticket` SET `merchant_id` = ? WHERE `user_id` = ?", (merchant_id, user_id))
	except:
		pass

def worker_update_receive(user_id, receive):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `receive` = ? WHERE `user_id` = ?", (receive, user_id))

		worker_update_balane(user_id, -receive)	
	except:
		pass

def worker_clear_receive(user_id, receive):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `receive` = receive + ? WHERE `user_id` = ?", (-receive, user_id))
	except:
		pass

def worker_update_balane(user_id, receive):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `workers` SET `balance` = balance + ? WHERE `user_id` = ?", (receive, user_id))
	except:
		pass

# Работа с пользователями казино
def user_clear_fake(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `all` = ? WHERE `user_id` = ?", ('0', user_id))
		return 1
	except:
		return 0

def user_add_fake(user_id, deposit):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `all` = ? WHERE `user_id` = ?", (deposit, user_id))
		return 1
	except:
		return 0

def user_clear_stats(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `win` = ? WHERE `user_id` = ?", (0, user_id))
			cur.execute("UPDATE `users` SET `lose` = ? WHERE `user_id` = ?", (0, user_id))

		return 1
	except:
		return 0

def exists_promo(name):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `promocode` WHERE `name` = ?', (name,)).fetchall()
			if (bool(len(result)) == True):
				for row in result:
					return row[1]
			else:
				return 0
	except:
		return 0

def delete_promo(name):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("DELETE FROM `promocode` WHERE `name` = ?", (name,))
	except:
		pass		

def user_update_username(user_id, username):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `user_name` = ? WHERE `user_id` = ?", (username, user_id))

		return 1
	except:
		return 0

def user_update_status(user_id, status):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

		return 1
	except:
		return 0

def user_set_balance(user_id, value):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?", (value, user_id))

		return 1
	except:
		return 0

def user_balance_repl_percent(user_id):
	try:
		balance = user_balance(user_id)
		balance = repl_percent(balance)
		user_set_balance(balance)
	except:
		pass

def user_update_balance(user_id, value):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `balance` = balance + ? WHERE `user_id` = ?", (value, user_id))

		user_balance_repl_percent(user_id)
		return 1
	except:
		return 0

def user_update_invite_code(user_id, code):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `invite_code` = ? WHERE `user_id` = ?", (code, user_id))
	except:
		pass

def user_update_win(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `win` = win + ? WHERE `user_id` = ?", (1, user_id))

		return 1
	except:
		return 0		

def user_update_lose(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `lose` = lose + ? WHERE `user_id` = ?", (1, user_id))

		return 1
	except:
		return 0				

def user_update_receive(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `receive` = receive + ? WHERE `user_id` = ?", (1, user_id))

		return 1
	except:
		return 0

def user_add_listpay(user_id, code, amount):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `payments` (`user_id`, `code`, `amount`) VALUES(?,?,?)", (user_id, code, amount))
	except:
		pass										

def user_balance_repl_percent(user_id):
	try:

		balance = user_balance(user_id)
		balance = repl_percent(balance)
		user_set_balance(balance)

	except:
		pass
