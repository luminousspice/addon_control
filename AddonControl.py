from AddonControl import AddonControl, AnkiwebRepo, dump_data, load_data

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *

def addons_folder():
    dir = mw.pm.addonFolder()
    if isWin:
        dir = dir.encode(sys.getfilesystemencoding())
    path = os.path.join(dir, "AddonControlAddons")
    # if the directory doesn't exist make it
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# example install code using fuzzy search
def install_occlusion():
    addon = control.fuzzy_search_addons("Image Occlusion")[0]
    control.install_addon(addon)
    control.load_addons()
    control.save_state()

def command_line_addon_control():
    print "What would you like to do?"
    print "1) Update addon list"
    print "2) Print entire addon list"
    print "3) Search for an addon to install"
    print "4) Remove an addon"
    opt = raw_input("Enter the option number: ")
    opt = int(opt)
    if opt == 1:
        control.update_repos()
        control.save_state()
    elif opt == 2:
        for addon in control.all_addons():
            print "%s : %s" % (addon.name,
                "Installed" if addon.installed else "Not Installed")
    elif opt == 3:
        name = raw_input("Name: ")
        matches = control.fuzzy_search_addons(name)
        for i, addon in enumerate(matches):
            print "%i) %s" % (i, addon.name)

        install = raw_input("Number to install (-1 for none): ")
        install = int(install)
        if install == -1:
            return
        else:
            control.install_addon(matches[install])
            control.load_addons()
            control.save_state()
    elif opt == 4:
       installed = control.installed_addons()
       for i, addon in enumerate(installed):
           print "%i) %s" % (i, addon.name)

       remove = raw_input("Addon to remove (-1 for none): ")
       remove = int(remove)
       if remove == -1:
           return
       else:
           control.remove_addon(installed[remove])
           control.save_state()

def open_addon_control():
    pass

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
mw.connect(action, SIGNAL("triggered()"), command_line_addon_control)
mw.form.menuTools.addAction(action)

action2 = QAction("Install Image Occlusion", mw)
mw.connect(action2, SIGNAL("triggered()"), install_occlusion)
mw.form.menuTools.addAction(action2)
