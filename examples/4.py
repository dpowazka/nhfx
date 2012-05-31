from nhfx.xquery import *

#Task is to remove some not used tags and empty text nodes.

def isempty(node):
    return len(node.value.replace(" ", "").replace("\n","").replace("\r","")) == 0

xml = read_from("69.xml")
root = parse(xml)

tags = ["TintColor", "Scale", "FlipHorizontally", "FlipVertically", "Origin"]

map(delete, filter(isnamed(*tags),root))


for text in filter(AND(istext, isempty), root):
    text.delete()
    
print root.render()