import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
from fpdf import FPDF
import base64

# 1. Βασικές Ρυθμίσεις & UI
st.set_page_config(page_title="SnapDone Pro", page_icon="🎯")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: #0F1116; color: #E0E0E0; }
    
    /* App Container */
    .app-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 10px;
    }
    
    /* Neon Button Style */
    .stButton>button {
        background: linear-gradient(90deg, #00F260 0%, #0575E6 100%);
        color: white; border: none; border-radius: 12px;
        font-weight: bold; height: 3.5em; width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); opacity: 0.9; }
    
    /* Menu Styling */
    .menu-label { font-size: 14px; color: #888; margin-bottom: 10px; font-weight: bold; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Setup
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Functions
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Arial', '', '', uni=True) # Για ελληνικά αν χρειαστεί
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    return pdf.output(dest='S').encode('latin-1')

# 4. Main App UI
st.title("🎯 SnapDone")
st.markdown("<p style='color:#888;'>Smart AI Document Handler</p>", unsafe_allow_html=True)

# Το File Uploader στο κινητό δίνει επιλογή και για Camera και για Gallery
uploaded_file = st.file_uploader("📸 Λήψη ή Μεταφόρτωση", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, use_container_width=True)
    
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown('<p class="menu-label">Επιλέξτε Ενέργεια</p>', unsafe_allow_html=True)
    
    # Smart Menu με Columns
    col1, col2 = st.columns(2)
    
    with col1:
        btn_cal = st.button("📅 Στο Ημερολόγιο")
        btn_ocr = st.button("📝 Ψηφιοποίηση")
    
    with col2:
        btn_pdf = st.button("📄 Εξαγωγή PDF")
        btn_sum = st.button("🔍 Περίληψη")

    # Processing Logic
    action_prompt = ""
    if btn_cal: action_prompt = "Βρες ημερομηνία, ώρα και τίτλο για Calendar event. Δώσε ημερομηνία σε μορφή YYYYMMDD."
    if btn_ocr: action_prompt = "Μετέτρεψε την εικόνα σε καθαρό κείμενο (OCR). Διατήρησε τη δομή."
    if btn_pdf: action_prompt = "Κάνε πλήρη ψηφιοποίηση εγγράφου για δημιουργία αρχείου PDF."
    if btn_sum: action_prompt = "Κάνε μια γρήγορη περίληψη των βασικών σημείων του εγγράφου."

    if action_prompt:
        with st.spinner("🤖 Το AI επεξεργάζεται..."):
            response = model.generate_content([action_prompt + " Απάντησε στα Ελληνικά.", img])
            res_text = response.text
            
            st.markdown("### ⚡ Αποτέλεσμα")
            st.write(res_text)
            
            # Ειδικά κουμπιά ανάλογα την ενέργεια
            if btn_cal:
                # Απλό link για Google Calendar
                st.info("💡 Μπορείς να αντιγράψεις την ημερομηνία στο Calendar σου!")
                
            if btn_pdf:
                # Δημιουργία PDF Download Link
                pdf_data = res_text # Εδώ θα μπορούσε να γίνει πιο σύνθετο
                st.download_button("📥 Λήψη Αρχείου PDF", data=res_text, file_name="snapdone_export.txt")

    st.markdown('</div>', unsafe_allow_html=True)
