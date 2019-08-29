from pims import Bioformats
import numpy as np
import os
from PIL import Image
from matplotlib import pyplot as plt
from skimage import feature,filters,io
from skimage.morphology import disk
from math import sqrt, pi, cos, sin
from collections import defaultdict

def nd2_read(fileName):
  with Bioformats(fileName) as images:
    images.bundle_axes="tzyxc"
    return images[0]

def full_nd2_read(fileName):
  with Bioformats(fileName) as images:
    images.bundle_axes="zyxc"
    img = np.reshape(images[0],(72,5,)+images[0].shape[1:])
    return img

def cut_full_image(img):
  output = {}
  for time in range(img.shape[0]):
    tmp_img = img[time,:,:]
    COL_THRES = 80000
    HOR_THRES = 90000
    HOR_SHIFT = 30
    LEFT = 48
    RIGHT =15
    DOWN = 70
    c = 0
    band_start = -1
    verticle_lines = []
    while c < tmp_img.shape[1]:
      avg = np.sum(tmp_img[:,c,0])/tmp_img.shape[0]
      if band_start == -1:
        if (avg>COL_THRES):
          band_start = c
      else:
        if (avg<=COL_THRES) or c==tmp_img.shape[1]-1:
          verticle_lines.append((band_start+c)//2)
          band_start = -1
      c+=1
    
    # print(verticle_lines)
    for i in range(len(verticle_lines)):
      verticle_slice = tmp_img[:,verticle_lines[i]-LEFT:verticle_lines[i]+RIGHT]
      r = 0
      band_start = -1
      horizontal_lines = []
      while r < tmp_img.shape[0]:
        avg = np.sum(verticle_slice[r,LEFT-HOR_SHIFT:LEFT,0])/HOR_SHIFT
        if band_start == -1:
          if (avg>HOR_THRES):
            band_start = r
        else:
          if (avg<=HOR_THRES) or r==tmp_img.shape[0]-1:
            horizontal_lines.append((band_start+r)//2)
            band_start = -1
            r+=DOWN-1
        r+=1
      # print(horizontal_lines)
      for j in range(len(horizontal_lines)):
        horizontal_slice = verticle_slice[horizontal_lines[j]:horizontal_lines[j]+DOWN,:]
        key = "{}{}".format(i+1,chr(97+j))
        if key not in output:
          dims = list(img.shape)
          dims[1] = DOWN
          dims[2] = LEFT+RIGHT
          new_array = np.zeros(dims,np.int32)
          if new_array[time].shape[0] != horizontal_slice.shape[0]:
            new_array[time,0:horizontal_slice.shape[0],:] = np.copy(horizontal_slice)
          else:
            new_array[time] = np.copy(horizontal_slice)
          output[key] = new_array
        else:
          if output[key][time].shape[0] != horizontal_slice.shape[0]:
            output[key][time,0:horizontal_slice.shape[0],:] = np.copy(horizontal_slice)
          else:
            output[key][time] = np.copy(horizontal_slice)
  return output

def save_tiff_batch(output,sample_name):
  for key in output:
    img = output[key]
    img = img.astype(np.int32)
    if not os.path.isdir("./result"):
      os.mkdir("./result")
    if not os.path.isdir("./result/{}/".format(sample_name)):
      os.mkdir("./result/{}/".format(sample_name))
    io.imsave("result/{}/{}.tiff".format(sample_name,key),img,'tifffile')
        

def tiff_in_folder(path):
  for (dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        if filename.endswith('.tiff'): 
          yield tif_read(os.sep.join([dirpath, filename]))

def tif_read(fileName):
  return io.imread(fileName,plugin='tifffile')

def sum_z(img):
  new_dim = list(img.shape)
  z_dim = new_dim.pop(1)
  new = np.zeros(new_dim,np.int)
  for z in range(z_dim):
    new[:]+=img[:,z,:]
  return new

def save_tiff(img,fileName):
  io.imsave(fileName,img,'tifffile')


def array_to_png(img):
  dim = img.shape
  new = np.zeros((dim[0],dim[1],dim[2],3))
  for t in range(dim[0]):
    dic_min = np.amin(img[t,:,:,0])
    dic_max = np.amax(img[t,:,:,0])
    pbd_min = np.amin(img[t,:,:,1])
    pbd_max = np.amax(img[t,:,:,1])
    gfp_min = np.amin(img[t,:,:,2])
    gfp_max = np.amax(img[t,:,:,2])
    for y in range(dim[1]):
      for x in range(dim[2]):
        new[t][y][x][0]=(255*(img[t,y,x,0]-dic_min)/(dic_max-dic_min))
        new[t][y][x][1]=(255*(img[t,y,x,2]-pbd_min)/(pbd_max-pbd_min))
        new[t][y][x][2]=(255*(img[t,y,x,1]-gfp_min)/(gfp_max-gfp_min))
  new = new.astype(np.uint8)
  return new

def one_to_png(img):
  dim = img.shape
  new = np.zeros((dim[0],dim[1],dim[2]))
  for t in range(dim[0]):
    min = np.amin(img[t,:,:])
    max = np.amax(img[t,:,:])
    for y in range(dim[1]):
      for x in range(dim[2]):
        new[t][y][x]=(255*(img[t,y,x]-min)/(max-min))
  new = new.astype(np.uint8)
  return new

def save_png(masks,directory):
  for i in range(len(masks)):
    io.imsave(os.path.join(directory,"{}.png".format(i)),masks[i])


def circle_detection(img, sigma = 1, rmin = 9, rmax = 15, steps = 100, threshold = 0.4, binary_input = False):
  assert img.ndim == 2
  if not binary_input:
    canny_result = canny(img,sigma)
  else:
    canny_result = []
    for r in range(img.shape[0]):
      for c in range(img.shape[1]):
        if img[r,c]:
          canny_result.append((r,c))

  points = []
  for r in range(rmin, rmax + 1):
    for t in range(steps):
      points.append((r, int(r * cos(2 * pi * t / steps)), int(r * sin(2 * pi * t / steps))))

  acc = defaultdict(int)
  for x, y in canny_result:
      for r, dx, dy in points:
          a = x - dx
          b = y - dy
          acc[(a, b, r)] += 1

  circles = []
  for k, v in sorted(acc.items(), key=lambda i: -i[1]):
      x, y, r = k
      if v / steps >= threshold and all((x - xc) ** 2 + (y - yc) ** 2 > rc ** 2 for _, xc, yc, rc in circles):
          # print(v / steps, x, y, r)
          circles.append((v / steps, x, y, r))
  # print("-------")
  return circles


def canny(img,sigma):
  assert img.ndim == 2
  img = img/np.max(img)
  edge = feature.canny(img,sigma=sigma)
  # plt.imshow(edge,cmap=plt.cm.gray)
  # plt.show()
  canny_result = []
  for r in range(edge.shape[0]):
    for c in range(edge.shape[1]):
      if edge[r,c]:
        canny_result.append((r,c))
  return canny_result

def hotspots(image,COUNT_THRES = 12):
  assert image.ndim == 3
  thres=0.4
  time_steps = image.shape[0]
  summed_edge = np.zeros(image.shape[1:3])
  for i in range(time_steps):
    img = image[i,:,:]
    img = img/np.max(img)
    img = (img * 255).astype(np.uint8)
    med = filters.median(img, disk(3))
    med = med/np.max(med)
    edge = feature.canny(med,sigma=1)
    summed_edge += edge
  summed_edge = summed_edge>time_steps/6
  # plt.imshow(summed_edge)
  # plt.show()
  hot = circle_detection(summed_edge,threshold=thres,binary_input=True)
  while len(hot) == 0 and thres>0.1:
    hot = circle_detection(summed_edge,threshold=thres,binary_input=True)
    thres-=0.1
  if len(hot) == 0:
    raise ValueError('impropriate input')
  return sorted(hot,key = lambda x:-x[0])[0]