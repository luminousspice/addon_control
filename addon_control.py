# import stuff to make gui
from aqt import mw
from aqt.qt import *

# import stuff needed to do stuff
import urllib2
import re
from BeautifulSoup import BeautifulSoup
import json

# define abstract classes
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
        self.installedPath = ""

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


# define ankiweb specific addon stuff
class AnkiwebAddon(Addon):
    def __init__(self, name, codeNumber):
        self.name=name
        self.codeNumber=codeNumber

    def install(self, path):
        pass # this will probably want to call the thing already in anki to install addons
    
    def remove(self):
        pass # will just delete the directory we installed to

    # TODO don't be stupid about this
    def update(self):
        self.remove()
        self.install()


class AnkiwebRepo:
    """
    Scrapes the addon list from Ankiweb and updates the repos plugin list
    """
    def update_addon_list(self):
        # get the web page
        soup = BeautifulSoup(urllib2.urlopen('https://ankiweb.net/shared/addons/').read())

        # get the javascript data
        jdata = str(soup.find('div', {'id': 'content'}).findAll('script')[1])
        jdata = jdata[24:-29] # gross!! TODO seriously?
        
        # update list
        for addon in json.loads(jdata):
            addon_id = addon[0]
            addon_name = addon[1]
            # check if addon already in list
            matches = [ad for ad in self.addons if ad.name == addon_name and
                    ad.codeNumber == addon_id ]
            if len(matches) != 0:
                # we already have it in the list, TODO update version or
                # something
                pass
            else:
                thisOne = AnkiwebAddon(addon_name, addon_id)
                self.addons.append(thisOne)


# TODO extract and put in correct place
def find_matching_addons(addon_name, addon_list):
    matches = []
    for addon in addon_list:
        if re.search(".*?".join(addon_name), addon.name.lower()):
            matches.append(addon)

    return matches
