from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import base64
import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os
import logging

# -------------------- Setup --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Optional: allow frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file")

# -------------------- Routes --------------------

# Serve HTML directly (NO Jinja2)
@app.get("/")
async def read_root():
    return FileResponse(os.path.join(BASE_DIR, "templates", "index.html"))

# Main API
@app.post("/upload_and_query")
async def upload_and_query(image: UploadFile = File(...), query: str = Form(...)):
    try:
        # Read image
        image_content = await image.read()
        if not image_content:
            raise HTTPException(status_code=400, detail="Empty file")

        # Validate image
        try:
            img = Image.open(io.BytesIO(image_content))
            img.verify()
        except Exception as e:
            logger.error(f"Invalid image format: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid image format")

        # Encode image
        encoded_image = base64.b64encode(image_content).decode("utf-8")

        # Prepare message
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        },
                    },
                ],
            }
        ]

        # API call function
        def make_api_request(model_name):
            try:
                response = requests.post(
                    GROQ_API_URL,
                    json={
                        "model": model_name,
                        "messages": messages,
                        "max_tokens": 1000,
                    },
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    timeout=30,
                )
                return response
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {str(e)}")
                return None

        # ⚠️ Use different models if available
        llama_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        llava_model = "meta-llama/llama-4-scout-17b-16e-instruct"  # change if you have vision-specific model

        llama_response = make_api_request(llama_model)
        llava_response = make_api_request(llava_model)

        # Process responses
        responses = {}

        for model_name, response in [
            ("llama", llama_response),
            ("llava", llava_response),
        ]:
            if response and response.status_code == 200:
                try:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]
                    responses[model_name] = answer
                    logger.info(f"{model_name} response OK")
                except Exception as e:
                    logger.error(f"Parsing error: {str(e)}")
                    responses[model_name] = "Error parsing response"
            else:
                error_msg = (
                    f"API error: {response.status_code}" if response else "Request failed"
                )
                logger.error(error_msg)
                responses[model_name] = error_msg

        return JSONResponse(status_code=200, content=responses)

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# -------------------- Run --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)