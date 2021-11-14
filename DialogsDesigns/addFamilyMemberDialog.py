import sqlite3

from PyQt5.QtWidgets import QDialog, QColorDialog, QMessageBox

from DialogsDesigns.addFamilyMember import Ui_Dialog as addFamilyMemberDialogDesign


class addFamilyMemberDialog(QDialog, addFamilyMemberDialogDesign):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.chooseColor.clicked.connect(self.onChooseColorClicked)
        self.addMember.clicked.connect(self.onAddMemberClicked)

        self.colorID = None
        self.con = sqlite3.connect('events.db')
        self.cur = self.con.cursor()
        self.familyMembers = list(
            map(lambda x: x[0], self.cur.execute('''select name from familyMembers''')))

    def onChooseColorClicked(self):
        self.color = QColorDialog.getColor().toRgb().getRgb()[:-1]
        self.resultLabel.setText(str(self.color))
        self.resultLabel.setStyleSheet(
            f'''background-color: rgb({self.color[0]}, {self.color[1]}, {self.color[2]});
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: rgb(0, 0, 0);
            font: bold 14px;
            min-width: 10em;
            padding: 6px;''')

    def onAddMemberClicked(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Ошибка")
        if self.nameLabel.text() == '':
            dlg.setText("Не указано имя")
            dlg.exec()
        elif self.nameLabel.text() in self.familyMembers:
            dlg.setText("Такое имя уже есть")
            dlg.exec()
        elif self.resultLabel.text() == 'Выберите цвет':
            dlg.setText("Цвет не выбран")
            dlg.exec()
        else:
            try:
                if self.color not in tuple(
                        self.cur.execute('''select Red, Green, Blue from colors''')):
                    self.cur.execute(f'''insert into colors(red, green, blue)
                    values({self.color[0]}, {self.color[1]}, {self.color[2]})''')
                    self.con.commit()

                self.colorID = list(self.cur.execute(f'''select id from colors where
                Red = {self.color[0]} and Green = {self.color[1]} and Blue = {self.color[2]}'''))[
                    0][0]
                self.cur.execute(f'''insert into familyMembers(name, color)
                        values("{self.nameLabel.text()}", {self.colorID})''')
                self.con.commit()
                self.close()
            except Exception as e:
                print(e)
