from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from AddonControl import AddonControl, AnkiwebRepo, dump_data, load_data

from PyQt4 import QtCore, QtGui

def install_occlusion():
    addon = control.fuzzy_search_addons("Image Occlusion")[0]
    control.install_addon(addon)
    control.load_addons()

def do_the_thing():
    pass

def addons_folder():
    dir = mw.pm.addonFolder()
    if isWin:
        dir = dir.encode(sys.getfilesystemencoding())
    path = os.path.join(dir, "AddonControlAddons")
    # if the directory doesn't exist make it
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def save_state():
    dump_data(control)

# load AddonControl data
# if pickled version exists, load that one
folder = addons_folder()

persist_path = os.path.join(folder, "AddonControlData.pickle")
if os.path.isfile(persist_path):
    control = load_data(persist_path)
    control.load_addons()
else:
    # default initializer
    control = AddonControl(folder)
    control.repositories.append( AnkiwebRepo() )
    control.update_repos()

# install UI elements
action = QAction("AddonControl", mw)
mw.connect(action, SIGNAL("triggered()"),do_the_thing)
mw.form.menuTools.addAction(action)

action2 = QAction("Install Image Occlusion", mw)
mw.connect(action2, SIGNAL("triggered()"), install_occlusion)
mw.form.menuTools.addAction(action2)

action3 = QAction("Save PackageControl State", mw)
mw.connect(action3, SIGNAL("triggered()"), save_state)
mw.form.menuTools.addAction(action3)
