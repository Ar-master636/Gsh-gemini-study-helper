import streamlit as st
import os
from google import genai
from google.genai import types

# --- 1. A E S T H E T I C S ---
# Set the page configuration for a clean, focused look
st.set_page_config(
    page_title="✨ GSF: Study Vibes Only", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for that Gen Z polish (Dark Mode base, vibrant accents)
st.markdown("""
<style>
/* 1. Dark Mode Base (assuming Streamlit theme is dark) */
.stApp {
    background-color: #121212; /* Deep Black/Gray */
    color: #F0F0F0; /* Off-White Text */
}

/* 2. Custom Title Styling (Vibrant Accent) */
h1 {
    color: #8C9EFF; /* Soft Lavender/Blue */
    text-align: center;
    font-weight: 800; /* Extra Bold */
}

/* 3. Button Vibe (Aesthetic Button Look) */
.stButton>button {
    background-color: #FF5E5E; /* Punchy Pink/Coral */
    color: white;
    font-weight: bold;
    border-radius: 12px; /* Soft, modern corners */
    padding: 10px 20px;
    transition: all 0.2s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* Subtle Shadow */
}
.stButton>button:hover {
    background-color: #FF8F8F; /* Lighter Pink on Hover */
    transform: translateY(-2px);
}

/* 4. Text Input Area */
textarea {
    border-radius: 10px;
    border: 1px solid #444444; 
    background-color: #1E1E1E; /* Slightly Lighter input field */
}

/* 5. Subheaders (Use a secondary accent color) */
h2, h3 {
    color: #4BC0C8; /* Teal/Aqua Accent */
    border-bottom: 2px solid #4BC0C8;
    padding-bottom: 5px;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# --- 2. Configuration & Initialization ---
# Streamlit Community Cloud uses st.secrets for secure API key storage.
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # Error message shown if the key is missing during deployment
    st.error("🔑 Need the API key, fam. Check your Streamlit secrets or env vars.")
    st.stop()
    
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Error initializing Gemini: {e}")
    st.stop()
    
# --- 3. Gemini Prompt (Updated for Gen Z tone/output) ---
@st.cache_data(show_spinner="🪡 Forging the notes... hold tight.")
def generate_study_notes(raw_content: str):
    """Sends content to the Gemini API and returns structured study notes."""
    
    # The aesthetic prompt that guides the AI's output style
    prompt = f"""
    You are a professional study genius. Your only task is to transform the provided raw content into highly aesthetic, structured, and easy-to-digest study notes. You must use Markdown and engaging emojis.

    1. **Vibe Check Summary:** Start with a 1-2 sentence **bold** summary of the core topic, like a TikTok caption.
    2. **🧠 Core Takeaways:** Use 5-7 concise bullet points. Start each with an engaging emoji.
    3. **✨ Key Terms & Definitions:** Create a table for quick reference.
    4. **💡 The Main Event:** Use H3 headings to break down the main content into digestible chunks.

    --- RAW CONTENT ---
    {raw_content}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        return response.text
    except Exception as e:
        return f"An error occurred while generating notes: {e}"

# --- 4. S T R E A M L I T  UI  ---

st.title("✨ GSF: Study Vibes Only")
st.markdown("### **Input your brain dump, get instant, aesthetic notes.** No cap. 👇")

# Input Area
input_content = st.text_area(
    "Paste the Tea ☕ (Lecture, Article, Transcript)",
    height=300,
    placeholder="Drop the raw info here... the longer the better, tbh.",
)

# Button and Logic
if st.button("🚀 FORGE THE NOTES", use_container_width=True):
    if len(input_content) < 50:
        st.warning("🤏 Need more content than that, bestie (min 50 chars).")
    else:
        # Call the aesthetic AI function
        study_notes = generate_study_notes(input_content)
        
        # Display the output
        st.subheader("🎉 Your Notes Just Dropped")
        
        # Render the aesthetically pleasing markdown
        st.markdown(study_notes)

st.divider()
st.caption("Powered by Google's Gemini. Built with 💖 for maximum productivity.")
