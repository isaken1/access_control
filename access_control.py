#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import time
import serial


class Access_Control():

    def __init__(self):
        self.con = lite.connect('access_db.db')
        self.port = serial.Serial('/dev/ttyACM0', 9600)
        self.tag = ''
        self.cur = self.con.cursor()

    def read_tag(self):
        try:
            response = self.port.read(15)
            self.tag = str(response.split(':')[1])
            #tag = str(response.split('#')[0])
            print "Tag lida: {0}".format(self.tag)
            self.port.flush()
            return self.tag
        except KeyboardInterrupt:
            return
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
            sys.exit(1)

        finally:
            if self.con:
                self.con.close()

    def insert_data(self):
        try:
            nome = raw_input("Insira o seu nome: \n")

            self.cur.execute("""
                INSERT INTO Usuario (UltimaEntrada, Nome, Tag) VALUES
                (DateTime(CURRENT_TIMESTAMP, 'localtime'), ?, ?)
                """, (nome, self.tag,))

            print 'A tag {0} foi cadastrada com sucesso, {1}'.format(self.tag, nome)

            self.con.commit()
        except lite.Error, e:

            if self.con:
                self.con.rollback()

            print "Error %s" % e.args[0]
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
        except lite.Error as e:
            print "Ocorreu um erro: ", e.args[0]
        finally:
            self.con.close()