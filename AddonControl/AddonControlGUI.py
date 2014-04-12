from PyQt4 import QtCore, QtGui
import aqt

class AddonControlGUI(QtGui.QWidget):
    def __init__(self, control):
        super(AddonControlGUI, self).__init__()
        self.control = control
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AddonControl')
        self.show()

