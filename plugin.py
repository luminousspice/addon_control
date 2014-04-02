from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

from AddonControl import AddonControl, AnkiwebRepo

def setup_repos(control):
    control.repositories.append( AnkiwebRepo() )

def testFunction():
    st = ""
    for addon in control.all_addons():
        st += addon.name + '\n'

    showInfo(st)

def doInstall():
    addon = control.all_addons()[5]
    print addon.codeNumber
    control.install_addon(addon)
    print "installed"

control = AddonControl()
setup_repos(control)
control.update_repos()

action = QAction("test", mw)
mw.connect(action, SIGNAL("triggered()"), doInstall)
mw.form.menuTools.addAction(action)
