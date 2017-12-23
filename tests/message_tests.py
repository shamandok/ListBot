# -*- coding: utf-8 -*-
import os
import pytest
import telebot
import time


should_skip = 'TOKEN' and 'CHAT_ID' not in os.environ
if not should_skip:
    TOKEN = os.environ['TOKEN']
    CHAT_ID = os.environ['CHAT_ID']
    GROUP_ID = os.environ['GROUP_ID']


@pytest.mark.skipif(should_skip, reason="No environment variables configured")
class testListBot:
    def test_message_handler(self):
        bot = telebot.TeleBot('458178330:AAFU4pElGPQb06VbUzypJzHtdzH107Ngqoc')
        msg = self.create_text_message('/help')

        @bot.message_handler(commands=['help', 'start'])
        def command_handler(message):
            message.text = 'got'

        bot.process_new_messages([msg])
        time.sleep(1)
        assert msg.text == 'got'

    def test_send_message_with_markdown(self):
        bot = telebot.TeleBot('458178330:AAFU4pElGPQb06VbUzypJzHtdzH107Ngqoc')
        markdown = """
        *bold text*
        _italic text_
        [text](URL)
        """
        ret_msg = bot.send_message(203344707, markdown, parse_mode="Markdown")
        assert ret_msg.message_id
