import re
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

    @abstractmethod
    def install(self, path):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def update(self):
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
    def __init__(self):
        self.repositories = []
        self.addon_path = "" # TODO huh

    def update_repos(self):
        for repo in self.repositories:
            repo.update_addon_list()

    def install_addon(self, addon):
        # TODO create better path
        addon.install(self.addon_path)

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

    # TODO probably wrong
    def installed_addons(self):
        return [addon for addon in [repo.addons for repo in self.repositories] if addon.install == True ]

    def fuzzy_search_addons(self, search_name):
        matches = []
        for addon in self.all_addons():
            if re.search(".*?".join(search_name), addon.name.lower()):
                matches.append(addon)
        return matches
