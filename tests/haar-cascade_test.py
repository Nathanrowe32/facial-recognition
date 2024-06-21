import cv2 as cv
from pathlib import Path
from imgbeddings import imgbeddings
from PIL import Image
import numpy
import psycopg2
import os
import uuid


# Replace with the path to your Haar cascade model file
parent_dir_path = str(Path(Path(__file__)).parents[1])
haar_cascade_path = parent_dir_path + '\data\haarcascades\haarcascade_frontalface_default.xml'
input_path = parent_dir_path + '\input'
output_path = parent_dir_path + '\output'

# Connecting to database
connection = psycopg2.connect()

def load_inputs(input_path):
  # Load the Haar cascade classifier
  face_cascade = cv.CascadeClassifier(haar_cascade_path)
  for filename in os.listdir(input_path):
    # Load the image
    print(f"Began working on {filename}!")
    img = cv.imread(input_path + "/" + filename)
    # Convert the image to grayscale (improves processing speed)
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray_img, 1.1, 4)
    draw_rectangle(faces, img)
    

# Draw a red rectangle around each detected face
def draw_rectangle(faces, img):
  for (x, y, w, h) in faces:
    cv.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    # Generate a unique filename with numbering to avoid overwriting
    unique_filename = output_path + "/" + uuid.uuid4().hex + ".png"
    # Save the image with the bounding box
    cv.imwrite(unique_filename, img)
    print(f"Successfully finished {unique_filename} and saved to {output_path}!")

def post_imbeddings(connection):
  for filename in os.listdir(input_path):
    # opening the image
    img = Image.open(input_path + "/" + filename)
    # loading the `imgbeddings`
    ibed = imgbeddings()
    # calculating the embeddings
    embedding = ibed.to_embeddings(img)
    cur = connection.cursor()
    try:
      # Check if a record with the filename already exists
      cur.execute("SELECT * FROM pictures WHERE filename = %s", (filename,))
      existing_record = cur.fetchone()

      if not existing_record:
        # Insert only if the filename doesn't exist
        cur.execute("INSERT INTO pictures values (%s,%s)", (filename, embedding[0].tolist()))
        connection.commit()
      else:
        print(f"Skipping insertion: filename '{filename}' already exists.")

    except Exception as e:
      print(f"Error during insertion: {e}")
      # Handle other potential errors here (e.g., database connection issues)
      connection.rollback()  # Rollback the transaction if an error occurs
    print(filename + "imbedding completed")
  connection.commit()

def calculate_embedding(file_name):
  # opening the image
  img = Image.open(file_name)
  # loading the `imgbeddings`
  ibed = imgbeddings()
  # calculating the embeddings
  return ibed.to_embeddings(img)

def fetch_highest_similarity(connection, embedding):
  cur = connection.cursor()
  string_representation = "["+ ",".join(str(x) for x in embedding[0].tolist()) +"]"
  cur.execute("SELECT * FROM pictures ORDER BY embedding <-> %s LIMIT 1;", (string_representation,))
  rows = cur.fetchall()
  for row in rows:
      print(row[0])
  cur.close()


def main():
  load_inputs(input_path)
  post_imbeddings(connection)

  embedding = calculate_embedding(input_path + "/image_7.png")
  fetch_highest_similarity(connection, embedding)


if __name__=="__main__":
  main()