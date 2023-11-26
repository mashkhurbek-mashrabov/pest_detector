import os
import traceback

import requests
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

from bot.controllers.base import BaseController
from bot.string import pests_string
from detector.detect import pest_detector


class BotController(BaseController):
    def greeting(self, restart: bool = False):
        self.sync_user()
        self.send_message(message_text=self.messages('greeting'))

    def image_receiver(self):
        try:
            self.bot.send_message(chat_id=self.chat_id, text="Loading...")
            photo_id = self.message.photo[-1].file_id
            image_url = self.create_photo_url(file_id=photo_id)
            image = Image.open(requests.get(image_url, stream=True).raw)
            saved_image_path, result_dict = pest_detector(image)
            photo = open(saved_image_path, 'rb')
            caption = ''
            for key, value in result_dict.items():
                caption += (f"<b>{value.get('class_name').title()}</b>: {value.get('count')}\n\n"
                            f"{pests_string.get(key)}\n\n")
            if len(caption) > 1024:
                caption = caption[:1024]
            self.bot.send_photo(chat_id=self.chat_id, photo=photo, caption=caption, parse_mode="HTML")
        except:
            print(traceback.format_exc())