from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

backMenu_btn = KeyboardButton('◀️ В главное меню')
reviewBtn = InlineKeyboardMarkup(resize_keyboard=True).add(InlineKeyboardButton('🚀 Отзывы', url='t.me/YandexSaleReviews'))

# Меню выбора оплаты
qiwi_btn = KeyboardButton('🥝 QIWI')
btc_btn = KeyboardButton('📀 BITCOIN')
card_btn = KeyboardButton('💳 Банковская карта')
paymentsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(qiwi_btn).add(btc_btn).add(card_btn).add(backMenu_btn)

# Меню проверки оплаты
checkPay_btn = KeyboardButton('💎 Я оплатил')
cancelPay_btn = KeyboardButton('❌ Отмена')
checkPayMenu = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).add(checkPay_btn).add(cancelPay_btn)