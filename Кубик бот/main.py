
import logging
import functions as func
import menu
import math
import texts
import random
import time
import asyncio
import threading
import datetime

import utils.dice as dice

import traceback

from utils.user import *
from states import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Configure logging
logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.config('bot_token'))

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    check = await func.first_join(message.chat.id, message.chat.first_name, message.chat.username, message.text, bot)

    await message.answer('<b>Главное меню</b>', reply_markup=menu.main_menu(), parse_mode='html')


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if str(message.chat.id) in config.config('admin_id_manager'):
        await message.answer('/check user_id - данные о пользователе', reply_markup=menu.admin_menu())
        

@dp.message_handler()
async def send_message(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    if message.text == menu.main_menu_btn[0]: # Games
        await bot.send_message(chat_id=chat_id, text='Создайте игру или выберите уже имеющуюся:', reply_markup=dice.dice_menu())
        await func.check_user_data(bot, chat_id)

    if message.text == menu.main_menu_btn[3]: # Games
        await bot.send_message(chat_id=chat_id, text='Сомневаешься в боте?\n\nНаши отзывы - @otzivmela')
        await func.check_user_data(bot, chat_id)

    if message.text == menu.main_menu_btn[4]: # Games
        await bot.send_message(chat_id=chat_id, text='Приветствую!\n\n🚸Если хочешь найти игрока в кубик или же пообщаться то тебе в наш чат!\n🚸Вступай в него - https://t.me/joinchat/JfmH7VCNzMg1x2YzMgBajg')
        await func.check_user_data(bot, chat_id)

    if message.text == menu.main_menu_btn[2]: # Help
        await bot.send_message(chat_id=chat_id, text=dice.help_txt)
        await func.check_user_data(bot, chat_id)

    if message.text == menu.main_menu_btn[1]: # profile
        info = func.profile(chat_id)
        msg = texts.profile.format(
                id=info[0],
                login=f'@{username}',
                data=info[5][:19],
                balance=info[3]
            )

        await bot.send_message(chat_id=chat_id, text=msg, reply_markup=menu.profile())
        await func.check_user_data(bot, chat_id)

    if '/check ' in message.text:
        try:
            if str(message.chat.id) in config.config('admin_id_manager'):
                user = User(message.text.split(' ')[1])
                if user.who_invite != '0':
                    who_invite = await bot.get_chat(user.who_invite)
                    who_invite = f'{who_invite.id} | @{who_invite.username}'
                else:
                    who_invite = 'Никто'
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"""
USER_ID: {user.user_id}
Ник: {user.first_name}
Логин: {user.username}
Баланс: {user.balance}
Кто пригласил: {who_invite}
Дата первого входа: {user.date}
"""
                )
        except:
            await message.answer('Ошибка')

