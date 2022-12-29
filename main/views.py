from django.shortcuts import render, HttpResponse
import telebot
from .models import User

def index(request):
    token = '5483780994:AAEbxwH96hNEMT22-b4foF46bn69ocrxlJY'
    bot = telebot.TeleBot(token)
    @bot.message_handler(commands=['start'])
    def start(message):
        user = User.objects.get_or_create(name=message.chat.username, chat_id=message.chat.id)
        bot.send_message(message.chat.id, f'Привет, {user[0].name}')
    bot.polling(none_stop=True)
    return HttpResponse('<h1>Bot started</h1>')
