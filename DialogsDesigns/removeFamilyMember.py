# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'removeFamilyMember.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(403, 300)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setStyleSheet("    background-color: rgb(156, 231, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(0, 0, 0);\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setStyleSheet("    background-color: rgb(156, 231, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(0, 0, 0);\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;")
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 202, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.removeMember = QtWidgets.QPushButton(Dialog)
        self.removeMember.setStyleSheet("    background-color: rgb(156, 231, 255);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(0, 0, 0);\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;")
        self.removeMember.setObjectName("removeMember")
        self.verticalLayout.addWidget(self.removeMember)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "?????????????? ?????????? ??????????"))
        self.label.setText(_translate("Dialog", "???????????????? ?????????? ??????????:"))
        self.removeMember.setText(_translate("Dialog", "??????????????"))
