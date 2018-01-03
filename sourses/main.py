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

    print(message.text)

    if message.text == 'Меню':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Events', 'Timetable', 'Add event', 'Else']])
        u_id = message.from_user.id
        user = dynamic_dict_of_users[u_id]
        if len(user.events) == 0:
            bot.send_message(message.chat.id, 'У Вас пока нет событий', reply_markup=keyboard)
        else:
            for i in user.events:
                bot.send_message(message.chat.id, i + " - " + user.events[i], reply_markup=keyboard)
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
        user.normalize_timetable()
        for i in user.timetable:
            bot.send_message(message.chat.id, i + '\n' + user.timetable[i])
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
        u_id = message.from_user.id
        user = dynamic_dict_of_users[u_id]
        for i in user.events:
            bot.send_message(message.chat.id,i + ' ' + user.events[i], reply_markup=keyboard)
        bot.register_next_step_handler(message, need_action_menu)
    elif message.text == 'Timetable':
        bot.send_message(message.chat.id, "Timetable", reply_markup=keyboard)
        bot.register_next_step_handler(message, need_action_menu)
    elif message.text == 'Add event':
        keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard1.add(*[telebot.types.KeyboardButton('Cancel')])
        u_id = message.from_user.id
        user = dynamic_dict_of_users[u_id]
        bot.send_message(message.chat.id, "Введите Событие в формате дд.мм.гггг", reply_markup=keyboard1)
        bot.register_next_step_handler(message, need_action_add_event)
    elif message.text == 'Else':
        bot.send_message(message.chat.id, "Else")
        bot.register_next_step_handler(message, need_action_menu)
    else:
        bot.send_message(message.chat.id, "Don't know what you mean", reply_markup=keyboard)
        bot.register_next_step_handler(message, need_action_menu)


def need_action_add_event(message):
    u_id = message.from_user.id
    user = dynamic_dict_of_users[u_id]
    if len(message.text) == 10 and len(message.text.split('.')) == 3 and (0 < int(message.text[-4:]) < 2100):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton('Cancel')])
        bot.send_message(message.chat.id, "Теперь напишите описание события", reply_markup=keyboard)
        user.set_tmp_event(message.text)
        bot.register_next_step_handler(message, need_action_add_event)
    elif message.text == 'Cancel':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton('Меню')])
        bot.send_message(message.chat.id, "Отмена", reply_markup=keyboard)
        bot.register_next_step_handler(message, need_action_menu)
        date = user.get_tmp_event()
        user.events.pop(date)
        user.set_tmp_event('')
    else:
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton('Меню')])
        bot.send_message(message.chat.id, "Событие добавлено", reply_markup=keyboard)
        date = user.get_tmp_event()
        user.events[date] = message.text
        print(user.events)
        bot.register_next_step_handler(message, need_action_menu)





bot.polling(none_stop=True, interval=0)
