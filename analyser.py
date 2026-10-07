from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()
class TextData(BaseModel):
    text: str

def analyze_text(text):
    words = text.split()
    word_count = len(words)
    character_count = len(text)
    unique_words = set()

    for word in words:
        word = word.lower().strip(".,!?")
        unique_words.add(word)

    unique_word_count = len(unique_words)
    sentence_count = (
        text.count(".") +
        text.count("!") +
        text.count("?")
    )

    if sentence_count == 0:
        sentence_count = 1
    total_length = 0

    for word in words:
        clean_word = word.strip(".,!?")
        total_length = total_length + len(clean_word)

    if word_count > 0:
        average_word_length = round(total_length / word_count, 2)
    else:
        average_word_length = 0

    result = {
        "word_count": word_count,
        "character_count": character_count,
        "unique_word_count": unique_word_count,
        "sentence_count": sentence_count,
        "average_word_length": average_word_length,
        "uppercase_text": text.upper(),
        "lowercase_text": text.lower()
    }

    return result

@app.get("/")
def home():
    return {"message": "Text Analyzer API is running"}

@app.post("/analyze")
def analyze(data: TextData):

    if data.text.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Please enter some text"
        )
    result = analyze_text(data.text)

    return result