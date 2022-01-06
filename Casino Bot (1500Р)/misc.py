import random, string, sqlite3

import database
from datetime import datetime, timedelta

def worker_date(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `workers` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[6]
	except:
		pass

def repl(string_0):
	try:

		return string_0.replace('_', '\\_')

	except:
		pass

def replcode(string_0):
	try:
		
		code = ''
		for i in range(5):
			code += string_0[i]

		return code

	except:
		pass

def replphone():
	try:

		operators = ['910', '915', '916', '919', '925', '926', '929', '903', '905', '906', '909', '961', '962', '963', '964', '965', '977']
		nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

		choice = random.choice(operators)
		psw = ''.join([random.choice(nums) for x in range(7)])

		return f'+7{choice}{psw}'

	except:
		pass

def repldate(user_id):
	try:
		date = datetime.strptime(worker_date(user_id), '%Y-%m-%d')
		date = str(date - datetime.now()).split(',')
		date = date[0]
		date = date.replace('-', '')

		if ('days' in date):
			date = date.replace('days', '')
		elif ('day' in date):
			date = date.replace('day', '')

		return date
	except:
		pass

def bill_create(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))	

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def repl(string_0):
	try:

		return string_0.replace('_', '\\_')

	except:
		pass

def repl_percent(value):
	try:

		return float("{0:.2f}".format(float(value)))

	except:
		return 0

def repl_share(value):
	try:
		percent = float(value) / 100 * 80
		return repl_percent(percent)
	except:
		pass

def repl_share_support(value):
	try:
		percent = float(value) / 100 * 70
		return repl_percent(percent)
	except:
		pass						