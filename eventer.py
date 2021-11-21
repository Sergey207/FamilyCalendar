import datetime
import sqlite3
import time

import plyer
from PyQt5.QtCore import QDate


def getEvents():
    date_now = datetime.datetime.now()
    cur = sqlite3.connect("events.db").cursor()
    colors = {i[0]: i[1:] for i in cur.execute('select * from colors')}
    familyMembers = {i[0]: colors[i[1]] for i in
                     cur.execute('select id, color from familyMembers')}
    typesOfRegular = {i[0]: i[1] for i in cur.execute('select * from typesOfRegular')}

    events = []
    for idOfType, title in typesOfRegular.items():
        for i in cur.execute(f'''select * from events where typeOfRegular = {idOfType}'''):
            date = QDate(int(i[4].split('.')[2]), int(i[4].split('.')[1]),
                         int(i[4].split('.')[0]))
            timeOfEvent = datetime.time(*map(int, i[5].split(':')))
            match i[1]:
                case 1 | 2 | 3 | 4 | 5 | 6 | 7:
                    while (date.year(), date.month()) <= (
                            date_now.year, date_now.month + 2):
                        events.append((familyMembers[i[0]], i[1], i[2], i[3], date, timeOfEvent))
                        date = date.addDays(i[1])
                case 8:
                    while (date.year(), date.month()) <= (
                            date_now.year, date_now.month + 2):
                        events.append((familyMembers[i[0]], i[1], i[2], i[3], date, timeOfEvent))
                        date = date.addMonths(1)
                case 9:
                    while (date.year(), date.month()) <= (
                            date_now.year, date_now.month + 2):
                        events.append((familyMembers[i[0]], i[1], i[2], i[3], date, timeOfEvent))
                        date = date.addYears(1)
                case 10:
                    events.append((familyMembers[i[0]], i[1], i[2], i[3], date, timeOfEvent))
    qdate_now = QDate(date_now.year, date_now.month, date_now.day)
    timeNow = datetime.datetime.now().time()
    return tuple(filter(lambda x: x[4] == qdate_now and x[5] >= timeNow, events))


def show_notification(title='Событие', message='Событие случилось'):
    plyer.notification.notify(message=message, app_name='Семейный календарь',
                              app_icon='Photos/bell.ico', title=title)


if __name__ == '__main__':
    while True:
        events_today = getEvents()
        time_now = datetime.datetime.now().time()
        for event in events_today:
            if event[-1].hour <= time_now.hour and event[-1].minute <= time_now.minute:
                show_notification(event[2], event[3])
        time.sleep(60)
