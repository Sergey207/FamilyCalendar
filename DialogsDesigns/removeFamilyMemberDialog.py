import sqlite3

from PyQt5.QtWidgets import QDialog

from DialogsDesigns.removeFamilyMember import Ui_Dialog


class removeFamilyMemberDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(removeFamilyMemberDialog, self).__init__()
        self.setupUi(self)
        self.removeMember.clicked.connect(self.onRemoveMemberClicked)

        self.con = sqlite3.connect('events.db')
        self.cur = self.con.cursor()
        self.comboBox.addItems(list(map(lambda x: x[0], self.cur.execute(
            '''select name from familyMembers'''))))

    def onRemoveMemberClicked(self):
        try:
            id = tuple(self.cur.execute(
                f'select id from familyMembers where name="{self.comboBox.currentText()}"'))[0][0]
            self.cur.execute(
                f'delete from events where familyMember = {id}')
            self.con.commit()
            self.cur.execute(
                f'delete from familyMembers where name = "{self.comboBox.currentText()}"')
            self.con.commit()
            self.close()
        except BaseException as e:
            print(e)
