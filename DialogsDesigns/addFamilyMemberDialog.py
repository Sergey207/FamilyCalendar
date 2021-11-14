import sqlite3

from PyQt5.QtWidgets import QDialog, QColorDialog, QMessageBox

from DialogsDesigns.addFamilyMember import Ui_Dialog as addFamilyMemberDialogDesign


class addFamilyMemberDialog(QDialog, addFamilyMemberDialogDesign):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.color = None
        self.colors = list(
            sqlite3.connect("../events.db").cursor().execute('''select * from colors'''))
        self.familyMembers = list(map(lambda x: x[0], sqlite3.connect(
            '../events.db').cursor().execute(
            '''select name from familyMembers''')))
        self.chooseColor.clicked.connect(self.onChooseColorClicked)
        self.addMember.clicked.connect(self.onAddMemberClicked)

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
                connection = sqlite3.connect("../events.db")
                cursor = connection.cursor()

                if self.color not in tuple(map(lambda x: x[2:], self.colors)):
                    cursor.execute(f'''insert into colors(red, green, blue) 
                    values({self.color[0]}, {self.color[1]}, {self.color[2]})''')
                    connection.commit()

                color = list(cursor.execute(f'''select id from colors where
                Red = {self.color[0]} and Green = {self.color[1]} and Blue = {self.color[2]}'''))[
                    0][0]
                cursor.execute(f'''insert into familyMembers(name, color) 
                        values("{self.nameLabel.text()}", {color})''')
                connection.commit()
                self.close()
            except Exception as e:
                print(e)
