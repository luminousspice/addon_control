import urllib2
from BeautifulSoup import BeautifulSoup
import json

# get the web page
soup = BeautifulSoup(urllib2.urlopen('https://ankiweb.net/shared/addons/').read())

# get the javascript data
jdata = str(soup.find('div', {'id': 'content'}).findAll('script')[1])
jdata = jdata[24:-29] # gross!! TODO seriously?

for addon in json.loads(jdata):
    addon_id = addon[0]
    addon_name = addon[1]
