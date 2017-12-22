# -*- coding: utf-8 -*-

class testListBot:
    bot=telebot.Tlebot("458178330:AAFU4pElGPQb06VbUzypJzHtdzH107Ngqoc")
    def simple_mes():
        bot.send_message(203344707, "HiHi!")
        return 0
    def test_pos():
        assert simple_mes() == 0
