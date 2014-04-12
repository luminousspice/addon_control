from AddonControl import AddonControl, AnkiwebRepo, dump_data, load_data
from AddonControl import AddonControlGUI

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

control = None
__window = None

def addons_folder():
    dir = mw.pm.addonFolder()
    if isWin:
        dir = dir.encode(sys.getfilesystemencoding())
    path = os.path.join(dir, "AddonControlAddons")
    # if the directory doesn't exist make it
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def open_addon_control():
    global control
    global __window
    __window = AddonControlGUI(control)

# load AddonControl
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
mw.connect(action, SIGNAL("triggered()"), open_addon_control)
mw.form.menuTools.addAction(action)
