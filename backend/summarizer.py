from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

def generate_summary(text: str, max_length=150, min_length=30) -> str:
    if not text.strip():
        return "No text provided for summarization."

    # HuggingFace requires a prefix for T5
    input_text = "summarize: " + text.strip()
    summary = summarizer(input_text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']
