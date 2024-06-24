import requests
import os

SERVER_URL = "http://127.0.0.1:5000/"

def upload_image():
    image_path = "input/image_1.png"

    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Prepare the multipart form data (replace 'image' with the expected field name on the server)
        files = {'image': (os.path.basename(image_path), image_file)}
        # Send a POST request with the image data
        response = requests.post(SERVER_URL + "upload", files=files)

    # Check the response status code
    if response.status_code == 200:
        print(f"Upload successful! Response: {response.text}")
    else:
        print(f"Error uploading file: {response.text}")


if __name__ == "__main__":
  upload_image()