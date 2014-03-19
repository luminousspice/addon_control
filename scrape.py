import urllib2
import re
from BeautifulSoup import BeautifulSoup
import json
from addonD import addonD
from difflib import * 

class FuzzyMatcher():

    def __init__(self):
        self.pattern = ''

    def setPattern(self, pattern):
        self.pattern = '.*?'.join(map(re.escape, list(pattern)))

    def score(self, string):
        match = re.search(self.pattern, string)
        if match is None:
            return 0
        else:
            return 100.0 / ((1 + match.start()) * (match.end() - match.start() + 1))

# get the web page
soup = BeautifulSoup(urllib2.urlopen('https://ankiweb.net/shared/addons/').read())

# get the javascript data
jdata = str(soup.find('div', {'id': 'content'}).findAll('script')[1])
jdata = jdata[24:-29] # gross!! TODO seriously?


addons = []
for addon in json.loads(jdata):
    addon_id = addon[0]
    addon_name = addon[1]
    thisOne = addonD(addon_name, addon_id)
    addons.append(thisOne)


search_name = raw_input("Name?: ")
fuzz = FuzzyMatcher()
fuzz.setPattern(search_name)

matches = [s for s in [addon.name for addon in addons] if re.search(".*?".join(search_name), s)]
print matches

for addon in addons:
    print addon.name
    print fuzz.score(addon.name)
