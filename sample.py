import os
import cv2
import numpy as np
import random

# Parameters
N = 256  # Size of the sample
V = 0.17*255  # Variance threshold
X = 100  # Maximum number of iterations

# Folders
input_folder = 'IMSLP_curatedimages'
output_folder = 'IMSLP_sampledimages256'

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate over images in input folder
for filename in os.listdir(input_folder):
    img = cv2.imread(os.path.join(input_folder, filename), cv2.IMREAD_GRAYSCALE)
    
    for _ in range(X):
        # Sample a random N by N part of the image
        try:
            h, w = img.shape
        except AttributeError:
            break
        x = random.randint(0, w - N)
        y = random.randint(0, h - N)
        sample = img[y:y+N, x:x+N]
        
        # Calculate variance of the sample
        variance = np.var(sample)
        
        # If variance is above threshold, save the sample and break
        if variance > V:
            cv2.imwrite(os.path.join(output_folder, filename), sample)
            break
    else:
        # If the loop finishes without breaking, it means no sample with variance above V was found
        print(f"No sample with variance above {V} found for image {filename}")