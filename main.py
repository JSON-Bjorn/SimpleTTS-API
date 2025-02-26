from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from gtts import gTTS, lang
from typing import Optional
import pyttsx3
import tempfile
import os
import uuid
app = FastAPI(
    title="TTS API",
    description="A flexible Text-to-Speech API supporting multiple engines and voices",
    version="1.0.0"
)

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Get available voices
pyttsx_voices = engine.getProperty('voices')

@app.get("/")
async def read_root():
    return {"message": "Welcome to the TTS API", "status": "active"}

@app.get("/voices")
async def get_voices():
    # Get gTTS supported languages
    gtts_langs = lang.tts_langs()
    
    # Get pyttsx3 voices
    pyttsx_voice_list = [
        {
            "id": i,
            "name": voice.name,
            "languages": [voice.languages[0] if voice.languages else "en-US"]
        }
        for i, voice in enumerate(pyttsx_voices)
    ]
    
    return {
        "gtts_languages": gtts_langs,
        "pyttsx3_voices": pyttsx_voice_list
    }

@app.post("/synthesize")
async def synthesize_speech(
    text: str,
    engine_type: str = Query("gtts", enum=["gtts", "pyttsx3"]),
    language: str = Query("en", description="Language code for gTTS or voice ID for pyttsx3"),
    speed: float = Query(1.0, ge=0.5, le=2.0),
):
    try:
        # Create a unique filename
        filename = f"{uuid.uuid4()}.mp3"
        output_path = os.path.join(tempfile.gettempdir(), filename)
        
        if engine_type == "gtts":
            # Validate language code for gTTS
            available_langs = lang.tts_langs()
            if language not in available_langs:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid language code for gTTS. Available languages: {', '.join(available_langs.keys())}"
                )
            
            # Use gTTS for synthesis
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(output_path)
        
        elif engine_type == "pyttsx3":
            try:
                # Only convert to int if using pyttsx3
                voice_id = int(language)
                if voice_id < 0 or voice_id >= len(pyttsx_voices):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid voice ID. Must be between 0 and {len(pyttsx_voices)-1}. Available voices: {[f'{v.name} (ID: {i})' for i, v in enumerate(pyttsx_voices)]}"
                    )
                
                # Configure pyttsx3
                engine.setProperty('voice', pyttsx_voices[voice_id].id)
                engine.setProperty('rate', int(engine.getProperty('rate') * speed))
                
                # Save to file
                engine.save_to_file(text, output_path)
                engine.runAndWait()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"For pyttsx3 engine, language parameter must be a valid voice ID (integer between 0 and {len(pyttsx_voices)-1})"
                )
        
        # Return the audio file
        return FileResponse(
            output_path,
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
            background=None
        )
    
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)