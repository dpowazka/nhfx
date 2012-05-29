from nhfx import *

 
#The task here is to replace all asset_names and texture filenams 
#with shorten paths D:\work\AvoiderAndroid\gleed2d\player_2 -> player_2
root = parse(open("69.xml").read())
    
ContentRootFolder = filter(parent_is(named("ContentRootFolder")), root)[0]
ContentRootFolder.value = "D:\\work\\AvoiderAndroid\\gleed2d\\"
    
for asset in filter(AND(parent_is(named("asset_name")), texts), root):
    asset.value = asset.value.split("\\")[-1]
    
    
for texture in filter(AND(parent_is(named("texture_filename")), texts), root):
    texture.value = texture.value.split("\\")[-1]
    
print root.render() 