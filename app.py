import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SnapDone AI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# 2. CSS — Dark Glassmorphism
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; }
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }

.stApp {
    background: #04050a;
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
}

/* Ambient blobs */
.stApp::before {
    content: '';
    position: fixed; top: -30%; left: -15%;
    width: 650px; height: 650px;
    background: radial-gradient(circle, rgba(99,102,241,0.16) 0%, transparent 70%);
    animation: blob1 14s ease-in-out infinite alternate;
    pointer-events: none; z-index: 0;
}
.stApp::after {
    content: '';
    position: fixed; bottom: -25%; right: -10%;
    width: 550px; height: 550px;
    background: radial-gradient(circle, rgba(16,185,129,0.13) 0%, transparent 70%);
    animation: blob2 17s ease-in-out infinite alternate;
    pointer-events: none; z-index: 0;
}
@keyframes blob1 { from{transform:translate(0,0) scale(1);} to{transform:translate(50px,35px) scale(1.12);} }
@keyframes blob2 { from{transform:translate(0,0) scale(1);} to{transform:translate(-40px,-25px) scale(1.18);} }

.block-container {
    max-width: 500px !important;
    padding: 1.5rem 1rem 5rem !important;
    position: relative; z-index: 1;
}

/* ── LOGO ── */
.snap-logo {
    text-align: center;
    margin-bottom: 1.8rem;
    animation: fadeDown .7s ease both;
}
.snap-logo .icon {
    font-size: 52px;
    display: block; margin-bottom: 6px;
    animation: pulseGlow 3s ease-in-out infinite;
}
@keyframes pulseGlow {
    0%,100% { filter: drop-shadow(0 0 12px rgba(99,102,241,.6)); }
    50%      { filter: drop-shadow(0 0 28px rgba(16,185,129,.8)); }
}
.snap-logo .title {
    font-family: 'Syne', sans-serif;
    font-size: 38px; font-weight: 800; letter-spacing: -1.5px;
    background: linear-gradient(135deg, #818cf8 0%, #34d399 55%, #818cf8 100%);
    background-size: 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 5s linear infinite;
}
.snap-logo .tagline {
    color: rgba(255,255,255,.3); font-size: 11px;
    letter-spacing: 3px; text-transform: uppercase;
    margin-top: 4px; font-weight: 300;
}
@keyframes shimmer { 0%{background-position:0% 50%;} 100%{background-position:200% 50%;} }
@keyframes fadeDown { from{opacity:0;transform:translateY(-18px);} to{opacity:1;transform:translateY(0);} }
@keyframes fadeUp   { from{opacity:0;transform:translateY(14px);}  to{opacity:1;transform:translateY(0);} }

/* ── GLASS CARD ── */
.glass {
    background: rgba(255,255,255,.04);
    backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 22px; padding: 20px;
    box-shadow: 0 8px 40px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.07);
    margin-bottom: 14px;
    animation: fadeUp .5s ease both;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: rgba(99,102,241,.06) !important;
    border: 2px dashed rgba(99,102,241,.4) !important;
    border-radius: 18px !important;
    padding: 8px !important;
    transition: all .3s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(99,102,241,.75) !important;
    background: rgba(99,102,241,.1) !important;
}
[data-testid="stFileUploader"] label { display: none !important; }
[data-testid="stFileUploadDropzone"] {
    color: rgba(255,255,255,.4) !important;
}

/* ── IMAGE ── */
[data-testid="stImage"] img {
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,.5) !important;
}

