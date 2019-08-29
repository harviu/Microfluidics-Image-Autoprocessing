from generate_values import *
from image_process import *

img = tif_read("./result/_122718 y3469_001_xy01/2b.tiff")
print(hotspots(img[:,:,:,1],10))