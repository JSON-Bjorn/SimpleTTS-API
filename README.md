# Simple TTS API

A flexible Text-to-Speech API supporting multiple engines (gTTS and pyttsx3) with various voices and languages.
Might be extended to support more engines in the future or have its functionality changed to be a screen reader.

## Features

- Multiple TTS engine support (gTTS and pyttsx3)
- Language selection for gTTS
- Voice selection for pyttsx3
- Adjustable speech speed
- Simple REST API interface

## Installation

1. Ensure you have Python 3.10 or later installed

2. Clone this repository or download the source code

3. Create and activate a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/macOS
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

1. Start the server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. The API will be available at `http://localhost:8000`
   (Use http://localhost:8000/docs for Swagger)

## API Endpoints

### GET /

- Health check endpoint
- Returns: `{"message": "Welcome to the TTS API", "status": "active"}`

### GET /voices

- Lists available voices and languages
- Returns:
  - `gtts_languages`: Dictionary of available gTTS language codes and names
  - `pyttsx3_voices`: List of available pyttsx3 voices with IDs and names

### POST /synthesize

- Converts text to speech
- Parameters:
  - `text` (string, required): The text to convert to speech
  - `engine_type` (string, optional): TTS engine to use (`"gtts"` or `"pyttsx3"`, default: `"gtts"`)
  - `language` (string, optional):
    - For gTTS: Language code (e.g., `"en"`, `"fr"`, `"es"`)
    - For pyttsx3: Voice ID (integer)
  - `speed` (float, optional): Speech rate multiplier (0.5 to 2.0, default: 1.0)
- Returns: Audio file (MP3 format)

## Examples

### Using gTTS

```bash
curl -X POST "http://localhost:8000/synthesize" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Hello, world!&engine_type=gtts&language=en" \
     --output output.mp3
```

### Using pyttsx3

```bash
curl -X POST "http://localhost:8000/synthesize" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "text=Hello, world!&engine_type=pyttsx3&language=0&speed=1.2" \
     --output output.mp3
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 400: Bad Request (invalid parameters)
- 500: Internal Server Error

Error responses include a JSON object with an `error` field containing the error message.

## License

This project is open source and available under the MIT License.

## Contact

Bjorn or Felix
