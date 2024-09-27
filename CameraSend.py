from flask import Flask, request, make_response
import os
from dotenv import load_dotenv
import google.generativeai as gai
from PIL import Image
from gtts import gTTS
import uuid

# Initialize Flask app
app = Flask(_name_)

# Directory to save images and output files
save_directory = r'E:\Coding\DSU_DEVHACK\imagegemini\public'

# Ensure the directory exists, if not, create it
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# Load environment variables
load_dotenv()

# Configure the Google Generative AI API
gai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create a model instance
model = gai.GenerativeModel("gemini-1.5-flash-latest")

# Function to process the image using Gemini model
def gemini_img_bot(image_path):
    # Recreate chat session to ensure no session issues
    chat = model.start_chat(history=[])

    # Open and process the image with a context manager
    with Image.open(image_path) as image:
        input_message = "Describe the image for blind people."
        # Send the input message and image to the chat model
        response = chat.send_message([input_message, image])
    
    return response.text

# Flask route to handle image uploads
@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if an image file was provided
    if 'image' not in request.files:
        return "No image file found in the request.", 400

    # Get the uploaded image file
    image_file = request.files['image']
    if image_file.filename == '':
        return "No selected file.", 400

    # Generate a unique filename for each request using a UUID
    unique_id = str(uuid.uuid4())[:8]
    image_path = os.path.join(save_directory, f'input_{unique_id}.jpg')

    # Save the uploaded image file
    image_file.save(image_path)
    print(f"Image received and saved to {image_path}")

    # Process the saved image using the Gemini bot
    response_text = gemini_img_bot(image_path)

    # Save the response to output.txt
    output_text_path = os.path.join(save_directory, f"output_{unique_id}.txt")
    with open(output_text_path, "w") as f:
        f.write(response_text)

    # Save the response as an audio file (MP3)
    output_audio_path = os.path.join(save_directory, f"output_{unique_id}.mp3")
    tts = gTTS(text=response_text, lang='en')
    tts.save(output_audio_path)

    # Print and return the response
    print("Response:", response_text)

    # Return the response with cache control headers to ensure fresh responses
    response = make_response({
        "message": "Image successfully processed.",
        "description": response_text,
        "text_file": output_text_path,
        "audio_file": output_audio_path
    })
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    
    return response, 200

# Run the Flask app if this script is executed
if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5001)  # Run the Flask server on port 5001
