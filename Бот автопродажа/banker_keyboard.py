from telebot import types

# Клавиатура основная
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)
    btn1 = types.KeyboardButton('💁🏻‍♀️ Мой профиль')
    btn2 = types.KeyboardButton('🚀 Каталог')
    btn3 = types.KeyboardButton('Тех. поддержка')
    btn4 = types.KeyboardButton('Правила')
    btn5 = types.KeyboardButton('О нас')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    return markup



# Клавиатура администратора
def admin_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = False, resize_keyboard = True)
    btn1 = types.KeyboardButton('Добавить товары')
    btn2 = types.KeyboardButton('Удалить товары')
    btn3 = types.KeyboardButton('Рассылка')
    btn4 = types.KeyboardButton('Назад')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup    