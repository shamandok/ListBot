import unittest
import telebot
import os


class TestStringMethods(unittest.TestCase):
    @unittest.skipIf('TOKEN' and 'CHAT_ID' not in os.environ, "No environment variables configured")
    def test_send_mes(self):
        bot = telebot.TeleBot(os.environ['TOKEN'])
        ret_msg = bot.send_message(os.environ['CHAT_ID'], "text")
        assert ret_msg.message_id


    @unittest.skipIf('TOKEN' and 'CHAT_ID' not in os.environ, "No environment variables configured")
    def test_send_message_with_markdown(self):
        bot = telebot.TeleBot(os.environ['TOKEN'])
        markdown = """
           *bold text*
           _italic text_
           [text](URL)
           """
        ret_msg = bot.send_message(os.environ['CHAT_ID'], markdown, parse_mode="Markdown")
        assert ret_msg.message_id


if __name__ == '__main__':
    unittest.main()
