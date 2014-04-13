import re
import os
import pickle
import aqt
from anki.utils import  isWin, isMac
from abc import ABCMeta, abstractmethod

"""
This class represents an installable addon. Addons must keep track of whether or
not they are installed and where they are installed to (if they are)

They also must know how to install themselves to some directory, remove
themselves, and update themselves should a newer version become available
(dealing with versions is a subclass responsibility as different repositories
may need to handle this differently
"""
class Addon(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.installed = False
        self.installed_path = ""
        self.name = ""

    @abstractmethod
    def install(self, path):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def load(self):
        pass

"""
This class represents a collection of addons somewhere we would like to be able
to install plugins from

It will maintain a list of plugins available from the repository. It must be
able to update this list without on demand
"""
class Repository(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.addons = []

    @abstractmethod
    def update_addon_list(self):
        pass

"""
This class is the addon controller, any external interactions with addon system
should be done by interacting with AddonControl
"""
class AddonControl(object):
    def __init__(self, addons_folder):
        self.repositories = []
        self.addons_folder = addons_folder

    def save_state(self):
        dump_data(self)

    def update_repos(self):
        for repo in self.repositories:
            repo.update_addon_list()

    def load_addons(self):
        for addon in self.installed_addons():
            addon.load()

    def install_addon(self, addon):
        # these paths don't reall have to be too sane
        nicer_name = "".join(x for x in addon.name if x.isalnum())
        addon_path = os.path.join(self.addons_folder, nicer_name)
        # if the directory doesn't exist make it
        if not os.path.exists(addon_path):
            os.makedirs(addon_path)
        addon.install(addon_path)

    def remove_addon(self, addon):
        addon.remove()

    def update_addon(self, addon):
        addon.update()

    def all_addons(self):
        all_addons = []
        for repo in self.repositories:
            for addon in repo.addons:
                all_addons.append(addon)
        return all_addons

    def installed_addons(self):
        installed_addons = []
        for repo in self.repositories:
            for addon in repo.addons:
                if addon.installed == True:
                    installed_addons.append(addon)
        return installed_addons

    def fuzzy_search_addons(self, search_name):
        matches = []
        for addon in self.all_addons():
            if re.search(".*?".join(search_name.lower()), addon.name.lower()):
                matches.append(addon)
        return matches

    # makes sure addons with a particular name are installed
    # useful for loading addons from file
    def ensure_installed(self, addon_name):
        for addon in self.all_addons():
            if addon.name == addon_name:
                if not addon.installed:
                    self.install_addon(addon)
                return True # success
        return False
    
    

# saving state
# dumps data controller's directory
def dump_data(controller):
    with open(os.path.join(controller.addons_folder, "AddonControlData.pickle"), 'wb') as f:
        pickle.dump(controller, f)

def load_data(from_where):
    with open(from_where, 'rb') as f:
        control = pickle.load(f)
        return control
