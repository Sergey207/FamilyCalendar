import sqlite3

from PyQt5.QtCore import QRect, QDate
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QCalendarWidget


class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        QCalendarWidget.__init__(self, parent)

        self.cur = sqlite3.connect('events.db').cursor()
        self.updateDB()
        self.grayColor, self.blackColor = QColor(150, 150, 150), QColor(0, 0, 0)
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setStyleSheet('''font-size: 18px;''')

    def updateDB(self):
        self.colors = {i[0]: (i[1], i[2], i[3]) for i in self.cur.execute('select * from colors')}
        self.familyMembers = {i[0]: self.colors[i[1]] for i in
                              self.cur.execute('select id, color from familyMembers')}
        self.irregularEvents = tuple([
            [self.familyMembers[i[0]], i[1], i[2],
             QDate(int(i[3].split('.')[2]), int(i[3].split('.')[1]),
                   int(i[3].split('.')[0]))] for i in self.cur.execute(
                '''select familyMember, title, text, date from events where not isEventRegular''')])
        print(self.irregularEvents)

    def paintCell(self, painter: QPainter, rect: QRect, date: QDate):
        if self.monthShown() == date.month():
            painter.setPen(self.blackColor)
        else:
            painter.setPen(self.grayColor)
        painter.drawText(rect, 0, str(date.day()))
        if date == date.currentDate():
            painter.setBrush(QColor(178, 236, 93, 150))
            painter.drawRect(rect)
