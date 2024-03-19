import vertexai
from vertexai.generative_models import GenerativeModel, Part

import cv2
def generate_text(project_id: str, location: str) -> str:
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)
    # Load the model
    multimodal_model = GenerativeModel("gemini-1.0-pro-vision")
    img = cv2.imread("/Users/cna/personal/trade/CVNA-2024-03-17-2023-09-17.png")

    # Query the model
    response = multimodal_model.generate_content(
        [
            # Add an example imageur
            Part.from_uri("gs://vertex-ai-samples/vision/ocr/form.jpg", "image/jpeg"),
            # Part.from_data(img.tobytes(), "image/png"),
            # Add an example query
            """Using the Qullamaggie breakout strategy, If you were to rank the setup from 1 to 5 (1 being bad, 5 being great), what number would you give it?
volume: $7866285
averageVolume: $7883534
averageVolume10days: $5645470
regularMarketVolume: $7866285
averageDailyVolume10Day: $5645470
marketCap: $14133408768""",
        ]
    )
    print(response)
    return response.text

generate_text('trade-417518',"europe-west1")
