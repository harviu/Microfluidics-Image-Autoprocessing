from model_yeast import *
from skimage.transform import rescale, resize, downscale_local_mean

def get_mask(png):
  model = unet()
  model.load_weights("unet_yeast.hdf5")
  results = []
  for t in range(len(png)):
    test = png[t]/255
    test = resize(test,(256,256))
    test = test[None,:]
    result = model.predict(test,verbose=0)
    res = resize(result[0], (100, 124), anti_aliasing=True)
    res *= 255
    res = res.astype(np.uint8)
    results.append(res)
  return results
