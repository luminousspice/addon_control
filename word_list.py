wfile = open('/usr/share/dict/words')
words = [ line.strip() for line in wfile ]
print words
