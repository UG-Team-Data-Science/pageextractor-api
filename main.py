import time
import base64
import io
import logging
import json
from PIL import Image
from typing import Optional, List
from cgi import parse_header
from multipart import MultipartParser

from pydantic import BaseModel

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request

from pageextractor import PageExtractor

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the model at startup
    app.state.model = PageExtractor(sam_type='sam2.1_hiera_tiny', device='cuda')
    yield
    # Cleanup on shutdown if needed
    # app.state.model = None  # Uncomment if cleanup is required


app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    content_type = request.headers.get('content-type', '')
    user_agent = request.headers.get('user-agent', '')
    logging.info(f"Request: {request.method} {request.url} Content-Type: {content_type} User-Agent: {user_agent}")

    # Log all headers for debugging
    headers_dict = dict(request.headers)
    logging.info(f"Headers: {json.dumps(headers_dict, indent=2)}")

    body = await request.body()

    if 'multipart/form-data' in content_type:
        form = await request.form()
        logging.info(f"Form fields: {list(form)}")
    elif 'application/json' in content_type:
        try:
            data = json.loads(body.decode())
            logging.info(f"JSON keys: {list(data.keys())}")
        except:
            pass
    else:
        # Log body for other content types
        logging.info(f"Body length: {len(body)} bytes")

    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

@app.post("/v1/images/edits")
async def edit_image(image: UploadFile = File(...), prompt: str = Form("page."), response_format: str = Form("b64_json")):
    # Validate response_format
    if response_format not in ["b64_json"]:
        raise HTTPException(status_code=400, detail="Invalid response_format, only b64_json is supported")

    # Read uploaded image
    try:
        image_bytes = await image.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Extract pages using pageextractor with preloaded model
    img = Image.open(io.BytesIO(image_bytes))
    cropped = app.state.model.extract_page(img, prompt=prompt)[2]

    # Convert cropped PIL Image to PNG bytes and base64
    cropped_bytes_io = io.BytesIO()
    cropped.save(cropped_bytes_io, format='PNG')
    cropped_bytes = cropped_bytes_io.getvalue()
    b64_data = base64.b64encode(cropped_bytes).decode()

    created = int(time.time())
    return {"created": created, "data": [{"b64_json": b64_data}]}
