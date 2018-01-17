"""Кнопки more..
edit timetable
edit events"""

from User import *
import telebot
import constants

dynamic_dict_of_users = {'0': '0'}
tmp = {}

bot = telebot.TeleBot('458178330:AAFU4pElGPQb06VbUzypJzHtdzH107Ngqoc')

keyboard_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_menu.add(telebot.types.KeyboardButton('Меню'))

keyboard_menu2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_menu2.add(*[telebot.types.KeyboardButton(name) for name in ['Events', 'Timetable', 'Add event', 'More...']])

keyboard_menu2_more = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_menu2_more.add(*[telebot.types.KeyboardButton(name) for name in ['Edit timetable', 'Edit events',
                                                                          'See more features', 'delete myself',
                                                                          'back']])

keyboard_cancel = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_cancel.add(telebot.types.KeyboardButton('Cancel'))

keyboard_edit = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard_edit.add(*[telebot.types.KeyboardButton(name) for name in ['Edit date', 'Edit description',
                                                                    'delete event', 'back']])


@bot.message_handler(commands=['start'])
def handle_text(message):
    u_id = message.from_user.id
    if u_id in dynamic_dict_of_users:
        user = dynamic_dict_of_users[u_id]
        for i in user.get_events():
            bot.send_message(message.chat.id, i + user.events[i])
    else:
        u1 = User(u_id)
        tmp[u_id] = u1
        dynamic_dict_of_users.update(tmp)
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Да', 'Нет']])
        bot.send_message(message.chat.id, constants.start_mes, reply_markup=keyboard)
        print("nas")
        bot.register_next_step_handler(message, need_action_start)


@bot.message_handler(commands=['timetable'])
def handle_text(message):
    u_id = message.from_user.id
    user = dynamic_dict_of_users[u_id]
    tmp = user.get_timetable()
    for i in tmp:
        bot.send_message(message.chat.id, i + '\n' + tmp[i], reply_markup=keyboard_menu)
    bot.register_next_step_handler(message, need_action_menu)


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, constants.help_mes, reply_markup=keyboard_menu)
    bot.register_next_step_handler(message, need_action_menu)


@bot.message_handler(commands=['list'])
def handle_text(message):
    bot.send_message(message.chat.id, constants.list_mes, reply_markup=keyboard_menu)
    bot.register_next_step_handler(message, need_action_menu)


def need_action_menu(message):
    if message.text == 'Меню':
        u_id = message.from_user.id
        user = dynamic_dict_of_users[u_id]
        tmp = user.get_events()
        if len(tmp) == 0:
            bot.send_message(message.chat.id, 'У Вас пока нет событий', reply_markup=keyboard_menu2)
        else:

            for i in tmp:
                bot.send_message(message.chat.id, i + " - " + tmp[i], reply_markup=keyboard_menu2)
    else:
        bot.send_message(message.chat.id, constants.undefined_command, reply_markup=keyboard_menu)
    bot.register_next_step_handler(message, need_action_from_menu)


def need_action_start(message):
    if message.text == 'Да':
        u_id = message.from_user.id
        user = dynamic_dict_of_users[u_id]
        user.parse_timetable()
        print("parsing...")
        print(user.get_timetable())
        user.normalize_timetable()
        print("-----------------------")
        print(user.get_timetable())
        tmp = user.get_timetable()
        for i in tmp:
            bot.send_message(message.chat.id, i + '\n' + tmp[i], reply_markup=keyboard_menu)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, "Меню", reply_markup=keyboard_menu)
    else:
        bot.send_message(message.chat.id, constants.undefined_command, reply_markup=keyboard_menu)

    bot.register_next_step_handler(message, need_action_menu)


def need_action_from_menu(message):
    u_id = message.from_user.id
    user = dynamic_dict_of_users[u_id]
    if message.text == 'Events':
        if len(user.get_events()) == 0:
            bot.send_message(message.chat.id, "У вас пока нет событий", reply_markup=keyboard_menu)
        else:
            for i in user.events:
                bot.send_message(message.chat.id, i + ' ' + user.events[i], reply_markup=keyboard_menu)
        bot.register_next_step_handler(message, need_action_menu)
    elif message.text == 'Timetable':
        tmp = user.get_timetable()
        for i in tmp:
            bot.send_message(message.chat.id, i + '\n' + tmp[i], reply_markup=keyboard_menu)
        bot.register_next_step_handler(message, need_action_menu)
    elif message.text == 'Add event':
        bot.send_message(message.chat.id, "Введите Событие в формате дд.мм.гггг", reply_markup=keyboard_cancel)
        bot.register_next_step_handler(message, need_action_add_event)
    elif message.text == 'More...':
        bot.send_message(message.chat.id, "More...", reply_markup=keyboard_menu2_more)
        bot.register_next_step_handler(message, need_action_more)
    else:
        bot.send_message(message.chat.id, constants.undefined_command, reply_markup=keyboard_menu)
        bot.register_next_step_handler(message, need_action_menu)


def need_action_add_event(message):  # !!!!!!ДОБАВИТЬ HANDLER!!!!!!!!
    u_id = message.from_user.id
    user = dynamic_dict_of_users[u_id]
    if len(message.text) == 10 and len(message.text.split('.')) == 3 and (0 < int(message.text[-4:]) < 2100):
        bot.send_message(message.chat.id, "Теперь напишите описание события", reply_markup=keyboard_cancel)
        user.set_tmp_event(message.text)
        bot.register_next_step_handler(message, need_action_add_event)
    elif message.text == 'Cancel':
        try:
            bot.send_message(message.chat.id, "Отмена", reply_markup=keyboard_menu)
            bot.register_next_step_handler(message, need_action_menu)
            date = user.get_tmp_event()
            user.events.pop(date)
            user.set_tmp_event('')
        except KeyError:
            pass
    else:
        bot.send_message(message.chat.id, "Событие добавлено", reply_markup=keyboard_menu)
        date = user.get_tmp_event()
        user.events[date] = message.text
        print(user.events)
        bot.register_next_step_handler(message, need_action_menu)


