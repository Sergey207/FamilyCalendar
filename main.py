import datetime
import sqlite3
import sys

import plyer
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTime, QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from DialogsDesigns.addFamilyMemberDialog import addFamilyMemberDialog
from DialogsDesigns.changeColorFamilyMemberDialog import changeColorFamilyMemberDialog
from DialogsDesigns.design import Ui_MainWindow as mainWindowDesign
from DialogsDesigns.removeFamilyMemberDialog import removeFamilyMemberDialog


class Window(QMainWindow, mainWindowDesign):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setupUi(self)
        self.setMinimumSize(1024, 768)

        self.checkBoxes = []
        self.stackedWidget.setCurrentIndex(0)
        self.updateFamilyMembersCheckBoxes()

        self.addEventButton.clicked.connect(self.onAddEventButtonClicked)
        self.addFamilyMemberButton.clicked.connect(self.addFamilyMemberClicked)
        self.changeColorFamilyMember.clicked.connect(
            self.onChangeColorFamilyMemberClicked)
        self.removeFamilyMember.clicked.connect(self.onRemoveFamilyMemberClicked)
        self.toExcelButton.clicked.connect(self.toExcelButtonClicked)

        self.radioButton.clicked.connect(self.onRadioButtonClicked)
        self.radioButton_2.clicked.connect(self.onRadioButtonClicked)
        self.typesOfRegular = tuple(
            map(lambda x: x[0], self.cursor.execute('''select title from typesOfRegular''')))
        self.dateComboBox.addItems(self.typesOfRegular)
        self.titleEdit.textChanged.connect(
            lambda: self.titleEdit.setText(self.titleEdit.text()[:19]))
        self.cancelButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.addButton.clicked.connect(self.addEvent)
        self.radioButton.click()

    def updateDB(self):
        self.connection = sqlite3.connect(
            "events.db")  # Сделать создание базы данных при её отсутствии TODO
        self.cursor = self.connection.cursor()
        self.colors = list(self.cursor.execute('''select * from colors'''))
        self.familyMembers = tuple(map(lambda x: x[1:], self.cursor.execute(
            '''select * from familyMembers''')))
        self.events = tuple(self.cursor.execute('''select * from events'''))
        self.calendarWidget.updateDB()

    # page 1
    def addFamilyMemberClicked(self):
        dlg = addFamilyMemberDialog()
        dlg.exec()
        if dlg.colorID is not None:
            self.updateFamilyMembersCheckBoxes()

    def onChangeColorFamilyMemberClicked(self):
        dlg = changeColorFamilyMemberDialog()
        dlg.exec()
        if dlg.resultLabel.text() != 'Выберите новый цвет':
            self.updateFamilyMembersCheckBoxes()

    def onRemoveFamilyMemberClicked(self):
        dlg = removeFamilyMemberDialog()
        dlg.exec()
        self.updateFamilyMembersCheckBoxes()

    def onAddEventButtonClicked(self):
        try:
            self.stackedWidget.setCurrentIndex(1)
            time_now = datetime.datetime.now().time()
            date_now = datetime.datetime.now().date()
            self.dateTimeEdit.setTime((QTime(time_now.hour, time_now.minute)))
            self.dateTimeEdit.setDate((QDate(date_now.year, date_now.month, date_now.day)))
            self.familyMembersComboBox.clear()
            self.familyMembersComboBox.addItems(tuple(map(lambda x: x[0], self.familyMembers)))
        except BaseException as e:
            print(e)

    def updateFamilyMembersCheckBoxes(self):
        self.updateDB()
        for checkbox in self.checkBoxes:
            self.verticalLayout.removeWidget(checkbox)
        self.checkBoxes.clear()
        for (memberName, colorID) in sorted(self.familyMembers, key=lambda x: x[0]):
            self.checkBoxes.append(QtWidgets.QCheckBox(self.centralwidget))
            self.checkBoxes[-1].setText(memberName)
            self.checkBoxes[-1].setChecked(True)
            r, g, b = list(filter(lambda x: x[0] == colorID, self.colors))[0][1:]
            self.checkBoxes[-1].setStyleSheet(f'''color: rgb({r}, {g}, {b});
background-color: rgb({255 - r}, {255 - g}, {255 - b});
border-style: outset;
border-width: 2px;
border-radius: 10px;
border-color: rgb(0, 0, 0);
font: bold 14px;
min-width: 10em;
padding: 6px;''')
            self.verticalLayout.insertWidget(0, self.checkBoxes[-1])

    def toExcelButtonClicked(self):
        print('To Excel Button clicked')  # TODO

    # page 2
    def onRadioButtonClicked(self):
        self.dateComboBox.setEnabled(False if self.sender() == self.radioButton else True)

    def addEvent(self):
        if self.titleEdit.text() == '':
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Ошибка')
            dlg.setText('Не указан заголовок события!')
            dlg.exec()
        else:
            f_m = tuple(self.connection.execute('''select name, id from familyMembers'''))
            date = self.dateTimeEdit.date()
            if self.radioButton.isChecked():
                self.cursor.execute(
                    f'''insert into events(familyMember, isEventRegular, title, text, date)
values({list(filter(lambda x: x[0] == self.familyMembersComboBox.currentText(), f_m))
                    [0][1]},0 , "{self.titleEdit.text()}", "{self.textEdit.text()}", 
"{date.day()}.{date.month()}.{date.year()}")''')
            self.connection.commit()
            self.stackedWidget.setCurrentIndex(0)
        # self.events = tuple(self.cursor.execute('''select * from events'''))
        # print(self.events)
        # pass  # Добавление события TODO


def show_notification(title='Событие', message='Событие случилось'):
    plyer.notification.notify(message=message, app_name='Семейный календарь',
                              app_icon='Photos/bell.ico', title=title)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
