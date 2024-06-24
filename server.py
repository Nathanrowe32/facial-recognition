from flask import Flask, request
import os
import uuid

server = Flask(__name__)
output_path = "output/"

@server.route("/upload", methods=["POST"])
def handle_upload():

  file = request.files.get("image")

  # Check if a file was uploaded
  if file:
    # Save the file to the upload folder
    unique_filename = output_path + uuid.uuid4().hex + ".png"
    file.save(unique_filename)
    # Return success message with filename
    return f"File uploaded successfully: {unique_filename}", 200
  else:
    # Return error message if no file uploaded
    return "No file uploaded!", 400

@server.route("/debug", methods=["POST"])
def debug():
  try:
    return "server is awake.", 200
  except:
    return "server crashed.", 400

if __name__ == "__main__":
  server.run(debug=True)