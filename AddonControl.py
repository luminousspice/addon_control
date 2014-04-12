from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from AddonControl import AddonControl, AnkiwebRepo

from PyQt4 import QtCore, QtGui

def install_something():
    addon = control.fuzzy_search_addons("Image Occlusion")[0]
    control.install_addon(addon)
    control.load_addons()

# load AddonControl data
control = AddonControl()
control.repositories.append( AnkiwebRepo() )
control.update_repos()

# install UI elements
action = QAction("AddonControl", mw)
mw.connect(action, SIGNAL("triggered()"),install_something)
mw.form.menuTools.addAction(action)
