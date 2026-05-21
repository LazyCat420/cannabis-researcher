import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import httpx
from io import BytesIO

async def test_clip():
    model_name = "openai/clip-vit-base-patch32"
    print("Loading CLIP processor and model...")
    processor = CLIPProcessor.from_pretrained(model_name)
    model = CLIPModel.from_pretrained(model_name)
    
    # Test images (one budding plant from Overgrow, one product/other if possible)
    urls = [
        "https://overgrow.com/uploads/default/optimized/3X/1/3/13959340f22abd19f50ac5b4821d5548560e22e6_2_690x447.jpeg", # budding plant
        "https://overgrow.com/uploads/default/optimized/3X/9/1/91d7a04497542982831fbcc9b261d909f50b24d6_2_523x500.jpeg", # budding plant
    ]
    
    # Zero-shot classification candidate labels
    candidate_labels = [
        "a budding cannabis plant",
        "a close-up of a cannabis bud",
        "marijuana flower in bloom",
        "something else",
        "a product label or text",
        "an empty room",
        "a seedling or sprout",
        "hash or concentrate"
    ]
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        for url in urls:
            print(f"\nDownloading: {url}")
            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    img = Image.open(BytesIO(resp.content)).convert("RGB")
                    
                    # Process inputs
                    inputs = processor(
                        text=candidate_labels,
                        images=img,
                        return_tensors="pt",
                        padding=True
                    )
                    
                    # Forward pass
                    with torch.no_grad():
                        outputs = model(**inputs)
                        logits_per_image = outputs.logits_per_image # image-to-text similarity
                        probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]
                        
                    print("Classification probabilities:")
                    for label, prob in zip(candidate_labels, probs):
                        print(f"  {label}: {prob:.4f}")
                        
                    # Sum of positive labels
                    pos_prob = sum(probs[i] for i in range(3))
                    print(f"Total positive probability (budding plant): {pos_prob:.4f}")
                else:
                    print(f"Failed to download image, status: {resp.status_code}")
            except Exception as e:
                print(f"Error testing image {url}: {e}")

if __name__ == "__main__":
    asyncio.run(test_clip())
