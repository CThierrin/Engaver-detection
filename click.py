'''
import cv2
import numpy as np
import os

def click_event(event, x, y, flags, param, img, img_path, img_list, img_index):
    if event == cv2.EVENT_LBUTTONDOWN:
        N = 100  # Sample size
        height, width, _ = img.shape
        x_start = max(0, x - N // 2)
        y_start = max(0, y - N // 2)
        x_end = min(width, x + N // 2 + N % 2)
        y_end = min(height, y + N // 2 + N % 2)
        sample = img[y_start:y_end, x_start:x_end]
        cv2.imwrite('sample.jpg', sample)

        # Move to the next image
        img_index[0] += 1
        if img_index[0] < len(img_list):
            img_path[0] = img_list[img_index[0]]
            img[0] = cv2.imread(img_path[0])
            cv2.imshow('Image', img[0])
        else:
            cv2.destroyAllWindows()

# Load the image files
img_folder = 'images'
img_list = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
img_path = [img_list[0]]
img = [cv2.imread(img_path[0])]
img_index = [0]

# Create a window to display the image
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', lambda event, x, y, flags, param: click_event(event, x, y, flags, param, img[0], img_path, img_list, img_index))

# Display the image
cv2.imshow('Image', img[0])
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
import cv2
import numpy as np
import os

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        N = 256  # Sample size
        height, width, _ = img[0].shape
        x_start = max(0, x - N // 2)
        y_start = max(0, y - N // 2)
        x_end = min(width, x + N // 2 + N % 2)
        y_end = min(height, y + N // 2 + N % 2)
        sample = img[0][y_start:y_end, x_start:x_end]
        filename = img_path[0].split("\\")[-1]
        cv2.imwrite(os.path.join("IMSLP_measures", filename), sample)

# Load the image files
img_folder = 'IMSLP_curatedimages'
img_list = [os.path.join(img_folder, f) for f in os.listdir(img_folder) if f.endswith(('.png'))]
img_path = [img_list[0]]
img = [cv2.imread(img_path[0])]
img_index = [0]

# Create a window to display the image
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', click_event)

while True:
    try:
        cv2.imshow('Image', img[0])
    except:
        img_index[0] = min(len(img_list) - 1, img_index[0] + 1)
        img_path[0] = img_list[img_index[0]]
        img[0] = cv2.imread(img_path[0])
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):  # Press 'q' to quit
        break
    elif key == ord('a'):  # Press left arrow key
        img_index[0] = max(0, img_index[0] - 1)
        img_path[0] = img_list[img_index[0]]
        img[0] = cv2.imread(img_path[0])
    elif key == ord('d'):  # Press right arrow key
        img_index[0] = min(len(img_list) - 1, img_index[0] + 1)
        img_path[0] = img_list[img_index[0]]
        img[0] = cv2.imread(img_path[0])

cv2.destroyAllWindows()