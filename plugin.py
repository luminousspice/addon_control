from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from AddonControl import AddonControl, AnkiwebRepo

from PyQt4 import QtCore, QtGui

class AddonControlWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self, mw)
        self.init_ui()

    def init_ui(self):
        okButton = QtGui.QPushButton("OK")
        cancelButton = QtGui.QPushButton("Cancel")

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()


def triggerAddonControl():
    AddonControlWindow()

# load AddonControl data
control = AddonControl()
control.repositories.append( AnkiwebRepo() )
control.update_repos()

# install UI elements
action = QAction("AddonControl", mw)
mw.connect(action, SIGNAL("triggered()"), triggerAddonControl)
mw.form.menuTools.addAction(action)
