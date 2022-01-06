from aiogram import types
from utils.user import User
from utils.mydb import *

# import sqlite3
import random
import datetime
import config


my_games_txt = """
🃏 Мои игры: {}

💖 Выигрыш: {} RUB
💔 Проигрыш: {} RUB
📊 Профит: {} RUB

Данные приведены за все время
"""

raiting_txt = """
📊 ТОП 3 игроков:

🥇 1 место - {} RUB
🥈 2 место - {} RUB
🥉 3 место - {} RUB

🏆 Ваше место в рейтинге: {} из {} ({} RUB)

Данные приведены за последние 30 дней.
Рейтинг обновляется каждые несколько минут.
"""

help_txt = """
По всем вопросам и выплатам @melvin_hb
"""

dice_game_info_txt = """
🎲Кости #{}
💰Ставка: {} RUB

👤Создал: {}
"""


dice_game_result_txt = """
🎲Кости #{}
💰Банк: {} RUB

👤 {} and {}

👆Ваш результат: {}
👇Результат соперника: {}

{}
"""


game_result_txt = """
{} #{}
💰Банк: {} RUB

ℹ️Результаты:
❕ {} | {}
❕ {} | {}

Итог: {}
"""


class Game():

    def __init__(self, code):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM games WHERE id = "{code}"')
        info = cursor.fetchall()

        if len(info) == 0:
            self.status = False
        else:
            self.status = True

            self.id_game = info[0][0]
            self.user_id = info[0][1]
            self.bet = float(info[0][2])

    def del_game(self):
        conn, cursor = connect()

        cursor.execute(f'DELETE FROM games WHERE id = "{self.id_game}"')
        conn.commit()


def dice_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='❇️Создать игру', callback_data='create_dice'),
        types.InlineKeyboardButton(text='🔁Обновить', callback_data='reload_dice'),
    )

    markup = get_games_menu(markup)

    markup.add(
        types.InlineKeyboardButton(text='📝Мои игры', callback_data='my_games_dice'),
        types.InlineKeyboardButton(text='🏆Рейтинг', callback_data='rating_dice')
    )

    return markup


def get_games_menu(markup):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM games')
    games = cursor.fetchall()

    for i in games:
        markup.add(types.InlineKeyboardButton(text=f'🎲Игра #{i[0]} | {i[2]} RUB', callback_data=f'dice_game:{i[0]}'))

    return markup


def cancel_dice():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='❌Отменить', callback_data='cancel_dice')
    )

    return markup


def back_dice():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='⬅️Назад', callback_data='back_dice')
    )

    return markup


def create_game(user_id, bet):
    conn, cursor = connect()

    cursor.execute(f'INSERT INTO games VALUES("{random.randint(111111, 999999)}", "{user_id}", "{bet}")')
    conn.commit()


