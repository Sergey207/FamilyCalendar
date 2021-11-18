import sqlite3

from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView

from DialogsDesigns.deleteEventDesign import Ui_Dialog


class deleteEventDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.con = sqlite3.connect("events.db")
        self.cur = self.con.cursor()
        self.f_m = {i[0]: i[1] for i in self.cur.execute("select id, name from familyMembers")}
        self.t_o_r = {i[0]: i[1] for i in self.cur.execute("select * from typesOfRegular")}
        self.updateTable()
        self.pushButton.clicked.connect(self.deleteEvents)

    def updateTable(self):
        self.events = tuple(self.cur.execute("select * from events"))
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(len(self.events))
        self.tableWidget.setHorizontalHeaderLabels(("Член семьи", "Тип регулярности", "Заголовок",
                                                    "Текст", "Дата"))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for i, line in enumerate(self.events):
            for j, value in enumerate(line):
                if j == 0:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(self.f_m[value]))
                elif j == 1:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(self.t_o_r[value]))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))

    def deleteEvents(self):
        selected_rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        for row in selected_rows:
            query = []
            for i, title in enumerate(("familyMember", "typeOfRegular", "title", "text", "date")):
                v = self.tableWidget.item(row, i).text()
                if i == 0:
                    for index, value in self.f_m.items():
                        if self.tableWidget.item(row, i).text() == value:
                            v = str(index)
                            break
                elif i == 1:
                    for index, value in self.t_o_r.items():
                        if self.tableWidget.item(row, i).text() == value:
                            v = str(index)
                            break
                else:
                    v = f'"{v}"'

                query.append(f"{title}={v}")
            self.cur.execute('delete from events where ' + ' and '.join(query))
            self.con.commit()
            self.close()