/* ── DETECT BADGE ── */
.detect-badge {
    display: flex; align-items: center; gap: 12px;
    background: rgba(52,211,153,.09);
    border: 1px solid rgba(52,211,153,.28);
    border-radius: 14px; padding: 12px 16px;
    margin: 14px 0; animation: fadeUp .4s ease both;
}
.detect-badge .di { font-size: 26px; }
.detect-badge .dt { color: #34d399; font-weight: 500; font-size: 14px; line-height: 1.5; }
.detect-badge .dl { color: rgba(255,255,255,.35); font-size: 10px;
                    text-transform: uppercase; letter-spacing: 1.5px; }

/* ── SECTION LABEL ── */
.sec-label {
    font-family: 'Syne', sans-serif;
    font-size: 10px; font-weight: 700;
    letter-spacing: 3px; text-transform: uppercase;
    color: rgba(255,255,255,.28); margin: 14px 0 10px;
}

/* ── BUTTONS ── */
.stButton > button {
    width: 100% !important;
    background: rgba(255,255,255,.05) !important;
    border: 1px solid rgba(255,255,255,.1) !important;
    border-radius: 13px !important;
    color: rgba(255,255,255,.78) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important; font-weight: 500 !important;
    height: auto !important; padding: 10px 14px !important;
    transition: all .22s ease !important;
    text-align: left !important;
}
.stButton > button:hover {
    background: rgba(99,102,241,.22) !important;
    border-color: rgba(99,102,241,.55) !important;
    color: #fff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 22px rgba(99,102,241,.25) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Primary / Auto-detect button — first column */
.primary-btn .stButton > button {
    background: linear-gradient(135deg, rgba(99,102,241,.35), rgba(52,211,153,.25)) !important;
    border-color: rgba(99,102,241,.55) !important;
    color: #fff !important;
    font-weight: 600 !important;
}

/* ── RESULT BOX ── */
.result-box {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.08);
    border-left: 3px solid #6366f1;
    border-radius: 16px; padding: 18px;
    color: rgba(255,255,255,.82);
    line-height: 1.75; font-size: 14px;
    margin-top: 14px; animation: fadeUp .4s ease both;
    white-space: pre-wrap; word-break: break-word;
}
.result-label {
    font-family: 'Syne', sans-serif;
    font-size: 10px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    color: #818cf8; margin-bottom: 10px;
}

/* ── DOWNLOAD BTN ── */
[data-testid="stDownloadButton"] button {
    width: 100% !important;
    background: linear-gradient(135deg, #6366f1, #34d399) !important;
    border: none !important; border-radius: 13px !important;
    color: #fff !important; font-weight: 600 !important;
    font-size: 14px !important; padding: 11px !important;
    margin-top: 10px !important;
    box-shadow: 0 4px 20px rgba(99,102,241,.4) !important;
    transition: all .22s !important;
}
[data-testid="stDownloadButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(99,102,241,.55) !important;
}

/* ── vCARD PRE ── */
.vcard-pre {
    background: rgba(0,0,0,.35);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 10px; padding: 12px;
    font-family: 'Courier New', monospace;
    font-size: 11px; color: rgba(255,255,255,.5);
    margin-top: 10px; white-space: pre-wrap;
}

/* ── UPLOAD HINT ── */
.up-hint {
    text-align: center; padding: 28px 16px;
    color: rgba(255,255,255,.28); animation: fadeUp .6s ease both;
}
.up-hint .uhi { font-size: 52px; opacity:.55; display: block; margin-bottom:10px; }
.up-hint .uht { font-family:'Syne',sans-serif; font-size:16px;
                color:rgba(255,255,255,.45); margin-bottom:6px; }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,.1); border-radius: 4px; }

/* ── TEXT / MARKDOWN ── */
.stMarkdown p, .stMarkdown li { color: rgba(255,255,255,.7) !important; font-size: 14px !important; }

/* ── RADIO (input mode selector) ── */
[data-testid="stRadio"] > div {
    display: flex !important; gap: 8px !important;
    background: rgba(0,0,0,.25) !important;
    border-radius: 12px !important; padding: 4px !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    margin-bottom: 12px !important;
}
[data-testid="stRadio"] label {
    flex: 1 !important; text-align: center !important;
    border-radius: 9px !important; padding: 7px 4px !important;
    cursor: pointer !important; transition: all .2s !important;
    color: rgba(255,255,255,.5) !important; font-size: 13px !important;
    font-weight: 500 !important;
}
[data-testid="stRadio"] label:has(input:checked) {
    background: rgba(99,102,241,.35) !important;
    color: #fff !important;
    box-shadow: 0 2px 10px rgba(99,102,241,.3) !important;
}
[data-testid="stRadio"] input[type=radio] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. GEMINI SETUP
# ─────────────────────────────────────────────
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# ─────────────────────────────────────────────
# 4. HELPERS
# ─────────────────────────────────────────────
def ai(prompt: str, img) -> str:
    import io as _io
    buf = _io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    img_part = {"mime_type": "image/jpeg", "data": buf.getvalue()}
    r = model.generate_content([prompt + "\n\nΑπάντα πάντα στα Ελληνικά.", img_part])
    return r.text.strip()

