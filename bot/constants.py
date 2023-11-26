from django.db import models
from django.utils.translation import gettext_lazy as _


class BotUserSteps(models.IntegerChoices):
    START = 1, _('start')


