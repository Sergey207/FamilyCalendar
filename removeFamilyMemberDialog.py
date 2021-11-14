import sqlite3

from PyQt5.QtWidgets import QDialog

from removeFamilyMember import Ui_Dialog


class removeFamilyMemberDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(removeFamilyMemberDialog, self).__init__()
        self.setupUi(self)
        self.comboBox.addItems(list(map(lambda x: x[0],
                                        sqlite3.connect('events.db').cursor().execute(
                                            '''select name from familyMembers'''))))
        self.removeMember.clicked.connect(self.onRemoveMemberClicked)

    def onRemoveMemberClicked(self):
        try:
            con = sqlite3.connect('events.db')
            cur = con.cursor()
            cur.execute(f'delete from familyMembers where name = "{self.comboBox.currentText()}"')
            con.commit()
            self.close()
        except BaseException as e:
            print(e)
