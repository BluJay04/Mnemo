import streamlit as st
import requests

st.title("📚 AskMyBook – PDF/Image/Text Summarizer")

upload_option = st.radio("Choose input type:", ["Text", "PDF File", "Image"])

if upload_option == "Text":
    text_input = st.text_area("Paste book/chapter text:")
    if st.button("Summarize Text") and text_input.strip():
        with st.spinner("Summarizing..."):
            res = requests.post("http://localhost:8000/summarize", json={"text": text_input})
            st.success("Done!")
            st.write(res.json()["summary"])

elif upload_option == "PDF File":
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if st.button("Summarize PDF") and pdf_file:
        with st.spinner("Extracting and summarizing PDF..."):
            files = {"file": pdf_file.getvalue()}
            res = requests.post("http://localhost:8000/summarize/pdf", files=files)
            st.success("Done!")
            st.write(res.json()["summary"])

elif upload_option == "Image":
    img_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if st.button("Summarize Image") and img_file:
        with st.spinner("Extracting and summarizing image..."):
            files = {"file": img_file.getvalue()}
            res = requests.post("http://localhost:8000/summarize/image", files=files)
            st.success("Done!")
            st.write(res.json()["summary"])

st.header("🧠 Flashcard Generator")

passage = st.text_area("Enter a passage of text:")
highlight_text = st.text_input("Enter comma-separated keywords to generate questions on:")

if st.button("Generate Flashcards"):
    if passage and highlight_text:
        highlights = [h.strip() for h in highlight_text.split(",") if h.strip()]
        with st.spinner("Generating flashcards..."):
            res = requests.post("http://localhost:8000/flashcards", json={
                "text": passage,
                "highlights": highlights
            })
            flashcards = res.json()["flashcards"]
            st.subheader("📇 Generated Flashcards")
            for i, fc in enumerate(flashcards):
                st.markdown(f"**Q{i+1}:** {fc['question']}")
                st.markdown(f":orange[Answer:] {fc['answer']}")
    else:
        st.warning("Please enter both passage and highlight terms.")

st.header("🕒 Memory Recall Trainer")

st.write("Use this tool to decide if a flashcard should be reviewed now.")

last_time = st.date_input("Last Reviewed Date")
recall = st.selectbox("Recall Score", ["0 - Forgot", "1 - Hesitated", "2 - Perfect"])
seen_count = st.slider("Times Seen", 1, 10)
difficulty = st.selectbox("Difficulty", ["1 - Easy", "2 - Medium", "3 - Hard"])

if st.button("Check Review Status"):
    res = requests.post("http://localhost:8000/recency_score", json={
        "last_reviewed": last_time.isoformat(),
        "recall_score": int(recall[0]),
        "times_seen": seen_count,
        "difficulty": int(difficulty[0]),
    })
    result = res.json()
    st.subheader(f"🔁 Status: {result['status']}")
    st.write(f"Days Since Last Review: {result['days_since']}")
    st.write(f"Recommended Next Review After: {result['next_review_after']} days")
    st.progress(result['score'])
