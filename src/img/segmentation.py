'''
Created on Jun 9, 2020

@author: mark
'''
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
import skimage.segmentation as seg
import time


import skimage.color as color

def image_show(image, nrows=1, ncols=1, cmap='gray'):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 14))
    ax.imshow(image, cmap='gray')
    ax.axis('off')
    return fig, ax

def image_show2(img):
    image = io.imread(img) 
    plt.imshow(image)
    
    return image
    
def denoise(image):
    image_gray = color.rgb2gray(image) 
    image_show(image_gray)
    
    return image_gray
    
def circle_points(resolution, center, radius):
    """
    Generate points which define a circle on an image.Centre refers to the centre of the circle
    """   
    radians = np.linspace(0, 2*np.pi, resolution)
    c = center[1] + radius*np.cos(radians)#polar coordinates
    r = center[0] + radius*np.sin(radians)
    
    return np.array([c, r]).T


# Exclude last point because a closed path should not have duplicate points
points = circle_points(200, [80, 250], 80)[:-1]
image_gray=image_show2('6th-dynasty1.jpg')
image_use=denoise(image_gray)
image_slic = seg.slic(image_gray,n_segments=30)

# label2rgb replaces each discrete label with the average interior color
image_show(color.label2rgb(image_slic, image_gray, kind='avg'))

#snake = seg.active_contour(image_slic, points,boundary_condition='fixed',alpha=0.05, beta=0.5)
#fig, ax = image_show(image_slic)
#snake = seg.active_contour(image_use, points,boundary_condition='fixed',alpha=0.05, beta=0.5)
#fig, ax = image_show(image_use)
#time.sleep(5)

#ax.plot(points[:, 0], points[:, 1], '--r', lw=3)
#ax.plot(points[:, 0], points[:, 1], '--r', lw=3)

#ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3,)

print('stop')
