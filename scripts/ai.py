import vertexai
from vertexai.generative_models import GenerativeModel, Part,Image

import cv2

def load_image_from_local(local_path: str) -> Image:
    with open(local_path, 'rb') as file:
        image_bytes = file.read()
    return Image.from_bytes(image_bytes)

def generate_text(project_id: str, location: str,text:str, image_path:str) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    # Load the model
    multimodal_model = GenerativeModel("gemini-1.0-pro-vision")

    # Query the model
    response = multimodal_model.generate_content(
        [
            # Add an example imageur
            load_image_from_local(image_path),
            # Add an example query
            text,
        ]
    )
    print(response)
    return response.text

text = """Using the Qullamaggie breakout strategy, If you were to rank the setup from 1 to 7 (1 being bad, 7 being great), what number would you give it? where should I enter the trade?
          
volume: $9740973
averageVolume: $53925716
averageVolume10days: $106217030
regularMarketVolume: $9740973
averageDailyVolume10Day: $106217030
marketCap: $2510013952"""
image_path="plots/SOUN-2024-03-20-2023-09-20.png"

generate_text('trade-417518',"europe-west1",text, image_path)
