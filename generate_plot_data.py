import numpy as np
import math
import os
from matplotlib import pyplot as plt
from skimage import io
import random
from image_process import sum_z,tif_read

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

  while(time<dic.shape[0]):
    #find chamber interesting area
    CHAMBER_THRESHOLD = 100000
    width = 20
    max_area = 0
    max_dic_x = -1
    for i in range(x_length-6):
      temp_area = dic[time,:,i:i+5]
      if sum(sum(temp_area>CHAMBER_THRESHOLD))>max_area:
        max_area = sum(sum(temp_area>CHAMBER_THRESHOLD))
        max_dic_x=i+5
    start = max(max_dic_x-width,0)
    end = min(max_dic_x,dic.shape[2])
    chamber_area = gfp[time,:,start:end]
    # print(max_dic_x)

    #find max gfp
    max_gfp = np.argmax(chamber_area)
    max_gfp_x = max_gfp%width+max_dic_x-width
    max_gfp_y = math.floor(max_gfp/width)

    #find max in background
    aoi = gfp[time,:,max_gfp_x-20:max_gfp_x+20]
    tmp = []
    for ele in aoi.flatten():
      if ele >30000:
        tmp.append(ele)
    aoi = tmp
    hist = np.histogram(aoi,30)
    nums = hist[0][np.argmax(hist[0]):]
    d1 = []
    d2 = []
    for i in range(len(nums)-1):
      d1.append(nums[i]-nums[i+1])
    for i in range(len(d1)-1):
      d2.append(d1[i]-d1[i+1])
    max_d2 = np.argmax(d2)
    max_back = (hist[1][max_d2+1]+hist[1][max_d2+2])/2

    #modes
    if mode == 0:
      vals.append(float(gfp[time,max_gfp_y,max_gfp_x]))
    elif mode == 1:
      vals.append(get3x3Ave(gfp[time],max_gfp_y,max_gfp_x))
    elif mode == 2:
      vals.append(gfp[time,max_gfp_y,max_gfp_x]-max_back)
    else:
      vals.append(get3x3Ave(gfp[time],max_gfp_y,max_gfp_x)-max_back)
    time += 1
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

  