from nhfx.xquery import *


root = parse(open("69.xml").read())
map(delete, filter(isnamed("Item"), root))
print filter(isnamed("Item"), root)

    

