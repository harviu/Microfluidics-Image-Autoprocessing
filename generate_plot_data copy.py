import numpy as np
import math
import os
from matplotlib import pyplot as plt
from skimage import io
import random
from image_process import sum_z,tif_read

def cropped_to_vals(img):
  RAD = 8
  dic = img[:,:,:,0]
  gfp = img[:,:,:,2]
  vals = []
  time=0
  x_length = dic.shape[2]
  y_length = dic.shape[1]
  gfp_max = []
  while(time<dic.shape[0]):
    #find max gfp
    idr, idc = np.unravel_index(np.argmax(gfp[time]),gfp[time].shape)
    gfp_max.append((idr,idc))
    time += 1
  # print(gfp_max)

  cluster = []
  for k in gfp_max:
    r,c = k
    for clu in cluster:
      mean_r = clu['r']
      mean_c = clu['c']
      if abs(mean_r-r)<=RAD and abs(mean_c-c)<=RAD:
        mean_r = (mean_r * clu['count'] + r)
        mean_c = (mean_c * clu['count'] + c)
        clu['count'] += 1
        mean_r /= clu['count']
        mean_c /= clu['count']
        break
    else:
      new = {}
      new['r'] = r
      new['c'] = c
      new['count'] = 1
      cluster.append(new)
  
  main_clu = cluster[0]
  for clu in cluster:
    if clu['count'] > main_clu['count']:
      main_clu = clu
  print(main_clu)
  return vals

def with_out_mask(dic,gfp,mode):
  """
  Take summed DIC and GFP as input, output the values of maxium local intensity
  mode:
  0: simple_max
  1: ave_max
  2: local_max
  3: local_ave_max
  """

  vals = []
  vals_max = []
  time=0
  x_length = dic.shape[2]
  y_length = dic.shape[1]
  gfp_max = []
  dic_max = []

  while(time<dic.shape[0]):
    #find chamber interesting area
    CHAMBER_THRESHOLD = 100000
    HORIZONTAL_THRESHOLD = 80000
    width = 35
    max_area = 0
    max_dic_x = -1
    for i in range(x_length):
      temp_area = sum(dic[time,:,i]>CHAMBER_THRESHOLD)
      if temp_area>max_area:
        max_area = temp_area
        max_dic_x=i

    # start = max(max_dic_x-(width-5),0)
    # end = min(max_dic_x+5,dic.shape[2])
    # chamber_area = gfp[time,:,start:end]

    max_tmp = 0
    max_dic_y = -1
    for j in range(y_length):
      tmp = sum(dic[time,j,:]>HORIZONTAL_THRESHOLD)
      if max_tmp<tmp:
        max_tmp = tmp
        max_dic_y = j

    dic_max.append((max_dic_y,max_dic_x))
    #find max intensity columns 
    # for i in range(x_length):
    #   c_max = max(gfp[time,:,i])
    #   print(c_max)

    #find max gfp
    idr, idc = np.unravel_index(np.argmax(gfp[time]),gfp[time].shape)
    idr = idr - max_dic_y
    idc = idc - max_dic_x
    gfp_max.append((idr,idc))

    #find max in background
    # aoi = gfp[time,:,max_gfp_x-20:max_gfp_x+20]
    # tmp = []
    # for ele in aoi.flatten():
    #   if ele >30000:
    #     tmp.append(ele)
    # aoi = tmp
    # hist = np.histogram(aoi,30)
    # nums = hist[0][np.argmax(hist[0]):]
    # d1 = []
    # d2 = []
    # for i in range(len(nums)-1):
    #   d1.append(nums[i]-nums[i+1])
    # for i in range(len(d1)-1):
    #   d2.append(d1[i]-d1[i+1])
    # max_d2 = np.argmax(d2)
    # max_back = (hist[1][max_d2+1]+hist[1][max_d2+2])/2

    #modes
    # if mode == 0:
    #   vals.append(float(gfp[time,max_gfp_y,max_gfp_x]))
    # elif mode == 1:
    #   vals.append(get3x3Ave(gfp[time],max_gfp_y,max_gfp_x))
    # elif mode == 2:
    #   vals.append(gfp[time,max_gfp_y,max_gfp_x]-max_back)
    # else:
    #   vals.append(get3x3Ave(gfp[time],max_gfp_y,max_gfp_x)-max_back)

    time += 1
  # max_r = max_c=-1000
  # min_r = min_c=1000
  # for k in gfp_max:
  #   r,c = k
  #   max_r = r if r>max_r else max_r
  #   max_c = c if c>max_c else max_c
  #   min_r = r if r<min_r else min_r
  #   min_c = c if c<min_c else min_c
    
  # m = np.zeros((max_r-min_r+1,max_c-min_c+1))
  # for k in gfp_max:
  #   r,c = k
  #   m[r-min_r,c-min_c] = 1
  # plt.imshow(m)
  # plt.show()
  cluster = []
  for k in gfp_max:
    r,c = k
    for clu in cluster:
      mean_r = clu['r']
      mean_c = clu['c']
      if mean_r-r<=5 and mean_c-c<=5:
        mean_r = (mean_r * clu['count'] + r)
        mean_c = (mean_c * clu['count'] + c)
        clu['count'] += 1
        mean_r /= clu['count']
        mean_c /= clu['count']
        break
    else:
      new = {}
      new['r'] = r
      new['c'] = c
      new['count'] = 1
      cluster.append(new)
  print(cluster)
  main_clu = cluster[0]
  for clu in cluster:
    if clu['count'] > main_clu['count']:
      main_clu = clu
  time = 0
  while(time<dic.shape[0]):
    cood_r,cood_c = dic_max[time]
    r = main_clu['r'] + cood_r
    c = main_clu['c'] + cood_c
    # print(time)
    value = int(np.max(gfp[time,r-5:r+5,c-6:c+6]))
    vals.append(value)
    time+=1
  return vals
  

def get5x5Ave(data,y,x):
  sum = 0
  for i in range(-2,3):
    for j in range(-2,3):
      sum += data[y+i,x+j]
  sum /= 5*5
  return sum

def get3x3Ave(data,y,x):
  sum = 0
  for i in range(-1,2):
    for j in range(-1,2):
      sum += data[y+i,x+j]
  sum /= 3*3
  return sum

  