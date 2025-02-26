from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from fastapi.responses import FileResponse
from typing import List

# Configuration
IMAGE_DIR = "/Users/sandyaudumala/Image search engine/Images"
TEXT_DATA_FILE = "extracted_text.json"

# Load extracted text data
try:
    with open(TEXT_DATA_FILE, "r", encoding="utf-8") as file:
        extracted_texts = json.load(file)
except FileNotFoundError:
    extracted_texts = {}

# Initialize FastAPI
app = FastAPI(title="Image Search API")

# ✅ Enable CORS to allow requests from any frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this to your frontend domain)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def root():
    return {"message": "Welcome to the Image Search API"}

@app.get("/search", response_model=List[str])
def search_images(keyword: str):
    """
    Search for images that contain the given keyword in the extracted text.
    """
    matching_images = [
        filename for filename, text in extracted_texts.items() if keyword.lower() in text.lower()]

    if not matching_images:
        raise BaseException(status_code=404, detail="No matching images found")

    print(matching_images)
    return matching_images

#query = input("Enter search query: ")
#matches = search_images(query)
#print("Matching images:", matches)


@app.get("/image/{filename}")
def get_image(filename: str):
    """
    Serve the requested image file.
    """
    file_path = os.path.join(IMAGE_DIR, filename)

    if not os.path.exists(file_path):
        raise BaseException(status_code=404, detail="Image not found")

    return FileResponse(file_path, media_type="image/jpeg")

# Run with: uvicorn script_name:app --reload