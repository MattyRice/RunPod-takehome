import runpod
import torch
from transformers import FluxForConditionalGeneration, AutoTokenizer
from PIL import Image
import io
import base64

# Load the model and tokenizer
model = FluxForConditionalGeneration.from_pretrained("black-forest-labs/FLUX.1-dev")
tokenizer = AutoTokenizer.from_pretrained("black-forest-labs/FLUX.1-dev")

def generate_image(prompt):
    # Tokenize the input prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Generate image
    with torch.no_grad():
        image = model.generate(**inputs, num_inference_steps=50)[0]
    
    # Convert image to PIL Image
    pil_image = Image.fromarray(image.numpy())
    
    # Convert image to base64 for easy transmission
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

def handler(event):
    try:
        prompt = event.get('input', {}).get('prompt')
        if not prompt:
            return {"error": "No prompt provided"}
        
        generated_image = generate_image(prompt)
        
        return {
            "image": generated_image,
            "prompt": prompt
        }
    except Exception as e:
        return {"error": str(e)}

# RunPod requires this to start the serverless endpoint
runpod.serverless.start({"handler": handler})