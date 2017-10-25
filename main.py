import telebot

bot = telebot.TeleBot("458178330:AAFU4pElGPQb06VbUzypJzHtdzH107Ngqoc")

all_updates = bot.get_updates()
#last_update = all_updates[-1]


def log(message, answer):
    print('\n------')
    from datetime import datetime
    print(datetime.now())
    print("Message from {0} {1}. (id = {2})\n Text - {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))
    print("Answer - ", answer)

@bot.message_handler(commands=['menu'])
def handle_text(message):
    bot.send_message(message.chat.id, 'Hi')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if (message.text == 'Hi') or (message.text == 'Hello'):
        answer = 'What is your name?'
        bot.send_message(message.chat.id, answer)
        log(message,answer)
    elif (message.text == 'Sosok') or message.text == 'Nadezhda' or message.text == 'Liza':
        answer = """ Nice to meet you, """+message.text+"""! My name is MDbot! 
I am just the product of testing 
send me what you want to change!"""
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    else:
        answer = message.text[::-1]
        bot.send_message(message.chat.id, answer)
        log(message, answer)


bot.polling(none_stop=True, interval=0)
