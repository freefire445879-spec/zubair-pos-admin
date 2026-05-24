import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MZ Central Hub", page_icon="🛡️", layout="wide")

FIREBASE_DB_URL = "https://zubairpos-cloud-default-rtdb.firebaseio.com/"

# --- ULTRA-PREMIUM HIGH CONTRAST CSS ---
st.markdown("""
    <style>
    /* Global Background */
    .stApp { background-color: #0b0f19; color: #ffffff; }
    
    /* Input Text & Labels High Contrast */
    label, .st-bb, .st-ae, .st-af, div[data-testid="stMarkdownContainer"] p {
        color: #ffcc00 !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    
    /* Login & Guest Box Styling */
    .login-box {
        background: #1a2235;
        padding: 40px;
        border-radius: 15px;
        border: 2px solid #ff4b4b;
        box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.4);
        text-align: center;
        margin-top: 50px;
    }

    /* Guest Screen Styling */
    .guest-header {
        color: #00e676 !important;
        font-size: 35px;
        font-weight: 900;
        text-align: center;
        text-shadow: 2px 2px 5px rgba(0,230,118,0.5);
        margin-bottom: 20px;
    }
    .guest-text {
        font-size: 20px;
        color: #ffffff;
        text-align: center;
        line-height: 1.6;
    }

    /* Admin Section Cards */
    .section-card {
        background: #1a2235;
        padding: 24px;
        border-radius: 14px;
        border-left: 6px solid #ff4b4b;
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }
    
    .section-heading {
        color: #ff4b4b !important;
        font-size: 22px;
        font-weight: 900;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 2px solid #334155;
        padding-bottom: 8px;
    }

    .list-header {
        font-weight: bold;
        color: #ffcc00;
        border-bottom: 2px solid #ff4b4b;
        padding-bottom: 10px;
        margin-bottom: 15px;
        font-size: 14px;
    }

    /* Developer Footer */
    .dev-footer {
        text-align: center;
        color: #8892b0;
        font-size: 14px;
        font-weight: bold;
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #334155;
    }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION STATE ---
if "auth_status" not in st.session_state:
    st.session_state.auth_status = "unauthenticated"

# ==========================================
# 🛑 LOGIN SCREEN
# ==========================================
if st.session_state.auth_status == "unauthenticated":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1 style="color: #ffffff;">🛡️ MZ Central Gateway</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color: #aaaaaa;">Please login to access the system</p>', unsafe_allow_html=True)
        
        user_in = st.text_input("Username:")
        pass_in = st.text_input("Password:", type="password")
        
        st.write("")
        if st.button("🔐 LOGIN AS ADMIN", type="primary", use_container_width=True):
            if user_in == "MZAdmin" and pass_in == "Zubair@786":
                st.session_state.auth_status = "admin"
                st.toast("✅ Admin Logged In Successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid Username or Password!")
                
        st.write("---")
        if st.button("👤 CONTINUE AS GUEST", use_container_width=True):
            st.session_state.auth_status = "guest"
            st.toast("👋 Welcome Guest!")
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# 🌟 GUEST VIEW (MARKETING PORTFOLIO)
# ==========================================
elif st.session_state.auth_status == "guest":
    # Header
    st.markdown('<div class="guest-header" style="font-size:24px; font-weight:bold;">🚀 MZ Professional Tools</div>', unsafe_allow_html=True)
    
    # Welcome text
    st.markdown("""
    <div class="guest-text" style="font-size:18px; line-height:1.5;">
        Welcome to MZ Software Solutions! <br><br>
        We provide all types of <b>Premium POS (Point of Sale) Software</b> tailored to your business needs.<br>
        Like professional software, all profit management, inventory control, and billing systems are available.<br><br>
        <i>Choose what you want, and we will build it for you!</i>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    # Columns with buttons      
    g_col1, g_col2, g_col3 = st.columns(3)
    
    # A session state flag to show contact info after button click
    if "show_contact" not in st.session_state:
        st.session_state.show_contact = False
    
    def show_contact():
        st.session_state.show_contact = True
    
    with g_col1:
        if st.button("🛒 Buy Retail POS System", use_container_width=True):
            show_contact()
    with g_col2:
        if st.button("💊 Buy Pharmacy POS", use_container_width=True):
            show_contact()
    with g_col3:
        if st.button("🔧 Custom Software Order", use_container_width=True):
            show_contact()
    
    st.write("---")  # separator
    
    # Show contact info only if a button was clicked
    if st.session_state.show_contact:
        st.success("📞 **Contact Us for Support / Purchase: 03476712269 (MZ Professional Tools)**")
        st.info("We are available 24/7 to resolve your issues and provide the best software experience.")
    
    st.write("---")  # separator
    
    # Logout button at bottom
    if st.button("⬅️ Logout / Back to Login"):
        st.session_state.auth_status = "unauthenticated"
        st.session_state.show_contact = False   # reset to avoid showing contact after logout
        st.experimental_rerun()
# ==========================================
# 🛡️ ADMIN VIEW (ORIGINAL SYSTEM)
# ==========================================
elif st.session_state.auth_status == "admin":
    # --- LOGOUT BUTTON ---
    colA, colB = st.columns([8, 1])
    with colB:
        if st.button("🚪 Logout"):
            st.session_state.auth_status = "unauthenticated"
            st.rerun()

    st.markdown("""
        <div style="text-align:center; margin-bottom: 20px;">
            <h1 style="color: #ff4b4b;">🛡️ SYSTEM SECURITY & LICENSE TERMINAL</h1>
        </div>
    """, unsafe_allow_html=True)

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

    # --- MESSAGE BOX FOR DELETION ---
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
            if st.button("❌ Cancel", use_container_width=True): st.rerun()

    # Cache Load
    all_licenses = get_all_licenses()

    # Session States
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
            index=0 if st.session_state.sel_block == "-" else 1, horizontal=True
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
        st.markdown('<div style="background:#1e293b; padding:15px; border-radius:10px; border:1px solid #ffcc00; margin-top:5px;">', unsafe_allow_html=True)
        st.markdown('<b style="color:#ffcc00;">⏳ Expiry Timeline Extension</b>', unsafe_allow_html=True)
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

    # --- SECTION 2: MZ CUSTOM DATAGRID ---
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📊 MZ Live Registered Nodes</div>', unsafe_allow_html=True)
    search_query = st.text_input("🔍 Filter Registry (HWID / Client Name):", "").lower()

    h1, h2, h3, h4, h5, h6, h7 = st.columns([2.2, 1.8, 2.0, 1.2, 1.4, 0.7, 0.7])
    h1.markdown('<div class="list-header">💻 HARDWARE ID</div>', unsafe_allow_html=True)
    h2.markdown('<div class="list-header">👤 CUSTOMER NAME</div>', unsafe_allow_html=True)
    h3.markdown('<div class="list-header">🛡️ STATUS</div>', unsafe_allow_html=True)
    h4.markdown('<div class="list-header">⏳ EXPIRY</div>', unsafe_allow_html=True)
    h5.markdown('<div class="list-header">🔄 CYCLE</div>', unsafe_allow_html=True)
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
            
            if data.get("status") == "blocked":
                block_until_str = data.get("blocked_until", "-")
                try:
                    block_date = datetime.strptime(block_until_str, "%Y-%m-%d").date()
                    remaining_days = (block_date - datetime.now().date()).days
                    if remaining_days > 0: c3.error(f"🔴 BLOCKED ({remaining_days} Days)")
                    else: c3.error("🔴 BLOCKED (Expired)")
                except: c3.error("🔴 BLOCKED")
            else: c3.success("🟢 ACTIVE")
                
            c4.write(data.get("expiry", ""))
            c5.info(f"⏱️ {data.get('offline_limit_days', 30)} Days")
            
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
                
            if c7.button("🗑️", key=f"del_{hwid}", use_container_width=True):
                confirm_delete_dialog(hwid, name)
            st.markdown("<hr style='margin: 0px; margin-bottom: 10px; border-top: 1px solid #334155;'>", unsafe_allow_html=True)

    if not found_records: st.info("MZ, No network machines matched your query.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- DEVELOPER FOOTER ---
st.markdown('<div class="dev-footer">Developed by Muhammad Zubair</div>', unsafe_allow_html=True)