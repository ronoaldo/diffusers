import re
import unidecode
import torch
import os
import random
import readline
import atexit
from pprint import pprint
from diffusers import StableDiffusionPipeline

def slugify(text):
    text = unidecode.unidecode(text).lower()
    return re.sub(r'[\W_]+', '-', text)

model_id = "stabilityai/stable-diffusion-2-1"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

seed = random.randint(0, 2**64-1)
steps = 50

PROMPT_HISTORY="./prompts.txt"
try:
    readline.read_history_file(PROMPT_HISTORY)
except:
    pass
atexit.register(readline.write_history_file, PROMPT_HISTORY)

os.makedirs("./output", exist_ok=True)
while True:
    prompt = input(f"stable-diffusion v2-1: seed={seed}, steps={steps}, type 'quit' to exit\ndiffuse> ")

    if prompt.startswith("seed"):
        try:
            seed = int(prompt.split("=")[1])
        except Exception as e:
            print(f"Invalid seed (err={e})")
    elif prompt.startswith("steps"):
        try:
            steps = int(prompt.split("=")[1])
        except Exception as e:
            print(f"Invalid step count (err={e})")
    elif prompt == "quit":
        break
    else:
        # Save seed and steps into history
        readline.add_history(f"# seed={seed} steps={steps}")
        generator = torch.Generator("cuda").manual_seed(seed)
        result = pipe(prompt, num_inference_steps=steps, generator=generator)
        print(f"Result: {result}")
        image = result.images[0]

        fname = f"./output/{slugify(prompt)}_{steps}_{seed}.png"
        image.save(f"{fname}")
        print(f"Image saved at {fname}\n")

print("Exiting ...")