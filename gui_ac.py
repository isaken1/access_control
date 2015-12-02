# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acd.ui'
#
# Created: Wed Nov 11 10:25:06 2015
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


class Ac_dialog(QtGui.QDialog):
    def __init__(self):
        super(Ac_dialog, self).__init__()
        self.con = lite.connect('access_db.db')
        self.port = serial.Serial('/dev/ttyACM0', 9600)
        self.tag = ''
        self.cur = self.con.cursor()
        self.setupUi(self)

    def setupUi(self, ac_dialog):
        ac_dialog.setObjectName(_fromUtf8("ac_dialog"))
        ac_dialog.setWindowModality(QtCore.Qt.WindowModal)
        ac_dialog.resize(414, 145)
        ac_dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(ac_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_tag_t = QtGui.QLabel(ac_dialog)
        self.lbl_tag_t.setObjectName(_fromUtf8("lbl_tag_t"))
        self.horizontalLayout.addWidget(self.lbl_tag_t)
        self.lbl_tag = QtGui.QLabel(ac_dialog)
        self.lbl_tag.setObjectName(_fromUtf8("lbl_tag"))
        self.horizontalLayout.addWidget(self.lbl_tag)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lbl_nome_t = QtGui.QLabel(ac_dialog)
        self.lbl_nome_t.setObjectName(_fromUtf8("lbl_nome_t"))
        self.horizontalLayout.addWidget(self.lbl_nome_t)
        self.lbl_nome = QtGui.QLabel(ac_dialog)
        self.lbl_nome.setObjectName(_fromUtf8("lbl_nome"))
        self.horizontalLayout.addWidget(self.lbl_nome)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.cancel_button = QtGui.QPushButton(ac_dialog)
        self.cancel_button.setObjectName(_fromUtf8("cancel_button"))
        self.horizontalLayout_2.addWidget(self.cancel_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.read_button = QtGui.QPushButton(ac_dialog)
        self.read_button.setObjectName(_fromUtf8("read_button"))
        self.horizontalLayout_2.addWidget(self.read_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.cancel_button.clicked.connect(self.reject)
        self.read_button.clicked.connect(self.read_tag)
        self.retranslateUi(ac_dialog)
        QtCore.QMetaObject.connectSlotsByName(ac_dialog)

    def retranslateUi(self, ac_dialog):
        ac_dialog.setWindowTitle(_translate("ac_dialog", "Controle de Acesso", None))
        self.lbl_tag_t.setText(_translate("ac_dialog", "Tag:", None))
        self.lbl_tag.setText(_translate("ac_dialog", "Insira uma tag", None))
        self.lbl_nome_t.setText(_translate("ac_dialog", "Usuário:", None))
        self.lbl_nome.setText(_translate("ac_dialog", "Insira uma tag", None))
        self.cancel_button.setText(_translate("ac_dialog", "Cancelar", None))
        self.read_button.setText(_translate("ac_dialog", "Ler Tag", None))

    def read_tag(self):
        try:
            if not self.port.isOpen():
                self.port.open()
                self.read_tag()
            else:
                response = self.port.read(15)
                self.tag = str(response.split(':')[1])
                print "Tag lida: {0}".format(self.tag)
                self.port.flush()
                self.lbl_tag.setText(self.tag)
                self.check_tag()
        except KeyboardInterrupt as e:
            QtGui.QErrorMessassage.showMessage(e.args[0])
        finally:
            self.port.close()

    def create_table(self):
        try:
            self.cur.executescript('CREATE TABLE IF NOT EXISTS Usuario (UserID INTEGER PRIMARY KEY, UltimaEntrada TEXT, Nome TEXT, Tag TEXT); CREATE UNIQUE INDEX TagUnrepeatable ON Usuario (Tag);')
            self.con.commit()

        except lite.Error, e:
            if self.con:
                self.con.rollback()
            print 'Error %s' % e.args[0]
            self.label.setText('Error %s' % e.args[0])
            QtGui.QErrorMessassage.showMessage(e.args[0])
            sys.exit(1)

        finally:
            if self.con:
                self.con.close()

    #def insert_data(self):
        #try:
            #nome = raw_input("Insira o seu nome: \n")

            #self.cur.execute("""
                #INSERT INTO Usuario (UltimaEntrada, Nome, Tag) VALUES
                #(DateTime(CURRENT_TIMESTAMP, 'localtime'), ?, ?)
                #""", (nome, self.tag,))

            #print 'A tag {0} foi cadastrada com sucesso, {1}'.format(self.tag, nome)

            #self.con.commit()
        #except lite.Error, e:

            #if self.con:
                #self.con.rollback()

            #print "Error %s" % e.args[0]
            #sys.exit(1)

        #finally:
            #if self.con:
                #self.con.close()

    def check_tag(self):
        try:
            self.cur.execute("SELECT UserID, Nome FROM Usuario WHERE Tag = ?",
                  (self.tag,))
            user = self.cur.fetchone()
            print 'Olá {0}. Hora da entrada: {1}'.format(user[1],
                 time.strftime("%c"))
            self.cur.execute("UPDATE Usuario SET UltimaEntrada = DateTime(CURRENT_TIMESTAMP, 'localtime') WHERE UserID = {0};".format(user[0]))
            self.con.commit()
            #QtGui.QErrorMessage.showMessage(QtCore.QString('Olá {0}. Hora da entrada: {1}'.format(user[1],
                 #time.strftime("%c"))))
            self.lbl_nome.setText(user[1])
        except lite.Error as e:
            print "Ocorreu um erro: ", e.args[0]
            QtGui.QErrorMessassage.showMessage(QtCore.QString(e.args[0]))
        finally:
            self.con.close()