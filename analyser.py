from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze(data: TextInput):

    text = data.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    words = text.split()
    clean_words = [word.strip(".,!?").lower() for word in words]

    total_length = sum(len(word) for word in clean_words)
    average_length = round(total_length / len(words), 2)

    sentence_count = (
        text.count(".") +
        text.count("!") +
        text.count("?")
    )

    return {
        "word_count": len(words),
        "character_count": len(text),
        "unique_word_count": len(set(clean_words)),
        "sentence_count": sentence_count,
        "average_word_length": average_length,
        "uppercase_text": text.upper(),
        "lowercase_text": text.lower()
    }