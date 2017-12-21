import telebot
import constants

bot = telebot.TeleBot(constants.key)

all_updates = bot.get_updates()
last_update = all_updates[len(all_updates)-1]


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
    bot.send_message(message.chat.id, constants.start_message)


@bot.message_handler(commands=['list'])
def handle_text(message):
        bot.send_message(message.chat.id, constants.list_message)


@bot.message_handler(commands=['help'])
def handle_text(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Перейти на GitHub",
                                                    url=constants.github_url)
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Исходный код", reply_markup=keyboard)


@bot.message_handler(commands=['site'])
def handle_text(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Перейти на сайт МГТУ",
                                                    url=constants.bmstu_url)
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Нажми на кнопку и посмотри расписание на сайте МГТУ", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if (message.text == 'Hi') or (message.text == 'Hello'):
        answer = constants.content[0]
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    elif (message.text == 'Monday') or message.text == 'monday' or message.text == 'mon' or message.text == 'Mon' or message.text == 'Понедельник':
        answer = constants.content[1]
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    elif (message.text == 'Tuesday') or message.text == 'tuesday' or message.text == 'tue' or message.text == 'Tue':
        answer = constants.content[2]
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    elif (message.text == 'Wednesday') or message.text == 'wednesday' or message.text == 'wed' or message.text == 'Wed':
        answer = constants.content[3]
        bot.send_message(message.chat.id, answer)
        log(message, answer)

    elif (message.text == 'Thursday') or message.text == 'thursday' or message.text == 'thu' or message.text == 'Thu':
        answer = constants.content[4]
        bot.send_message(message.chat.id, answer)
        log(message, answer)

    elif (message.text == 'Friday') or message.text == 'friday' or message.text == 'fri' or message.text == 'Fri':
        answer = constants.content[5]
        bot.send_message(message.chat.id, answer)
        log(message, answer)

    else:
        answer = constants.unknown_text
        bot.send_message(message.chat.id, answer)
        log(message, answer)


print(last_update)
bot.polling(none_stop=True, interval=0)
