from telebot import types
from senior_config import workers_chat_link

def main_keyboard():
    main_keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Подать заявку", callback_data="to_team")
    main_keyboard.row(button)
    return main_keyboard

def second_keyboard(id, username):
    second_keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="✅Отправить", callback_data=f"send-{id}-{username}")
    button1 = types.InlineKeyboardButton(text="❌Отменить", callback_data="close")
    second_keyboard.add(button, button1)
    return second_keyboard

def admin_chat_keyboard(id, username):
    admin_chat_keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="✅Принять", callback_data=f"accept-{id}-{username}")
    button1 = types.InlineKeyboardButton(text="❌Отклонить", callback_data=f"reject-{id}-{username}")
    admin_chat_keyboard.add(button, button1)
    return admin_chat_keyboard

def chat_keyboard():
    chat_keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="➡️Перейти в чат", url=workers_chat_link)
    chat_keyboard.add(button)
    return chat_keyboard

def admin_menu_keyboard():
    admin_menu_keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Добавить админа", callback_data=f"add_admin")
    button1 = types.InlineKeyboardButton(text="Удалить админа", callback_data=f"del_admin")
    admin_menu_keyboard.row(button)
    admin_menu_keyboard.row(button1)
    return admin_menu_keyboard
