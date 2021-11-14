import sqlite3

from PyQt5.QtWidgets import QDialog, QColorDialog, QMessageBox

from DialogsDesigns.changeColorFamilyMember import Ui_Dialog


class changeColorFamilyMemberDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.chooseColor.clicked.connect(self.onChooseColorClicked)
        self.changeColor.clicked.connect(self.onChangeColorClicked)

        self.con = sqlite3.connect('events.db')
        self.cur = self.con.cursor()
        self.comboBox.addItems(list(map(lambda x: x[0], self.cur.execute(
            '''select name from familyMembers'''))))
        self.colors = list(self.cur.execute('''select Red, Green, Blue from colors'''))

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

    def onChangeColorClicked(self):
        if self.resultLabel.text() == 'Выберите новый цвет':
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Ошибка')
            dlg.setText('Цвет не выбран')
            dlg.exec()
        else:
            if self.color not in self.colors:
                self.cur.execute(f'''insert into colors(red, green, blue)
                            values({self.color[0]},{self.color[1]},{self.color[2]})''')
                self.con.commit()

            newColorID = int(list(self.cur.execute(f'''select id from colors 
where red = {self.color[0]} and green = {self.color[1]} and blue = {self.color[2]}'''))[0][0])
            self.cur.execute(f'''update familyMembers
set color={newColorID}
where name = "{self.comboBox.currentText()}"''')
            self.con.commit()

            self.close()
