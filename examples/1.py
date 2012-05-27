from nhfx import *

 
root = parse(open("69.xml").read())
    
ContentRootFolder = one(root, parent(named("ContentRootFolder")))
ContentRootFolder.value = "D:\\work\\AvoiderAndroid\\gleed2d\\"
    
has_asset_name = lambda e: len(e.filter(named("asset_name")))==1
items = root.filter(AND(named("Item"), has_asset_name))
for item in items:
    asset_name = one(item, AND(texts, parent(named("asset_name"))))
    asset_name.value = asset_name.value.split("\\")[-1]
        
    texture_filename = one(item, AND(texts, parent(named("texture_filename"))))
    texture_filename.value = texture_filename.value.split("\\")[-1]
        
write_to(root.render(), "69b.xml")