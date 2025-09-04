# FastAPI OpenAI Image Edit Compatible API

This is a FastAPI application that provides an endpoint compatible with OpenAI's image edit API.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the server:
   ```
   python main.py
   ```
   Or with uvicorn:
   ```
   uvicorn main:app --reload
   ```

The server will run on http://localhost:8000

## Usage

Send a POST request to `/v1/images/edits` with multipart/form-data:

- `image`: PNG or JPEG file (required)
- `mask`: PNG file (optional)
- `prompt`: string (required)
- `n`: integer 1-10 (optional, default 1)
- `size`: "256x256", "512x512", "1024x1024" (optional, default "1024x1024")
- `response_format`: "url" or "b64_json" (optional, default "url")

## Note

The actual image editing logic is not implemented. Replace the TODO section in `main.py` with your image processing code.