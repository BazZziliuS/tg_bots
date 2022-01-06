import telebot
from telebot import types

main = telebot.types.ReplyKeyboardMarkup(True)
main.row('🔗 Сократить ссылку','🔎 Деанон', '♻️ Генератор')
main.row('ℹ️ Информация по IP', '🆔 Информация по ID')
#main.row('🖼 Скрины для скама')
main.row('🖼 Сделать скриншот')
main.row('🖥 Профиль', '📆 Информация')
#main.row('🎁 Конкурс')

screen = types.InlineKeyboardMarkup(row_width=1)
screen.add(
    types.InlineKeyboardButton(text='☑️ Готовые шаблоны', callback_data='shablon'),
    #types.InlineKeyboardButton(text='🎯 Создать свой поддельный скрин', callback_data='gen_proxy'),
)

shab = types.InlineKeyboardMarkup(row_width=1)
shab.add(
    types.InlineKeyboardButton(text='📦 Авито', callback_data='avito'),
    types.InlineKeyboardButton(text='🧺 Юла', callback_data='youla'),
)

ff = telebot.types.ReplyKeyboardMarkup(True)
ff.row('✉️ Запрос почты','🔌 Оплата по ссылке', '🔑 Подозрительный домен')
ff.row('🔐 CVC код', '📞 Авито — 900')
ff.row('💳 Cписание/баланс', '🚨 Запрос кода')
ff.row('📧 Запрос почты', '🔕 Нет уведомления', '📆 Информация')

cancle = telebot.types.ReplyKeyboardMarkup(True)
cancle.row('🎯 Вернуться в меню')

info = types.InlineKeyboardMarkup(row_width=1)
info.add(
    types.InlineKeyboardButton(text='👨‍💻 Админ & создатель', url='https://t.me/Shifter_LZT'),
    types.InlineKeyboardButton(text='🔝 Топ донатеров', callback_data='top_donator'),
)

gen = types.InlineKeyboardMarkup(row_width=1)
gen.add(
    types.InlineKeyboardButton(text='🔐 Генератор паролей', callback_data='gen_pass'),
    types.InlineKeyboardButton(text='🧰 Генератор ников', callback_data='gen_nick'),
    types.InlineKeyboardButton(text='🌐 Генератор прокси', callback_data='gen_proxy'),
)

spas = types.InlineKeyboardMarkup(row_width=1)
spas.add(
    types.InlineKeyboardButton(text='❓ Я нашел баг что делать?', callback_data='i_bag'),
    #types.InlineKeyboardButton(text='🔗 Сократить ссылку', callback_data='shorter'),
)

gen_pass = types.InlineKeyboardMarkup(row_width=1)
gen_pass.add(
    types.InlineKeyboardButton(text='🧬 Сгенерировать', callback_data='generate_pass'),
    types.InlineKeyboardButton(text='⚙️ Параметры', callback_data='settings_pass'),
    types.InlineKeyboardButton(text='◀️ Назад', callback_data='back_gen'),
)

gen_proxy = types.InlineKeyboardMarkup(row_width=1)
gen_proxy.add(
    types.InlineKeyboardButton(text='🔄 Сгенерировать', callback_data='generate_proxy'),
    types.InlineKeyboardButton(text='◀️ Назад', callback_data='back_gen'),
)

gen_proxy2 = types.InlineKeyboardMarkup(row_width=1)
gen_proxy2.add(
    #types.InlineKeyboardButton(text='http/s', callback_data='gen_http'),
    #types.InlineKeyboardButton(text='socks 4', callback_data='gen_socks4'),
    types.InlineKeyboardButton(text='socks 5', callback_data='gen_socks5'),
    types.InlineKeyboardButton(text='◀️ Назад', callback_data='back_gen'),
)

gen_nick = types.InlineKeyboardMarkup(row_width=1)
gen_nick.add(
    types.InlineKeyboardButton(text='💈 Сгенерировать', callback_data='gene_nick'),
    types.InlineKeyboardButton(text='⚠️ Сгенерировать 5 ников', callback_data='gene_nick5'),
    types.InlineKeyboardButton(text='◀️ Назад', callback_data='back_gen'),
)

admin = types.InlineKeyboardMarkup(row_width=1)
admin.add(
    types.InlineKeyboardButton(text='✉️ Рассылка', callback_data='sender'),
    types.InlineKeyboardButton(text='⚙️ Настройки бота', callback_data='admin_settings')
    )

admin_sending_btn = [
    '✅ Начать', # 0
    '🔧 Отложить', # 1
    '❌ Отменить' # 2
]


admin_sending = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
admin_sending.add(
    admin_sending_btn[0],
    admin_sending_btn[1],
    admin_sending_btn[2],
)