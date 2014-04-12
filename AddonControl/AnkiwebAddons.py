from AddonControl import Addon, Repository
import urllib2
from BeautifulSoup import BeautifulSoup
import json
from zipfile import ZipFile
import sys
import shutil
import os
from cStringIO import StringIO

# ankiqt stuff
import aqt
from aqt.downloader import download
from aqt.utils import showInfo

# define ankiweb specific addon stuff
class AnkiwebAddon(Addon):
    def __init__(self, name, codeNumber):
        super(AnkiwebAddon,self).__init__()
        self.name=name
        self.codeNumber=codeNumber

    # TODO refactor
    def install(self, path):
        ret = download(aqt.mw, str(self.codeNumber))
        if not ret:
            return # TODO error
        data, fname = ret
        aqt.mw.progress.finish()

        if fname.endswith(".py"):
            # .py files go directly into the addon folder
            path = os.path.join(path, fname)
            try:
                open(path, "w").write(data)
            except:
                print "Error somewhere"
            showInfo(_("Download successful. Please restart Anki."))
            self.installed = True
            self.installed_path = os.path.dirname(path)
            return

        # .zip file
        z = ZipFile(StringIO(data))
        base = path
        for n in z.namelist():
            if n.endswith("/"):
                # folder; ignore
                continue
            # write
            z.extract(n, base)

        showInfo(_("Download successful. Please restart Anki."))
        self.installed = True
        self.installed_path = path

    def remove(self):
        if self.installed:
            shutil.rmtree(self.installed_path)
            self.installed = False
        # TODO what else can plugins change that we can track?

    # TODO don't be stupid about this
    def update(self):
        self.remove()
        self.install()

    def files(self):
        return [f for f in os.listdir(self.installed_path) if f.endswith(".py")]

    def load(self):
        # we don't care about the addons menu, we have our own
        print "Loading ", self.name
        sys.path.insert(0, self.installed_path)
        for f in self.files():
            try:
                __import__(f.replace(".py",""))
            except:
                print "import failed"

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
