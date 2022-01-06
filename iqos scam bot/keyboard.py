from telebot import types


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn = types.KeyboardButton(text='Купить iQOS')
    btn2 = types.KeyboardButton(text='Купить стики HEETS')
    btn4 = types.KeyboardButton(text='Помощь')
    markup.add(btn, btn2)
    markup.add(btn4)
    return markup

def admin_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton(text='Рассылка')
    btn2 = types.KeyboardButton(text='Кол-во пользователей')
    btn3 = types.KeyboardButton(text='Список всех пользователей')
    markup.add(btn, btn2)
    markup.add(btn3)
    return markup