import os
import cv2
import numpy as np
import random

# Parameters
N = 128  # Size of the sample
V = 0.17*255  # Variance threshold
X = 100  # Maximum number of iterations

# Folders
input_folder = 'IMSLP_measures'
output_folder = 'IMSLP_measurescropped'

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate over images in input folder
for filename in os.listdir(input_folder):
        img = cv2.imread(os.path.join(input_folder, filename), cv2.IMREAD_GRAYSCALE)
    
  
        # Sample a random N by N part of the image
        try:
            h, w = img.shape
        except AttributeError:
            continue

        sample = img[int(h/8):int(h*7/8), 0:int(w)]
        

        cv2.imwrite(os.path.join(output_folder, filename), sample)
           