def make_pdf(title: str, body: str) -> bytes:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import cm
        from reportlab.lib.colors import HexColor

        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4,
                                leftMargin=2.5*cm, rightMargin=2.5*cm,
                                topMargin=2.5*cm, bottomMargin=2.5*cm)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('T', parent=styles['Title'],
                                     fontSize=20, textColor=HexColor('#6366f1'),
                                     spaceAfter=18, fontName='Helvetica-Bold')
        body_style  = ParagraphStyle('B', parent=styles['Normal'],
                                     fontSize=11, leading=18,
                                     textColor=HexColor('#1a1a2e'), spaceAfter=6)
        story = [Paragraph(title, title_style), Spacer(1, 8)]
        safe = lambda t: t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        for line in body.split('\n'):
            story.append(Paragraph(safe(line), body_style) if line.strip() else Spacer(1, 5))
        doc.build(story)
        return buf.getvalue()
    except Exception:
        return body.encode('utf-8')

def make_vcard(name, company, role, phone, email, website, address) -> str:
    lines = ["BEGIN:VCARD", "VERSION:3.0"]
    if name:    lines.append(f"FN:{name}")
    if company: lines.append(f"ORG:{company}")
    if role:    lines.append(f"TITLE:{role}")
    if phone:   lines.append(f"TEL;TYPE=WORK:{phone}")
    if email:   lines.append(f"EMAIL;TYPE=WORK:{email}")
    if website: lines.append(f"URL:{website}")
    if address: lines.append(f"ADR:;;{address};;;;")
    lines.append("END:VCARD")
    return "\n".join(lines)

def make_ics(summary, dtstart, dtend, description, location) -> str:
    return "\n".join([
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//SnapDone AI//EL",
        "BEGIN:VEVENT",
        f"UID:snapdone-{abs(hash(summary))}@ai",
        f"SUMMARY:{summary}",
        f"DTSTART:{dtstart}",
        f"DTEND:{dtend}",
        f"DESCRIPTION:{description}",
        f"LOCATION:{location}",
        "STATUS:CONFIRMED",
        "END:VEVENT", "END:VCALENDAR"
    ])

# ─────────────────────────────────────────────
# 5. AUTO-DETECT PROMPT
# ─────────────────────────────────────────────
AUTO_DETECT_PROMPT = """
Κοίτα αυτή την εικόνα. Κατηγοριοποίησέ τη ΜΟΝΟ με έναν από τους παρακάτω κωδικούς:

INVOICE  → λογαριασμός, απόδειξη, τιμολόγιο, ΔΕΗ/ΕΥΔΑΠ/τηλεφωνία, receipt
BIZCARD  → επαγγελματική κάρτα (business card)
TICKET   → εισιτήριο, boarding pass, κράτηση, QR εισόδου
TEXT     → έγγραφο, γράμμα, άρθρο, χειρόγραφο, συνταγή γιατρού, σύμβαση
PRODUCT  → προϊόν, συσκευασία, barcode, ετικέτα
OTHER    → οτιδήποτε άλλο

Απάντα ΜΟΝΟ τον κωδικό (πχ INVOICE). Τίποτα άλλο.
"""

DETECT_INFO = {
    "INVOICE": ("🧾", "Λογαριασμός / Απόδειξη", "Βρέθηκε οικονομικό έγγραφο"),
    "BIZCARD": ("💼", "Επαγγελματική Κάρτα",    "Βρέθηκε business card"),
    "TICKET":  ("🎫", "Εισιτήριο / Boarding",   "Βρέθηκε εισιτήριο ή κράτηση"),
    "TEXT":    ("📝", "Έγγραφο / Κείμενο",      "Βρέθηκε κείμενο ή έγγραφο"),
    "PRODUCT": ("📦", "Προϊόν / Ετικέτα",       "Βρέθηκε ετικέτα ή συσκευασία"),
    "OTHER":   ("🔍", "Άγνωστος τύπος",         "Δεν αναγνωρίστηκε κατηγορία"),
}

