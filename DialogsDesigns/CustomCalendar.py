import datetime
import sqlite3
from pprint import pprint

from PyQt5.QtCore import QRect, QDate, QTime
from PyQt5.QtGui import QColor, QPainter, QFont, QPen
from PyQt5.QtWidgets import QCalendarWidget


class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        QCalendarWidget.__init__(self, parent)

        self.cur = sqlite3.connect('events.db').cursor()
        self.checkboxes = []
        self.grayColor, self.blackColor = QColor(150, 150, 150), QColor(0, 0, 0)
        self.todayRect = None
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.bigFont = QFont()
        self.bigFont.setPointSize(10)
        self.littleFont = QFont()
        self.littleFont.setPointSize(6)

    def updateCheckboxes(self, checkboxes):
        self.checkboxes = checkboxes
        self.repaint()

    def repaint(self):
        self.todayRect = None
        QCalendarWidget.repaint(self)

    def paintCell(self, painter: QPainter, rect: QRect, date: QDate):
        self.updateDB(self.checkboxes)
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
            painter.drawText(rect, 1, f"{date.day()}")
            new_line_simbols = '\n\n'
            for color, t_o_r, title in tuple(map(lambda x: x[:-2],
                                                 filter(lambda x: x[-2] == date,
                                                        sorted(self.events, key=lambda x: x[-1])))):
                symbolsPerLine = rect.width() // 6
                parts_of_title = []
                while len(str(title)) >= symbolsPerLine:
                    parts_of_title.append(str(title[:symbolsPerLine]))
                    title = title[symbolsPerLine:]
                parts_of_title.append(str(title))
                title = '\n'.join(parts_of_title)

                painter.setPen(QColor(*color))
                painter.setFont(self.littleFont)
                painter.drawText(rect, 1, f'{new_line_simbols}{title}')
                new_line_simbols += '\n' * len(parts_of_title)
            if self.todayRect is not None:
                painter.setPen(QPen(QColor(255, 0, 0), 2))
                painter.drawRect(self.todayRect)
        except BaseException as e:
            print('PaintCell ->', e)

    def updateDB(self, checkboxes=None):
        if checkboxes is not None:
            checkboxes = tuple(
                map(lambda x: x.text(), filter(lambda x: x.checkState(), checkboxes)))
        self.colors = {i[0]: i[1:] for i in self.cur.execute('select * from colors')}
        self.familyMembers = {i[0]: self.colors[i[1]] for i in
                              self.cur.execute('select id, color from familyMembers')}
        self.familyMembersNames = {i[0]: i[1] for i in
                                   self.cur.execute('select id, name from familyMembers')}
        self.typesOfRegular = {i[0]: i[1] for i in self.cur.execute('select * from typesOfRegular')}

        self.events = []
        for idOfType, title in self.typesOfRegular.items():
            for i in self.cur.execute(f'''select * from events where typeOfRegular = {idOfType}'''):
                if checkboxes is None or self.familyMembersNames[i[0]] in checkboxes:
                    print(self.familyMembersNames[i[0]], checkboxes)
                    date = QDate(int(i[4].split('.')[2]), int(i[4].split('.')[1]),
                                 int(i[4].split('.')[0]))
                    time = QTime(*map(int, i[5].split(':')))
                    match i[1]:
                        case 1 | 2 | 3 | 4 | 5 | 6 | 7:
                            while (date.year(), date.month()) <= (
                                    self.yearShown() + 1, self.monthShown() + 2):
                                self.events.append(
                                    (self.familyMembers[i[0]], i[1], i[2], date, time))
                                date = date.addDays(i[1])
                        case 8:
                            while (date.year(), date.month()) <= (
                                    self.yearShown() + 1, self.monthShown() + 2):
                                self.events.append(
                                    (self.familyMembers[i[0]], i[1], i[2], date, time))
                                date = date.addMonths(1)
                        case 9:
                            while (date.year(), date.month()) <= (
                                    self.yearShown() + 1, self.monthShown() + 2):
                                self.events.append(
                                    (self.familyMembers[i[0]], i[1], i[2], date, time))
                                date = date.addYears(1)
                        case 10:
                            self.events.append((self.familyMembers[i[0]], i[1], i[2], date, time))