@dp.callback_query_handler()
async def handler_call(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.from_user.id
    message_id = call.message.message_id
    first_name = call.from_user.first_name
    username = call.from_user.username


    if call.data == 'qiwi':
        resp = func.replenish_balance(chat_id)
        await bot.send_message(chat_id=chat_id, text=resp[0], reply_markup=resp[1], parse_mode='html')

    if call.data == 'banker':
        await bot.send_message(chat_id=chat_id, text='Если вы хотите оплатить чеком, отправьте его @melvin_hb', parse_mode='html')

    if call.data == 'withdraw':
        await Withdraw.withdraw_sum.set()
        await bot.send_message(chat_id=chat_id, text=f'Введите сумму на вывод от {config.config("min_withdraw_sum")} до {User(chat_id).balance} RUB')

    if call.data == 'cancel_payment':
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='❕ Добро пожаловать!')

    if call.data == 'check_payment':
        check = func.check_payment(chat_id)
        if check[0] == 1:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'✅ Оплата прошла\nСумма - {check[1]} руб')

            try:
                await bot.send_message(chat_id=config.config('channel_logs'), text=texts.logs.format(
                    'QIWI',
                    first_name,
                    f'@{username}',
                    chat_id,
                    datetime.datetime.now(),
                    check[1]
                ))
            except:
                pass

        if check[0] == 0:
            await bot.send_message(chat_id=chat_id, text='❌ Оплата не найдена', reply_markup=menu.to_close)

    if call.data == 'admin_info':
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=func.admin_info(),
            reply_markup=menu.admin_menu(),
            parse_mode='html'
        )

    if call.data == 'give_balance':
        await Admin_give_balance.user_id.set()
        await bot.send_message(chat_id=chat_id, text='Введите ID человека, которому будет изменён баланс')

    if call.data == 'email_sending':
        await bot.send_message(chat_id=chat_id, text='Выбирите вариант рассылки', reply_markup=menu.email_sending())

    if call.data == 'email_sending_photo':
        await Email_sending_photo.photo.set()
        await bot.send_message(chat_id=chat_id, text='Отправьте фото боту, только фото!')

    if call.data == 'email_sending_text':
        await Admin_sending_messages.text.set()
        await bot.send_message(chat_id=chat_id, text='Введите текст рассылки',)

    if call.data == 'email_sending_info':
                bot.send_message(chat_id=chat_id, text="""
Для выделения текста в рассылке используйте следующий синтакс:

1 | <b>bold</b>, <strong>bold</strong>
2 | <i>italic</i>, <em>italic</em>
3 | <u>underline</u>, <ins>underline</ins>
4 | <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
5 | <b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
6 | <a href="http://www.example.com/">inline URL</a>
7 | <a href="tg://user?id=123456789">inline mention of a user</a>
8 | <code>inline fixed-width code</code>
9 | <pre>pre-formatted fixed-width code block</pre>
10 | <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
""")
                bot.send_message(chat_id=chat_id, text="""
Так это будет выглядить в рассылке:

1 | <b>bold</b>, <strong>bold</strong>
2 | <i>italic</i>, <em>italic</em>
3 | <u>underline</u>, <ins>underline</ins>
4 | <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
5 | <b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
6 | <a href="http://www.example.com/">inline URL</a>
7 | <a href="tg://user?id=123456789">inline mention of a user</a>
8 | <code>inline fixed-width code</code>
9 | <pre>pre-formatted fixed-width code block</pre>
10 | <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
""",
                    parse_mode='html'
                    )

    if call.data == 'create_dice':
        await CreateGame.bet.set()
        await bot.send_message(chat_id=chat_id,
                               text=f'💰 Введите сумму ставки от {config.config("min_bank")} до {User(chat_id).balance} RUB',
                               reply_markup=dice.cancel_dice())

    if call.data == 'reload_dice':
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                    text='Создайте игру или выберите уже имеющуюся:',
                                    reply_markup=dice.dice_menu())

    if call.data == 'my_games_dice':
        resp = dice.my_games_dice(chat_id)

        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=resp[0], reply_markup=resp[1])

    if call.data == 'rating_dice':
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=dice.rating_dice(chat_id),
                                    reply_markup=dice.back_dice())

    if call.data == 'back_dice':
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                    text='✅Создайте игру или выберите уже имеющуюся:',
                                    reply_markup=dice.dice_menu())

    if call.data == 'help_dice':
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=dice.help_txt)

    if call.data == 'cancel_dice':
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        await bot.clear_step_handler_by_chat_id(chat_id)

    if 'dice_game:' in call.data:
        game = dice.Game(call.data.split(':')[1])
        if game.status == True and game.user_id != str(chat_id):
            info = dice.dice_game(call.data.split(':')[1])

            if info == False:
                await bot.send_message(chat_id=chat_id, text='🚫 Игра не найдена')
            else:
                await bot.send_message(chat_id=chat_id, text=info[0], reply_markup=info[1])
        else:
            await bot.send_message(chat_id=chat_id, text='🚫 Нельзя играть с самим собой')

    if 'start_game_dice:' in call.data:
        game = dice.Game(call.data.split(':')[1])
        if game.status != False and game.user_id != str(chat_id):
            if User(chat_id).balance >= game.bet:
                await dice.main_start(game, bot, chat_id)
            else:
                await bot.send_message(chat_id=chat_id, text='❌Для игры пополните баланс')
        else:
            await bot.send_message(chat_id=chat_id, text='❌Ошибка')

    if call.data == 'exit':
        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='<b>Главное меню</b>', parse_mode='html')

    if call.data == 'back_to_admin_menu':
        await bot.send_message(chat_id=chat_id, text='Меню админа', reply_markup=menu.admin_menu())

    if call.data == 'withdrawal_requests':
        await bot.send_message(chat_id=chat_id, text='Лист', reply_markup=func.withdrawal_requests())

    if 'withdraw:' in call.data:
        info = func.get_info_withdraw(call.data.split(':')[1])

        await bot.send_message(chat_id=chat_id, text=info[0], reply_markup=info[1])

    if 'withdraw_del:' in call.data:
        await func.withdraw_del(call.data.split(':')[1], bot)
        await bot.send_message(chat_id=chat_id, text='Удалено')


