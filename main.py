#!/usr/bin/python
# -*- coding: utf-8 -*-

from gui_ac import Ac_dialog
from PyQt4 import QtGui


def main():
    import sys
    app = QtGui.QApplication(sys.argv)

    ac = Ac_dialog()
    ac.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()