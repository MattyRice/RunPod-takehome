import os
import torch
from diffusers import FluxPipeline
import base64
from io import BytesIO
from PIL import Image
import runpod
from huggingface_hub import login

# Login to Hugging Face
hf_token = os.environ.get("HF_TOKEN")
if hf_token:
    login(token=hf_token)
    print("Logged in to Hugging Face")
else:
    print("WARNING: No Hugging Face token provided")

# Global variables to load the model just once when the container starts
model = None

def init():
    global model
    print("Loading FLUX.1-dev model...")
    model = FluxPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev", 
        torch_dtype=torch.float16,
        use_auth_token=hf_token
    ).to("cuda")
    print("Model loaded successfully")

def handler(event):
    global model
    
    # Initialize model if not already loaded
    if model is None:
        init()
    
    # Extract prompt from the event
    prompt = event.get("input", {}).get("prompt", "")
    if not prompt:
        return {"error": "No prompt provided"}
    
    # Set optional parameters with defaults
    num_inference_steps = event.get("input", {}).get("num_inference_steps", 50)
    guidance_scale = event.get("input", {}).get("guidance_scale", 7.5)
    seed = event.get("input", {}).get("seed", None)
    
    # Set random seed if provided
    generator = None
    if seed is not None:
        generator = torch.Generator(device="cuda").manual_seed(seed)
    
    # Generate image
    try:
        print(f"Generating image with prompt: {prompt}")
        with torch.inference_mode():
            image = model(
                prompt=prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=generator
            ).images[0]
        
        # Convert image to base64 string
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return {
            "status": "success",
            "output": {
                "image_base64": image_base64,
                "prompt": prompt
            }
        }
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

# Initialize the model when the container starts
init()

# Start the runpod handler
runpod.serverless.start({"handler": handler})