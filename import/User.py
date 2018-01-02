import requests
from bs4 import BeautifulSoup


class User(object):

    def __init__(self, u_id):
        """User's constructor. It needs one parameter const int param"""

        self.user_id = u_id

        self.events = {}

        self.tasks = {}

        self.timetable = []

    def set_id(self, u_id):
        """Helpful function that changes field User.user_id.
        :param u_id: user id"""

        self.user_id = u_id

    def add_event(self, date, description):
        """Function allows you to add events.
        :param date: date, in which the event is going to be
        :param description: description of the event, that you want to add
        Function creates a pair 'param01': param02' and add it to dictionary events"""

        self.events[date] = description

    def change_event_date(self, old_date, new_date):
        """Function allows you to change the key in dictionary events.
        :param old_date: date, that you want to change
        :param new_date: date, that you want to add"""

        try:
            description = self.events[old_date]
            self.events.pop(description)
            self.events[new_date] = description

        except BaseException:
            return 'Такой даты не существует в вашем списке событий'

    def change_event_description(self, date, new_description):
        """Function allows you to change the value in dictionary events.
        :param date: date of the event you want to change description
        :param new_description: new decription of the event"""

        self.events[date] = new_description

    def parse_timetable(self):
        """Function add the timetable from official site to timetable array"""
        s = requests.get('https://students.bmstu.ru/schedule/62f5611c-a264-11e5-b4d3-005056960017')
        b = BeautifulSoup(s.text, "html.parser")

        if (b is None) or len(b) == 0:
            self.timetable.append("Cannot download the timetable at this moment. Try again later.")
        else:
            first = b.select('.table ')

            for i in first:
                self.timetable.append(i.getText())
