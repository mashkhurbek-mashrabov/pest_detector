import os

import telebot
from telebot.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

from bot.constants import BotUserSteps
from bot.models import TelegramBotUser
from bot.string import messages


class BaseController:
    def __init__(self, message, bot: telebot.TeleBot):
        self.bot = bot
        self.message = message
        self.user = TelegramBotUser.objects.get_or_create(chat_id=self.chat_id)[0]
        self.step = self.user.step

    def sync_user(self):
        self.user.name = self.message.from_user.first_name
        self.user.username = self.message.from_user.username
        self.user.save()

    def t(self, code, language=None):
        if language:
            return messages.get(code)
        if self.user.language:
            return messages.get(code)
        else:
            return code

    def set_step(self, step: BotUserSteps):
        user = self.user
        user.step = step
        user.save()

    def send_message(self, message_code=None, reply_markup=None, message_text=None,
                     chat_id=None, message_arguments=None, reply_to_message_id=None, as_reply=False):

        if not chat_id:
            chat_id = self.chat_id

        if message_code:
            message_text = self.t(message_code)

        if message_arguments:
            message_text = message_text.format(*message_arguments)

        if as_reply:
            reply_to_message_id = reply_to_message_id if reply_to_message_id else self.message_id

        return self.bot.send_message(
            chat_id=chat_id,
            text=message_text,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            disable_web_page_preview=True,
            parse_mode='HTML')

    def edit_message(self, message_code=None, reply_markup=None, message=None,
                     chat_id=None, message_id=None, message_arguments=None):

        if not message_id:
            message_id = self.message_id

        if not chat_id:
            chat_id = self.chat_id

        if message_code:
            message = self.t(message_code)

        if message_arguments:
            message = message.format(*message_arguments)

        return self.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=message,
            reply_markup=reply_markup,
            parse_mode='HTML',
            disable_web_page_preview=True)

    def delete_message(self, chat_id=None, message_id=None):

        if not message_id:
            message_id = self.message_id

        if not chat_id:
            chat_id = self.chat_id

        return self.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id)

    def answer_callback(self, message_id=None, message=None, message_code=None, show_alert=False):
        if not message_id:
            message_id = self.message.id
        if message_code:
            message = self.t(message_code)
        self.bot.answer_callback_query(callback_query_id=message_id, text=message, show_alert=show_alert)

    @property
    def message_text(self):
        return self.message.text

    @property
    def main_menu_reply_button(self):
        return KeyboardButton(text=self.t('main menu'))

    @property
    def main_menu_inline_button(self):
        return InlineKeyboardButton(self.t('main menu'), callback_data=CallbackData.main_menu_button)

    @property
    def back_reply_button(self):
        return KeyboardButton(text=self.t('back button'))

    @property
    def back_inline_button(self):
        return InlineKeyboardButton(self.t('back button'), callback_data=CallbackData.back_button)

    @property
    def skip_reply_button(self):
        return KeyboardButton(text=self.t('skip'))

    @property
    def skip_inline_button(self):
        return InlineKeyboardButton(text=self.t('skip'), callback_data=CallbackData.skip)

    @property
    def cancel_reply_button(self):
        return KeyboardButton(text=self.t('cancel'))

    @property
    def chat_id(self):
        return self.message.from_user.id

    @property
    def message_id(self):
        return self.message.message_id

    @property
    def callback_query_id(self):
        return self.message.message.message_id

    @property
    def callback_data(self):
        return self.message.data if hasattr(self.message, 'data') else None

    @staticmethod
    def messages(code):
        return messages.get(code)

    @staticmethod
    def inline_markup(row_width=2):
        return InlineKeyboardMarkup(row_width=row_width)

    @staticmethod
    def reply_markup(row_width=2, one_time_keyboard=False):
        return ReplyKeyboardMarkup(row_width=row_width, one_time_keyboard=one_time_keyboard, resize_keyboard=True)

    def remove_keyboard(self):
        return self.send_message(message_text=self.messages('next emoji'), reply_markup=ReplyKeyboardRemove())

    def create_photo_url(self, file_id):
        file_info = self.bot.get_file(file_id)
        url = f'https://api.telegram.org/file/bot{os.getenv("BOT_TOKEN")}/{file_info.file_path}'
        return url
