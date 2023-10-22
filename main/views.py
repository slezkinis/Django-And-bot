from django.shortcuts import render, HttpResponse
import telebot
from .models import User
from time import sleep
import random as rnd


register = False
token = '5483780994:AAEbxwH96hNEMT22-b4foF46bn69ocrxlJY'
bot = telebot.TeleBot(token)
HELP = '''
/help - Помощь с командами
/start - Регистрация
/link - Получить реферальную ссылку
/link_info - Информация о вашей реферальной ссылке
/game - Старт игры
/score - Количество твоих очков
/rating - ТОП игроки
'''


def index(request):
    while True:
        @bot.message_handler(commands=['help'])
        def help(message):
            bot.send_message(message.chat.id, HELP)


        @bot.message_handler(commands=['start'])
        def start(message):
            global register
            plus = False
            user = User.objects.get_or_create(chat_id=message.chat.id)
            sp = (message.text).split()
            if user[0].name:
                bot.send_message(message.chat.id, f'Привет, {message.chat.username}!')
            elif message.chat.username:
                if len(sp) == 2:
                    links = User.objects.filter(user_id=sp[1])
                    if links:
                        link_user = User.objects.get(user_id=sp[1])
                        if link_user.name == user[0].name:
                            bot.send_message(message.chat.id, 'Нельзя переходить по своей же ссылке!')
                            return
                        bot.send_message(message.chat.id, f'Ты перешёл по пригласительной ссылке пользователя {link_user.name}!')
                        link_user.count_link = link_user.count_link + 1
                        plus = True
                        link_user.save()
                    else:
                        bot.send_message(message.chat.id, 'Неверный код приглашения! Проверь правильность ввода!')
                        return
                test_user = User.objects.filter(name=message.chat.username)
                if not test_user:
                    bot.send_message(message.chat.id, f'Привет, {message.chat.username}! Приятно познакомиться!')
                    user[0].name = message.chat.username
                    if plus:
                        user[0].score = user[0].score + 3
                    user[0].save()
                    bot.send_message(message.chat.id, 'Напиши /help для информации о командах!')
                else:
                    bot.send_message(message.chat.id, f'Привет! Давай знакомиться! Придумай свой ник, а я проверю, чтобы твоё имя было уникальным.')
                    register = True
                    if plus:
                        user[0].score = user[0].score + 3
                        user[0].save()
            else:
                bot.send_message(message.chat.id, f'Привет! Давай знакомиться! Придумай свой ник, а я проверю, чтобы твоё имя было уникальным.')
                register = True
                if plus:
                    user[0].score = user[0].score + 3
                    user[0].save()

        
        @bot.message_handler(commands=['link_info'])
        def link_info(message):
            users = User.objects.filter(chat_id=message.chat.id)
            if users:
                user = User.objects.get(chat_id=message.chat.id)
                if len((message.text).split()) == 2:
                    if (message.text).split()[1] == 'Yes':
                        number = user.count_link
                        ch = 0
                        while ch < number:
                            if ch + 8 <= number:
                                ch = ch + 8
                            else:
                                break
                        user.count_link = number - ch
                        add = int(13 * (ch / 8))
                        user.score = user.score + add
                        user.save()
                        mes = ''
                        if add == 1:
                            mes = f'Тебе добавилось {add} очка. Поздравляю!'
                        elif add >= 2 and add <= 4:
                            mes = f'Тебе добавилось {add} очка. Поздравляю!'
                        else:
                            mes = f'Тебе добавилось {add} очков. Поздравляю!'
                        bot.send_message(message.chat.id, mes)
                    else:
                        bot.send_message(message.chat.id, 'Я тебя не совсем понимаю! Проверьте правильность ввода!')
                else:
                    link_number = user.count_link
                    mes = ''
                    if link_number == 1:
                        mes = f'По твоей ссылке перёл и зарегистрировался {link_number} человек.'
                    elif link_number >= 2 and link_number <= 4:
                        mes = f'По твоей ссылке перешло и зарегистрировалось {link_number} человека.'
                    else:
                        mes = f'По твоей ссылке перешло и зарегистрировалось {link_number} человек.'
                    bot.send_message(
                        message.chat.id,
                        mes
                    )
                    if link_number >= 8:
                        bot.send_message(message.chat.id, 'У тебя хватает для вывода очков. Напиши /link_info и через пробел Yes если хочешь вывести')
            else:
                bot.send_message(message.chat.id, 'Ты не зарегистрирован! Напиши /start для регистрации.')

        
        @bot.message_handler(commands=['link'])
        def link(message):
            users = User.objects.filter(chat_id=message.chat.id)
            if users:
                user = User.objects.get(chat_id=message.chat.id)
                user_id = user.id
                chat_id = message.chat.id
                link_id = f'{chat_id}_{user_id}'
                link = f'https://t.me/SlezkinIvanBot?start={link_id}'
                user.user_id = link_id
                user.save()
                bot.send_message(chat_id, link)
                bot.send_message(chat_id, 'Это твоя ссылка, по которой ты можешь приводить друзей! За каждые 8 друзей ты получишь 13 очков! Каждый зарегистрированный друг получит плюс 3 балла! Главное не забывай время от времени прописывать команду /link_info для просмотра пришедших друзей! Если ты заберёшь очки, то количество пришедших друзей станет равно 0.')
            else:
                bot.send_message(message.chat.id, 'Ты не зарегистрирован! Напиши /start для регистрации.')


        @bot.message_handler(commands=['game'])
        def game(message):
            users = User.objects.filter(chat_id=message.chat.id)
            if users:
                bot.send_message(
                    message.chat.id,
                    'Это игра, в которой тебе нужно угадать число, которое загадал бот. Числа будут от 1 до 3. Ты можешь поставить ставку. Если ты выиграешь, то тебе начислятся твоя ставка и плюс 1 очко, а если проиграешь, то отнимутся! Если у тебя нет очков, то ставь 0! Удачи!'
                )
                sleep(2)
                bot.send_message(message.chat.id, 'Я загадал! Сообщением напиши число, а потом, через пробел, ставку!')
            else:
                bot.send_message(message.chat.id, 'Ты не зарегистрирован! Напиши /start для регистрации.')
        

        @bot.message_handler(commands=['score'])
        def score(message):
            users = User.objects.filter(chat_id=message.chat.id)
            if users:
                user = User.objects.get(chat_id=message.chat.id)
                mes = ''
                if user.score == 1:
                    mes = f'У тебя {user.score} балл! Ты молодчина!!'
                elif user.score >= 2 and user.score <= 4:
                    mes = f'У тебя {user.score} балла! Ты молодчина!!'
                else:
                    mes = f'У тебя {user.score} баллов! Ты молодчина!!'

                bot.send_message(
                    message.chat.id,
                    mes
                )
            else:
                bot.send_message(message.chat.id, 'Ты не зарегистрирован! Напиши /start для регистрации.')


        @bot.message_handler(commands=['print'])
        def send_all(message):
            if int(message.chat.id) == 1509726530:
                mes = (message.text).split()
                otprv = str(mes[1:])
                otprv = otprv.replace('[', '').replace(']', '').replace(',', '').replace("'", "")
                for user in User.objects.all():
                    try:
                        bot.send_message(user.chat_id, '❗️Уведомление:❗️')
                        bot.send_message(user.chat_id, otprv)
                    except telebot.apihelper.ApiTelegramException:
                        continue
                bot.send_message('1509726530',f"Рассылка отправлена {len(User.objects.all())} пользователям (пользователю)")
            else:
                bot.send_message(message.chat.id, 'Вы не создатель!! Вам сюда лезть не надо:)')


        @bot.message_handler(commands=['send'])
        def send(message):
            if int(message.chat.id) == 1509726530:
                mes = (message.text).split()
                chat_id = int(mes[1])
                user = User.objects.get(chat_id=chat_id)
                otprv = str(mes[2:])
                otprv = otprv.replace('[', '').replace(']', '').replace(',', '').replace("'", "")
                try:
                    bot.send_message(user.chat_id, '❗️ Личное уведомление:❗️')
                    bot.send_message(user.chat_id, otprv)
                except:
                    bot.send_message('1509726530',f"!!Рассылка не отправлена пользователю {user.name}")
                    return
                sleep(1)
                bot.send_message('1509726530',f"Рассылка отправлена пользователю {user.name}")
            else:
                bot.send_message(message.chat.id, 'Вы не создатель!! Вам сюда лезть не надо:)')


        @bot.message_handler(commands=['rating'])
        def rating(message):
            users = User.objects.order_by('-score')
            if len(users) >= 3:
                otv = f'''
                🥇 Первое место: {users[0].name}. Рейтинг: {users[0].score}.
🥈 Вторе место: {users[1].name}. Рейтинг: {users[1].score}.
🥉 Третье место: {users[2].name}. Рейтинг: {users[2].score}.
                '''
            elif len(users) == 2:
                otv = f'''
                🥇 Первое место: {users[0].name}. Рейтинг: {users[0].score}.
🥈 Вторе место: {users[1].name}. Рейтинг: {users[1].score}.
                '''
            elif len(users) == 1:
                otv = f'''
                🥇 Первое место: {users[0].name}. Рейтинг: {users[0].score}.
                '''
            else:
                otv = 'Пока нет ни одного участника! Стань первым!'
            bot.send_message(message.chat.id, otv)


        @bot.message_handler(content_types = ['text'])
        def text(message):
            global register
            if register:
                user = User.objects.get(chat_id=message.chat.id)
                name = message.text
                test_user = User.objects.filter(name=name)
                if len(test_user) == 0:
                    user.name = name
                    user.save()
                    bot.send_message(message.chat.id, f'Привет, {user.name}! Приятно познакомиться!')
                    bot.send_message(message.chat.id, 'Напиши /help для информации о командах!')
                    register = False
                else:
                    bot.send_message(message.chat.id, 'Такое имя занято! Придумай другое!')
            else:
                users = User.objects.filter(chat_id=message.chat.id)
                if users:
                    user = User.objects.get(chat_id=message.chat.id)
                    correct_number = rnd.randint(1, 3)
                    a = (message.text).split()
                    if len(a) < 2:
                        bot.send_message(message.chat.id, 'Ты указал только одно! Нужно указывать и ответ и ставку! Поробуй ещё раз!')
                        return
                    otv, bid = (message.text).split()
                    try:
                        otv, bid = int(otv), int(bid)
                    except ValueError:
                        bot.send_message(message.chat.id, 'Ставка или ответ не являются числами! Проверь и поробуй ещё раз!')
                        return
                    if bid < 0:
                        bot.send_message(message.chat.id, "Ставка не может быть отрицательной")
                        return
                    if bid == 0 and user.score != 0:
                        bot.send_message(message.chat.id, "Неверная ставка")
                        return
                    if otv < 1 or otv > 3:
                        bot.send_message(message.chat.id, 'Введённый ответ меньше 1 или больше 3! Проверь и попробуй ещё раз!')
                        return
                    score = user.score
                    if bid > score:
                        mes = ''
                        if user.score == 1:
                            mes = f'У тебя {user.score} балл, а ты поставил {bid}! Поставь меньше!'
                        elif user.score >= 2 and user.score <= 4:
                            mes = f'У тебя {user.score} балла, а ты поставил {bid}! Поставь меньше!'
                        else:
                            mes = f'У тебя {user.score} баллов, а ты поставил {bid}! Поставь меньше!'
                        bot.send_message(message.chat.id, mes)
                        return
                    if otv == correct_number:
                        mes = ''
                        if score + bid + 1 == 1:
                            mes = f'Ты выирал! Теперь у тебя {score + bid + 1} балл! Поздравляю! Давай сыграем ещё раз?'
                        elif score + bid + 1 >= 2 and score + bid + 1 <= 4:
                            mes = f'Ты выирал! Теперь у тебя {score + bid + 1} балла! Поздравляю! Давай сыграем ещё раз?'
                        else:
                            mes = f'Ты выирал! Теперь у тебя {score + bid + 1} баллов! Поздравляю! Давай сыграем ещё раз?'
                        bot.send_message(message.chat.id, mes)
                        bot.send_message(message.chat.id, 'Я загадал! Сообщением напиши число, а потом, через пробел, ставку!')
                        user.score = score + bid + 1
                        user.save()
                    else:
                        mes = ''
                        if score - bid == 1:
                            mes = f'Ты не угадал! Правильный ответ был {correct_number}. Теперь у тебя {score - bid} балл! Попробуй ещё раз!'
                        elif score - bid >= 2 and score - bid <= 4:
                            mes = f'Ты не угадал! Правильный ответ был {correct_number}. Теперь у тебя {score - bid} балла! Попробуй ещё раз!'
                        else:
                            mes = f'Ты не угадал! Правильный ответ был {correct_number}. Теперь у тебя {score - bid} баллов! Попробуй ещё раз!'
                        bot.send_message(message.chat.id, mes)
                        bot.send_message(message.chat.id, 'Я загадал! Сообщением напиши число, а потом, через пробел, ставку!')
                        user.score = score - bid
                        user.save()
                else:
                    bot.send_message(message.chat.id, 'Ты не зарегистрирован! Напиши /start для регистрации.')

        bot.polling(none_stop=True)