# ─────────────────────────────────────────────
# 6. UI
# ─────────────────────────────────────────────

# Logo
st.markdown("""
<div class="snap-logo">
  <span class="icon">✦</span>
  <div class="title">SnapDone AI</div>
  <div class="tagline">Scan · Analyse · Act</div>
</div>
""", unsafe_allow_html=True)

# Upload card
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown('<div class="sec-label" style="margin-top:0;">Φόρτωσε Εικόνα</div>', unsafe_allow_html=True)

input_mode = st.radio(" ", ["📷 Κάμερα", "🖼️ Γκαλερί"], horizontal=True, label_visibility="collapsed")

uploaded = None
if input_mode == "📷 Κάμερα":
    uploaded = st.camera_input(" ", label_visibility="collapsed")
else:
    uploaded = st.file_uploader(" ", type=["jpg","jpeg","png","webp"], label_visibility="collapsed")
    if not uploaded:
        st.markdown("""
        <div class="up-hint">
          <span class="uhi">📲</span>
          <div class="uht">Επέλεξε αρχείο</div>
          <div>λογαριασμό · κάρτα · έγγραφο · εισιτήριο</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── If file uploaded ──
if uploaded:
    img = Image.open(uploaded)

    # Preview card
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.image(img, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── AUTO DETECT ──
    file_key = getattr(uploaded, "name", "camera_snapshot")
    if "detected_type" not in st.session_state or st.session_state.get("last_file") != file_key:
        with st.spinner("🔍 Ανίχνευση τύπου εικόνας…"):
            raw = ai(AUTO_DETECT_PROMPT, img).strip().upper().split()[0]
            detected = raw if raw in DETECT_INFO else "OTHER"
            st.session_state["detected_type"] = detected
            st.session_state["last_file"] = file_key

    detected = st.session_state["detected_type"]
    icon, label, sub = DETECT_INFO[detected]

    st.markdown(f"""
    <div class="detect-badge">
      <span class="di">{icon}</span>
      <div>
        <div class="dl">Αναγνωρίστηκε ως</div>
        <div class="dt"><strong>{label}</strong> — {sub}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ACTION BUTTONS per type ──
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Επιλέξτε Ενέργεια</div>', unsafe_allow_html=True)

    result_text = ""
    action_done = None

    # ══════════════════════════════════════
    # INVOICE
    # ══════════════════════════════════════
    if detected == "INVOICE":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            b_analyze = st.button("🧾 Πλήρης Ανάλυση", key="inv_analyze")
            st.markdown('</div>', unsafe_allow_html=True)
            b_calendar = st.button("📅 → Ημερολόγιο", key="inv_cal")
        with col2:
            b_pdf = st.button("📄 Εξαγωγή PDF", key="inv_pdf")
            b_ocr  = st.button("📝 Εξαγωγή Κειμένου", key="inv_ocr")

        if b_analyze:
            action_done = "analyze"
            with st.spinner("⏳ Ανάλυση λογαριασμού…"):
                result_text = ai("""
Αναλύσε αυτόν τον λογαριασμό / απόδειξη / τιμολόγιο πλήρως:
1. 🏢 Εκδότης / Προμηθευτής
2. 📅 Ημερομηνία έκδοσης & ημερομηνία λήξης πληρωμής
3. 💶 Συνολικό ποσό (ΦΠΑ ξεχωριστά αν υπάρχει)
4. 📋 Ανάλυση χρεώσεων
5. 📌 Αριθμός λογαριασμού / αναφοράς
6. ⚠️ Σημαντικές σημειώσεις
""", img)

        if b_calendar:
            action_done = "calendar"
            with st.spinner("📅 Εξαγωγή δεδομένων για ημερολόγιο…"):
                raw_cal = ai("""
Από αυτόν τον λογαριασμό, εξάγε ΜΟΝΟ:
ΤΙΤΛΟΣ: [σύντομος τίτλος πληρωμής]
ΠΟΣΟ: [ποσό €]
ΗΜΕΡΟΜΗΝΙΑ: [DD/MM/YYYY - ημ. λήξης πληρωμής]
ΕΚΔΟΤΗΣ: [εταιρεία]
ΣΗΜΕΙΩΣΕΙΣ: [κωδικός πληρωμής ή extra]
""", img)
                result_text = raw_cal

            # Parse and offer ICS download
            lines_map = {}
            for line in raw_cal.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    lines_map[k.strip()] = v.strip()

            title_ev = lines_map.get("ΤΙΤΛΟΣ", "Πληρωμή")
            amount   = lines_map.get("ΠΟΣΟ", "")
            date_str = lines_map.get("ΗΜΕΡΟΜΗΝΙΑ", "")
            issuer   = lines_map.get("ΕΚΔΟΤΗΣ", "")
            notes    = lines_map.get("ΣΗΜΕΙΩΣΕΙΣ", "")

            # Build ICS date (try to parse DD/MM/YYYY)
            try:
                from datetime import datetime
                d = datetime.strptime(date_str, "%d/%m/%Y")
                dtstart = d.strftime("%Y%m%d")
                dtend   = dtstart
            except Exception:
                dtstart = "20250101"
                dtend   = "20250101"

            desc = f"Ποσό: {amount}\\nΕκδότης: {issuer}\\n{notes}"
            ics_content = make_ics(f"💳 {title_ev}", dtstart, dtend, desc, issuer)

            st.download_button(
                label="⬇️ Κατέβασε .ics για Google/Apple Calendar",
                data=ics_content.encode("utf-8"),
                file_name="payment.ics",
                mime="text/calendar"
            )

        if b_pdf:
            action_done = "pdf"
            with st.spinner("📄 Δημιουργία PDF…"):
                ocr_text = ai("Μετέτρεψε ολόκληρη αυτή την εικόνα σε καθαρό κείμενο, διατηρώντας τη δομή.", img)
                pdf_bytes = make_pdf("Σαρωμένο Έγγραφο — SnapDone AI", ocr_text)
                result_text = ocr_text

            st.download_button(
                label="⬇️ Κατέβασε PDF",
                data=pdf_bytes,
                file_name="snapdone_document.pdf",
                mime="application/pdf"
            )

        if b_ocr:
            action_done = "ocr"
            with st.spinner("📝 Εξαγωγή κειμένου…"):
                result_text = ai("Μετέτρεψε ολόκληρη αυτή την εικόνα σε καθαρό ψηφιακό κείμενο (OCR). Διατήρησε τη δομή.", img)

    # ══════════════════════════════════════
    # BIZCARD
    # ══════════════════════════════════════
    elif detected == "BIZCARD":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            b_extract = st.button("💼 Εξαγωγή Στοιχείων", key="bc_extract")
            st.markdown('</div>', unsafe_allow_html=True)
            b_vcf = st.button("📇 Αποθήκευση vCard (.vcf)", key="bc_vcf")
        with col2:
            b_pdf2 = st.button("📄 Εξαγωγή PDF", key="bc_pdf")
            b_sum2 = st.button("🔍 Περίληψη", key="bc_sum")

        extracted = {}
        if b_extract or b_vcf:
            action_done = "bizcard"
            with st.spinner("💼 Εξαγωγή στοιχείων…"):
                raw_bc = ai("""
Από αυτή την επαγγελματική κάρτα, εξάγε ΑΚΡΙΒΩΣ τα παρακάτω (αν κάτι δεν υπάρχει γράψε —):
ΟΝΟΜΑ: 
ΕΤΑΙΡΕΙΑ: 
ΘΕΣΗ: 
ΤΗΛΕΦΩΝΟ: 
EMAIL: 
WEBSITE: 
ΔΙΕΥΘΥΝΣΗ: 
""", img)
                result_text = raw_bc
                for line in raw_bc.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        extracted[k.strip()] = v.strip().replace("—", "").strip()

            if b_vcf:
                vcf = make_vcard(
                    extracted.get("ΟΝΟΜΑ",""),
                    extracted.get("ΕΤΑΙΡΕΙΑ",""),
                    extracted.get("ΘΕΣΗ",""),
                    extracted.get("ΤΗΛΕΦΩΝΟ",""),
                    extracted.get("EMAIL",""),
                    extracted.get("WEBSITE",""),
                    extracted.get("ΔΙΕΥΘΥΝΣΗ",""),
                )
                st.download_button(
                    label="⬇️ Κατέβασε .vcf (Επαφή)",
                    data=vcf.encode("utf-8"),
                    file_name="contact.vcf",
                    mime="text/vcard"
                )
                st.markdown(f'<div class="vcard-pre">{vcf}</div>', unsafe_allow_html=True)

        if b_pdf2:
            action_done = "pdf"
            with st.spinner("📄 Δημιουργία PDF…"):
                body = ai("Παρουσίασε όλα τα στοιχεία αυτής της επαγγελματικής κάρτας με επαγγελματική μορφή.", img)
                pdf_b = make_pdf("Επαγγελματική Κάρτα — SnapDone AI", body)
                result_text = body
            st.download_button("⬇️ Κατέβασε PDF", data=pdf_b, file_name="bizcard.pdf", mime="application/pdf")

        if b_sum2:
            action_done = "sum"
            with st.spinner("🔍 Περίληψη…"):
                result_text = ai("Κάνε μια σύντομη επαγγελματική περίγραφη αυτού του ατόμου/εταιρείας βάσει της κάρτας.", img)

    # ══════════════════════════════════════
    # TICKET
    # ══════════════════════════════════════
    elif detected == "TICKET":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            b_tinfo = st.button("🎫 Ανάλυση Εισιτηρίου", key="tk_info")
            st.markdown('</div>', unsafe_allow_html=True)
            b_tcal = st.button("📅 → Ημερολόγιο", key="tk_cal")
        with col2:
            b_tpdf = st.button("📄 Εξαγωγή PDF", key="tk_pdf")
            b_tocr = st.button("📝 Εξαγωγή Κειμένου", key="tk_ocr")

        if b_tinfo:
            action_done = "ticket_info"
            with st.spinner("🎫 Ανάλυση εισιτηρίου…"):
                result_text = ai("""
Αναλύσε αυτό το εισιτήριο / boarding pass / κράτηση:
1. ✈️ Προορισμός / Εκδήλωση
2. 📅 Ημερομηνία & Ώρα
3. 🪑 Θέση / Gate / Αίθουσα
4. 🔢 Κωδικός κράτησης / Αριθμός
5. 👤 Κάτοχος / Επιβάτης
6. 📌 Σημαντικές οδηγίες ή πληροφορίες
""", img)

        if b_tcal:
            action_done = "ticket_cal"
            with st.spinner("📅 Εξαγωγή για ημερολόγιο…"):
                raw_t = ai("""
Από αυτό το εισιτήριο, εξάγε ΜΟΝΟ:
ΤΙΤΛΟΣ: [τίτλος εκδήλωσης/πτήσης]
ΗΜΕΡΟΜΗΝΙΑ: [DD/MM/YYYY]
ΩΡΑ: [HH:MM 24ωρο]
ΤΟΠΟΣ: [αεροδρόμιο/χώρος]
ΣΗΜΕΙΩΣΕΙΣ: [gate, θέση, κωδικός]
""", img)
                result_text = raw_t

            lm = {}
            for line in raw_t.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    lm[k.strip()] = v.strip()
            try:
                from datetime import datetime
                ds = lm.get("ΗΜΕΡΟΜΗΝΙΑ","01/01/2025")
                hr = lm.get("ΩΡΑ","00:00")
                dt = datetime.strptime(f"{ds} {hr}", "%d/%m/%Y %H:%M")
                dtstart = dt.strftime("%Y%m%dT%H%M%S")
                dtend   = dtstart
            except Exception:
                dtstart = dtend = "20250101T000000"

            ics2 = make_ics(lm.get("ΤΙΤΛΟΣ","Εκδήλωση"), dtstart, dtend, lm.get("ΣΗΜΕΙΩΣΕΙΣ",""), lm.get("ΤΟΠΟΣ",""))
            st.download_button("⬇️ Κατέβασε .ics", data=ics2.encode("utf-8"), file_name="event.ics", mime="text/calendar")

        if b_tpdf:
            action_done = "pdf"
            with st.spinner("📄 Δημιουργία PDF…"):
                body = ai("Μετέτρεψε όλα τα στοιχεία αυτού του εισιτηρίου σε οργανωμένο κείμενο.", img)
                pdf_b = make_pdf("Εισιτήριο — SnapDone AI", body)
                result_text = body
            st.download_button("⬇️ Κατέβασε PDF", data=pdf_b, file_name="ticket.pdf", mime="application/pdf")

        if b_tocr:
            action_done = "ocr"
            with st.spinner("📝 Εξαγωγή κειμένου…"):
                result_text = ai("OCR: Εξάγε όλο το κείμενο από αυτό το εισιτήριο.", img)

    # ══════════════════════════════════════
    # TEXT / DOCUMENT
    # ══════════════════════════════════════
    elif detected in ("TEXT", "OTHER", "PRODUCT"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
            b_docr = st.button("📝 OCR — Ψηφιοποίηση", key="tx_ocr")
            st.markdown('</div>', unsafe_allow_html=True)
            b_dsum = st.button("🔍 Περίληψη", key="tx_sum")
        with col2:
            b_dpdf = st.button("📄 Εξαγωγή PDF", key="tx_pdf")
            b_dpres = st.button("💊 Ανάλυση Συνταγής", key="tx_presc")

        if b_docr:
            action_done = "ocr"
            with st.spinner("📝 Ψηφιοποίηση…"):
                result_text = ai("""
Μετέτρεψε ΟΛΟΚΛΗΡΗ αυτή την εικόνα σε καθαρό ψηφιακό κείμενο.
Διατήρησε παραγράφους, λίστες και δομή. Μη παραλείψεις τίποτα.
""", img)

        if b_dsum:
            action_done = "summary"
            with st.spinner("🔍 Περίληψη…"):
                result_text = ai("""
Κάνε επαγγελματική περίληψη του εγγράφου σε 5-7 bullet points.
Ξεκίνα με μια πρόταση που συνοψίζει το θέμα.
""", img)

        if b_dpdf:
            action_done = "pdf"
            with st.spinner("📄 Δημιουργία PDF…"):
                body = ai("OCR πλήρες: Εξάγε όλο το κείμενο διατηρώντας τη δομή.", img)
                pdf_b = make_pdf("Ψηφιοποιημένο Έγγραφο — SnapDone AI", body)
                result_text = body
            st.download_button("⬇️ Κατέβασε PDF", data=pdf_b, file_name="document.pdf", mime="application/pdf")

        if b_dpres:
            action_done = "prescription"
            with st.spinner("💊 Ανάλυση συνταγής…"):
                result_text = ai("""
Αναλύσε αυτή τη συνταγή γιατρού λεπτομερώς:
1. 💊 Φάρμακα — Ονομασία & Δόση
2. 📋 Οδηγίες χρήσης
3. ⏰ Συχνότητα & Χρόνος λήψης
4. 📅 Διάρκεια θεραπείας
5. ⚠️ Προφυλάξεις ή αντενδείξεις αν αναφέρονται
""", img)

    st.markdown('</div>', unsafe_allow_html=True)  # end glass card for buttons

    # ── RESULT ──
    if result_text:
        st.markdown(f"""
        <div class="result-box">
          <div class="result-label">✦ Αποτέλεσμα Ανάλυσης</div>
          {result_text}
        </div>
        """, unsafe_allow_html=True)

        # Copy as text download
        st.download_button(
            label="⬇️ Αποθήκευση ως .txt",
            data=result_text.encode("utf-8"),
            file_name="snapdone_result.txt",
            mime="text/plain",
            key="dl_txt"
        )
