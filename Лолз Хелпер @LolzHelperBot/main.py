try:
    # Библиотеки
    import telebot
    import datetime
    import random
    import time
    import json
    import requests
    import sys

    from telebot import types

    import urllib.request, phonenumbers, sqlite3, os

    from datetime import datetime, date, timedelta

    from phonenumbers import geocoder, carrier, timezone

    from bs4 import BeautifulSoup as bs

    import threading

    lock = threading.Lock()
    conn = sqlite3.connect('base.db', check_same_thread=False)
    cur = conn.cursor()

    # Файлы
    import kb
    import cfg
    import functions as func
    import general as gen

    bot = telebot.TeleBot(cfg.TOKEN)
    chat_ids_file = 'data/ids.txt'
    conn = sqlite3.connect("base.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
            (user_id TEXT, name TEXT, data TEXT, short INTEGER, deanon INTEGER, gen_pass INTEGER, gen_name INTEGER, ip INTEGER, tg_id INTEGER, screen INTEGER)''')
    q = conn.cursor()
    q.execute('''CREATE TABLE IF NOT EXISTS ban
            (user_id TEXT)''')
    w = conn.cursor()
    w.execute('''CREATE TABLE IF NOT EXISTS sett
            (user_id TEXT, kolvo TEXT, big TEXT, little TEXT, num TEXT, symb TEXT)''')    
    e = conn.cursor()
    conn.commit()
    conn.close()


    def save_chat_id(chat_id):
        chat_id = str(chat_id)
        with open(chat_ids_file,"a+") as ids_file:
            ids_file.seek(0)

            ids_list = [line.split('\n')[0] for line in ids_file]

            if chat_id not in ids_list:
                ids_file.write(f'{chat_id}\n')
                ids_list.append(chat_id)
                dtn = datetime.now()
                print(f'Новый пользователь: {chat_id}, время {dtn}')
            else:
                dtn = datetime.now()
                print(f'пользователь {chat_id} уже сохранен, время {dtn}')
        return

    def send_message_users(message):
        with open(chat_ids_file, "r") as ids_file:
            ids_list = [line.split('\n')[0] for line in ids_file]
        bot.send_message(message.chat.id, 'Рассылка начата, ожидайте вам прийдет отчет.', reply_markup=kb.admin)
        no = 0
        ye = 0
        for chat_id in ids_list:
            data = {
                'chat_id': chat_id,
                'from_chat_id': message.chat.id,
                'message_id': message.message_id,
                'disable_notification': False
            }
            response = requests.post(f'https://api.telegram.org/bot{cfg.TOKEN}/forwardMessage', data=data)
            if '"ok":true' in response.text:
                ye += 1
            if 'bot was blocked' in response.text:
                no += 1
        bot.send_message(message.chat.id, f'Рассылка успешно закончена! Заблокировали бота - <pre>{no}</pre>, дошло - <pre>{ye}</pre>', parse_mode='HTML')



    def generator_url(message):
        try:
            if str(message.text) == '🎯 Вернуться в меню':
                bot.send_message(message.chat.id, '⚡️ Главное меню', parse_mode='HTML', reply_markup=kb.main)
            elif "http" in str(message.text):
                bot.send_message(message.chat.id, f'♻️ Подождите, ссылка сокращается!\nЭто занимает не более 10 секунд',parse_mode='HTML', reply_markup=kb.main)
                text = ''
                r = requests.get(f'https://bitly.su/api/?api=6cc27794b7d2d7cee3bf3d93141a7251b1cef652&url={message.text}')
                data = json.loads(r.text)
                link1 = data['shortenedUrl']
                linkRequest = {"destination": message.text, "domain": { "fullName": "rebrand.ly" }}
                requestHeaders = {"Content-type": "application/json","apikey": "a2b087f48d5c4b2785c9a80bf210ad96",}
                r = requests.post("https://api.rebrandly.com/v1/links", data = json.dumps(linkRequest), headers=requestHeaders)
                linkss = r.json()
                requestHeaders = {"Content-type": "application/x-www-form-urlencoded"}
                r = requests.post("https://goo.su/api/convert", data = f'token=9diDHhJOrxWgCMiwoiy9kkamxkUUGTocUlv7MuCJMQpuwpw0OlTcs5ObNOn4&url={message.text}', headers=requestHeaders)
                data = json.loads(r.text)
                link11 = str(data['short_url'])
                r2 = requests.get(f"{cfg.clck_url_2}{message.text}")
                r3 = requests.get(f"{cfg.clck_url_3}{message.text}")
                r4 = requests.get(f"{cfg.clck_url_4}{message.text}")
                #r5 = requests.get(f"{cfg.clck_url_5}{message.text}")
                text = f"""
1️⃣ {text}{link1}
2️⃣ https://{text}{r2.text}
3️⃣ {text}{link11}
4️⃣ {text}{r3.text}
5️⃣ {text}{r4.text}
    """
                func.act_count_link("add", message.chat.id,)
                bot.send_message(message.chat.id, f'🔗 Готово! Вот ваши ссылки:\n{text}',parse_mode='HTML',disable_web_page_preview = True, reply_markup=kb.main)
            else:
                bot.send_message(message.chat.id, f'🔗 Ссылка указана неверно!',parse_mode='HTML', reply_markup=kb.main)

        except Exception as e:
                bot.send_message(message.chat.id, f'⚒ Произошла ошибка!',parse_mode='HTML', reply_markup=kb.main)
                print(e)
                

    def iddef(message):
        if str(message.text) == '🎯 Вернуться в меню':
            bot.send_message(message.chat.id, '⚡️ <b>Главное меню</b>', parse_mode='HTML', reply_markup=kb.main)
        else:
            try:
                bot.send_message(message.chat.id, f'''<b>♻️ Подождите, поиск данных в БД.
Это занимает не более 20 секунд</b>''', parse_mode='HTML', reply_markup=kb.main)
                r = requests.get('http://d4n13l3k00.ml/api/checkTgId?uid=' + message.text).json()['data']
                if r == 'NOT_FOUND':
                    bot.send_message(message.chat.id, f'''<b> 🔎 Результат поиска:</b>

😞 <code>Пользователя в БД не найдено..</code>
    ''', parse_mode='HTML', reply_markup=kb.main)
                

                else:
                    info = r.split('|')
                    num = info[0].split('\n')
                    text = message.text + '\n'
                    if num[0].isdigit() == True and text == info[1]:
                        bot.send_message(message.chat.id, f'''<b> 🔎 Результат поиска:</b>
                    
🆔 <b>Айди пользователя</b> - <code>{info[1]}</code>                
📱 <b>Номер телефона</b> - <code>{num[0]}</code>
    ''', parse_mode='HTML', reply_markup=kb.main)
                        func.act_count_tg_id("add", message.chat.id,)
                    else:
                        print(num[0].isdigit())
                        print(f'{num[0]}')
                        bot.send_message(message.chat.id, f'''<b>системный сбой, попробуйте позже</b>''', parse_mode='HTML', reply_markup=kb.main)
            except Exception as e:
                print(e)
                time.sleep(3.3)
                bot.send_message(message.chat.id, 'Не верный ID! Попробуйте еще раз', reply_markup=kb.main)


    def screenshot(message):
        if str(message.text) == '🎯 Вернуться в меню':
            bot.send_message(message.chat.id, '⚡️ <b>Главное меню</b>', parse_mode='HTML', reply_markup=kb.main)
        else:
            try:
                user_link = str(message.text)
                r = requests.get(f"https://webshot.deam.io/{user_link}/?width=1440&height=1024?type=png")
                bot.send_photo(message.chat.id, r.content, caption=f'Скриншот с сайта "{user_link}"', parse_mode='HTML', reply_markup=kb.main)
                func.act_count_screen("add", message.chat.id,)
            except Exception as e:
                bot.send_message(message.chat.id, 'Ошибочка вышла! Попробуйте позже', reply_markup=kb.main)
                print(e)


    def ipdef(message):
        if str(message.text) == '🎯 Вернуться в меню':
            bot.send_message(message.chat.id, '⚡️ <b>Главное меню</b>', parse_mode='HTML', reply_markup=kb.main)
        else:
            try:
                r = requests.get(f"https://api.ipdata.co/{message.text}?api-key=7149ffee49a432bb1c7557e3235afdf78a2d22fcdde3a4ecd7a5d5ca")
                data = json.loads(r.text)
                city = str(data['city'])
                region = str(data['region'])
                country_name = str(data['country_name'])
                country_code = str(data['country_code'])
                continent_name = str(data['continent_name'])
                continent_code = str(data['continent_code'])
                calling_code = str(data['calling_code'])
                latitude = str(data['latitude'])
                longitude = str(data['longitude'])
                postal = str(data['postal'])
                
                time_zone = str(data['time_zone']['name'])
                time_zone2 = str(data['time_zone']['current_time'])
                
                currency = str(data['currency']['name'])
                currency2 = str(data['currency']['code'])
                
                #languages = str(data['languages']['name']) Error = list indices must be integers or slices, not str
                
                bot.send_message(message.chat.id, f'''<b> 🔎 Результат поиска:</b>

<b>IP</b> - {message.text}

➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>Город</b>: <code>{city}</code> | <code>{region}</code>
<b>Страна</b>: <code>{country_name} ({country_code})</code>
<b>Часовой пояс</b>: <code>{time_zone}</code>
<b>Код страны</b>: <code>+{calling_code}</code>
<b>Широта</b>: <code>{latitude}</code> | <b>Долгота</b>: <code>{longitude}</code>
<b>Почтовый индекс</b>: <code>{postal}</code>
<b>Континет</b>: <code>{continent_name} ({continent_code})</code>
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
<b>Валюта</b>: <code>{currency} ({currency2})</code>
<b>Точное время</b>: <code>{time_zone2}</code>
    ''', parse_mode='HTML', reply_markup=kb.main)
                func.act_count_ip("add", message.chat.id,)
            except Exception as e:
                bot.send_message(message.chat.id, 'Не верный айпи! Попробуйте еще раз', reply_markup=kb.main)
                print(e)
       
    def deanondef(message):
        if str(message.text) == '🎯 Вернуться в меню':
            bot.send_message(message.chat.id, '⚡️ <b>Главное меню</b>', parse_mode='HTML', reply_markup=kb.main)
        else:
                try:
                    if '+' in str(message.text):                    
                            z = phonenumbers.parse(str(message.text), None)
                            vall = phonenumbers.is_valid_number(z)
                            if vall == True:
                                vall = 'Существует'
                            else:
                                vall = 'Не существует'
                            coun = geocoder.description_for_number(z, 'ru')
                            timee = timezone.time_zones_for_geographical_number(z)
                            oper = carrier.name_for_number(z, "ru")
                    
                            uty = requests.get("https://api.whatsapp.com/send?phone="+str(message.text))
                            if uty.status_code==200:
                                utl2 = f'https://api.whatsapp.com/send?phone={message.text}'
                                what = types.InlineKeyboardMarkup(row_width=2)
                                what.add(
                                types.InlineKeyboardButton(text='✅ Whatsapp', url=utl2),
                                )
                            else:
                                utl2 = 'Не существует'
                                what = types.InlineKeyboardMarkup(row_width=2)
                                what.add(
                                types.InlineKeyboardButton(text='✅ Whatsapp', url=utl2)                            )
                            answer = ''
                            try:
                                resAV = requests.get('https://mirror.bullshit.agency/search_by_phone/'+str(message.text))
                                contentAV = bs(resAV.text, 'html.parser')
                                h1 = contentAV.find('h1')
                                if h1.text == '503 Service Temporarily Unavailable':
                                    answer += f'Процесс невозможен, попробуйте позже'
                                else:
                                    for url in contentAV.find_all(['a']):
                                        user_link = url['href']
                                        try:
                                            avito_url = requests.get('https://mirror.bullshit.agency'+user_link)
                                            content = bs(avito_url.text, 'html.parser')
                                            url = content.find(['a'])
                                            
                                            linkAV = url['href']
                                            answer += f'{linkAV}\n'
                                        except:
                                            answer += f'{user_link}\n'
                                            continue
                            except:
                                answer += 'Не найдено'
                            if answer == '' or answer == ' ':
                                answer += 'Не найдено'
                            else:
                                pass
                            num = str(message.text)
                            rq = requests.post('https://www.instagram.com/accounts/account_recovery_send_ajax/',
                                        data={'email_or_username':num[1:]},
                                        headers={'accept-encoding':'gzip, deflate, br', 'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                                        'content-type':'application/x-www-form-urlencoded', 'cookie':'ig_did=06389D42-D5BA-42C2-BCA6-49C2913D682B; csrftoken=SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL; mid=XyIqeAALAAF1N7j0GbPCNuWhznuX; rur=FRC; urlgen="{\"109.252.48.249\": 25513\054 \"109.252.48.225\": 25513}:1k5JBz:E-7UgfDDLsdtlKvXiWBUphtFMdw"',
                                        'referer':'https://www.instagram.com/accounts/password/reset/', 'origin':'https://www.instagram.com',
                                        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95 (Edition Yx)',
                                        'x-csrftoken':'SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL', 'x-ig-app-id':'936619743392459',
                                        'x-instagram-ajax': 'a9aec8fa634f', 'x-requested-with': 'XMLHttpRequest'})
                            aq = rq.json()
                            if aq['status'] == 'ok':
                                insta = 'Существует'
                            else:
                                insta = 'Не существует'
                            user_all_info = f"""
<b>ℹ️ Информация по номеру {message.text}</b>:

├{z}
├<b>Страна</b>: <code>{coun}</code>
├<b>Оператор</b>: <code>{oper}</code>
├<b>Существование</b>: <code>{vall}</code>
├<b>Часовой пояс</b>: <code>{timee}</code>
├<b>Avito</b>: <code>{answer}</code>
├<b>Instagram</b>: <code>{insta}</code>
└<b>WhatsApp</b>: {utl2}"""
                            bot.send_message(message.chat.id, user_all_info, parse_mode='HTML', reply_markup=what, disable_web_page_preview = True)
                            bot.send_message(message.chat.id, '⚡️ <b>Главное меню</b>', parse_mode='HTML', reply_markup=kb.main)
                            func.act_count_deanon("add", message.chat.id,)
                    else:
                        bot.send_message(message.chat.id, f'😝 Введите пожалуйста номер телефона заново.', parse_mode='HTML', reply_markup=kb.main)
                except Exception as e:
                    bot.send_message(message.chat.id, 'Произошла ошибка, попробуй еще раз😝', reply_markup=kb.main)
                    print(e)
                
                
                
    @bot.message_handler(commands=['start'])
    def handle_start_command(message):
        user_id = message.chat.id
        if str(message.chat.id) in open(chat_ids_file).read():
            chat_id=message.from_user.id
            func.first_join(user_id=chat_id, name=message.from_user.username)
            bot.send_message(message.from_user.id, f'👋', reply_markup=kb.main, parse_mode='HTML')
        elif str(message.chat.id) not in open(chat_ids_file).read():
            chat_id=message.from_user.id
            func.first_join(user_id=chat_id, name=message.from_user.username)
            bot.send_message(message.from_user.id, f'👋 Привет новенький', reply_markup=kb.main, parse_mode='HTML')
            save_chat_id(message.chat.id) 

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        save_chat_id(message.chat.id)
        u = message.chat.id
        u_u = message.chat.username
        user_id = message.chat.id
        chat_id = message.chat.id
        if message.text == '🔗 Сократить ссылку':
            msg = bot.send_message(u, '<b>ℹ️ Отправьте ссылку:\n\nПример:</b> <code>https://google.com/</code>',parse_mode='HTML', reply_markup=kb.cancle)
            bot.register_next_step_handler(msg, generator_url)

        elif message.text == '🔎 Деанон':
            ab = bot.send_message(u, '🔎 Введите номер телефона (вместе с +):', parse_mode='HTML', reply_markup=kb.cancle)
            bot.register_next_step_handler(ab, deanondef)

        elif message.text == '🖼 Сделать скриншот':
            ab = bot.send_message(u, '''👋 Привет, это инструмент для создания скриншотов разных вебсайтов.
Отправь мне любую ссылку на сайт и сделаю скриншот, после отправлю тебе''', parse_mode='HTML', reply_markup=kb.cancle)
            bot.register_next_step_handler(ab, screenshot)

        elif message.text == '🖥 Профиль':
            conn = sqlite3.connect("base.db")
            cursor = conn.cursor()
            base = cursor.execute(f'SELECT * FROM users WHERE user_id = "{u}"').fetchone()
            bot.send_message(u, f'''🙋 Приветствую!
🤫 Твои личные данные:

🆔 <b>Id</b>: <code>{u}</code>
👤 <b>Username</b>: @{u_u}
🕰 <b>Регистрация</b>: {base[2]}

✂️ <b>Ссылок сокращено</b>: <code>{base[3]}</code>
🚨 <b>Пробито номеров</b>: <code>{base[4]}</code>
🖊 <b>Ников сгенерировано</b>: <code>{base[6]}</code>
🌏 <b>IP пробито</b>: <code>{base[7]}</code>
👥 <b>TG юзеров пробито</b>: <code>{base[9]}</code>
👻 <b>Прокси сгенерировано</b>: <code>{base[8]}</code>
🖼 <b>Скриншотов сделано</b>: <code>{base[10]}</code>
    ''', parse_mode='HTML')

        elif message.text == 'ℹ️ Информация по IP':
            ab = bot.send_message(u, 'ℹ️ Введите ip адресс:', parse_mode='HTML', reply_markup=kb.cancle)
            bot.register_next_step_handler(ab, ipdef)
            
        elif message.text == '🆔 Информация по ID':
            ab = bot.send_message(u, '🆔 <b>Введите id юзара которого хотите пробить:</b>\n\n<code>Псс: Получить айди человека можно в боте</code> @userinfobot', parse_mode='HTML', reply_markup=kb.cancle)
            bot.register_next_step_handler(ab, iddef)

        elif message.text == '📆 Информация':
            bot.send_message(chat_id=chat_id, text=func.users_info(), reply_markup=kb.info, parse_mode='HTML')
            
        elif message.text == '♻️ Генератор':
            bot.send_message(u, f'''♻️ Выберите генератор:''', reply_markup=kb.gen, parse_mode='HTML')
        elif message.text == '🆘 Помощь111f':
            bot.send_message(u, f'''🆘 С каким разделом Вам помочь?''', reply_markup=kb.spas, parse_mode='HTML')
        elif message.text == '1🖼 Скрины для скама':
            bot.send_message(u, f'''📂 Выберите раздел:''', reply_markup=kb.screen, parse_mode='HTML')
        elif message.text == '/a':
            if chat_id in cfg.admin:
                bot.send_message(chat_id=chat_id, text=func.stata(qq=message.message_id), reply_markup=kb.admin, parse_mode='HTML')
            else:
                bot.send_message(chat_id=chat_id, text='❌ У тебя нет прав администратора!', reply_markup=kb.main, parse_mode='HTML')

    #try:
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        user_id = call.message.chat.id
        u = call.message.chat.id
        message = call.message
        message_id = call.message.message_id

        if call.data == 'top_donator':
            msg = bot.send_message(u, '''<b>Топ 10 донатеров</b>
@MagTro - 70Р
@riobunt - 30Р
@Spark_Admins - 11Р''', parse_mode='HTML')
        if call.data == 'sender':
            msg = bot.send_message(u, 'перешли сообщение где я админ:')
            bot.register_next_step_handler(msg, send_message_users)
        if call.data == 'gen_pass':
            bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''📝 Выберите действие: (Функция пока что офф)''', reply_markup=kb.gen_pass, parse_mode='HTML')
        if call.data == 'gen_nick':
            bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''📝 Выберите действие:)''', reply_markup=kb.gen_nick, parse_mode='HTML')
        if call.data == 'gene_nick':
                line = random.choice(open('names.txt').readlines())
                bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''
✅ <b>Ник</b> успешно сгенерировано:
<code>{line}</code>''', reply_markup=kb.gen_nick, parse_mode='HTML')
                func.act_count_name("add", message.chat.id,)

        if call.data == 'gene_nick5':
                line = random.choice(open('names.txt').readlines())
                line2 = random.choice(open('names.txt').readlines())
                line3 = random.choice(open('names.txt').readlines())
                line4 = random.choice(open('names.txt').readlines())
                line5 = random.choice(open('names.txt').readlines())
                bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''
