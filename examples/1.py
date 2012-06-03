from nhfx.xquery import *

 
#The task here is to replace all asset_names and texture filenams 
#with shorten paths D:\work\AvoiderAndroid\gleed2d\player_2 -> player_2
path = "69.xml"
root = parse(read_from(path))
    
ContentRootFolder = filter(parent_is(isnamed("ContentRootFolder")), root)[0]
ContentRootFolder.value = "D:\\work\\AvoiderAndroid\\gleed2d\\"
    
for asset in filter(AND(parent_is(isnamed("asset_name")), istext), root):
    asset.value = asset.value.split("\\")[-1]
    
    
for texture in filter(AND(parent_is(isnamed("texture_filename")), istext), root):
    texture.value = texture.value.split("\\")[-1]
    
write_to(root.render(), path)