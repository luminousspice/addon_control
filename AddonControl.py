from AddonControl import AddonControl, AnkiwebRepo, dump_data, load_data
from AddonControl import AddonControlGUI

from aqt import mw
from aqt.utils import showInfo, getFile
from aqt.qt import *

from os.path import expanduser

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

# reads file where each line is the exact name of an addon
# installs the first addon it finds with matching name
# TODO ability to specify repository
def install_from_file():
    global control
    fname = getFile(mw, _("Install addons from file"),
            None, filter="*", dir=expanduser('~') )
    f = open(fname, 'r')
    for line in f:
        if line.strip() == "":
            continue
        if not control.ensure_installed(line.strip()):
            showInfo("Could not install " + line)
    showInfo("All addons from file are installed")
    control.load_addons()
    control.save_state()
    

# load AddonControl
# if pickled version exists, load that one
folder = addons_folder()
# TODO store state in Anki profile instead of pickled
persist_path = os.path.join(folder, "AddonControlData.pickle")
if os.path.isfile(persist_path):
    control = load_data(persist_path)
    control.load_addons()
else:
    # default initializer
    control = AddonControl(folder)
    control.repositories.append( AnkiwebRepo() ) # TODO better way to handle repos
    control.update_repos()

# install UI elements
action = QAction("AddonControl", mw)
mw.connect(action, SIGNAL("triggered()"), open_addon_control)
mw.form.menuTools.addAction(action)

action = QAction("Install addons from file", mw)
mw.connect(action, SIGNAL("triggered()"), install_from_file)
mw.form.menuTools.addAction(action)
