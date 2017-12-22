# -*- coding: utf-8 -*-
import sys

sys.path.append('../')
from telebot import types

class testListBot:
    def test_message_handler(self):
        bot = telebot.TeleBot('')
        msg = self.create_text_message('/help')

        @bot.message_handler(commands=['help', 'start'])
        def command_handler(message):
            message.text = 'got'

        bot.process_new_messages([msg])
        time.sleep(1)
        assert msg.text == 'got'
