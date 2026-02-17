from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="The Translator Service")

# Load a small English-to-French model
# This runs once when the server starts
print("Loading translation model...")
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
print("Model loaded!")

class TranslationRequest(BaseModel):
    text: str

@app.get("/")
def health_check():
    return {"status": "active", "service": "the_translator"}

@app.post("/translate")
def translate_text(request: TranslationRequest):
    try:
        # The model returns a list of dicts: [{'translation_text': 'Bonjour world'}]
        result = translator(request.text, max_length=512)
        translation = result[0]['translation_text']
        
        return {
            "original": request.text,
            "translation": translation,
            "model": "Helsinki-NLP/opus-mt-en-fr"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)