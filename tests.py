from AddonControl import *

# naive test
repo = AnkiwebRepo()
repo.update_addon_list()
print "first time done"
repo.update_addon_list() # nothing should print
