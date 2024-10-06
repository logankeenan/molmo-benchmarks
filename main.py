from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor, GenerationConfig, BitsAndBytesConfig

import time
import os
import torch
import json

# Load the image
image_path = 'test-image.png'
image = Image.open(image_path)

# Get the original dimensions
width, height = image.size

os.makedirs("images", exist_ok=True)

# Extract the base name and extension
base_name, ext = os.path.splitext(image_path)

# Save the original image to images/ directory
original_image_path = f'images/{base_name}_original{ext}'
image.save(original_image_path)

# Store all image paths to process
image_paths = [original_image_path]

# Generate images with resolutions from 10% to 90%
for i in range(1, 10):
    scale = i * 0.1
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Resize the image
    resized_image = image.resize((new_width, new_height))

    # Save the resized image with a new name
    resized_image_path = f'images/{base_name}_{int(scale * 100)}{ext}'
    resized_image.save(resized_image_path)
    image_paths.append(resized_image_path)

model_name = 'allenai/Molmo-7B-D-0924'
prompt = "What is the point coordinate of the sign up button. Only include the json response in the output {x, y}"
enable_bits_and_bytes = True

torch_dtype = torch.bfloat16
if enable_bits_and_bytes:
    torch_dtype = "auto"

processor = AutoProcessor.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype=torch_dtype,
    device_map='cuda'
)

arguments = {"device_map": "cuda", "torch_dtype": torch_dtype, "trust_remote_code": True}

if not enable_bits_and_bytes:
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="fp4",
        bnb_4bit_use_double_quant=False,
    )
    arguments["quantization_config"] = quantization_config

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    **arguments
)

for image_file in image_paths:
    inputs = processor.process(
        images=[Image.open(image_file)],
        text=prompt
    )
    inputs = {k: v.to(model.device).unsqueeze(0) for k, v in inputs.items()}

    if enable_bits_and_bytes:
        model.to(dtype=torch.bfloat16)
        inputs["images"] = inputs["images"].to(torch.bfloat16)

    generation_start_time = time.time()
    output = model.generate_from_batch(
        inputs,
        GenerationConfig(max_new_tokens=200, stop_strings="<|endoftext|>"),
        tokenizer=processor.tokenizer
    )

    generated_tokens = output[0, inputs['input_ids'].size(1):]
    generated_text = processor.tokenizer.decode(generated_tokens, skip_special_tokens=True)

    generation_time = time.time() - generation_start_time

    # Collect results for each image
    # Create result for the current image
    result = {
        "image_name": os.path.basename(image_file),
        "model_used": model_name,
        "enable_bits_and_bytes": enable_bits_and_bytes,
        "generation_time_ms": round(generation_time * 1000, 2),
        "generated_text": generated_text
    }

    # Print the result in JSON format
    print(json.dumps(result, indent=4))
