import openai
import os
import json
import base64

# Set up OpenAI API key
openai.api_key = ".."

# Directory containing images
image_directory = "/Users/sandyaudumala/Image search engine/Images"
output_json_file = "extracted_text.json"

# Function to encode images in base64 format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to extract text from an image using OpenAI API
def extract_text_from_image(image_path):
    image_data = encode_image(image_path)
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that extracts text from images."},
            {"role": "user", "content": [
                {"type": "text", "text": "Extract text from this image:"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]}
        ],
        max_tokens=500
    )
    
    return response["choices"][0]["message"]["content"]

# Process images in the directory
extracted_texts = {}

for filename in os.listdir(image_directory):
    if filename.lower().endswith(("png", "jpg", "jpeg")):
        image_path = os.path.join(image_directory, filename)
        print(f"Processing: {filename}")
        
        try:
            extracted_texts[filename] = extract_text_from_image(image_path)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            extracted_texts[filename] = "Error extracting text"

# Save extracted text to JSON file
with open(output_json_file, "w", encoding="utf-8") as json_file:
    json.dump(extracted_texts, json_file, indent=4, ensure_ascii=False)

print(f"Extraction completed. Results saved to {output_json_file}")