import os
import requests
import json, io
from PIL import Image
import base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Your API endpoint
API_URL = "https://cloud.olakrutrim.com/v1/images/generations/diffusion"

# Your API key (if required)
API_KEY = "your_api_key_here"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    
    # Set up the payload for generating 4 images
    payload = {
        "modelName": "diffusion1XL",
        "prompt": prompt,
        "prompt2": "", 
        "imageHeight": 1024, 
        "imageWidth": 1024, 
        "negativePrompt": None, 
        "negativePrompt2": None, 
        "numOutputImages": 4,  # Generate 4 images
        "guidanceScale": 7.5, 
        "numInferenceSteps": 10, 
        "seed": None, 
        "outputImgType": "pil"
    }

    headers = {
        "content-type": "application/json", 
        "Authorization": f"Bearer {API_KEY}"
    }

    # Send the POST request to the API
    response = requests.post(API_URL, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        output = response.json()
        img_datas = output.get("data", [])

        images = []
        for img_data in img_datas:
            # Decode the base64 string to bytes
            img_bytes = base64.b64decode(img_data["b64_json"])
            # Convert bytes to image
            img = Image.open(io.BytesIO(img_bytes))
            # Save image to a buffer
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            # Encode image to base64 string to send to the frontend
            encoded_img = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            images.append(encoded_img)

        return jsonify({"images": images})

    else:
        return jsonify({"error": "Failed to generate images", "details": response.text}), 500

if __name__ == '__main__':
    app.run(debug=True)
