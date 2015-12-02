# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_ac.ui'
#
# Created: Tue Nov  3 21:17:17 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sqlite3 as lite
import sys
import time
import serial

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class AC_Dialog(QtGui.QDialog):
    def __init__(self):
        super(AC_Dialog, self).__init__()
        self.setupUi(self)

        self.con = lite.connect('access_db.db')
        self.port = serial.Serial('/dev/ttyACM0', 9600)
        self.tag = ''
        self.cur = self.con.cursor()

    def setupUi(self, AC_Dialog):
        AC_Dialog.setObjectName(_fromUtf8("AC_Dialog"))
        AC_Dialog.resize(453, 86)
        self.verticalLayout_2 = QtGui.QVBoxLayout(AC_Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(AC_Dialog)
        self.label.setText(_fromUtf8(""))
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(AC_Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Retry)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(AC_Dialog)
        QtCore.QMetaObject.connectSlotsByName(AC_Dialog)

    def retranslateUi(self, AC_Dialog):
        AC_Dialog.setWindowTitle(_translate("AC_Dialog", "Controle de Acesso", None))

    def read_tag(self):
        try:
            self.label.setText('Por favor, insira uma tag')
            response = self.port.read(15)
            self.tag = str(response.split(':')[1])
            #tag = str(response.split('#')[0])
            print "Tag lida: {0}".format(self.tag)
            self.label.setText(self.tag)
            self.port.flush()
            #return self.tag
        except KeyboardInterrupt:
            return
        #finally:
            #self.port.close()

    def create_table(self):
        try:
            self.cur.executescript('CREATE TABLE IF NOT EXISTS Usuario (UserID INTEGER PRIMARY KEY, UltimaEntrada TEXT, Nome TEXT, Tag TEXT); CREATE UNIQUE INDEX TagUnrepeatable ON Usuario (Tag);')
            self.con.commit()

        except lite.Error, e:
            if self.con:
                self.con.rollback()
            print 'Error %s' % e.args[0]
            self.label.setText('Error %s' % e.args[0])
            sys.exit(1)

        finally:
            if self.con:
                self.con.close()

    def check_tag(self):
        try:
            self.cur.execute("SELECT UserID, Nome FROM Usuario WHERE Tag = ?",
                  (self.tag,))
            user = self.cur.fetchone()
            print 'Olá {0}. Hora da entrada: {1}'.format(user[1],
                 time.strftime("%c"))
            self.cur.execute("UPDATE Usuario SET UltimaEntrada = DateTime(CURRENT_TIMESTAMP, 'localtime') WHERE UserID = {0};".format(user[0]))
            self.con.commit()
            QtGui.QMessageBox.showMessage('Olá {0}. Hora da entrada: {1}'.format(user[1],
                 time.strftime("%c")))
        except lite.Error as e:
            print "Ocorreu um erro: ", e.args[0]
        finally:
            self.con.close()