def need_action_more(message):
    u_id = message.from_user.id
    user = dynamic_dict_of_users[u_id]


    if message.text == 'Edit timetable':
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard_edit)
        bot.register_next_step_handler(message, need_action_edit_event)
    elif message.text == 'Edit events':
        bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard_edit)
        bot.register_next_step_handler(message, need_action_edit_event)
    elif message.text == 'See more features':
        bot.send_message(message.chat.id, 'You could see it on ...', reply_markup=keyboard_menu2)
        bot.register_next_step_handler(message, need_action_more)
    elif message.text == 'delete myself':
        bot.send_message(message.chat.id, 'ok', reply_markup=keyboard_menu)
        bot.register_next_step_handler(message, need_action_more)
    elif message.text == 'back':  # !!!!!!!!!!!ИСПРАВИТЬ!!!!!!!!!!
        bot.send_message(message.chat.id, 'back', reply_markup=keyboard_menu2)
        bot.register_next_step_handler(message, need_action_from_menu)
    else:
        bot.send_message(message.chat.id, constants.undefined_command, reply_markup=keyboard_edit)
        bot.register_next_step_handler(message, need_action_more)


def need_action_edit_event(message):
    u_id = message.from_user.id
    user = dynamic_dict_of_users[u_id]

    if message.text == 'Cancel':
        bot.send_message(message.chat.id, "As you say", reply_markup=keyboard_menu)
        bot.register_next_step_handler(message, need_action_menu)
    elif message.text == 'Edit date':
        for i in user.get_events():
            bot.send_message(message.chat.id, user[i])
        bot.send_message(message.chat.id, """Введите дату события, которую хотите изменить, затем пробел,
а потом новую дату

Пример: 22.04.2018 23.04.2019""", reply_markup=keyboard_cancel)
        bot.register_next_step_handler(message, need_action_check_two_dates_event)

    elif message.text == 'Edit description':
        for i in user.get_events():
            bot.send_message(message.chat.id, user[i])
        bot.send_message(message.chat.id, """Введите дату события, описание которого хотите изменить, затем дефис 
(без пробелов), а потом новое описание

Пример: 22.04.2018-Я хочу, чтобы у события, запланированного на эту дату было именно это описание""",
                         reply_markup=keyboard_cancel)
        bot.register_next_step_handler(message, need_action_check_date_and_description_event)
    else:
        bot.send_message(message.chat.id, constants.undefined_command, reply_markup=keyboard_menu2_more)


def need_action_check_two_dates_event(message):
    u_id = message.from_user.id
    user = dynamic_dict_of_users[u_id]
    two_dates = message.text.split()
    if len(message.text) == 21 and 1000 < int(two_dates[0][-4:]) < 2100 and 1000 < int(two_dates[1][-4:]) < 2100 and \
            two_dates[0] in user.events:
        user.change_event_date(two_dates[0], two_dates[1])
        bot.send_message(message.chat.id, "Изменения внесены", reply_markup=keyboard_menu)
        bot.register_next_step_handler(message, need_action_menu)
    elif message.text == 'Cancel':
        bot.send_message(message.chat.id, "Действие отменено", reply_markup=keyboard_menu2_more)
        bot.register_next_step_handler(message, need_action_more)
    else:
        bot.send_message(message.chat.id, "Вы ввели что-то не то, попробуйте еще раз")
        bot.send_message(message.chat.id, """Введите дату события, которую хотите изменить, затем пробел,
а потом новую дату

Пример: 22.04.2018 23.04.2019""", reply_markup=keyboard_cancel)
        bot.register_next_step_handler(message, need_action_check_two_dates_event)


def need_action_check_date_and_description_event(message):
    try:
        u_id = message.from_user.id
        user = dynamic_dict_of_users[u_id]
        two_dates = message.text.split('-')
        if 1000 < int(two_dates[0][-4:]) < 2100:
            user.change_event_description(two_dates[0], two_dates[1])
            bot.send_message(message.chat.id, "Изменения внесены", reply_markup=keyboard_menu)
            bot.register_next_step_handler(message, need_action_menu)

        elif message.text == 'Cancel':
            bot.send_message(message.chat.id, "Действие отменено", reply_markup=keyboard_menu2_more)
            bot.register_next_step_handler(message, need_action_more)
        else:
            bot.send_message(message.chat.id, "Вы ввели что-то не то, попробуйте еще раз")
            bot.send_message(message.chat.id, """Введите дату события, описание которого хотите изменить, затем дефис 
(без пробелов), а потом новое описание

Пример: 22.04.2018-Я хочу, чтобы у события, запланированного на эту дату было именно это описание""",
                             reply_markup=keyboard_cancel)
            bot.register_next_step_handler(message, need_action_check_date_and_description_event)
    except ValueError:
        bot.send_message(message.chat.id, "Вы ввели что-то не то, попробуйте еще раз")
        bot.send_message(message.chat.id, """Введите дату события, описание которого хотите изменить, затем дефис 
        (без пробелов), а потом новое описание

        Пример: 22.04.2018-Я хочу, чтобы у события, запланированного на эту дату было именно это описание""",
                         reply_markup=keyboard_cancel)
        bot.register_next_step_handler(message, need_action_check_date_and_description_event)


bot.polling(none_stop=True, interval=0)
