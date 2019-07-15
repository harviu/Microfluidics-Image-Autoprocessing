from nd2reader import ND2Reader
import numpy as np
from skimage import io
import os

def nd2_read(fileName):
  """
  Channel Order: DIC GFP PBD
  """
  with ND2Reader(fileName) as images:
    images.bundle_axes="tzyxc"
    dim = images.sizes
    flip = np.zeros((dim["t"],dim["z"],dim["y"],dim["x"],dim["c"]),np.uint32)
    flip[:,:,:,:,0] = images[0][:,:,:,:,0]
    flip[:,:,:,:,1] = images[0][:,:,:,:,2]
    flip[:,:,:,:,2] = images[0][:,:,:,:,1]
    return flip

def tif_read(fileName):
  return io.imread(fileName,plugin='tifffile')

def sum_z(img):
  new_dim = list(img.shape)
  z_dim = new_dim.pop(1)
  new = np.zeros(new_dim,np.uint32)
  for z in range(z_dim):
    new[:]+=img[:,z,:]
  return new


def array_to_png(img):
  dim = img.shape
  new = np.zeros((dim[0],dim[1],dim[2],3))
  for t in range(dim[0]):
    dic_min = np.amin(img[t,:,:,0])
    dic_max = np.amax(img[t,:,:,0])
    gfp_min = np.amin(img[t,:,:,1])
    gfp_max = np.amax(img[t,:,:,1])
    pbd_min = np.amin(img[t,:,:,2])
    pbd_max = np.amax(img[t,:,:,2])
    for y in range(dim[1]):
      for x in range(dim[2]):
        new[t][y][x][0]=(255*(img[t,y,x,0]-dic_min)/(dic_max-dic_min))
        new[t][y][x][1]=(255*(img[t,y,x,1]-gfp_min)/(gfp_max-gfp_min))
        new[t][y][x][2]=(255*(img[t,y,x,2]-pbd_min)/(pbd_max-pbd_min))
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