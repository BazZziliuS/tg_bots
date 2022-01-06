import sqlite3
from time import time
from random import choice
import _parser_
import threading

lock = threading.Lock()

conn = sqlite3.connect('bot.db', check_same_thread=False)
cur = conn.cursor()


def reset_attacks():
	cur.execute('UPDATE attacks SET count = 0')
	conn.commit()


def add_proxy(proxy):
	lock.acquire(True)

	cur.execute('INSERT INTO proxies (proxy) VALUES(?)', (proxy,))
	conn.commit()

	lock.release()


def del_proxy(proxy):
	lock.acquire(True)

	cur.execute('DELETE FROM proxies WHERE proxy = ?', (proxy,))
	conn.commit()

	lock.release()


def update_proxies(proxies):
	lock.acquire(True)

	cur.execute('SELECT proxy FROM proxies')
	proxies_db = list(map(lambda p: p[0], cur.fetchall()))

	lock.release()

	for p in proxies:
		if not p in proxies_db:
			add_proxy(p)


def get_rand_proxy():
	return choice(get_proxies())


def get_proxies():
	lock.acquire(True)

	cur.execute('SELECT proxy FROM proxies')
	proxies = list(map(lambda p: p[0], cur.fetchall()))

	lock.release()

	if not proxies:
		parsed = _parser_.get_proxies()
		open('last_parsing.txt', 'w').write(str(time()))

		update_proxies(parsed)
		return parsed

	return proxies


def get_count_attack(user_id):
	lock.acquire(True)

	cur.execute('SELECT count FROM attacks WHERE id = ?', (user_id,))
	attacks = cur.fetchone()

	lock.release()

	if not attacks:
		cur.execute('INSERT INTO attacks (id) VALUES(?)', (user_id,))
		return 0

	return attacks[0]


def act_count_attack(act, user_id):
	current = get_count_attack(user_id)

	lock.acquire(True)

	if act.lower() == 'add':
		cur.execute('UPDATE attacks SET count = ? WHERE id = ?', (current+1, user_id))
	elif act.lower() == 'remove':
		cur.execute('UPDATE attacks SET count = ? WHERE id = ?', (current-1, user_id))

	conn.commit()

	lock.release()


def get_bomber_state(user_id):
	lock.acquire(True)

	cur.execute('SELECT * FROM attacks WHERE id = ?', (user_id,))
	if not cur.fetchone():
		cur.execute('INSERT INTO attacks (id) VALUES(?)', (user_id,))

	cur.execute('SELECT state FROM attacks WHERE id = ?', (user_id,))
	state = cur.fetchone()[0]

	lock.release()
	conn.commit()

	return state	


def set_bomber_state(state, user_id):
	lock.acquire(True)

	cur.execute('UPDATE attacks SET state = ? WHERE id = ?', (state, user_id))
	conn.commit()

	lock.release()


def get_call_attacks_state(user_id):
	lock.acquire(True)

	cur.execute('SELECT * FROM call_attacks WHERE user = ?', (user_id,))
	if not cur.fetchone():
		cur.execute('INSERT INTO call_attacks (user) VALUES(?)', (user_id,))

	cur.execute('SELECT state FROM call_attacks WHERE user = ?', (user_id,))
	state = cur.fetchone()[0]

	lock.release()
	conn.commit()

	return state


def set_call_attacks_state(state, user_id):
	lock.acquire(True)

	cur.execute('SELECT * FROM call_attacks WHERE user = ?', (user_id,))
	if not cur.fetchone():
		cur.execute('INSERT INTO call_attacks (user) VALUES(?)', (user_id,))

	cur.execute('UPDATE call_attacks SET state = ? WHERE user = ?', (state, user_id))

	lock.release()
	conn.commit()


def referals_count(user_id):
    lock.acquire(True)

    cur.execute('SELECT * FROM referals WHERE referer = ?', (user_id,))
    referals = cur.fetchall()

    lock.release()
    return len(referals)


def get_referal(user_id):
    lock.acquire(True)

    cur.execute('SELECT referer FROM referals WHERE id = ?', (user_id,))
    referal = cur.fetchone()

    lock.release()

    if referal:
        return referal[0]


def set_referal(user_id, referer_id):
    if not get_referal(user_id):
        lock.acquire(True)

        cur.execute('INSERT INTO referals (id, referer) VALUES(?, ?)', (user_id, referer_id))

        lock.release()
        conn.commit()