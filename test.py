import os
import sys
import base64
from pathlib import Path
from openai import OpenAI

api_key = os.environ.get('RUGLLM_TOKEN', 'bla')
base_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8020/v1/'
model = sys.argv[2] if len(sys.argv) > 2 else 'rug-dsc/pageextractor-0'

print(f'Using {base_url} and {model}')

client = OpenAI(base_url=base_url, api_key=api_key)

result = client.images.edit(
    model=model,
    image=open("example-04.png", "rb"),
    prompt='page.',
)


# Save the first returned image to disk
b64 = result.data[0].b64_json
img_bytes = base64.b64decode(b64)
out_path = Path("edit_output.png")
out_path.write_bytes(img_bytes)
print(f"Saved: {out_path.resolve()}")
