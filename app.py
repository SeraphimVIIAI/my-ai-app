import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config με Dark Theme look
st.set_page_config(page_title="SnapDone", page_icon="🎯", layout="centered")

# 2. Advanced CSS για να κρύψουμε τα πάντα και να μοιάζει με App
st.markdown("""
    <style>
    /* Κρύβει το menu και το header του Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background και Card style */
    .stApp {
        background-color: #0E1117;
    }
    
    .main-container {
        background: #1E1E1E;
        padding: 25px;
        border-radius: 30px;
        border: 1px solid #333;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center;
    }
    
    h1 {
        color: #4CAF50 !important;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Στυλ για τα κουμπιά */
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 4em;
        background: linear-gradient(90deg, #4CAF50 0%, #2E7D32 100%);
        border: none;
        color: white;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
    }
    
    /* Στυλ για το κείμενο αποτελέσματος */
    .result-text {
        background: #2D2D2D;
        color: #E0E0E0;
        padding: 20px;
        border-radius: 20px;
        margin-top: 20px;
        line-height: 1.6;
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. API Setup
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. App UI
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("🎯 SnapDone")
st.write("📸 Βγάλε μια φωτογραφία για να ξεκινήσεις")

# Χρησιμοποιούμε st.camera_input αντί για file_uploader για "App" αίσθηση
img_file = st.camera_input("") 

if img_file:
    image = Image.open(img_file)
    
    if st.button("ΑΝΑΛΥΣΗ ΤΩΡΑ ✨"):
        with st.spinner("Το AI οργανώνει τα πάντα..."):
            prompt = "Λειτούργησε ως προσωπικός βοηθός. Ανάλυσε την εικόνα και δώσε 3 σύντομα βήματα στα ελληνικά με emojis."
            response = model.generate_content([prompt, image])
            
            st.markdown(f'<div class="result-text">{response.text}</div>', unsafe_allow_html=True)
            
st.markdown('</div>', unsafe_allow_html=True)
