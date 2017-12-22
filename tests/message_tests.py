# -*- coding: utf-8 -*-

class testListBot:
    bot=telebot.Telebot("458178330:AAFU4pElGPQb06VbUzypJzHtdzH107Ngqoc")
    def simple_mes():
        bot.get_me()
    def test_pos():
        assert simple_mes() == {'id': 458178330, 'is_bot': True, 'first_name': 'MDFileBot', 'username': 'MDFileBot', 'last_name': None, 'language_code': None}
