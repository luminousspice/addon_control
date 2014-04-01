from AnkiwebAddons import *

# TODO extract and put in correct place
def find_matching_addons(addon_name, addon_list):
    matches = []
    for addon in addon_list:
        if re.search(".*?".join(addon_name), addon.name.lower()):
            matches.append(addon)

    return matches

# naive test
repo = AnkiwebRepo()
repo.update_addon_list()
print "first time done"
repo.update_addon_list() # nothing should print
