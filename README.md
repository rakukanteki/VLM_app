# AI Medical Chatbot

An AI-powered medical image analysis chatbot built with FastAPI and Groq's vision models. This application allows users to upload medical images (e.g., X-rays, MRIs) and ask questions about them, receiving AI-generated responses based on the image content.

## Features

- **Image Upload & Analysis**: Upload medical images and query them with natural language questions.
- **AI-Powered Responses**: Utilizes Groq's Llama models for intelligent analysis and responses.
- **Web Interface**: User-friendly web interface for easy interaction.
- **API Endpoints**: RESTful API for integration with other systems.
- **CLI Tool**: Standalone script (`main.py`) for command-line usage.
- **Image Validation**: Ensures uploaded images are valid before processing.
- **Error Handling**: Comprehensive error handling and logging.

## Prerequisites

- Python 3.8 or higher
- A Groq API key (sign up at [Groq](https://groq.com/))

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn python-multipart pillow requests python-dotenv
   ```

4. **Set up environment variables**:
   - Create a `.env` file in the project root.
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

## Usage

### Web Application

1. **Run the FastAPI server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://127.0.0.1:8000`.

3. **Upload an image** and enter your query in the web interface.

### API Usage

The application provides the following endpoints:

- `GET /`: Serves the main web interface.
- `POST /upload_and_query`:
  - **Parameters**:
    - `image` (file): The medical image to analyze.
    - `query` (form): Your question about the image.
  - **Response**: JSON object with AI responses from different models.

Example API call using curl:
```bash
curl -X POST "http://127.0.0.1:8000/upload_and_query" \
     -F "image=@path/to/your/image.jpg" \
     -F "query=What does this X-ray show?"
```

### Command-Line Tool

Use `main.py` for processing images from your local filesystem:

```bash
python main.py
```

Note: You'll need to modify the script to specify the image path and query.

## Project Structure

```
ai_medical_chatbot/
├── app.py                 # Main FastAPI application
├── main.py                # Command-line version
├── README.md              # This file
├── templates/
│   └── index.html         # Web interface template
└── .env                   # Environment variables (create this)
```

## Dependencies

- **FastAPI**: Web framework for building APIs.
- **Uvicorn**: ASGI server for running FastAPI.
- **python-multipart**: Required for handling file uploads in FastAPI.
- **Pillow (PIL)**: Image processing and validation.
- **Requests**: HTTP library for API calls.
- **python-dotenv**: Environment variable management.

## Configuration

- **Models**: Currently uses `meta-llama/llama-4-scout-17b-16e-instruct` for both text and vision analysis. Update the model names in `app.py` if you have access to other Groq models.
- **API Settings**: Adjust `max_tokens` and other parameters in the API request as needed.
- **CORS**: Configured to allow all origins for development. Restrict in production.

## Troubleshooting

- **"python-multipart not installed"**: Install with `pip install python-multipart`.
- **API Key Issues**: Ensure `GROQ_API_KEY` is set in your `.env` file.
- **Image Upload Errors**: Check that your image is a valid format (JPEG, PNG, etc.) and not corrupted.
- **Port Conflicts**: If port 8000 is in use, modify the host/port in `app.py`.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test thoroughly.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer

This tool is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.