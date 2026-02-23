import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Config & Styling
st.set_page_config(page_title="SnapDone Pro", page_icon="🎯")

st.markdown("""
    <style>
    /* Απόκρυψη Streamlit UI */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Φόντο με Gradient */
    .stApp {
        background: radial-gradient(circle at top, #1a1a1a, #000000);
        color: white;
    }

    /* Glassmorphism Card */
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-top: -50px;
    }

    /* Τίτλος με εφέ Neon */
    .logo {
        font-size: 50px;
        font-weight: 900;
        background: linear-gradient(to right, #00ff88, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 10px 20px rgba(0, 255, 136, 0.3);
    }

    /* Επαγγελματικό Κουμπί */
    .stButton>button {
        background: linear-gradient(90deg, #00ff88 0%, #00bd68 100%);
        border: none;
        color: black;
        font-weight: 800;
        padding: 15px 30px;
        border-radius: 50px;
        width: 100%;
        font-size: 18px;
        text-transform: uppercase;
        transition: 0.3s all;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 20px rgba(0, 255, 136, 0.6);
    }

    /* Στυλ για την κάμερα */
    div[data-testid="stCameraInput"] {
        border-radius: 20px;
        border: 2px solid #00ff88;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Logic
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. UI Layout
st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
st.markdown('<h1 class="logo">SnapDone</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888;">AI-Powered Personal Assistant</p>', unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)
img_data = st.camera_input("")

if img_data:
    if st.button("🚀 ΕΝΑΡΞΗ ΑΝΑΛΥΣΗΣ"):
        with st.spinner("⏳ Επεξεργασία..."):
            img = Image.open(img_data)
            prompt = "Ανάλυσε την εικόνα σαν επαγγελματίας βοηθός. Δώσε τίτλο και 3 action items στα Ελληνικά με ωραία μορφοποίηση."
            response = model.generate_content([prompt, img])
            
            st.markdown("### 📋 Αποτέλεσμα")
            st.info(response.text)
st.markdown('</div>', unsafe_allow_html=True)
