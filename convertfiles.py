import os
import pdf2image
from PIL import Image

# Set the input and output directories
input_dir = 'IMSLPremaining'
output_dir = 'IMSLP_images'

# Loop through all PDF files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".pdf"):
        # Open the PDF file
        pdf_path = os.path.join(input_dir, filename)
        images = pdf2image.convert_from_path(pdf_path, poppler_path = r"poppler-24.02.0\Library\bin")

        # Loop through each page of the PDF
        for i, image in enumerate(images):
            # Check if the image is not greyscale
            if image.mode != 'L':
                # Convert the image to greyscale
                grey_image = image.convert('L')
                # Save the greyscale image as a PNG file
                image_path = os.path.join(output_dir, f"{filename[:-4]}_{i}.png")
                grey_image.save(image_path, 'PNG')
                print(f"Converted {filename} page {i+1} to greyscale and saved as {image_path}")
            else:
                # If the image is already greyscale, save it as is
                image_path = os.path.join(output_dir, f"{filename[:-4]}_{i}.png")
                image.save(image_path, 'PNG')
                print(f"Saved greyscale {filename} page {i+1} as {image_path}")