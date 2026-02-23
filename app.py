import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse

# 1. Ρύθμιση Σελίδας (Πρέπει να είναι η πρώτη εντολή Streamlit)
st.set_page_config(
    page_title="SnapDone AI", 
    page_icon="🎯", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Επαγγελματικό CSS για Mobile App Εμφάνιση
st.markdown("""
    <style>
    /* Γραμματοσειρά και Φόντο */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: #f8f9fa;
    }

    /* Στυλ για την Κάρτα Αποτελεσμάτων */
    .result-card {
        background-color: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 20px;
        border-left: 5px solid #4CAF50;
    }

    /* Στυλ για το Κουμπί Ανάλυσης */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 3.5em;
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 10px rgba(76,175,80,0.3);
    }

    /* Απόκρυψη στοιχείων Streamlit για καθαρό look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 3. Σύνδεση με το Gemini API
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("⚠️ Ξέχασες να βάλεις το API Key στα Secrets του Streamlit!")
    st.stop()

# 4. UI Εφαρμογής
st.title("🎯 SnapDone")
st.write("Η ζωή σου σε μια φωτογραφία. Οργάνωσε τα πάντα αμέσως.")

# Uploader που ανοίγει κάμερα στο κινητό
uploaded_file = st.file_uploader("Βγάλε φωτό ή διάλεξε από τη συλλογή", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Εμφάνιση της φωτογραφίας
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Ανάλυση & Οργάνωση ✨"):
        with st.spinner("Το AI μελετάει τη φωτογραφία..."):
            # Το Prompt που δίνει οδηγίες στο AI
            prompt = """
            Λειτούργησε ως προσωπικός βοηθός. Ανάλυσε την εικόνα και δώσε μου στα Ελληνικά:
            1. Έναν τίτλο για το τι βλέπεις.
            2. Μια σύντομη περίληψη.
            3. Τρία (3) συγκεκριμένα βήματα (Action Items) που πρέπει να γίνουν.
            
            Αν βρεις ημερομηνία λήξης ή ραντεβού, γράψε στο τέλος ακριβώς: 
            DATE:ΕΕΕΕΜΜΔΔ (π.χ. DATE:20260520). Αν όχι, γράψε DATE:NONE.
            """
            
            response = model.generate_content([prompt, image])
            output = response.text
            
            # Διαχωρισμός κειμένου από την ημερομηνία
            if "DATE:" in output:
                clean_text = output.split("DATE:")[0]
                found_date = output.split("DATE:")[1].strip()
            else:
                clean_text = output
                found_date = "NONE"

            # Εμφάνιση Αποτελέσματος
            st.markdown(f'<div class="result-card">{clean_text}</div>', unsafe_allow_html=True)

            # 5. Δημιουργία Google Calendar Link αν υπάρχει ημερομηνία
            if found_date != "NONE" and len(found_date) >= 8:
                # Φτιάχνουμε ένα link που ανοίγει το Google Calendar
                event_title = urllib.parse.quote("Υπενθύμιση SnapDone")
                cal_url = f"https://www.google.com/calendar/render?action=TEMPLATE&text={event_title}&dates={found_date}/{found_date}"
                
                st.markdown(f"""
                    <a href="{cal_url}" target="_blank">
                        <button style="width:100%; border-radius:15px; height:3em; background-color:#4285F4; color:white; border:none; font-weight:bold; margin-top:15px; cursor:pointer;">
                            📅 Προσθήκη στο Google Calendar
                        </button>
                    </a>
                    """, unsafe_allow_html=True)

st.divider()
st.caption("SnapDone AI v1.0 - Δημιουργήθηκε από έναν PhD ερευνητή.")
