from difflib import * 

fileN = raw_input("please enter the name of your textfile: ")
#wfile = open('/usr/share/dict/words')
wfile= open(fileN)
words = [ line.strip() for line in wfile ]

searchWord=raw_input("What word do you want to search?: ")
print get_close_matches(searchWord, words, 5)