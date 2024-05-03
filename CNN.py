import pandas as pd
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, RandomZoom, RandomCrop
from tensorflow.keras.callbacks import Callback
from keras.regularizers import l1_l2
import matplotlib as plt

import os

# Load the CSV file
df1 = pd.read_csv('out.csv')
#print(df1)
# Create a dictionary to map score titles to engravers
score_to_engraver = {row['File']: row['Engraver'] for index, row in df1.iterrows()}

# Create a list to store the image files and their corresponding engravers
image_files = []

# Iterate over the image files in the directory
image_dir = "IMSLP_measures"
for filename in os.listdir(image_dir):
    # Check if the file is a PNG image
    if filename.endswith('.png'):
        # Extract the score title from the filename
        title = filename.split("_")[0]+'.pdf'
        # Check if the score is in the CSV file
        if title in score_to_engraver:
            # Read the image
           # img = cv2.imread(os.path.join(image_dir, filename), cv2.IMREAD_GRAYSCALE)
            # Add the image and its engraver to the list
            image_files.append((filename, score_to_engraver[title]))

# Now you can use the image_files list to train your classifier
# Each element in the list is a tuple containing the image and its engraver
# Load the CSV file with image paths and corresponding engravers
#df = pd.read_csv('engravers.csv')

df = pd.DataFrame(image_files, columns = ["filename", "class"])

# Split the data into training and testing sets (80% for training, 20% for testing)
train_df, test_df = train_test_split(df, test_size=0.25, random_state=42)

# Define the image dimensions and channels
img_height, img_width, channels = 256, 256, 1

# Create data generators for training and testing
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(dataframe = train_df, directory = image_dir, color_mode = "grayscale", target_size=(img_height, img_width), batch_size=32, class_mode='categorical')

test_generator = test_datagen.flow_from_dataframe(
    dataframe = test_df, directory = image_dir, color_mode = "grayscale", 
    target_size=(img_height, img_width),
    batch_size=32,
    class_mode='categorical'
)
#print('Training classes:', train_df['class'].unique())
#print('Testing classes:', test_df['class'].unique())
#debug_callback = DebugCallback()

# Define the CNN model
model = Sequential()
#model.add(RandomZoom((-0.5,0),(-0.5,0)))
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, channels), kernel_regularizer=l1_l2(l1=0.01, l2=0.01)))
model.add(Dropout(0.2))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(len(set(df['class'])), activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(train_generator, epochs=9, validation_data=test_generator)

# Evaluate the model on the test set
test_loss, test_acc = model.evaluate(test_generator)
print(f'Test accuracy: {test_acc:.2f}')

# Generate predictions on the test set
test_pred = model.predict(test_generator)

# Convert predictions to class labels
test_pred_labels = np.argmax(test_pred, axis=1)

# Get the true labels from the test generator
test_true_labels = test_generator.classes

# Create a confusion matrix
cm = confusion_matrix(test_true_labels, test_pred_labels)
cm_display = ConfusionMatrixDisplay(confusion_matrix = cm)

cm_display.plot()
plt.show() 
print('Confusion Matrix:')
print(cm)

# Optional: Normalize the confusion matrix
cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
print('Normalized Confusion Matrix:')
print(cm_norm)
# Use the model to make predictions on new images
def predict_engraver(image_path):
    img = Image.open(image_path)
    img = img.resize((img_height, img_width))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    return np.argmax(prediction)

## Example usage:
#image_path = 'path/to/an/image.jpg'
#engraver = predict_engraver(image_path)
#print(f'Predicted engraver: {engraver}')

# ...

