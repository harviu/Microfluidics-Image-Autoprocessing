from generate_mask import *
from image_process import *
img = sum_z(nd2_read("122718 y3469tr_001_xy04_crop_3a.nd2"))
png = array_to_png(img)
save_png(get_mask(png),"result")
