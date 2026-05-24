import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MZ Central Hub", page_icon="🛡️", layout="wide")

FIREBASE_DB_URL = "https://zubairpos-cloud-default-rtdb.firebaseio.com/"

# --- ULTRA-PREMIUM CSS (FIXED LABELS & COLORFUL ANIMATION) ---
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #f4f6f9; }
    
    /* FIX: Force Labels to be Visible, Bold, and Dark Red */
    label, .st-bb, .st-ae, .st-af, div[data-testid="stMarkdownContainer"] p {
        color: #8B0000 !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    /* Colorful Typing Effect Styling */
    .typing-title {
        font-family: 'Courier New', Courier, monospace;
        background: linear-gradient(90deg, #E63946, #F4A261, #E76F51);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: 900;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        border-right: 4px solid #E63946;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
        margin-bottom: 5px;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #E63946; } }

    .sub-title {
        text-align: center;
        color: #2c3e50;
        font-weight: 800;
        font-size: 30px;
        letter-spacing: -1px;
        margin-bottom: 25px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Section Cards Blueprint */
    .section-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 14px;
        border-left: 6px solid #C0392B;
        box-shadow: 0px 8px 24px rgba(192, 57, 43, 0.12);
        margin-bottom: 25px;
    }
    
    .section-heading {
        color: #8B0000 !important;
        font-size: 22px;
        font-weight: 900;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 2px solid #ffcccc;
        padding-bottom: 8px;
    }

    /* List Custom Styling */
    .list-header {
        font-weight: bold;
        color: #2c3e50;
        border-bottom: 2px solid #E63946;
        padding-bottom: 10px;
        margin-bottom: 15px;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# --- AUDIO & ANIMATION INJECTOR ---
st.markdown("""
    <div class="typing-title">Welcome to MZ Central Control...</div>
    <audio autoplay>
        <source src="https://assets.mixkit.co/active_storage/sfx/2869/2869-84.wav" type="audio/wav">
    </audio>
""", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>🛡️ SYSTEM SECURITY & LICENSE TERMINAL</div>", unsafe_allow_html=True)

# --- FIREBASE LOGIC CORE ---
def get_all_licenses():
    try:
        res = requests.get(f"{FIREBASE_DB_URL}/security_licenses.json", timeout=10)
        return res.json() if (res.status_code == 200 and res.json()) else {}
    except: return {}

def save_or_update_license(hwid, name, expiry, limit, block_date, status="active"):
    try:
        res = requests.get(f"{FIREBASE_DB_URL}/security_licenses/{hwid}.json")
        existing = res.json() if res.status_code == 200 and res.json() else {}
        issuance_date = existing.get("issuance_date", datetime.now().strftime("%Y-%m-%d"))
        
        data = {
            "name": name, "expiry": str(expiry), "status": status,
            "blocked_until": str(block_date), "offline_limit_days": int(limit), "issuance_date": issuance_date
        }
        requests.put(f"{FIREBASE_DB_URL}/security_licenses/{hwid}.json", json=data)
        return True
    except: return False

def delete_license(hwid):
    try:
        requests.delete(f"{FIREBASE_DB_URL}/security_licenses/{hwid}.json")
        return True
    except: return False

# --- MESSAGE BOX (DIALOG) FOR DELETION ---
@st.dialog("⚠️ Confirm Deletion")
def confirm_delete_dialog(hwid, name):
    st.error(f"**MZ**, are you sure you want to completely remove the PC for **{name}**?")
    st.write("This action cannot be undone.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ OK, Delete It", use_container_width=True):
            delete_license(hwid)
            st.success(f"System for {name} has been deleted successfully, MZ!")
            st.rerun()
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

# Cache Load
all_licenses = get_all_licenses()

# --- RECOVERY / SESSION STATE FOR SELECTION ---
if "sel_hwid" not in st.session_state: st.session_state.sel_hwid = ""
if "sel_name" not in st.session_state: st.session_state.sel_name = ""
if "sel_limit" not in st.session_state: st.session_state.sel_limit = 30
if "sel_expiry" not in st.session_state: st.session_state.sel_expiry = datetime.now() + timedelta(days=365)
if "sel_block" not in st.session_state: st.session_state.sel_block = "-"
if "sel_status" not in st.session_state: st.session_state.sel_status = "active"

# --- SECTION 1: SYSTEM CONTROLS & INPUTS ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">📝 License Setup & Status Adjustments</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    hwid_input = st.text_input("Hardware ID (HWID):", value=st.session_state.sel_hwid)
    customer_name = st.text_input("Customer Name:", value=st.session_state.sel_name)
    
    block_radio = st.radio(
        "System Block State Configuration:",
        ["🟢 Active / Unblocked (No Restriction)", "🚫 Block System Setup"],
        index=0 if st.session_state.sel_block == "-" else 1,
        horizontal=True
    )
    
    if "Block System" in block_radio:
        try: init_b_date = datetime.strptime(st.session_state.sel_block, "%Y-%m-%d")
        except: init_b_date = datetime.now()
        block_until = st.date_input("Block Until Calendar Date:", init_b_date)
        final_block_val = block_until
        computed_status = "blocked"
    else:
        final_block_val = "-"
        computed_status = "active"

with col2:
    sec_progress = st.number_input("Security Check Frequency / Offline Guard (Days):", min_value=1, max_value=365, value=st.session_state.sel_limit)
    
    st.markdown('<div style="background:#fff5f5; padding:15px; border-radius:10px; border:1px solid #ffcccc; margin-top:5px;">', unsafe_allow_html=True)
    st.markdown('<b style="color:#B22222;">⏳ Expiry Timeline Extension</b>', unsafe_allow_html=True)
    expiry_date = st.date_input("License Validity Expiry Date:", st.session_state.sel_expiry)
    st.markdown('</div>', unsafe_allow_html=True)

st.write(" ")
b_col1, b_col3 = st.columns([1, 1])

with b_col1:
    if st.button("💾 SAVE / COMMIT ALL CHANGES", type="primary", use_container_width=True):
        if hwid_input.strip():
            with st.spinner("MZ, Synchronizing with Cloud Database..."):
                if save_or_update_license(hwid_input.strip(), customer_name, expiry_date, sec_progress, final_block_val, computed_status):
                    st.success(f"Great Job MZ! Successfully saved modifications for: {customer_name}")
                    st.session_state.sel_hwid = ""
                    st.rerun()
        else: st.error("MZ, Valid HWID String is mandatory.")

with b_col3:
    if st.button("🧹 RESET FORM FIELDS", use_container_width=True):
        st.session_state.sel_hwid = ""
        st.session_state.sel_name = ""
        st.session_state.sel_limit = 30
        st.session_state.sel_expiry = datetime.now() + timedelta(days=365)
        st.session_state.sel_block = "-"
        st.session_state.sel_status = "active"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# --- SECTION 2: MZ CUSTOM DATAGRID (WITH EDIT & DELETE ICONS) ---
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">📊 MZ Live Registered Nodes</div>', unsafe_allow_html=True)

search_query = st.text_input("🔍 Filter Registry (HWID / Client Name):", "").lower()

# Custom Headers Adjusted for New Columns
h1, h2, h3, h4, h5, h6, h7 = st.columns([2.2, 1.8, 2.0, 1.2, 1.4, 0.7, 0.7])
h1.markdown('<div class="list-header">💻 HARDWARE ID</div>', unsafe_allow_html=True)
h2.markdown('<div class="list-header">👤 CUSTOMER NAME</div>', unsafe_allow_html=True)
h3.markdown('<div class="list-header">🛡️ STATUS</div>', unsafe_allow_html=True)
h4.markdown('<div class="list-header">⏳ EXPIRY</div>', unsafe_allow_html=True)
h5.markdown('<div class="list-header">🔄 REFRESH CYCLE</div>', unsafe_allow_html=True)
h6.markdown('<div class="list-header">⚙️ EDIT</div>', unsafe_allow_html=True)
h7.markdown('<div class="list-header">🗑️ REMOVE</div>', unsafe_allow_html=True)

found_records = False

for hwid, data in all_licenses.items():
    name = data.get("name", "")
    if search_query in hwid.lower() or search_query in name.lower():
        found_records = True
        c1, c2, c3, c4, c5, c6, c7 = st.columns([2.2, 1.8, 2.0, 1.2, 1.4, 0.7, 0.7])
        
        c1.write(hwid)
        c2.write(name)
        
        # STATUS & DAYS REMAINING LOGIC
        if data.get("status") == "blocked":
            block_until_str = data.get("blocked_until", "-")
            try:
                block_date = datetime.strptime(block_until_str, "%Y-%m-%d").date()
                today = datetime.now().date()
                remaining_days = (block_date - today).days
                if remaining_days > 0:
                    c3.error(f"🔴 BLOCKED ({remaining_days} Days)")
                else:
                    c3.error("🔴 BLOCKED (Expired)")
            except:
                c3.error("🔴 BLOCKED")
        else:
            c3.success("🟢 ACTIVE")
            
        c4.write(data.get("expiry", ""))
        
        # SECURITY CHECK PROGRESSING PERIOD COLUMN
        limit_days = data.get("offline_limit_days", 30)
        c5.info(f"⏱️ {limit_days} Days")
        
        # EDIT BUTTON
        if c6.button("✏️", key=f"edit_{hwid}", use_container_width=True):
            st.session_state.sel_hwid = hwid
            st.session_state.sel_name = name
            st.session_state.sel_limit = int(data.get("offline_limit_days", 30))
            st.session_state.sel_block = data.get("blocked_until", "-")
            st.session_state.sel_status = data.get("status", "active")
            try: st.session_state.sel_expiry = datetime.strptime(data.get("expiry", "%Y-%m-%d"), "%Y-%m-%d")
            except: pass
            st.toast(f"⚡ MZ, Loaded Data for: {name}")
            st.rerun()
            
        # DELETE BUTTON
        if c7.button("🗑️", key=f"del_{hwid}", use_container_width=True):
            confirm_delete_dialog(hwid, name)

        st.markdown("<hr style='margin: 0px; margin-bottom: 10px; border-top: 1px solid #f0f0f0;'>", unsafe_allow_html=True)

if not found_records:
    st.info("MZ, No network machines matched your query.")

st.markdown('</div>', unsafe_allow_html=True)