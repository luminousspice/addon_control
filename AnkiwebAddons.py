# import stuff needed to do stuff
# thanks past david
import urllib2
import re
from BeautifulSoup import BeautifulSoup
import json
from AddonControl import Addon, Repository

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


class AnkiwebRepo(Repository):
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
                print "ADDING NEW ELEMENT" # for naive test
                thisOne = AnkiwebAddon(addon_name, addon_id)
                self.addons.append(thisOne)
