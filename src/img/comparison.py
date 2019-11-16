'''
Module used to compare images using structural similarity and mean squared error. 

Code based on Adrian Rosebrock from:  https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

Created on Nov 14, 2019

@author: mark
'''
# import the necessary packages
import os
from skimage import measure as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import csv

def printResults(values1, values2):
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    pathway=os.path.join(pn,'output','output_sse.csv')
    
    fieldnames = ['File 1','File 2','MSE','SSE']
    #print results out
    try:
        with open(pathway, 'w') as csvf:
             
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            for k in values1:
                
                mse=values1[k]
                sse=values2[k]
                
                vv=k.split(':')
                v1=vv[0]
                v2=vv[1]
                
                writer.writerow({'File 1': str(v1),'File 2':str(v2),
                            'MSE':str(mse),'SSE':str(sse)})
                
                print('File 1: '+str(v1)+ " File 2: "+str(v2)+" MSE: "+str(mse)+" SSE: "+str(sse))
            
    except IOError:
        print ("Could not read file:", csv)

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s =  ssim.compare_ssim(imageA, imageB)

    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
    
    return m, s

    # show first image
 #   ax = fig.add_subplot(1, 2, 1)
 #   plt.imshow(imageA, cmap = plt.cm.gray)
 #   plt.axis("off")

    # show the second image
 #   ax = fig.add_subplot(1, 2, 2)
 #   plt.imshow(imageB, cmap = plt.cm.gray)
 #   plt.axis("off")

    # show the images
 #   plt.show()

# load the images -- the original, the original + contrast,
# and the original + photoshop
pn=os.path.abspath(__file__)
pn=pn.split("src")[0]
        

#The data file path is now created where the data folder and dataFile.csv is referenced
path=os.path.join(pn,'images')

fileM={}
fileS={}

for fil in os.listdir(path):
    
    original = cv2.imread(os.path.join(path,fil))
    #contrast = cv2.imread(os.path.join(path,'2.jpg'))
    #shopped = cv2.imread(os.path.join(path,'1.jpg'))

    # convert the images to grayscale
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    
    for fil2 in os.listdir(path):
        if fil==fil2:
            continue
        contrast = cv2.imread(os.path.join(path,fil2))
        contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    #contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    #shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)

    # initialize the figure
        fig = plt.figure("Images")
        images = ("Original", original), ("Contrast", contrast)

        # loop over the images
        #for (i, (name, image)) in enumerate(images):
            # show the image
            # ax = fig.add_subplot(1, 3, i + 1)
            #ax.set_title(name)
        #plt.imshow(image, cmap = plt.cm.gray)
        #plt.axis("off")

        # show the figure
        #plt.show()

        # compare the images
        m, s=compare_images(original, contrast, "Original vs. Contrast")
        
        osS=fil.split(os.sep)
        osN=osS[len(osS)-1]
        
        ocS=fil2.split(os.sep)
        ocN=ocS[len(ocS)-1]
        
        fileM[str(osN)+":"+str(ocN)]=m
        fileS[str(osN)+":"+str(ocN)]=s
        #compare_images(original, contrast, "Original vs. Contrast")
        #compare_images(original, shopped, "Original vs. Photoshopped")
printResults(fileM,fileS)