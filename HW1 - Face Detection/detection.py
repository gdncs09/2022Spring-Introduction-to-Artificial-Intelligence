import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    for line in open(dataPath):
        line = line.split() 
        if len(line) == 2:
            img_name = line[0]
            face_num = int(line[1])
            img = cv2.imread('data/detect/'+img_name, cv2.IMREAD_UNCHANGED) #load the image
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #RGB -> BGR
        else:
            face_num = face_num - 1
            x = int(line[0])
            y = int(line[1])
            w = int(line[2])
            h = int(line[3])
            face = img[y : y + h, x : x + w] #get the face image
            face_resized = cv2.resize(face, (19,19)) #19x19 face image
            face_gray = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY) #gray color
            if clf.classify(face_gray) == 1: #face image positive
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3) #green
            else: #false
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 3) #red
        if face_num == 0: 
            plt.axis('off')
            plt.imshow(img, cmap='jet')
            plt.show()
    # read file to get image name to load image
    # because use cv2 to load image so need change color from RGB to BGR
    # get face image and transfer to 19x19 and gray color
    # use clf.classify() to check face image
    # if positive will be return 1, otherwise 0
    # draw rectangle 
    # raise NotImplementedError("To be implemented")
    # End your code (Part 4)