def my_games_dice(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM game_logs WHERE user_id = "{user_id}"')
    games = cursor.fetchall()

    amount_games = len(games)

    win_money = 0
    lose_money = 0
    markup = types.InlineKeyboardMarkup(row_width=2)

    if len(games) < int(config.config('range_game_list')):
        amount = len(games)
    else:
        amount = int(config.config('range_game_list'))


    for i in range(amount):
        if games[i][2] == 'win':
            win_money += float(games[i][3])

            markup.add(types.InlineKeyboardButton(text=f'{games[i][3]} RUB | ✅Победа', callback_data=f'gamelog'))

        elif games[i][2] == 'lose':
            lose_money += float(games[i][3])

            markup.add(types.InlineKeyboardButton(text=f'{games[i][3]} RUB | 🔴Проигрыш', callback_data=f'gamelog'))

    profit_money = win_money - lose_money
    profit_money = '{:.2f}'.format(profit_money)

    win_money = '{:.2f}'.format(win_money)
    lose_money = '{:.2f}'.format(lose_money)

    msg = my_games_txt.format(
        amount_games,
        win_money,
        lose_money,
        profit_money,
    )

    return msg, markup


def rating_dice(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM stats WHERE user_id = "{user_id}"')
    user = cursor.fetchall()

    if len(user) == 0:
        cursor.execute(f'INSERT INTO stats VALUES("{user_id}", "0")')
        conn.commit()

        user_money = 0
    else:
        user_money = user[0][1]

    cursor.execute(f'SELECT * FROM stats')
    games = cursor.fetchall()

    games = sorted(games, key=lambda money: float(money[1]), reverse=True)


    size_top = len(games)
    user_top = 0

    for i in games:
        user_top += 1

        if i[0] == str(user_id):
            break

    msg = raiting_txt.format(
        '{:.2f}'.format(games[0][1]),
        '{:.2f}'.format(games[1][1]),
        '{:.2f}'.format(games[2][1]),
        user_top,
        size_top,
        user_money
    )

    return msg


def dice_game(code):
    game = Game(code)

    if game.status == False:
        return False
    else:
        msg = dice_game_info_txt.format(
            game.id_game,
            game.bet,
            User(game.user_id).username
        )

        msg += f'👤 2Player: Ожидание...'

        markup = types.InlineKeyboardMarkup(row_width=2)


        markup.add(
            types.InlineKeyboardButton(text='🎲 Кости', callback_data=f'start_game_dice:{game.id_game}'),
            types.InlineKeyboardButton(text='⬅️ Назад', callback_data=f'back_dice')
        )

        return msg, markup


def start_game_dice(user_id, game, value_dice1, value_dice2):
    user = User(user_id)

    user.update_balance(-game.bet)
    user = User(user_id)

    value_dice1 = value_dice1
    value_dice2 = value_dice2

    win_money = ((game.bet * 2) / 100) * (100 - float(config.config('commission_percent')))
    profit_money = ((game.bet * 2) / 100) * float(config.config('commission_percent'))

    if value_dice1[0] > value_dice2[0]:
        user.update_balance(win_money)

        dice_write_game_log(game.id_game, user_id, 'win', win_money)
        dice_write_game_log(game.id_game, game.user_id, 'lose', win_money)

        status1 = '✅✅✅Поздравляем с победой!'
        status2 = '🔴🔴🔴Вы проиграли!'

    elif value_dice1[0] < value_dice2[0]:
        User(game.user_id).update_balance(win_money)

        dice_write_game_log(game.id_game, game.user_id, 'win', win_money)
        dice_write_game_log(game.id_game, user_id, 'lose', win_money)

        status1 = '🔴🔴🔴Вы проиграли!'
        status2 = '✅✅✅Поздравляем с победой!'


    try:
        conn, cursor = connect()

        msg = f"{user_id} | {game.user_id}"

        cursor.execute(f'INSERT INTO profit_logs VALUES ("{msg}", "{profit_money}", "{datetime.datetime.now()}")')
        conn.commit()
    except:
        pass

    msg1 = dice_game_result_txt.format(
        game.id_game,
        win_money,
        User(user_id).username,
        User(game.user_id).username,
        value_dice1[0],
        value_dice2[0],
        status1
    )

    msg2 = dice_game_result_txt.format(
        game.id_game,
        win_money,
        User(user_id).username,
        User(game.user_id).username,
        value_dice2[0],
        value_dice1[0],
        status2
    )

    return [user_id, game.user_id], [msg1, msg2], [value_dice2[1], value_dice1[1]]


def dice_write_game_log(id, user_id, status, bet):
    conn, cursor = connect()

    cursor.execute(f'INSERT INTO game_logs VALUES("{id}", "{user_id}", "{status}", "{bet}", "{datetime.datetime.now()}")')
    conn.commit()

    cursor.execute(f'SELECT * FROM stats WHERE user_id = "{user_id}"')
    stats = cursor.fetchall()

    if len(stats) == 0:
        cursor.execute(f'INSERT INTO stats VALUES("{user_id}", "0")')
        conn.commit()
    else:
        cursor.execute(f'UPDATE stats SET money = {float(stats[0][1]) + float(bet)} WHERE user_id = "{user_id}"')
        conn.commit()


def profit_logs(user_id, profit):
    conn, cursor = connect()

    cursor.execute(
        f'INSERT INTO profit_logs VALUES("{user_id}", "{profit}", "{datetime.datetime.now()}")')
    conn.commit()


async def roll_dice(bot, user_id):
    value = await bot.send_dice(user_id)

    return int(value.dice.value), value.message_id


async def start_roll(bot, game, chat_id):
    await bot.send_message(chat_id=chat_id, text='❕ Бросаем кости...')

    value_dice1 = await roll_dice(bot, chat_id)
    value_dice2 = await roll_dice(bot, game.user_id)


    if value_dice1[0] == value_dice2[0]:
        await bot.send_message(chat_id=chat_id, text='❕ Противник бросает кости...')
        await bot.forward_message(chat_id=chat_id, from_chat_id=game.user_id, message_id=value_dice2[1])
        await bot.send_message(chat_id=chat_id, text='🔵🔵🔵Ничья!!!\n\nПеребрасываем кости...')

        await bot.send_message(chat_id=game.user_id, text='❕ Противник бросает кости...')
        await bot.forward_message(chat_id=game.user_id, from_chat_id=chat_id, message_id=value_dice1[1])
        await bot.send_message(chat_id=game.user_id, text='🔵🔵🔵Ничья!!!\n\nПеребрасываем кости...')

        return await start_roll(bot, game, chat_id)
    else:
        return value_dice1, value_dice2


def check_win(value1, value2):
    if value1 > value2:
        return True
    else:
        return False


async def main_start(game, bot, chat_id):
    game.del_game()

    value_dice1, value_dice2 = await start_roll(bot, game, chat_id)

    info = start_game_dice(chat_id, game, value_dice1, value_dice2)

    from_chat_id = lambda i: 1 if i == 0 else 0 if i == 1 else 100

    for i in range(2):
        await bot.send_message(chat_id=info[0][i], text='❕ Противник бросает кости...')
        await bot.forward_message(chat_id=info[0][i], from_chat_id=info[0][from_chat_id(i)], message_id=info[2][i])
        await bot.send_message(chat_id=info[0][i], text=info[1][i])


def get_list_users(game, user_id):
    user_list = [user_id]

    user_list.append(game.user_id)

    if game.user_id2 != '0':
        user_list.append(game.user_id2)
    if game.user_id3 != '0':
        user_list.append(game.user_id3)
    if game.user_id4 != '0':
        user_list.append(game.user_id4)

    return user_list