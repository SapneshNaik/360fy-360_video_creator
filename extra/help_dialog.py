# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(362, 151)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        Dialog.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../resource/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)
        Dialog.setAutoFillBackground(False)
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.docButton = QtWidgets.QPushButton(Dialog)
        self.docButton.setGeometry(QtCore.QRect(180, 100, 141, 41))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../../Personal/cd01e9c9b9e961e1c896e5556cb7b159.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.docButton.setIcon(icon1)
        self.docButton.setObjectName("docButton")
        self.tubeButton = QtWidgets.QPushButton(Dialog)
        self.tubeButton.setGeometry(QtCore.QRect(50, 100, 111, 41))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../../Personal/YouTube-icon-full_color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tubeButton.setIcon(icon2)
        self.tubeButton.setObjectName("tubeButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 331, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 321, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 50, 221, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(30, 80, 211, 17))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Help"))
        self.docButton.setText(_translate("Dialog", "Documentation"))
        self.tubeButton.setText(_translate("Dialog", "YouTube"))
        self.label.setText(_translate("Dialog", "If you have trouble understanding something"))
        self.label_2.setText(_translate("Dialog", "please consider reading the documentation"))
        self.label_3.setText(_translate("Dialog", "or watching the tutorial videos."))
        self.label_4.setText(_translate("Dialog", "* Internet Charges may apply"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())