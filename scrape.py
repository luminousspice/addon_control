import urllib2
import re
from BeautifulSoup import BeautifulSoup
import json

class addonD: 
    def __init__(self, name1, codeNumber1):
        self.name=name1
        self.codeNumber=codeNumber1

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
    thisOne = addonD(addon_name, addon_id)
    addons.append(thisOne)


# find names that match
search_name = raw_input("Name?: ").lower()
matches = []
for addon in addons:
    if re.search(".*?".join(search_name), addon.name.lower()):
        matches.append(addon)

print [ (addon.name, addon.codeNumber) for addon in matches]
