import streamlit as st
import google.generativeai as genai
from PIL import Image

# Διαβάζει το κλειδί από τα Secrets του Streamlit (ασφάλεια)
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

st.set_page_config(page_title="Snap-to-Done", page_icon="📸")

st.title("📸 Snap-to-Done AI")
st.write("Βγάλε μια φωτογραφία και θα σου πω τι πρέπει να κάνεις!")

uploaded_file = st.file_uploader("Ανέβασε φωτό...", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    if st.button("Ανάλυση ✨"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        with st.spinner("Το AI μελετάει..."):
            response = model.generate_content([
                "Λειτούργησε ως προσωπικός βοηθός. Ανάλυσε την εικόνα και δώσε μου 3 σύντομα βήματα (action items) στα ελληνικά.", 
                image
            ])
            st.success("Έτοιμο!")
            st.write(response.text)
