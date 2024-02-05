import os
import cv2

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    
    # Begin your code (Part 1)
    dataset = []
    paths = os.listdir(dataPath) #data/train(test)/
    for path in paths: 
        imageLists = os.listdir(dataPath+'/'+path) #data/train(test)/face(non-face)/
        if path == 'face':#second element
            key = 1 
        elif path == 'non-face':
            key = 0
        for image in imageLists: #first element
            img = cv2.imread(dataPath+'/'+path+'/'+image, cv2.IMREAD_UNCHANGED)
            dataset.append((img, key)) 
    # find path to face and non-face folder to load image
    # if image in face folder second element will be 1, otherwise will be 0
    # save image and classification to dataset
    # raise NotImplementedError("To be implemented")
    # End your code (Part 1)
    return dataset