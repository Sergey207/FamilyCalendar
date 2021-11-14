from PyQt5.QtWidgets import QCalendarWidget


class MyCalendar(QCalendarWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def paintCell(self, painter, rect, date):
        QCalendarWidget.paintCell(self, painter, rect, date)
        print(rect, date)
