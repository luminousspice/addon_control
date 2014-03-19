import urllib2
import re
from BeautifulSoup import BeautifulSoup
import json

class Addon:
    def __init__(self, name, codeNumber):
        self.name=name
        self.codeNumber=codeNumber

def scrape_addon_list():
    addons = []
    # get the web page
    soup = BeautifulSoup(urllib2.urlopen('https://ankiweb.net/shared/addons/').read())

    # get the javascript data
    jdata = str(soup.find('div', {'id': 'content'}).findAll('script')[1])
    jdata = jdata[24:-29] # gross!! TODO seriously?
    
    # make list of addons
    addons = []
    for addon in json.loads(jdata):
        addon_id = addon[0]
        addon_name = addon[1]
        thisOne = Addon(addon_name, addon_id)
        addons.append(thisOne)

    return addons

def find_matching_addons(addon_name, addon_list):
    matches = []
    for addon in addon_list:
        if re.search(".*?".join(addon_name), addon.name.lower()):
            matches.append(addon)

    return matches

print [ (addon.name, addon.codeNumber) for addon in find_matching_addons(raw_input("Input:"),scrape_addon_list()) ]
