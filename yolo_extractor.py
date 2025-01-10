from inference_sdk import InferenceHTTPClient
import os
from roboflow import Roboflow
import supervision as sv
import cv2
from PIL import Image, ImageDraw, ImageFont
input_folder = 'IMSLP_curatedimages'
output_folder = 'output_yolo'
#CLIENT = InferenceHTTPClient(
#    api_url="https://detect.roboflow.com",
#    api_key="dSFWiw9myGofWrifDBA4"
#)
#filename = "PMLP24518-Gold 9 pts Gotth_69.png"
#image_name = os.path.join(input_folder, filename)
#image = Image.open(image_name)

#result = CLIENT.infer(image, model_id="yolo-omr/1")
#print(result)

rf = Roboflow(api_key="dSFWiw9myGofWrifDBA4")
project = rf.workspace().project("yolo-omr")
model = project.version(1).model

for filename in os.listdir(input_folder):
    print(filename)
    image_name = os.path.join(input_folder, filename)
    image = Image.open(image_name)
    result = model.predict(image_name, confidence=40, overlap=30).json()

    labels = [item["class"] for item in result["predictions"]]

    i = 0 
    # Draw bounding boxes
    for prediction in result["predictions"]:
        x = prediction["x"]
        y = prediction["y"]
        width = prediction["width"]
        height = prediction["height"]
        class_name = prediction["class"]

        if class_name != 'gClef':
            continue
            
        i= 1+1
        # Calculate the coordinates of the bounding box
        start_point = (x-width/2, y-height/2)
        end_point = (x + width/2, y + height/2)

        # Draw the bounding box
        color = (255,0,0)  # RGB color (Red)
    #    print(type(color))
        #draw.rectangle([start_point, end_point], outline=color, width=10)
        sample = image.crop((start_point[0], start_point[1], end_point[0], end_point[1]))
        sample.save(os.path.join(output_folder, f"{filename[:-4]}_{i}.png"))

    # Display the image with bounding boxes
    #image.show()