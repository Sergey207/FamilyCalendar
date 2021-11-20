import datetime
from pprint import pprint
import sqlite3

from PyQt5.QtCore import QRect, QDate
from PyQt5.QtGui import QColor, QPainter, QFont, QBrush, QPen
from PyQt5.QtWidgets import QCalendarWidget


class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        QCalendarWidget.__init__(self, parent)

        self.cur = sqlite3.connect('events.db').cursor()
        self.grayColor, self.blackColor = QColor(150, 150, 150), QColor(0, 0, 0)
        self.todayRect = None
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.bigFont = QFont()
        self.bigFont.setPointSize(10)
        self.littleFont = QFont()
        self.littleFont.setPointSize(6)

    def repaint(self):
        self.updateDB()
        QCalendarWidget.repaint(self)

    def paintCell(self, painter: QPainter, rect: QRect, date: QDate):
        new_line_simbols = ''
        try:

            if date.day() == datetime.datetime.now().date().day and \
                    date.month() == datetime.datetime.now().month and \
                    date.year() == datetime.datetime.now().year:
                self.todayRect = rect
            if self.monthShown() == date.month():
                painter.setPen(self.blackColor)
            else:
                painter.setPen(self.grayColor)
            painter.setFont(self.bigFont)
            painter.drawText(rect, 1, f"{new_line_simbols}{date.day()}")
            new_line_simbols += '\n\n'

            for color, t_o_r, title in tuple(map(lambda x: x[:-1],
                                                 filter(lambda x: x[-1] == date, self.events))):
                parts_of_title = []
                while len(title) >= 19:
                    parts_of_title.append(title[:19])
                    title = title[19:]
                parts_of_title.append(title)
                title = '\n'.join(parts_of_title)

                painter.setPen(QColor(*color))
                painter.setFont(self.littleFont)
                painter.drawText(rect, 1, f'{new_line_simbols}{title}')
                new_line_simbols += '\n' * len(parts_of_title)
            if self.todayRect is not None:
                painter.setPen(QPen(QColor(255, 0, 0), 2))
                painter.drawRect(self.todayRect)
        except BaseException as e:
            print(e)

    def updateDB(self):
        self.colors = {i[0]: (i[1], i[2], i[3]) for i in self.cur.execute('select * from colors')}
        self.typesOfRegular = {i[0]: i[1] for i in
                               self.cur.execute('select id, title from typesOfRegular')}
        self.familyMembers = {i[0]: self.colors[i[1]] for i in
                              self.cur.execute('select id, color from familyMembers')}

        pprint(self.typesOfRegular)
        self.events = []
        for idOfType, title in self.typesOfRegular.items():
            for i in self.cur.execute(f'''select * from events where typeOfRegular = {idOfType}'''):
                date = QDate(int(i[4].split('.')[2]), int(i[4].split('.')[1]),
                             int(i[4].split('.')[0]))
                minMonthNumber = self.monthShown() - 1 if self.monthShown() > 1 else 12
                maxMonthNumber = self.monthShown() + 1 if self.monthShown() < 12 else 1
                if i[1] == 1:
                    for monthNumber in (minMonthNumber, self.monthShown(), maxMonthNumber):
                        for dayNumber in range(1, 32):
                            if self.monthShown() <= 1 and monthNumber == 12:
                                year = self.yearShown() - 1
                            elif self.monthShown() >= 12 and monthNumber == 1:
                                year = self.yearShown() + 1
                            else:
                                year = self.yearShown()
                            if QDate(year, monthNumber, dayNumber) >= date:
                                self.events.append((self.familyMembers[i[0]], i[1], i[2],
                                                    QDate(year, monthNumber, dayNumber)))
                elif i[1] == 2:
                    while date.month() in (minMonthNumber, self.monthShown(), maxMonthNumber):
                        self.events.append((self.familyMembers[i[0]], i[1], i[2],
                                            date))
                        date.addDays(2)
                elif i[1] == 10:
                    self.events.append((self.familyMembers[i[0]], i[1], i[2],
                                        date))