✅ <b>Ники</b> успешно сгенерирован:
<code>{line}</code>
<code>{line2}</code>
<code>{line3}</code>
<code>{line4}</code>
<code>{line5}</code>''', reply_markup=kb.gen_nick, parse_mode='HTML')
                func.act_count_name("add5", message.chat.id,)

        if call.data == 'generate_pass':
            conn = sqlite3.connect("base.db")
            cursor = conn.cursor()
            kolvo = cursor.execute(f'SELECT kolvo FROM sett WHERE user_id = "{user_id}"').fetchone
            password = gen.hard_pass(12)
            password2 = gen.hard_pass(12)
            password3 = gen.hard_pass(12)
            password4 = gen.hard_pass(12)
            password5 = gen.hard_pass(12)
            bot.send_message(user_id, 
                text=f'''
Пароль успешно сгенерировано:
<code>{password}</code>
<code>{password2}</code>
<code>{password3}</code>
<code>{password4}</code>
<code>{password5}</code>
''', 
                reply_markup=kb.gen_pass, parse_mode='HTML')

        if call.data == 'back_gen':
            bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''♻️ Выберите генератор:''', reply_markup=kb.gen, parse_mode='HTML')

        if call.data == 'gen_proxy':
            bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''Выберите действие:''', reply_markup=kb.gen_proxy, parse_mode='HTML') 

        if call.data == 'generate_proxy':
            try:
                proxy = requests.get('http://d4n13l3k00.ml/api/proxy/socks5?c=10').json()
                if '.' in proxy[0] and ':' in proxy[0] and '.' in proxy[1] and ':' in proxy[1] and '.' in proxy[2] and ':' in proxy[2] and '.' in proxy[5] and ':' in proxy[5]:
                    bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''Вот ваши прокси:

{proxy[0]}
{proxy[1]}
{proxy[2]}
{proxy[3]}
{proxy[4]}
{proxy[5]}
{proxy[6]}

<b>Псс: socks5</b>''', reply_markup=kb.gen_proxy, parse_mode='HTML')
                    func.act_count_proxies("add", message.chat.id,)
            except Exception as e:
                print(e)
                bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''тех роботы.. Ожидайте''', reply_markup=kb.gen_proxy, parse_mode='HTML')

        if call.data == 'i_bag':
            bot.send_message(u, f'''Привет!
💨 Если вы нашли баг, оповестите об этом создатедя этого бота - @Shifter_LZT
🏆 Если баг серьёзный, он обязательно вас вознаградить''', reply_markup=kb.main)
            
        if call.data == 'shablon':
            bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''📝 Выберите действие:''', reply_markup=kb.shab, parse_mode='HTML')        
            
        if call.data == 'avito':
            bot.edit_message_text(chat_id=u, message_id=message_id, text=f'''📝 Вот менюшка, выбирай что хочешь :)

Что бы вернутся в главное меню напиши /start или нажми кнопки <b>НАЗАД</b> в меню ниже)''', reply_markup=kb.shablonu, parse_mode='HTML')        
            
    #except Exception as e:
     #   print(e)


    bot.polling(True)
except Exception as e:
    print(e)