import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Ρυθμίσεις Σελίδας
st.set_page_config(page_title="SnapDone AI", page_icon="🎯", layout="centered")

# 2. Επαγγελματικό CSS για Mobile Application Look
st.markdown("""
    <style>
    /* Κρύβουμε τα περιττά του Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: #0e1117; }
    
    /* Κάρτα Εφαρμογής */
    .app-card {
        background: #161b22;
        border-radius: 24px;
        padding: 20px;
        border: 1px solid #30363d;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    /* Custom Buttons για Μενού */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: #21262d;
        color: #58a6ff;
        border: 1px solid #30363d;
        font-weight: bold;
        transition: 0.2s;
    }
    .stButton>button:active { background: #58a6ff; color: white; }
    
    /* Κουμπί Ανάλυσης (Action) */
    .action-btn button {
        background: linear-gradient(90deg, #238636, #2ea043) !important;
        color: white !important;
        border: none !important;
    }
    
    .logo-text {
        font-size: 32px; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #58a6ff, #2ea043);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Setup Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. App UI
st.markdown('<div class="logo-text">SnapDone AI</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    
    # Το label=" " κρύβει το άσχημο κείμενο. Το uploader στο κινητό ανοίγει κάμερα/gallery.
    uploaded_file = st.file_uploader(" ", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, use_container_width=True)
        
        st.markdown("### 🛠️ Επιλέξτε Ενέργεια")
        
        # Το Μενού σου
        col1, col2 = st.columns(2)
        with col1:
            mode_cal = st.button("📅 Ημερολόγιο")
            mode_ocr = st.button("📝 Ψηφιοποίηση")
        with col2:
            mode_pdf = st.button("📄 Εξαγωγή PDF")
            mode_sum = st.button("🔍 Περίληψη")
            
        # Επιλογή Prompt βάσει μενού
        prompt = ""
        if mode_cal: prompt = "Βρες ημερομηνίες και ποσά για καταχώρηση στο Calendar."
        if mode_ocr: prompt = "Μετέτρεψε την εικόνα σε καθαρό κείμενο (OCR)."
        if mode_pdf: prompt = "Οργάνωσε το κείμενο για επίσημο έγγραφο PDF."
        if mode_sum: prompt = "Κάνε μια γρήγορη και επαγγελματική περίληψη."

        if prompt:
            with st.spinner("⏳ Επεξεργασία..."):
                response = model.generate_content([f"{prompt} Απάντησε στα Ελληνικά.", img])
                st.markdown("---")
                st.write(response.text)
                
    st.markdown('</div>', unsafe_allow_html=True)
