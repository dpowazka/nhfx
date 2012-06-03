from nhfx.xquery import *

def isempty(node):
    return len(node.value.replace(" ", "").replace("\n","").replace("\r","")) == 0


for level in range(1,73):
    path = "D:/work/AvoiderAndroid/assets/levels/%d.xml" % level
    print "Cleaning %s" % path
    
    xml = read_from(path)
    root = parse(xml)

    tags = ["TintColor", "Scale", "FlipHorizontally", "FlipVertically", "Origin"]

    map(delete, filter(isnamed(*tags),root))


    for text in filter(AND(istext, isempty), root):
        text.delete()
        
    write_to(root.render(), path)



