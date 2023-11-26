import traceback

import telebot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telebot.util import content_type_media

from bot.controllers.main import BotController
from bot.loader import bot


@csrf_exempt
def webhook_handler(request):
    if request.method == 'POST':
        bot.process_new_updates(
            [telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )]
        )
        return HttpResponse(status=200)
    else:
        return HttpResponse('.')


@bot.message_handler(commands=['start'])
def start_handler(message):
    controller = BotController(message, bot)
    controller.greeting()


@bot.message_handler(content_types=['text'])
def message_handler(message):
    controller = BotController(message, bot)
    user_step = controller.step
    message_text = message.text


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(message):
    controller = BotController(message, bot)
    user_step = controller.step
    callback_data = message.data


@bot.message_handler(content_types=['photo'])
def contact_handler(message):
    controller = BotController(message, bot)
    controller.image_receiver()


@bot.message_handler(func=lambda message: True, content_types=content_type_media)
def echo_all(message):
    pass
