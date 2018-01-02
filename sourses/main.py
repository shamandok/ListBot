from User import User
import telebot
import constants


dynamic_dict_of_users = {'0': '0'}
tmp = {}

bot = telebot.TeleBot('key')


@bot.message_handler(commands=['start'])
def handle_text(message):
    u_id = message.from_user.id
    if u_id in dynamic_dict_of_users:
        user = dynamic_dict_of_users[u_id]
        for i in user.events:

            bot.send_message(message.chat.id, i + user.events[i])
    else:
        u1 = User(u_id)
        tmp[u_id] = u1
        dynamic_dict_of_users.update(tmp)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Нужно', 'Не нужно']])
        bot.send_message(message.chat.id, constants.start_mes, reply_markup=keyboard)
        bot.register_next_step_handler(message, need_action_start)


@bot.message_handler(commands=['timetable'])
def handle_text(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton('Меню')])
    bot.send_message(message.chat.id, "Сейчас дам посмотреть", reply_markup=keyboard)
    bot.register_next_step_handler(message, need_action_menu)


@bot.message_handler(commands=['help'])
def handle_text(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton('Меню')])
    bot.send_message(message.chat.id, constants.help_mes, reply_markup=keyboard)
    bot.register_next_step_handler(message, need_action_menu)


@bot.message_handler(commands=['list'])
def handle_text(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton('Меню')])
    bot.send_message(message.chat.id, constants.list_mes, reply_markup=keyboard)
    bot.register_next_step_handler(message, need_action_menu)


def need_action_menu(message):
    if message.text == 'Меню':

        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Events', 'Timetable', 'Add event', 'Else']])
        print(dynamic_dict_of_users)
        bot.send_message(message.chat.id, 'Menu', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Что-то другое")
    bot.register_next_step_handler(message, need_action_from_menu)


def need_action_start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton('Меню')])
    if message.text == 'Нужно':
        u_id = message.from_user.id
        user = dynamic_dict_of_users[u_id]
        user.parse_timetable()
        for i in user.timetable:
            bot.send_message(message.chat.id, str(i))
        bot.send_message(message.chat.id, "___", reply_markup=keyboard)
        print(dynamic_dict_of_users)
    elif message.text == 'Не нужно':
        bot.send_message(message.chat.id, "Жаль", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Что-то другое", reply_markup=keyboard)

    bot.register_next_step_handler(message, need_action_menu)


def need_action_from_menu(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton('Меню')])
    if message.text == 'Events':
        bot.send_message(message.chat.id, "Events")
    elif message.text == 'Timetable':
        bot.send_message(message.chat.id, "Timetable")
    elif message.text == 'Add event':
        bot.send_message(message.chat.id, "Add event")
    elif message.text == 'Else':
        bot.send_message(message.chat.id, "Else")
    else:
        bot.send_message(message.chat.id, "Don't know what you mean")


print(bot.get_updates())
bot.polling(none_stop=True, interval=0)
