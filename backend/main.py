from fastapi import UploadFile, File
from summarizer import generate_summary, extract_text_from_pdf, extract_text_from_image

@app.post("/summarize/pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    extracted_text = extract_text_from_pdf(pdf_bytes)
    summary = generate_summary(extracted_text)
    return {"summary": summary}


@app.post("/summarize/image")
async def summarize_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    extracted_text = extract_text_from_image(image_bytes)
    summary = generate_summary(extracted_text)
    return {"summary": summary}

class FlashcardRequest(BaseModel):
    text: str
    highlights: list[str]

@app.post("/flashcards")
def generate_flashcards_api(request: FlashcardRequest):
    from flashcard_generator import generate_flashcards
    flashcards = generate_flashcards(request.text, request.highlights)
    return {"flashcards": flashcards}

class RecencyRequest(BaseModel):
    last_reviewed: str  # ISO format
    recall_score: int   # 0–2
    times_seen: int
    difficulty: int     # 1 (easy) – 3 (hard)

@app.post("/recency_score")
def recency_score(request: RecencyRequest):
    from recency_model import classify_recency
    result = classify_recency(
        last_reviewed=request.last_reviewed,
        recall_score=request.recall_score,
        times_seen=request.times_seen,
        difficulty=request.difficulty
    )
    return result
