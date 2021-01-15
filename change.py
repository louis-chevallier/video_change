

import numpy as np
import scipy, os
import PIL, cv2, glob
import matplotlib.pyplot as plt
import tqdm
import logging

folder = '/media/MPC/data/ftp/FTP/novodia/SmartCam_HD_Outdoor_C4D6553E360E/snap'
files = glob.glob(folder + '/*.jpg')
K=10
kernel = np.ones((K,K),np.float32)/K/K

kk = np.ones((3, 3), np.uint8)

fontScale = 1
font  = cv2.FONT_HERSHEY_SIMPLEX
color = (0, 255, 0)
thickness = 2

print(len(files))

files = sorted(files)

dct = {}

def desc(image) :
    #print("reading ", image)

    if image in dct :
        return dct[image]

    
    im = cv2.imread(image)
    imlp = cv2.filter2D(im,-1,kernel)
    imlp[0:100, 0:300,:] = 0
    im[0:100, 0:300,:] = 0    
    imlp = imlp.astype(float) / 255
    dct[image] = imlp
    if len(dct) > 100 :
        dct.clear()
    return imlp #(im.astype(float)/255).copy()

i1 = desc(files[0])
H,W,_ = i1.shape
red = np.ones((H,W,3)).astype(float)

def diff(p) :
    #print("path=", p)
    i1 = desc(p[0])#.copy()
    i2 = desc(p[1])#.copy()
    dd = np.abs(i1 - i2)
    ddt = dd > 0.1
    #ddtm = cv2.dilate(dd, kk, iterations=1)
    red[:,:,1] = 0
    n = ddt.sum()
    
    #print("n ", n)
    org = (50, 70)
    ppp = os.path.basename(p[0])
    """
    i11 = i1.copy()
    i3 = np.where(ddt, red, i1)
    cv2.putText(i11, str(n), org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.putText(i11, ppp, (50, 95), font, fontScale, color, thickness, cv2.LINE_AA)    
    plt.imshow(np.hstack((i11, i2, i3, ddt))); plt.show()
    """
    return n



ps = zip(files[0:-2], files[1:])
d = list(map(diff, tqdm.tqdm(ps)))
dd = [ files[i+1] for i, e in enumerate(d) if e > 50]
print(dd)
plt.plot(d); plt.show()

