import telebot
from telebot import types

admin = telebot.types.ReplyKeyboardMarkup(True)
admin.row('Статистика','Рассылка')
admin.row('Настройки','Пользователи')


main = telebot.types.ReplyKeyboardMarkup(True)
main.row('🃏 Играть')
main.row('🖥 Кабинет','📜 Информация')


otmena = telebot.types.ReplyKeyboardMarkup(True)
otmena.row('Отмена')

otziv = telebot.types.ReplyKeyboardMarkup(True)
otziv.row('Да', 'Нет')