@dp.message_handler(state=Admin_give_balance.user_id)
async def admin_give_balance_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text

    await Admin_give_balance.next()
    await message.answer('Введите сумму на которую будет изменен баланс')


@dp.message_handler(state=Admin_give_balance.balance)
async def admin_give_balance_2(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['balance'] = float(message.text)

            await Admin_give_balance.next()
            await message.answer(f"""
ID: {data['user_id']}
Баланс изменится на: {data['balance']}

Для подтверждения отправьте +
""")
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_give_balance.confirm)
async def admin_give_balance_3(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            func.give_balance(data['balance'], data['user_id'])

            await message.answer('✅ Баланс успешно изменен', reply_markup=menu.admin_menu())
    else:
        await message.answer('⚠️ Изменение баланса отменено')

    await state.finish()

@dp.message_handler(state=Email_sending_photo.photo, content_types=['photo'])
async def email_sending_photo_1(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['photo'] = random.randint(111111111, 999999999)

        await message.photo[-1].download(f'photos/{data["photo"]}.jpg')
        await Email_sending_photo.next()
        await message.answer('Введите текст рассылки')
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Email_sending_photo.text)
async def email_sending_photo_2(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text

            with open(f'photos/{data["photo"]}.jpg', 'rb') as photo:

                await message.answer_photo(photo, data['text'], parse_mode='html')

            await Email_sending_photo.next()
            await message.answer('Выбирите дальнейшее действие', reply_markup=menu.admin_sending())
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')

@dp.message_handler(state=Email_sending_photo.action)
async def email_sending_photo_3(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    try:
        if message.text in menu.admin_sending_btn:
            if message.text == menu.admin_sending_btn[0]: # Начать
            
                users = func.get_users_list()
                
                start_time = time.time()
                amount_message = 0
                amount_bad = 0
                async with state.proxy() as data:
                    photo_name = data["photo"]
                    text = data["text"]

                await state.finish()

                try:
                    await bot.send_message(
                        chat_id=config.config('admin_id_manager').split(':')[0],
                        text=f'✅ Вы запустили рассылку',
                        reply_markup=menu.admin_menu()
                        )
                except: pass

                
                for i in range(len(users)):
                    print(photo_name)
                    try:
                        with open(f'photos/{photo_name}.jpg', 'rb') as photo:
                            await bot.send_photo(
                                chat_id=users[i][0],
                                photo=photo,
                                caption=text,
                                parse_mode='html')
                        amount_message += 1
                    except Exception as e:
                        amount_bad += 1
                
                sending_time = time.time() - start_time

                try:
                    await bot.send_message(
                        chat_id=config.config('admin_id_manager').split(':')[0],
                        text=f'✅ Рассылка окончена\n'
                        f'👍 Отправлено: {amount_message}\n'
                        f'👎 Не отправлено: {amount_bad}\n'
                        f'🕐 Время выполнения рассылки - {sending_time} секунд'
                        
                        )              
                except:
                    pass

            elif message.text == menu.admin_sending_btn[1]: # Отложить
                await Email_sending_photo.next()

                await bot.send_message(
                    chat_id=chat_id,
                    text="""
Введите дату начала рассылке в формате: ДЕНЬ:ЧАСОВ:МИНУТ

Например 18:14:10 - рассылка будет сделана 18 числа в 14:10
"""
                )
                
            elif message.text == menu.admin_sending_btn[2]:
                await state.finish()

                await bot.send_message(
                    message.chat.id, 
                    text='Рассылка отменена', 
                    reply_markup=menu.main_menu()
                )
                
                await bot.send_message(
                    message.chat.id, 
                    text='Меню админа', 
                    reply_markup=menu.admin_menu()
                )
        else:   
            await bot.send_message(
                message.chat.id, 
                text='Не верная команда, повторите попытку', 
                reply_markup=menu.admin_sending())

    except Exception as e:
        await state.finish()
        await bot.send_message(
            chat_id=message.chat.id,
            text='⚠️ ERROR ⚠️'
        )


@dp.message_handler(state=Email_sending_photo.set_down_sending)
async def email_sending_photo_4(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['date'] = message.text
            date = data['date']

            if int(date.split(':')[0]) > 0 and int(date.split(':')[0]) < 33:
                if int(date.split(':')[1]) >= 0 and int(date.split(':')[1]) <= 24:
                    if int(date.split(':')[2]) >= 0 and int(date.split(':')[2]) < 61:
                        await Email_sending_photo.next()

                        await bot.send_message(
                            chat_id=message.chat.id,
                            text=f'Для подтверждения рассылки в {date} отправьте +'
                        )
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Email_sending_photo.set_down_sending_confirm)
async def email_sending_photo_5(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            data['type_sending'] = 'photo'

            func.add_sending(data)

            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Рассылка запланирована в {data["date"]}',
                reply_markup=menu.admin_menu()
            )
    else:
        bot.send_message(message.chat.id, text='Рассылка отменена', reply_markup=menu.admin_menu())

    await state.finish()

@dp.message_handler(state=Admin_sending_messages.text)
async def admin_sending_messages_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

        await message.answer(data['text'], parse_mode='html')

        await Admin_sending_messages.next()
        await bot.send_message(
            chat_id=message.chat.id,
            text='Выбирите дальнейшее действие',
            reply_markup=menu.admin_sending()
        )


@dp.message_handler(state=Admin_sending_messages.action)
async def admin_sending_messages_2(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    if message.text in menu.admin_sending_btn:
        if message.text == menu.admin_sending_btn[0]: # Начать

            users = func.get_users_list()

            start_time = time.time()
            amount_message = 0
            amount_bad = 0

            async with state.proxy() as data:
                text = data['text']

            await state.finish()

            try:
                await bot.send_message(
                    chat_id=config.config('admin_id_manager').split(':')[0],
                    text=f'✅ Вы запустили рассылку',
                    reply_markup=menu.admin_menu())
            except: pass

            for i in range(len(users)):
                try:
                    await bot.send_message(users[i][0], text, parse_mode='html')
                    amount_message += 1
                except Exception as e:
                    amount_bad += 1
            
            sending_time = time.time() - start_time

            try:
                await bot.send_message(
                    chat_id=config.config('admin_id_manager').split(':')[0],
                    text=f'✅ Рассылка окончена\n'
                    f'👍 Отправлено: {amount_message}\n'
                    f'👎 Не отправлено: {amount_bad}\n'
                    f'🕐 Время выполнения рассылки - {sending_time} секунд'
                    
                    )              
            except:
                print('ERROR ADMIN SENDING')

        elif message.text == menu.admin_sending_btn[1]: # Отложить
            await Admin_sending_messages.next()

            await bot.send_message(
                chat_id=chat_id,
                text="""
Введите дату начала рассылке в формате: ДЕНЬ:ЧАСОВ:МИНУТ\n

Например 18:14:10 - рассылка будет сделана 18 числа в 14:10
"""
            )

        elif message.text == menu.admin_sending_btn[2]:
            await bot.send_message(
                message.chat.id, 
                text='Рассылка отменена', 
                reply_markup=menu.main_menu()
            )
            await bot.send_message(
                message.chat.id, 
                text='Меню админа', 
                reply_markup=menu.admin_menu()
            )
            await state.finish()
        else:   
            await bot.send_message(
                message.chat.id, 
                text='Неверная команда, повторите попытку', 
                reply_markup=menu.admin_sending())


@dp.message_handler(state=Admin_sending_messages.set_down_sending)
async def admin_sending_messages_3(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['date'] = message.text
            date = data['date']

            if int(date.split(':')[0]) > 0 and int(date.split(':')[0]) < 33:
                if int(date.split(':')[1]) >= 0 and int(date.split(':')[1]) <= 24:
                    if int(date.split(':')[2]) >= 0 and int(date.split(':')[2]) < 61:
                        await Admin_sending_messages.next()

                        await bot.send_message(
                            chat_id=message.chat.id,
                            text=f'Для подтверждения рассылки в {date} отправьте +'
                        )
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_sending_messages.set_down_sending_confirm)
async def admin_sending_messages_4(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            data['type_sending'] = 'text'
            data['photo'] = random.randint(111111,9999999)

            func.add_sending(data)

            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Рассылка запланирована в {data["date"]}',
                reply_markup=menu.admin_menu()
            )
    else:
        bot.send_message(message.chat.id, text='Рассылка отменена', reply_markup=menu.admin_menu())

    await state.finish()

@dp.message_handler(state=Admin_buttons.admin_buttons_del)
async def admin_buttons_del(message: types.Message, state: FSMContext):
    try:
        func.admin_del_btn(message.text)

        await message.answer('Кнопка удалена', reply_markup=menu.admin_menu())
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_buttons.admin_buttons_add)
async def admin_buttons_add(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['name'] = message.text

        await Admin_buttons.next()
        await message.answer('Введите текст кнопки')

    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_buttons.admin_buttons_add_text)
async def admin_buttons_add_text(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text

        await Admin_buttons.next()
        await message.answer('Отправьте фото для кнопки')

    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_buttons.admin_buttons_add_photo, content_types=['photo'])
async def admin_buttons_add_photo(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['photo'] = random.randint(111111111, 999999999)

        await message.photo[-1].download(f'photos/{data["photo"]}.jpg')

        with open(f'photos/{data["photo"]}.jpg', 'rb') as photo:
            await message.answer_photo(photo, data['text'], parse_mode='html')
        
        await Admin_buttons.next()
        await message.answer('Для создания кнопки напишите +')

    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_buttons.admin_buttons_add_confirm)
async def admin_buttons_add_confirm(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            func.admin_add_btn(data["name"], data["text"], data["photo"])

            await message.answer('Кнопка создана', reply_markup=menu.admin_menu())
    else:
        await message.answer('Создание кнопки отменено')

    await state.finish()


@dp.message_handler(state=CreateGame.bet)
async def creategame_bet(message: types.Message, state: FSMContext):
    await state.finish()

    chat_id = message.chat.id
    try:
        user = User(chat_id)
        bet = float('{:.2f}'.format(float(message.text)))

        if bet <= user.balance and bet >= float(config.config('min_bank')):
            user.update_balance(-bet)
            dice.create_game(chat_id, bet)

            await bot.send_message(
                chat_id=message.chat.id,
                text='✅Ваша ставка принята!'
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Неверная ставка'
            )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text='⚠️ Что-то пошло не по плану'
        )


@dp.message_handler(state=Withdraw.withdraw_sum)
async def withdraw_sum(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    try:
        withdraw_sum = float('{:.2f}'.format(float(message.text)))

        user = User(chat_id)

        if withdraw_sum >= float(config.config('min_withdraw_sum')) and withdraw_sum <= user.balance:
            async with state.proxy() as data:
                data['withdraw_sum'] = withdraw_sum
            
            await Withdraw.next()
            await message.answer('Укажите реквизиты для вывода')
        else:
            await state.finish()
            await bot.send_message(chat_id=message.chat.id, text='Не верная сумма')

    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=message.chat.id, text='⚠️ Что-то пошло не по плану')


@dp.message_handler(state=Withdraw.info)
async def withdraw_info(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    try:
        info = message.text
    
        async with state.proxy() as data:
            data['info'] = info
        
        await Withdraw.next()
        await message.answer(f'Ваши реквизиты:\n{info}\n\nДля подтверждения отправьте +')

    except Exception as e:
        await state.finish()
        await bot.send_message(chat_id=message.chat.id, text='⚠️ Что-то пошло не по плану')


@dp.message_handler(state=Withdraw.confirm)
async def withdraw_confirm(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    try:
        if message.text == '+':
            async with state.proxy() as data:
                if func.add_withdraw(chat_id, data['withdraw_sum'], data['info']) == True:
                    await bot.send_message(chat_id=message.chat.id, text='Вы подали заявку на вывод!')
        else:
            await bot.send_message(chat_id=message.chat.id, text='Вывод отменен')

        await state.finish()
    except Exception as e:
        state.finish()
        await bot.send_message(chat_id=message.chat.id, text='⚠️ Что-то пошло не по плану')


async def sending_check(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        try:
            info = func.sending_check()

            if info != False:
                users = func.get_users_list()

                start_time = time.time()
                amount_message = 0
                amount_bad = 0

                if info[0] == 'text':
                    try:
                        await bot.send_message(
                            chat_id=config.config('admin_id_manager').split(':')[0],
                            text=f'✅ Запуск рассылки')
                    except: pass

                    for i in range(len(users)):
                        try:
                            await bot.send_message(users[i][0], info[1], parse_mode='html')
                            amount_message += 1
                        except Exception as e:
                            amount_bad += 1
                    
                    sending_time = time.time() - start_time

                    try:
                        await bot.send_message(
                            chat_id=config.config('admin_id_manager').split(':')[0],
                            text=f'✅ Рассылка окончена\n'
                            f'👍 Отправлено: {amount_message}\n'
                            f'👎 Не отправлено: {amount_bad}\n'
                            f'🕐 Время выполнения рассылки - {sending_time} секунд'
                            
                            )              
                    except:
                        print('ERROR ADMIN SENDING')

                elif info[0] == 'photo':
                    try:
                        await bot.send_message(
                            chat_id=config.config('admin_id_manager').split(':')[0],
                            text=f'✅ Запуск рассылки')
                    except: pass

                    
                    for i in range(len(users)):
                        try:
                            with open(f'photos/{info[2]}.jpg', 'rb') as photo:
                                await bot.send_photo(
                                    chat_id=users[i][0],
                                    photo=photo,
                                    caption=info[1],
                                    parse_mode='html')
                            amount_message += 1
                        except:
                            amount_bad += 1
                    
                    sending_time = time.time() - start_time

                    try:
                        await bot.send_message(
                            chat_id=config.config('admin_id_manager').split(':')[0],
                            text=f'✅ Рассылка окончена\n'
                            f'👍 Отправлено: {amount_message}\n'
                            f'👎 Не отправлено: {amount_bad}\n'
                            f'🕐 Время выполнения рассылки - {sending_time} секунд'
                            
                            )              
                    except:
                        print('ERROR ADMIN SENDING')

            else:
                pass
        except Exception as e: 
            print(e)


if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)
