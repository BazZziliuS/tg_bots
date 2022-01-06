import telebot

bot = telebot.TeleBot("токен", threaded=True, num_threads=300)
admin_1 = 1347410943
admin_chat = -1001191992636
workers_chat_link = 'https://t.me/joinchat/Uab6fpWz8hzqTJ26'

manual_link = "https://telegra.ph/Primer-11-16-3"
screens_bot = "screens_help_robot"
hello = "🎊Добро пожаловать в команду!🎊  \n\n" \
	f"📚Мануал для работы:  <a href='{manual_link}'>ССЫЛКА</a>\n\n" \
    f"🖼️Скрины для убедительности: <a href='t.me:/{screens_bot}'>ССЫЛКА</a>\n\n" \
    f"Читайте закреп!"
