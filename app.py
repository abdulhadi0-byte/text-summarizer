import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI Text Summarizer", page_icon="📝", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.main { background-color: #0a0a0f; }

.hero {
    text-align: center;
    padding: 40px 20px;
    background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
    border-radius: 20px;
    margin-bottom: 30px;
    border: 1px solid #ffffff15;
}

.hero h1 { font-size: 2.5rem; color: white; margin-bottom: 10px; }
.hero p { color: #aaaacc; font-size: 1.1rem; }

.summary-box {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    padding: 25px;
    border-radius: 15px;
    border-left: 4px solid #7c3aed;
    color: white;
    margin-top: 20px;
    font-size: 1rem;
    line-height: 1.7;
}

.stats-box {
    background-color: #1a1a2e;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    color: #aaaacc;
    border: 1px solid #ffffff15;
}

.stTextArea > div > div > textarea {
    background-color: #1a1a2e !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #7c3aed !important;
    font-size: 1rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    border-radius: 12px;
    width: 100%;
    padding: 14px;
    font-size: 1.1rem;
    font-weight: 600;
    border: none;
    margin-top: 10px;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #6d28d9, #4338ca);
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>📝 AI Text Summarizer</h1>
    <p>Paste any long text and get a smart AI-powered summary instantly</p>
</div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    with st.spinner("🔄 Loading AI model for the first time..."):
        return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_model()

text = st.text_area(
    "📄 Paste your text below:",
    height=250,
    placeholder="Paste any article, essay, or long text here and click Summarize..."
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""<div class="stats-box">📊 Words<br><b>{len(text.split()) if text else 0}</b></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="stats-box">🔤 Characters<br><b>{len(text) if text else 0}</b></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="stats-box">📝 Sentences<br><b>{text.count('.') if text else 0}</b></div>""", unsafe_allow_html=True)

if st.button("⚡ Summarize Now"):
    if text.strip():
        if len(text.split()) < 30:
            st.warning("⚠️ Please enter at least 30 words for a good summary.")
        else:
            with st.spinner("🤔 AI is summarizing your text..."):
                summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
                result = summary[0]['summary_text']

            st.markdown(f"""
            <div class="summary-box">
                <b>✨ AI Summary:</b><br><br>{result}
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="📥 Download Summary",
                data=result,
                file_name="summary.txt",
                mime="text/plain"
            )
    else:
        st.warning("⚠️ Please enter some text first.")