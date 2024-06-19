import cv2 as cv
from pathlib import Path

# Replace with the path to your Haar cascade model file
parent_dir_path = str(Path(Path(__file__)).parents[1])
haar_cascade_path = parent_dir_path + '\data\haarcascades\haarcascade_frontalface_alt.xml'
input_path = parent_dir_path + '\input'
output_path = parent_dir_path + '\output'

# Load the Haar cascade classifier
face_cascade = cv.CascadeClassifier(haar_cascade_path)

# Load the image
img = cv.imread(input_path + '\image.png')

# Convert the image to grayscale (improves processing speed)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# Detect faces in the grayscale image
faces = face_cascade.detectMultiScale(gray, 1.1, 4)

# Draw a red rectangle around each detected face
for (x, y, w, h) in faces:
  cv.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

  # Generate a unique filename with numbering to avoid overwriting
  unique_filename = f"{output_path}/test_output1.png"
  # Save the image with the bounding box
  cv.imwrite(unique_filename, img)

# Display the image with the drawn boxes
cv.imshow('Image with Faces Detected', img)

# Wait for a key press to close the window
cv.waitKey(0)
# Close all OpenCV windows
cv.destroyAllWindows()

print(f"Face detection completed and saved to {output_path}!")