import streamlit as st
from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import torch

# Custom text extractors
from research import extract_pdf         # Your PDF extractor function
from blog import extract_text_from_url   # Your URL/blog text extractor



import base64

def get_download_link(text, filename="summary.txt"):
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Summary as TXT</a>'
    return href



# ===== Page Setup =====
st.set_page_config(page_title="AI Summarizer", page_icon="📄")
st.title("📄 AI Text Summarizer")
st.markdown("Summarize content from **PDF files** or **web articles/blogs**.")

# ===== Load PEGASUS model and tokenizer =====
@st.cache_resource
def load_model():
    model_name = "google/pegasus-cnn_dailymail"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return tokenizer, model.to(device), device

tokenizer, model, device = load_model()

# ===== Helper Functions =====

def split_into_chunks(text, max_words=700):
    words = text.split()
    return [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def summarize_chunks(text, tokenizer, model, device):
    chunks = split_into_chunks(text)
    all_summaries = []

    for i, chunk in enumerate(chunks):
        inputs = tokenizer(
            chunk,
            truncation=True,
            padding="longest",
            max_length=1024,
            return_tensors="pt"
        ).to(device)

        summary_ids = model.generate(
            **inputs,
            max_length=180,
            min_length=60,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )

        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        all_summaries.append(summary)

    return '\n\n'.join(all_summaries)

# ===== UI Input Options =====

option = st.radio("Choose your input source:", ("📄 Upload PDF", "🌐 Enter URL / Blog"))

raw_text = ""

# === PDF Upload ===
if option == "📄 Upload PDF":
    uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        raw_text = extract_pdf("temp.pdf")
        st.success("✅ Text extracted from PDF!")

# === URL Input ===
elif option == "🌐 Enter URL / Blog":
    url = st.text_input("Paste the article or blog URL below:")
    if url:
        raw_text = extract_text_from_url(url)
        st.success("✅ Text extracted from URL!")

# === Summarization Button ===
if raw_text:
    if st.button("🧠 Summarize Text"):
        with st.spinner("Summarizing in chunks..."):
            final_summary = summarize_chunks(raw_text, tokenizer, model, device)
            st.subheader("📝 Summary")
            st.write(final_summary)
            st.markdown(get_download_link(final_summary), unsafe_allow_html=True)



# After: st.write(final_summary)

