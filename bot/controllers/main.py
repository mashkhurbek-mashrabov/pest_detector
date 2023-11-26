import requests
from PIL.Image import Image
from telebot.types import KeyboardButton

from bot.controllers.base import BaseController


class BotController(BaseController):
    def greeting(self, restart: bool = False):
        self.sync_user()
        self.send_message(message_text=self.messages('greeting'))

    def image_receiver(self):
        photo_id = self.message.photo[-1].file_id
        image_url = self.create_photo_url(file_id=photo_id)
        image = Image.open(requests.get(image_url, stream=True).raw)