import telebot

bot = telebot.TeleBot("458178330:AAFU4pElGPQb06VbUzypJzHtdzH107Ngqoc")

all_updates = bot.get_updates()
last_update = all_updates[-1]


def log(message, answer):
    print('\n------')
    from datetime import datetime
    print(datetime.now())
    print("Message from {0} {1}. (id = {2})\n Text - {3}".format(message.from_user.first_name,
                                                                   message.from_user.last_name,
                                                                   str(message.from_user.id),
                                                                   message.text))
    print("Answer - ", answer)


@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat.id, """Hi, I am timetable bot!

You can see the list of commands using /list
or you can send me the day
of the week to see the timetable for this""")


@bot.message_handler(commands=['list'])
def handle_text(message):
        bot.send_message(message.chat.id, """You can use /start to start the dialog

You can use /list to see all commands
You can use /help to read more about the bot""")


@bot.message_handler(commands=['help'])
def handle_text(message):
        bot.send_message(message.chat.id, """Fuck you^^$""")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if (message.text == 'Hi') or (message.text == 'Hello'):
        answer = 'Just send me the day of the week'
        bot.send_message(message.chat.id, answer)
        log(message,answer)
    elif (message.text == 'Monday') or message.text == 'monday' or message.text == 'mon' or message.text == 'Mon':
        answer = """10:15 - 11:50   АЯП (лаб)
12:00 - 13:35  АЯП (сем)
13:50 - 15:25  Дискретная математика (сем)
15:40 - 17:15   Иностр. язык
17:35 - 19:00  Экология (лек)"""
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    elif (message.text == 'Tuesday') or message.text == 'tuesday' or message.text == 'tue' or message.text == 'Tue':
        answer = """12:00 - 13:35  Физика(лаб/--)
13:50 - 15:25  Физика(лаб/сем)
15:40 - 17:15   Физика (лекция)
17:35 - 19:00  АЯП (лек/--)"""
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    elif (message.text == 'Wednesday') or message.text == 'wednesday' or message.text == 'wed' or message.text == 'Wed':
        answer = """8:30 - 10:05  Электротехника (лек)
10:15 - 11:50  Методы оптимизации (лек)
12:00 - 13:25  Физкультура"""
        bot.send_message(message.chat.id, answer)
        log(message, answer)

    elif (message.text == 'Thursday') or message.text == 'thursday' or message.text == 'thu' or message.text == 'Thu':
        answer = """8:30 - 10:05  Политология (сем)
10:15 - 11:50  Дискретная математика (лекция)
12:00 - 13:25  Политология (лек/--)"""
        bot.send_message(message.chat.id, answer)
        log(message, answer)

    elif (message.text == 'Friday') or message.text == 'friday' or message.text == 'fri' or message.text == 'Fri':
        answer = """8:30 - 10:05  Электротехника (сем)
10:15 - 11:50  ----
12:00 - 13:25  Электротехника (лаб)
13:35 - 15:25  Электротехника (лаб)"""
        bot.send_message(message.chat.id, answer)
        log(message, answer)

    #elif message.text == 'Saturday':
     #   bot.send_sticker(message.chat.id, 0x10355ae10, reply_to_message_id=None)
    else:
        answer = """I do not know what you mean
Use /list to see all commands"""
        bot.send_message(message.chat.id, answer)
        log(message, answer)


print(last_update)
bot.polling(none_stop=True, interval=0)
