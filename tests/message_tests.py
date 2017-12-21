# -*- coding: utf-8 -*-

import main

class testListBot:
    def simple_mes():
        main.bot.send_message(203344707, "HIhi")
        return 0
    def test_pos():
        assert simple_mes() == 0
