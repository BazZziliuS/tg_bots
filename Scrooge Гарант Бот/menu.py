from telebot import types


main_menu = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
main_menu.add('🔍 Найти user', '🤝 Мои сделки', '🎩Мой профиль', '🎁 Пожертвовать', '💬 Помощь')

admin_menu = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
admin_menu.add('Статистика', 'Рассылка', 'Изменить баланс', 'Оплата', 'Админы', 'Канал', 'Описание', 'Комиссия', 'Статус', 'Автопостинг', 'Приветствие')
admin_menu.row('Вернуться в главное меню')

profile_menu = types.InlineKeyboardMarkup(row_width=2)
profile_menu.add(
	types.InlineKeyboardButton(text='Пополнить', callback_data='input'),
	types.InlineKeyboardButton(text='Вывод', callback_data='output'),
)

donate_menu = types.InlineKeyboardMarkup(row_width=1)
donate_menu.add(
	types.InlineKeyboardButton(text='💰Пожертвовать', callback_data='donate'),
	types.InlineKeyboardButton(text='🥇Топ донатов', callback_data='top_donate'),)

donate = types.InlineKeyboardMarkup(row_width=1)
donate.add(
	types.InlineKeyboardButton(text='🥝QIWI', callback_data='donate_qiwi'),
	types.InlineKeyboardButton(text='🤖С баланса', callback_data='donate_balance'),
)
donat_keyboard = types.InlineKeyboardMarkup(row_width=1)
donat_keyboard.add(types.InlineKeyboardButton(text='🦆Стать частью Утиной Империи', url='https://t.me/scrooge_garantbot'))

input_menu = types.InlineKeyboardMarkup(row_width=2)
input_menu.add(
	types.InlineKeyboardButton(text='Qiwi', callback_data='input_qiwi'),
	types.InlineKeyboardButton(text='Bitcoin', callback_data='input_btc'),
)

update_name = types.InlineKeyboardMarkup(row_width=2)
update_name.add(
	types.InlineKeyboardButton(text='Есть вопрос?', url='https://t.me/imperial_scrooge'),
	types.InlineKeyboardButton(text='Наш чат услуг', url='https://t.me/joinchat/S_VgTx0fTRlGVD1n9zlljQ'),
	types.InlineKeyboardButton(text='💡Как пользоваться ботом?', callback_data='how'),

)

qiwi_menu = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
qiwi_menu.add('Токен', 'Номер', 'Карта', 'Баланс', 'Токен p2p', 'Api btc', 'Api secret btc')
qiwi_menu.add('Назад')

one_two = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
one_two.add('Первый', 'Второй', 'Отмена')

back = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
back.add('Отмена')

clear_inline = types.InlineKeyboardMarkup(row_width=2)




