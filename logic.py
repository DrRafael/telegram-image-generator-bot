import base64
import json
import time
from io import BytesIO
from PIL import Image
import requests


class Text2ImageAPI:
    """Client for FusionBrain (Kandinsky) Text2Image REST API."""

    def __init__(self, url: str, api_key: str, secret_key: str):
        self.url = url
        self.auth_headers = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self) -> int:
        """Fetches the primary model ID for image generation."""
        response = requests.get(f"{self.url}key/api/v1/models", headers=self.auth_headers)
        response.raise_for_status()
        data = response.json()
        return data[0]['id']

    def generate(self, prompt: str, model_id: int, images: int = 1, width: int = 1024, height: int = 1024) -> str:
        """Submits a text prompt for image generation and returns task UUID."""
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": prompt
            }
        }

        data = {
            'model_id': (None, str(model_id)),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(f"{self.url}key/api/v1/text2image/run", headers=self.auth_headers, files=data)
        response.raise_for_status()
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id: str, attempts: int = 10, delay: int = 10) -> list:
        """Polls the API status until generation completes or times out."""
        while attempts > 0:
            response = requests.get(f"{self.url}key/api/v1/text2image/status/{request_id}", headers=self.auth_headers)
            data = response.json()
            if data.get('status') == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
        
        raise TimeoutError("Image generation timed out.")

    @staticmethod
    def save_image(base64_string: str, file_path: str) -> None:
        """Decodes base64 string and saves binary image file to disk."""
        decoded_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(decoded_data))
        image.save(file_path)
