import os
from PIL import Image

# Set the input and output folders
input_folder = 'IMSLP_sampledimages256'
output_folder = 'IMSLP_sampledimages128 - Copy'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all the images in the input folder
for filename in os.listdir(input_folder):
    # Check if the file is an image
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif')):
        # Open the image using Pillow
        img = Image.open(os.path.join(input_folder, filename))
        
        # Resize the image to half its size
       # width, height = img.size
       # img = img.resize((width // 2, height // 2))
        
        # Add a subscript to the filename
        base, ext = os.path.splitext(filename)
        new_filename = f"{base}_half{ext}"
        
        # Save the resized image to the output folder
        img.save(os.path.join(output_folder, new_filename))