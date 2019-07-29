# from generate_mask import *
from image_process import *
from generate_plot_data import *
img = sum_z(nd2_read("../nd2/122718 y3469tr_001_xy04_crop_3a.nd2"))
dic = img[:,:,:,0]
gfp = img[:,:,:,1]
vals = with_out_mask(dic,gfp,0)
