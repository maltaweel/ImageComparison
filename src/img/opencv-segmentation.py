'''
Created on Jun 12, 2020

@author: mark
'''

import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

from os import listdir
import cv2


def path():
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    return pn

def detect_faces(cascade, test_image, scaleFactor = 1.1):
    # create a copy of the image to prevent any changes to the original one.
    image_copy = test_image.copy()

    #convert the test image to gray scale as opencv face detector expects gray images
    gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)

    # Applying the haar classifier to detect faces
    faces_rect = cascade.detectMultiScale(gray_image, scaleFactor=scaleFactor, minNeighbors=5)
    
    bounds=[]
    for (x, y, w, h) in faces_rect:
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 255, 0), 15)
        crop_img = image_copy[y:y+h, x:x+w]
        bounds.append(crop_img)
        

    return image_copy, bounds

def getImages():
    
    pth=path()
    pathway=os.path.join(pth,'images')
    face_output=os.path.join(pth,'faces_output')
    
    haar_path=os.path.join(pth,'haar_cascade','haarcascade_frontalface_default.xml')
    
    
     #print results out
    try:
        for f in listdir(pathway):
            
            test_image = cv2.imread(os.path.join(pathway,f))

            # Converting to grayscale
            test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)

            # Displaying grayscale image
            #plt.imshow(test_image_gray, cmap='gray')

            #get the xml cascade used to mark and define faces
            haar_cascade_face = cv2.CascadeClassifier(haar_path)
            
            #call the function to detect faces
            faces, bounds = detect_faces(haar_cascade_face, test_image)

            #convert to RGB and display image
            #plt.imshow(convertToRGB(faces))
            #cv2.waitKey(0)
            
            i=0
            for b in bounds:
                fileOut=os.path.join(face_output,str(i)+f)
                cv2.imwrite(fileOut, b)
                i+=1

    except IOError:
        print ("Could not read file:", IOError)
 

def run():
    getImages()
    print('Finished')

#launch the main
if __name__ == "__main__":
    run()