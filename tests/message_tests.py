# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import time
import pytest
import os

import telebot
from telebot import types
from telebot import util

should_skip = 'TOKEN' and 'CHAT_ID' not in os.environ

if not should_skip:
    TOKEN = os.environ['TOKEN']
    CHAT_ID = os.environ['CHAT_ID']
    GROUP_ID = os.environ['GROUP_ID']


@pytest.mark.skipif(should_skip, reason="No environment variables configured")
class TestTeleBot:
    def test_message_listener(self):
        msg_list = []
        for x in range(100):
            msg_list.append(self.create_text_message('Message ' + str(x)))

        def listener(messages):
            assert len(messages) == 100

        tb = telebot.TeleBot('')
        tb.set_update_listener(listener)

    def test_message_handler(self):
        tb = telebot.TeleBot('')
        msg = self.create_text_message('/help')

        @tb.message_handler(commands=['help', 'start'])
        def command_handler(message):
            message.text = 'got'

        tb.process_new_messages([msg])
        time.sleep(1)
        assert msg.text == 'got'

    def test_message_handler_reg(self):
        bot = telebot.TeleBot('')
        msg = self.create_text_message(r'https://web.telegram.org/')

        @bot.message_handler(regexp='((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
        def command_url(message):
            msg.text = 'got'

        bot.process_new_messages([msg])
        time.sleep(1)
        assert msg.text == 'got'

    def test_message_handler_lambda(self):
        bot = telebot.TeleBot('')
        msg = self.create_text_message(r'lambda_text')

        @bot.message_handler(func=lambda message: r'lambda' in message.text)
        def command_url(message):
            msg.text = 'got'

        bot.process_new_messages([msg])
        time.sleep(1)
        assert msg.text == 'got'

    def test_message_handler_lambda_fail(self):
        bot = telebot.TeleBot('')
        msg = self.create_text_message(r'text')

        @bot.message_handler(func=lambda message: r'lambda' in message.text)
        def command_url(message):
            msg.text = 'got'

        bot.process_new_messages([msg])
        time.sleep(1)
        assert not msg.text == 'got'

    def test_message_handler_reg_fail(self):
        bot = telebot.TeleBot('')
        msg = self.create_text_message(r'web.telegram.org/')

        @bot.message_handler(regexp='((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
        def command_url(message):
            msg.text = 'got'

        bot.process_new_messages([msg])
        time.sleep(1)
        assert not msg.text == 'got'

    def test_send_message_with_markdown(self):
        tb = telebot.TeleBot(TOKEN)
        markdown = """
        *bold text*
        _italic text_
        [text](URL)
        """
        ret_msg = tb.send_message(CHAT_ID, markdown, parse_mode="Markdown")
        assert ret_msg.message_id

    def test_send_message_with_disable_notification(self):
        tb = telebot.TeleBot(TOKEN)
        markdown = """
        *bold text*
        _italic text_
        [text](URL)
        """
        ret_msg = tb.send_message(CHAT_ID, markdown, parse_mode="Markdown", disable_notification=True)
        assert ret_msg.message_id

    def test_send_file(self):
        file_data = open('../examples/detailed_example/kitten.jpg', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_document(CHAT_ID, file_data)
        assert ret_msg.message_id

        ret_msg = tb.send_document(CHAT_ID, ret_msg.document.file_id)
        assert ret_msg.message_id

    def test_send_file_dis_noti(self):
        file_data = open('../examples/detailed_example/kitten.jpg', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_document(CHAT_ID, file_data, disable_notification=True)
        assert ret_msg.message_id

        ret_msg = tb.send_document(CHAT_ID, ret_msg.document.file_id)
        assert ret_msg.message_id

    def test_send_file_caption(self):
        file_data = open('../examples/detailed_example/kitten.jpg', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_document(CHAT_ID, file_data, caption="Test")
        assert ret_msg.message_id

        ret_msg = tb.send_document(CHAT_ID, ret_msg.document.file_id)
        assert ret_msg.message_id

    def test_send_video(self):
        file_data = open('./test_data/test_video.mp4', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_video(CHAT_ID, file_data)
        assert ret_msg.message_id

    def test_send_video_dis_noti(self):
        file_data = open('./test_data/test_video.mp4', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_video(CHAT_ID, file_data, disable_notification=True)
        assert ret_msg.message_id

    def test_send_video_more_params(self):
        file_data = open('./test_data/test_video.mp4', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_video(CHAT_ID, file_data, 1)
        assert ret_msg.message_id

    def test_send_video_more_params_dis_noti(self):
        file_data = open('./test_data/test_video.mp4', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_video(CHAT_ID, file_data, 1, disable_notification=True)
        assert ret_msg.message_id

    def test_send_file_exception(self):
        tb = telebot.TeleBot(TOKEN)
        try:
            tb.send_document(CHAT_ID, None)
            assert False
        except Exception as e:
            print(e)
            assert True

    def test_send_photo(self):
        file_data = open('../examples/detailed_example/kitten.jpg', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_photo(CHAT_ID, file_data)
        assert ret_msg.message_id

        ret_msg = tb.send_photo(CHAT_ID, ret_msg.photo[0].file_id)
        assert ret_msg.message_id

    def test_send_photo_dis_noti(self):
        file_data = open('../examples/detailed_example/kitten.jpg', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_photo(CHAT_ID, file_data)
        assert ret_msg.message_id

        ret_msg = tb.send_photo(CHAT_ID, ret_msg.photo[0].file_id, disable_notification=True)
        assert ret_msg.message_id

    def test_send_audio(self):
        file_data = open('./test_data/record.mp3', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_audio(CHAT_ID, file_data, 1, performer='eternnoir', title='pyTelegram')
        assert ret_msg.content_type == 'audio'
        assert ret_msg.audio.performer == 'eternnoir'
        assert ret_msg.audio.title == 'pyTelegram'

    def test_send_audio_dis_noti(self):
        file_data = open('./test_data/record.mp3', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_audio(CHAT_ID, file_data, 1, performer='eternnoir', title='pyTelegram',
                                disable_notification=True)
        assert ret_msg.content_type == 'audio'
        assert ret_msg.audio.performer == 'eternnoir'
        assert ret_msg.audio.title == 'pyTelegram'

    def test_send_voice(self):
        file_data = open('./test_data/record.ogg', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_voice(CHAT_ID, file_data)
        assert ret_msg.voice.mime_type == 'audio/ogg'

    def test_send_voice_dis_noti(self):
        file_data = open('./test_data/record.ogg', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_voice(CHAT_ID, file_data, disable_notification=True)
        assert ret_msg.voice.mime_type == 'audio/ogg'

    def test_get_file(self):
        file_data = open('./test_data/record.ogg', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_voice(CHAT_ID, file_data)
        file_id = ret_msg.voice.file_id
        file_info = tb.get_file(file_id)
        assert file_info.file_id == file_id

    def test_get_file_dis_noti(self):
        file_data = open('./test_data/record.ogg', 'rb')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_voice(CHAT_ID, file_data, disable_notification=True)
        file_id = ret_msg.voice.file_id
        file_info = tb.get_file(file_id)
        assert file_info.file_id == file_id

    def test_send_message(self):
        text = 'CI Test Message'
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_message(CHAT_ID, text)
        assert ret_msg.message_id
