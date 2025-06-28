import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Legal.AI - Property Doc Analyzer", layout="wide")

st.title("📄 Legal.AI - Indian Property Document Analyzer")
st.markdown("""
Upload large property-related PDFs (Sale Deeds, JDAs, Title Docs) and get targeted legal insights in seconds.
""")

# Sidebar upload
with st.sidebar:
    st.header("🧾 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    user_question = st.text_input("💬 Ask a question about the document", placeholder="e.g. Is the land RERA approved?")
    submit_btn = st.button("🔍 Analyze")

# If PDF is uploaded and button is clicked
if uploaded_file and submit_btn:
    reader = PdfReader(uploaded_file)
    num_pages = len(reader.pages)

    with st.spinner("Reading document and preparing analysis..."):
        # Simulated document scan
        doc_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        st.success("✅ Document loaded successfully!")

        st.subheader("📑 Basic Document Info")
        st.write(f"**Total Pages:** {num_pages}")

        st.subheader("🧠 AI Summary (Sample)")
        st.markdown("""
- ✅ Title appears marketable  
- 🚫 No RERA number found  
- ⚠️ Missing municipal/building approval reference  
- 📅 Completion deadline: 31/12/2025  
- 📝 Termination clause exists but is vague
        """)

        st.subheader("📄 Clause Snippets (Example)")
        st.code("Clause 5.2: The Allottee shall pay the builder 20% advance within 15 days.")
        st.code("Clause 8.1: The builder reserves the right to delay possession by 6 months.")

        if user_question:
            st.subheader("🔎 Answer to Your Question")
            st.info(f"**Q:** {user_question}\n\n**A:** Based on our scan, no RERA approval number is mentioned in the agreement.")
        
        st.markdown("---")
        st.caption("This is a demo. For legal verification, consult a licensed real estate lawyer.")
else:
    st.warning("⚠️ Upload a PDF and enter a question to begin analysis.")