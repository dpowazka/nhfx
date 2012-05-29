from nhfx import *


root = parse(open("69.xml").read())
map(delete, filter(named("Item"), root))
print filter(named("Item"), root)

    

