import sqlite3

from PyQt5.QtWidgets import QDialog, QColorDialog, QMessageBox

from DialogsDesigns.changeColorFamilyMember import Ui_Dialog


class changeColorFamilyMemberDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox.addItems(list(map(lambda x: x[0],
                                        sqlite3.connect('../events.db').cursor().execute(
                                            '''select name from familyMembers'''))))
        self.colors = list(
            sqlite3.connect('../events.db').cursor().execute(
                '''select Red, Green, Blue from colors'''))
        self.chooseColor.clicked.connect(self.onChooseColorClicked)
        self.changeColor.clicked.connect(self.onChangeColorClicked)

    def onChooseColorClicked(self):
        self.color = QColorDialog.getColor().toRgb().getRgb()[:-1]
        self.resultLabel.setText(str(self.color))
        self.resultLabel.setStyleSheet(
            f'''color: rgb({self.color[0]},{self.color[1]},{self.color[2]});''')

    def onChangeColorClicked(self):
        if self.resultLabel.text() == 'Выберите новый цвет':
            dlg = QMessageBox(self)
            dlg.setWindowTitle('Ошибка')
            dlg.setText('Цвет не выбран')
            dlg.exec()
        else:
            con = sqlite3.connect('../events.db')
            cur = con.cursor()
            if self.color not in self.colors:
                cur.execute(f'''insert into colors(red, green, blue)
                            values({self.color[0]},{self.color[1]},{self.color[2]})''')
                con.commit()
                
            newColorID = int(list(cur.execute(f'''select id from colors 
where red = {self.color[0]} and green = {self.color[1]} and blue = {self.color[2]}'''))[0][0])
            cur.execute(f'''update familyMembers
set color={newColorID}
where name = "{self.comboBox.currentText()}"''')
            con.commit()

            self.close()
