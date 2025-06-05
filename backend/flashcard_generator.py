from transformers import pipeline

# Load the question generation model
qg = pipeline("text2text-generation", model="valhalla/t5-small-qg-hl")

def generate_flashcards(text: str, highlights: list[str]) -> list[dict]:
    flashcards = []
    for hl in highlights:
        # T5 expects format: "highlight: <context> </hl> <highlight>"
        input_text = f"highlight: {text.replace(hl, f'<hl> {hl} <hl>')}"
        result = qg(input_text)[0]['generated_text']
        flashcards.append({"question": result, "answer": hl})
    return flashcards
