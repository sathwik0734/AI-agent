import json
import os
import requests
from io import BytesIO
from PIL import Image

# We use the inference API for a lightweight demo rather than downloading models locally
# to ensure it runs fast and reliably without huge memory requirements.
HF_API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"

def analyze_image(image_url: str) -> str:
    """
    A multimodal tool that uses HuggingFace to generate a caption for an image.
    """
    print(f"[Tool Execution] Calling analyze_image for {image_url}...")
    hf_token = os.getenv("HF_TOKEN")
    
    if not hf_token or hf_token == "your_huggingface_token_here":
        return json.dumps({"error": "HF_TOKEN not set or invalid. Please configure in .env."})

    headers = {"Authorization": f"Bearer {hf_token}"}
    
    try:
        # First fetch the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        
        # Send image to HuggingFace Inference API
        hf_response = requests.post(HF_API_URL, headers=headers, data=response.content)
        hf_response.raise_for_status()
        
        result = hf_response.json()
        if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
            caption = result[0]['generated_text']
            return json.dumps({"image_url": image_url, "caption": caption})
        else:
            return json.dumps({"error": "Unexpected response format from HuggingFace API.", "raw": str(result)})
            
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": f"Failed to process image or API request: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occurred: {str(e)}"})


ANALYZE_IMAGE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "analyze_image",
        "description": "Analyze an image from a URL and return a descriptive caption.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_url": {
                    "type": "string",
                    "description": "The direct URL to the image to analyze.",
                }
            },
            "required": ["image_url"],
        },
    }
}
