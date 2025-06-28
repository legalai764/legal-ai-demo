
import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
import os
import re

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page configuration
st.set_page_config(page_title="Legal.AI - Decode Indian Property Documents", layout="wide")
st.markdown(
    '''
    <style>
    body { background-color: #0e1117; color: white; }
    .stApp { background-color: #0e1117; }
    .title { font-size: 2.5em; font-weight: bold; }
    .subtitle { font-size: 1.5em; }
    </style>
    ''',
    unsafe_allow_html=True
)

# --- Logo and Title ---
st.image("https://via.placeholder.com/160x60?text=Legal.AI", width=160)
st.markdown("<div class='title'>Decode Indian Property Documents with AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload property PDFs and get instant legal insights, clause tagging, and summaries.</div>", unsafe_allow_html=True)
st.markdown("---")

# --- Upload Section ---
uploaded_file = st.file_uploader("📄 Upload your property document (PDF only)", type=["pdf"])
document_text = ""

if uploaded_file:
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            document_text += page.get_text()
    st.success("✅ Document parsed successfully!")

    st.markdown("### 🧠 Auto-Extracted Key Clauses:")
    clauses = {
        "Owner": re.findall(r"(?:owner(?:\s*is)?|in favour of)\s*([A-Z][a-zA-Z\s]+)", document_text, re.IGNORECASE),
        "Property Location": re.findall(r"located at\s+([^\n,.]+)", document_text, re.IGNORECASE),
        "Survey Number": re.findall(r"Survey No[:.]?\s*([\w\d/-]+)", document_text, re.IGNORECASE),
        "Sale Consideration": re.findall(r"Rs\.?\s?([\d,]+)", document_text)
    }
    for key, value in clauses.items():
        if value:
            st.markdown(f"**{key}:** {value[0]}")
        else:
            st.markdown(f"**{key}:** Not found")

    st.markdown("---")

    # --- Question Answering ---
    question = st.text_input("💬 Ask a legal question about this document")
    if question:
        with st.spinner("Thinking..."):
            full_prompt = f"The following is a property document in India:\n\n{document_text[:3000]}\n\nQuestion: {question}"
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a legal expert specialized in Indian property law."},
                        {"role": "user", "content": full_prompt}
                    ]
                )
                reply = response.choices[0].message.content
                st.markdown("### 🔍 Answer:")
                st.markdown(reply)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    st.markdown("---")

    # --- Summary ---
    if st.button("📑 Generate Legal Summary"):
        with st.spinner("Summarizing..."):
            try:
                summary_prompt = f"Summarize this Indian property document for a legal layperson:\n\n{document_text[:3000]}"
                summary_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Summarize Indian legal documents simply."},
                        {"role": "user", "content": summary_prompt}
                    ]
                )
                st.markdown("### 📄 Document Summary:")
                st.markdown(summary_response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error generating summary: {str(e)}")
