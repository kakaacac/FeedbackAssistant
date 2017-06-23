# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\jayden\projects\FeedbackAssistant\ui\add_feedback.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Add(object):
    def setupUi(self, Add):
        Add.setObjectName("Add")
        Add.resize(596, 442)
        self.confirm = QtWidgets.QDialogButtonBox(Add)
        self.confirm.setGeometry(QtCore.QRect(250, 400, 341, 32))
        self.confirm.setOrientation(QtCore.Qt.Horizontal)
        self.confirm.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.confirm.setObjectName("confirm")
        self.type_select = QtWidgets.QComboBox(Add)
        self.type_select.setGeometry(QtCore.QRect(80, 10, 221, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.type_select.setFont(font)
        self.type_select.setObjectName("type_select")
        self.type_select.addItem("")
        self.type_select.addItem("")
        self.type_select.addItem("")
        self.label = QtWidgets.QLabel(Add)
        self.label.setGeometry(QtCore.QRect(20, 10, 54, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.content = QtWidgets.QPlainTextEdit(Add)
        self.content.setGeometry(QtCore.QRect(23, 60, 551, 301))
        self.content.setObjectName("content")

        self.retranslateUi(Add)
        self.confirm.accepted.connect(Add.accept)
        self.confirm.rejected.connect(Add.reject)
        QtCore.QMetaObject.connectSlotsByName(Add)

    def retranslateUi(self, Add):
        _translate = QtCore.QCoreApplication.translate
        Add.setWindowTitle(_translate("Add", "Dialog"))
        self.type_select.setItemText(0, _translate("Add", "Homework"))
        self.type_select.setItemText(1, _translate("Add", "Performance"))
        self.type_select.setItemText(2, _translate("Add", "Improvement"))
        self.label.setText(_translate("Add", "Type:"))

