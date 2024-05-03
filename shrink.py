import cv2
import os

# Set the directory path to your folder of greyscale images
image_dir = 'IMSLP_TCB'

# Set the threshold for white pixels (adjust as needed)
white_threshold = 250

for filename in os.listdir(image_dir):
    if filename.endswith(".png"):  # adjust as needed
        image_path = os.path.join(image_dir, filename)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Initialize variables to track the crop boundaries
        top_crop = 0
        bottom_crop = -1
        left_crop = 0
        right_crop = -1

        # Loop until the next crop would increase the percentage of white pixels
        while True:
            # Calculate the percentage of white pixels in the current image
            _, thresh = cv2.threshold(img, white_threshold, 200, cv2.THRESH_BINARY)
            white_pixels = cv2.countNonZero(thresh)
            total_pixels = img.shape[0] * img.shape[1]
            white_percentage = (white_pixels / total_pixels) * 100

            # Crop one row/column at a time and check the new percentage of white pixels
            for direction in ['top', 'bottom', 'left', 'right']:
                if direction == 'top':
                    crop_img = img[top_crop:, :]
                elif direction == 'bottom':
                    crop_img = img[:bottom_crop, :]
                elif direction == 'left':
                    crop_img = img[:, left_crop:]
                elif direction == 'right':
                    crop_img = img[:, :right_crop]

                _, thresh_crop = cv2.threshold(crop_img, white_threshold, 200, cv2.THRESH_BINARY)
                white_pixels_crop = cv2.countNonZero(thresh_crop)
                total_pixels_crop = crop_img.shape[0] * crop_img.shape[1]
                white_percentage_crop = (white_pixels_crop / total_pixels_crop) * 100

                # If the new percentage of white pixels is higher, break the loop
                if white_percentage_crop > white_percentage:
                    break
                white_percentage = white_percentage_crop

                # Otherwise, update the crop boundaries and continue
                if direction == 'top':
                    top_crop += 1
                elif direction == 'bottom':
                    bottom_crop -= 1
                elif direction == 'left':
                    left_crop += 1
                elif direction == 'right':
                    right_crop -= 1
                
                

            # If we've reached the break condition, exit the loop
            else:
                break

        # Apply the final crop to the image
        img_cropped = img[top_crop+1:-bottom_crop+1, left_crop+1:-right_crop+1]

        # Save the cropped image with the same filename
        cv2.imwrite(os.path.join("IMSLP_TCBcropped", filename), img_cropped)
        print(image_path)