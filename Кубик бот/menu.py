from aiogram import types
from utils.mydb import *


main_menu_btn = [
    '🎲 Игра',
    '👤 Профиль',
    '⚠️ Support',
    '🚧 Отзывы',
    '🚸 Наш чат',
]

admin_sending_btn = [
    '✅ Начать', # 0
    '🔧 Отложить', # 1
    '❌ Отменить' # 2
]

to_close = types.InlineKeyboardMarkup(row_width=3)
to_close.add(
    types.InlineKeyboardButton(text='❌', callback_data='to_close')
)


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(main_menu_btn[0])
    markup.add(main_menu_btn[2], main_menu_btn[1])
    markup.add(main_menu_btn[3],main_menu_btn[4])

    return markup


def profile():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🤖Пополнить | QIWI', callback_data='qiwi'),
        types.InlineKeyboardButton(text='🤖Пополнить | BANKER', callback_data='banker'),
        types.InlineKeyboardButton(text='👑Заказать вывод', callback_data='withdraw'),
    )

    return markup


def payment_menu(url):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='👉 Перейти к оплате 👈', url=url),
    )
    markup.add(
        types.InlineKeyboardButton(text='🔄 Проверить', callback_data='check_payment'),
        types.InlineKeyboardButton(text='❌ Отменить оплату', callback_data='cancel_payment'),
    )

    return markup


def admin_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text='ℹ️ Информаци', callback_data='admin_info'),
        types.InlineKeyboardButton(text='🔧 Изменить баланс', callback_data='give_balance'),
        types.InlineKeyboardButton(text='⚙️ Запросы на вывод', callback_data='withdrawal_requests'),
        types.InlineKeyboardButton(text='⚙️ Рассылка', callback_data='email_sending'),
        )

    return markup


def email_sending():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add( 
        types.InlineKeyboardButton(text='✔️ Рассылка(только текст)', callback_data='email_sending_text'), 
        types.InlineKeyboardButton(text='✔️ Рассылка(текст + фото)', callback_data='email_sending_photo'),
        types.InlineKeyboardButton(text='ℹ️ Информация о выделениях', callback_data='email_sending_info')
    )

    return markup


def admin_sending():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        admin_sending_btn[0],
        admin_sending_btn[1],
        admin_sending_btn[2],
    )

    return markup


def admin_buttons():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🔧 Добавить', callback_data='admin_buttons_add'),
        types.InlineKeyboardButton(text='🔧 Удалить', callback_data='admin_buttons_del'),
        types.InlineKeyboardButton(text='❌ Выйти', callback_data='back_to_admin_menu')
    )

    return markup
