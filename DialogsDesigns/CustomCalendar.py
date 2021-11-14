from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QCalendarWidget


class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        QCalendarWidget.__init__(self, parent)
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.setStyleSheet('''font-size: 18px;''')

    def paintCell(self, painter, rect, date):
        # QCalendarWidget.paintCell(self, painter, rect, date)
        print(date)
        painter.drawText(rect,0, str(date.day()))
        if date == date.currentDate():
            painter.setBrush(QColor(178, 236, 93, 150))
            painter.drawRect(rect)
