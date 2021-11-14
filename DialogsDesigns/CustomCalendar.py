from PyQt5.QtCore import QRect, QDate
from PyQt5.QtGui import QColor, QPainter, QFont
from PyQt5.QtWidgets import QCalendarWidget


class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        QCalendarWidget.__init__(self, parent)
        self.grayColor, self.blackColor = QColor(150, 150, 150), QColor(0, 0, 0)
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setStyleSheet('''font-size: 18px;''')

    def paintCell(self, painter: QPainter, rect: QRect, date: QDate):
        # print('Drawing cell...')
        if self.monthShown() == date.month():
            painter.setPen(self.blackColor)
        else:
            painter.setPen(self.grayColor)
        painter.drawText(rect, 0, str(date.day()))
        if date == date.currentDate():
            painter.setBrush(QColor(178, 236, 93, 150))
            painter.drawRect(rect)
