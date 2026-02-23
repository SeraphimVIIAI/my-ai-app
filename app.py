import streamlit as st
import google.generativeai as genai
from PIL import Image
from fpdf import FPDF
import base64

# Page Config
st.set_page_config(page_title="SnapDone Dashboard", page_icon="💼", layout="centered")

# Επαγγελματικό Dark UI
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #0b0e11; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #00C853 0%, #009624 100%);
        color: white; font-weight: bold; border: none;
    }
    .action-card {
        background: #1c1f26; border-radius: 15px; padding: 20px;
        border: 1px solid #30363d; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# API Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("💼 SnapDone Business")
st.write("Ανέβασε ένα έγγραφο ή λογαριασμό για άμεση επεξεργασία.")

# Uploader (Ανοίγει κάμερα στο κινητό)
file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)
    
    st.markdown('<div class="action-card">', unsafe_allow_html=True)
    st.subheader("Επιλέξτε Λειτουργία")
    
    col1, col2 = st.columns(2)
    with col1:
        task_cal = st.button("📅 Εξαγωγή για Calendar")
        task_ocr = st.button("📝 Ψηφιοποίηση Κειμένου")
    with col2:
        task_sum = st.button("🔍 Σύνοψη Εγγράφου")
        task_pdf = st.button("📄 Δημιουργία PDF")

    prompt = ""
    if task_cal: prompt = "Βρες ημερομηνία λήξης και ποσό. Δώσε μου μόνο τα απαραίτητα για Calendar."
    if task_ocr: prompt = "Κάνε OCR και δώσε μου όλο το κείμενο του εγγράφου καθαρά."
    if task_sum: prompt = "Κάνε μια επαγγελματική σύνοψη των κυριότερων σημείων."
    if task_pdf: prompt = "Μετέτρεψε το έγγραφο σε δομημένο κείμενο για αρχειοθέτηση PDF."

    if prompt:
        with st.spinner("🤖 Το AI επεξεργάζεται..."):
            response = model.generate_content([f"{prompt} Απάντησε στα Ελληνικά.", img])
            result = response.text
            st.markdown("---")
            st.markdown(result)
            
            if task_pdf:
                # Απλή λήψη ως κείμενο/PDF
                st.download_button("📥 Λήψη Αρχείου", result, file_name="snapdone_export.txt")
    st.markdown('</div>', unsafe_allow_html=True)
