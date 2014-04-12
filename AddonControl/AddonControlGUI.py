from PyQt4 import QtCore, QtGui
import aqt

class AddonControlGUI(QtGui.QWidget):
    def __init__(self, control):
        super(AddonControlGUI, self).__init__()
        self.control = control
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AddonControl')

        # main layout
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addStretch(1)

        self.setup_filter_row()
        self.setup_table_row()
        self.setup_buttons_row()

        self.setLayout(self.vbox)

        self.show()

    def setup_filter_row(self):
        filter_field = QtGui.QLineEdit(self)
        filter_button = QtGui.QPushButton('Filter', self)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(filter_field)
        hbox.addWidget(filter_button)

        self.vbox.addLayout(hbox)

    def setup_table_row(self):
        table = QtGui.QTableWidget(self)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(table)

        self.vbox.addLayout(hbox)

    def setup_buttons_row(self):
        install_button = QtGui.QPushButton('Install', self)
        #update_button = QtGui.QPushButton('Update', self)
        remove_button = QtGui.QPushButton('Remove', self)

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(install_button)
        hbox.addWidget(remove_button)

        self.vbox.addLayout(hbox)


