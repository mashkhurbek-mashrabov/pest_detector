from django.db import models

from bot.constants import BotUserSteps


class TelegramBotUser(models.Model):
    chat_id = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    step = models.IntegerField(choices=BotUserSteps.choices, default=BotUserSteps.START)
