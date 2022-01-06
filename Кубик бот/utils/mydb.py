import sqlite3


def connect():
    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()

    return conn, cursor

conn, cursor = connect()

def create_tables():
    try:
        cursor.execute(f'CREATE TABLE users (user_id TEXT, first_name TEXT, username TEXT, balance DECIMAL(10, 2), who_invite TEXT, date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE check_payment (user_id TEXT, code TEXT, referral_code TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE sending (type TEXT, text TEXT, photo TEXT, date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE withdraw (id TEXT, user_id TEXT, withdraw_sum DECIMAL(10, 2), info TEXT, date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE game_logs (id TEXT, user_id TEXT, status TEXT, bet DECIMAL(10, 2), date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE games (id TEXT, user_id TEXT, bet DECIMAL(10, 2))')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE stats (user_id TEXT, money DECIMAL(10, 2))')
        conn.commit()
    except:
        pass
    
    try:
        cursor.execute(f'CREATE TABLE list (type TEXT, text TEXT, photo TEXT, date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE deposit_logs (user_id TEXT, type TEXT, sum DECIMAL(10, 2), date TEXT)')
        conn.commit()
    except:
        pass
    
    try:
        cursor.execute(f'CREATE TABLE withdraw_logs (user_id TEXT, sum DECIMAL(10, 2), date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE profit_logs (user_id TEXT, sum DECIMAL(10, 2), date TEXT)')
        conn.commit()
    except:
        pass


create_tables()
