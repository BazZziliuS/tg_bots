from utils.mydb import *

import config


class User():
    
    def __init__(self, user_id=None, username=None):
        if username != None:
            conn, cursor = connect()

            cursor.execute(f'SELECT * FROM users WHERE username = "{username}"')
            user = cursor.fetchone()

            if user != None:
                user_id = user[0]
            else:
                self.user_id = None
                return

        conn, cursor = connect()
        cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
        user = cursor.fetchone()

        self.user_id = user[0]
        self.first_name = user[1]
        self.username = user[2]
        self.balance = user[3]
        self.who_invite = user[4]
        self.date = user[5]


    def update_balance(self, value):
        conn, cursor = connect()
        cursor.execute(f'UPDATE users SET balance = {float(self.balance) + float(value)} WHERE user_id = "{self.user_id}"')
        conn.commit()

        return True


    def give_ref_reward(self, money):
        conn, cursor = connect()

        if self.who_invite != '0':
            User(self.who_invite).update_balance(float(float(money) / 100 * float(config.config("ref_percent"))))

            cursor.execute(f'SELECT * FROM stats WHERE user_id = "{self.who_invite}"')
            user = cursor.fetchall()

            if len(user) == 0:
                cursor.execute(f'INSERT INTO stats VALUES("{self.who_invite}", "0", "1", "{config.config("ref_reward")}")')
                conn.commit()
            else:
                if user[0][2] == None or user[0][3] == None:
                    cursor.execute(f'UPDATE stats SET ref_profit = 0 WHERE user_id = "{self.who_invite}"')
                    conn.commit()

                    cursor.execute(f'UPDATE stats SET ref_amount = 0 WHERE user_id = "{self.who_invite}"')
                    conn.commit()

                    cursor.execute(f'SELECT * FROM stats WHERE user_id = "{self.who_invite}"')
                    user = cursor.fetchall()

                cursor.execute(
                    f'UPDATE stats SET ref_profit = {float(user[0][3]) + float(float(money) / 100 * float(config.config("ref_percent")))} WHERE user_id = "{self.who_invite}"')
                conn.commit()