# import stuff needed to do stuff
# thanks past david
import urllib2
from BeautifulSoup import BeautifulSoup
import json
from AddonControl import Addon, Repository

# ankiqt stuff
import aqt
from aqt.downloader import download
from aqt.qt import showInfo

# define ankiweb specific addon stuff
class AnkiwebAddon(Addon):
    def __init__(self, name, codeNumber):
        self.name=name
        self.codeNumber=codeNumber

    # TODO be more clever about paths
    # TODO write custom handler so we can maintain a directory per addon
    def install(self, path):
        ret = download(aqt.mw, str(self.codeNumber))
        if not ret:
            return # TODO error
        data, fname = ret
        aqt.mw.progress.finish()
        aqt.mw.addonManager.install(data, fname)
        showInfo(_("Download successful. Please restart Anki."))

    
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
                thisOne = AnkiwebAddon(addon_name, addon_id)
                self.addons.append(thisOne)
