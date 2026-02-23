import streamlit as st
import google.generativeai as genai
from PIL import Image

# Config
st.set_page_config(page_title="SnapDone Pro", page_icon="🎯")

# Custom CSS για Premium Mobile Feel
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: #121212; }
    
    /* Container για το UI */
    .app-box {
        background: #1e1e1e;
        border-radius: 25px;
        padding: 25px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }
    
    /* Τίτλος με Gradient */
    .title-text {
        background: linear-gradient(90deg, #00C853, #B2FF59);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 40px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* Στυλ Κάμερας */
    div[data-testid="stCameraInput"] {
        border-radius: 20px;
        overflow: hidden;
        border: 2px solid #4CAF50;
    }
    
    /* Premium Κουμπί */
    .stButton>button {
        background: #4CAF50;
        color: white;
        border-radius: 50px;
        height: 55px;
        font-size: 18px;
        letter-spacing: 1px;
        text-transform: uppercase;
        border: none;
        box-shadow: 0 4px 15px rgba(76,175,80,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# UI
st.markdown('<h1 class="title-text">SnapDone</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#aaa; margin-bottom:30px;'>Smart AI Document Scanner</p>", unsafe_allow_html=True)

# Camera Input
image_data = st.camera_input("")

if image_data:
    st.markdown('<div class="app-box">', unsafe_allow_html=True)
    if st.button("ΕΠΕΞΕΡΓΑΣΙΑ ΜΕ AI ✨"):
        with st.spinner("🧠 Το AI αναλύει την εικόνα..."):
            img = Image.open(image_data)
            prompt = "Είσαι ένας ψηφιακός βοηθός. Ανάλυσε την εικόνα. Αν είναι λογαριασμός βρες ποσό/ημερομηνία. Αν είναι σημείωση κάνε περίληψη. Απάντησε στα Ελληνικά με bullet points."
            response = model.generate_content([prompt, img])
            
            st.success("Ανάλυση Ολοκληρώθηκε!")
            st.markdown(f"<div style='color:white;'>{response.text}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
