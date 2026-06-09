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
    st.markdown('<div class="guest-header" style="font-size:24px; font-weight:bold;">🚀 MZ Professional Tools</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="guest-text" style="font-size:18px; line-height:1.5;">
        Welcome to MZ Software Solutions! <br><br>
        We provide all types of <b>Premium POS (Point of Sale) Software</b> tailored to your business needs.<br>
        Like professional software, all profit management, inventory control, and billing systems are available.<br><br>
        <i>Choose what you want, and we will build it for you!</i>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    g_col1, g_col2, g_col3 = st.columns(3)
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
    
    st.write("---")
    if st.session_state.show_contact:
        st.success("📞 **Contact Us for Support / Purchase: 03476712269 (MZ Professional Tools)**")
        st.info("We are available 24/7 to resolve your issues and provide the best software experience.")
    
    st.write("---")
    if st.button("⬅️ Logout / Back to Login"):
        st.session_state.auth_status = "unauthenticated"
        st.session_state.show_contact = False
        st.rerun()

# ==========================================
# 🛡️ ADMIN VIEW (COMPLETE REVAMPED WORKFLOW)
# ==========================================
elif st.session_state.auth_status == "admin":
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

    # --- FIREBASE CORE FUNCTIONS ---
    def get_all_licenses():
        try:
            res = requests.get(f"{FIREBASE_DB_URL}/security_licenses.json", timeout=10)
            return res.json() if (res.status_code == 200 and res.json()) else {}
        except: return {}

    def get_all_registered_keys():
        try:
            res = requests.get(f"{FIREBASE_DB_URL}/registered_keys.json", timeout=10)
            return res.json() if (res.status_code == 200 and res.json()) else {}
        except: return {}

    def save_or_update_license(hwid, name, sec_key, issuance, expiry, limit, block_date, status, mobile, email, address):
        try:
            data = {
                "name": name, 
                "security_key": sec_key,
                "mobile": mobile,   
                "email": email,     
                "address": address, 
                "issuance_date": str(issuance),
                "expiry": str(expiry), 
                "status": status,
                "blocked_until": str(block_date), 
                "offline_limit_days": int(limit)
            }
            requests.put(f"{FIREBASE_DB_URL}/security_licenses/{hwid}.json", json=data)
            return True
        except: return False

    def delete_license(hwid):
        try:
            requests.delete(f"{FIREBASE_DB_URL}/security_licenses/{hwid}.json")
            return True
        except: return False

    def delete_registration_request(sec_key):
        try:
            requests.delete(f"{FIREBASE_DB_URL}/registered_keys/{sec_key}.json")
            return True
        except: return False

    # --- DIALOG BOXES ---
    @st.dialog("⚠️ Confirm Deletion")
    def confirm_delete_dialog(hwid, name):
        st.error(f"**MZ**, are you sure you want to completely remove the PC for **{name}**?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ OK, Delete It", use_container_width=True):
                delete_license(hwid)
                st.success(f"System for {name} has been deleted.")
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True): st.rerun()

    @st.dialog("👤 User Registration Details")
    def show_user_profile(name, hwid, sec_key, mobile, email, address, issue, expiry):
        st.markdown(f"<h3 style='color: #ffcc00;'>Details for: {name}</h3>", unsafe_allow_html=True)
        st.write("---")
        st.info(f"**📱 Mobile Number:** {mobile}")
        st.success(f"**📧 Email:** {email}")
        st.warning(f"**🏠 Address:** {address}")
        st.error(f"**🔑 Security Key:** {sec_key}")
        st.write(f"**💻 HWID:** {hwid}")
        st.write(f"**🗓️ Issuance Date:** {issue}")
        st.write(f"**⏳ Expiry Date:** {expiry}")
        st.write("---")
        if st.button("Close Window", use_container_width=True): st.rerun()

    # --- INITIALIZE SESSION STATES ---
    if "sel_hwid" not in st.session_state: st.session_state.sel_hwid = ""
    if "sel_name" not in st.session_state: st.session_state.sel_name = ""
    if "sel_sec_key" not in st.session_state: st.session_state.sel_sec_key = ""
    if "sel_limit" not in st.session_state: st.session_state.sel_limit = 30
    if "sel_issue" not in st.session_state: st.session_state.sel_issue = datetime.now().date()
    if "sel_expiry" not in st.session_state: st.session_state.sel_expiry = datetime.now().date() + timedelta(days=365)
    if "sel_block" not in st.session_state: st.session_state.sel_block = "-"
    if "sel_status" not in st.session_state: st.session_state.sel_status = "active"
    # Metadata vectors passed during Accept triggers
    if "sel_mobile" not in st.session_state: st.session_state.sel_mobile = "Not Provided"
    if "sel_email" not in st.session_state: st.session_state.sel_email = "Not Provided"
    if "sel_address" not in st.session_state: st.session_state.sel_address = "Not Provided"

    # ==========================================
    # PANEL 1: PENDING REQUESTS PANEL ("Requests for POS")
    # ==========================================
    st.markdown('<div class="section-card" style="border-left: 6px solid #00e676;">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading" style="color: #00e676 !important;">📋 Requests for POS (Pending Approval)</div>', unsafe_allow_html=True)
    
    pending_requests = get_all_registered_keys()
    if pending_requests:
        r_h1, r_h2, r_h3, r_h4, r_h5, r_h6 = st.columns([1.5, 1.2, 1.2, 1.8, 1.0, 1.0])
        r_h1.markdown('<div class="list-header">👤 CLIENT NAME</div>', unsafe_allow_html=True)
        r_h2.markdown('<div class="list-header">🔑 SEC KEY</div>', unsafe_allow_html=True)
        r_h3.markdown('<div class="list-header">📱 PHONE</div>', unsafe_allow_html=True)
        r_h4.markdown('<div class="list-header">💻 INCOMING HWID</div>', unsafe_allow_html=True)
        r_h5.markdown('<div class="list-header">✅ ACCEPT</div>', unsafe_allow_html=True)
        r_h6.markdown('<div class="list-header">❌ REJECT</div>', unsafe_allow_html=True)

        for skey, rdata in pending_requests.items():
            r_name = rdata.get("name", "Unknown")
            r_phone = rdata.get("phone", "Not Provided")
            r_hwid = rdata.get("hardware_id", "No HWID Sent")
            r_email = rdata.get("email", "Not Provided")
            r_address = rdata.get("address", "Not Provided")

            rc1, rc2, rc3, rc4, rc5, rc6 = st.columns([1.5, 1.2, 1.2, 1.8, 1.0, 1.0])
            rc1.write(r_name)
            rc2.write(f"`{skey}`")
            rc3.write(r_phone)
            rc4.write(f"`{r_hwid}`")
            
            # ACCEPT BUTTON: Loads data to upper setup section for final approval configuration
            if rc5.button("Accept 👍", key=f"acc_{skey}", use_container_width=True):
                st.session_state.sel_hwid = r_hwid
                st.session_state.sel_name = r_name
                st.session_state.sel_sec_key = skey
                st.session_state.sel_mobile = r_phone
                st.session_state.sel_email = r_email
                st.session_state.sel_address = r_address
                st.session_state.sel_issue = datetime.now().date()
                st.toast(f"📩 Loaded request data for {r_name}. Please set dates and press Save down below!")
                st.rerun()

            # REJECT BUTTON: Completely removes the request data node from Firebase
            if rc6.button("Reject 🗑️", key=f"rej_{skey}", use_container_width=True):
                delete_registration_request(skey)
                st.toast(f"❌ Deleted request for {r_name}")
                st.rerun()
    else:
        st.info("No current pending registration requests found.")
    st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # PANEL 2: LICENSE SETUP & MODIFICATIONS (MAIN FORM)
    # ==========================================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📝 License Setup & Status Adjustments</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        hwid_input = st.text_input("Hardware ID (HWID):", value=st.session_state.sel_hwid)
        customer_name = st.text_input("Customer Name:", value=st.session_state.sel_name)
        sec_key_input = st.text_input("Security Key Configured:", value=st.session_state.sel_sec_key)
        
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
        st.markdown('<b style="color:#ffcc00;">📅 Manage Validity Timelines (Editable)</b>', unsafe_allow_html=True)
        
        # BOTH DATES ARE FULLY EDITABLE VIA CALENDAR BOXES HERE
        issuance_date = st.date_input("License Date of Issuance:", value=st.session_state.sel_issue)
        expiry_date = st.date_input("License Validity Expiry Date:", value=st.session_state.sel_expiry)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write(" ")
    b_col1, b_col3 = st.columns([1, 1])
    with b_col1:
        if st.button("💾 SAVE / COMMIT ALL CHANGES", type="primary", use_container_width=True):
            if hwid_input.strip():
                with st.spinner("MZ, Synchronizing with Cloud Database..."):
                    # Committing data cleanly into security_licenses node
                    success = save_or_update_license(
                        hwid=hwid_input.strip(), 
                        name=customer_name.strip(), 
                        sec_key=sec_key_input.strip(), 
                        issuance=issuance_date,
                        expiry=expiry_date, 
                        limit=sec_progress, 
                        block_date=final_block_val, 
                        status=computed_status,
                        mobile=st.session_state.sel_mobile,
                        email=st.session_state.sel_email,
                        address=st.session_state.sel_address
                    )
                    if success:
                        # Auto delete request from pending lists if it was imported from one
                        if sec_key_input.strip() in pending_requests:
                            delete_registration_request(sec_key_input.strip())
                        
                        st.success(f"Great Job MZ! Successfully saved license for: {customer_name}")
                        # Reset States
                        st.session_state.sel_hwid = ""
                        st.session_state.sel_name = ""
                        st.session_state.sel_sec_key = ""
                        st.session_state.sel_mobile = "Not Provided"
                        st.session_state.sel_email = "Not Provided"
                        st.session_state.sel_address = "Not Provided"
                        st.session_state.sel_issue = datetime.now().date()
                        st.session_state.sel_expiry = datetime.now().date() + timedelta(days=365)
                        st.session_state.sel_block = "-"
                        st.session_state.sel_status = "active"
                        st.rerun()
            else: st.error("MZ, Valid HWID String is mandatory.")
            
    with b_col3:
        if st.button("🧹 RESET FORM FIELDS", use_container_width=True):
            st.session_state.sel_hwid = ""
            st.session_state.sel_name = ""
            st.session_state.sel_sec_key = ""
            st.session_state.sel_mobile = "Not Provided"
            st.session_state.sel_email = "Not Provided"
            st.session_state.sel_address = "Not Provided"
            st.session_state.sel_limit = 30
            st.session_state.sel_issue = datetime.now().date()
            st.session_state.sel_expiry = datetime.now().date() + timedelta(days=365)
            st.session_state.sel_block = "-"
            st.session_state.sel_status = "active"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # PANEL 3: LIVE RECOGNIZED SYSTEMS LIST
    # ==========================================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📊 MZ Live Registered Nodes</div>', unsafe_allow_html=True)
    search_query = st.text_input("🔍 Filter Registry (HWID / Client Name / Sec Key):", "").lower()

    h1, h2, h_sec, h3, h4, h5, h_view, h6, h7 = st.columns([1.6, 1.4, 1.2, 1.3, 1.1, 1.1, 0.7, 0.6, 0.6])
    h1.markdown('<div class="list-header">💻 HWID</div>', unsafe_allow_html=True)
    h2.markdown('<div class="list-header">👤 NAME</div>', unsafe_allow_html=True)
    h_sec.markdown('<div class="list-header">🔑 SEC KEY</div>', unsafe_allow_html=True)
    h3.markdown('<div class="list-header">🛡️ STATUS</div>', unsafe_allow_html=True)
    h4.markdown('<div class="list-header">⏳ EXPIRY</div>', unsafe_allow_html=True)
    h5.markdown('<div class="list-header">🔄 CYCLE</div>', unsafe_allow_html=True)
    h_view.markdown('<div class="list-header">👁️ INFO</div>', unsafe_allow_html=True)
    h6.markdown('<div class="list-header">⚙️ EDIT</div>', unsafe_allow_html=True)
    h7.markdown('<div class="list-header">🗑️ DEL</div>', unsafe_allow_html=True)

    all_licenses = get_all_licenses()
    found_records = False
    
    for hwid, data in all_licenses.items():
        name = data.get("name", "")
        sec_key = data.get("security_key", "-")
        u_mobile = data.get("mobile", "Not Provided")
        u_email = data.get("email", "Not Provided")
        u_address = data.get("address", "Not Provided")
        iss_dt = data.get("issuance_date", "-")
        exp_dt = data.get("expiry", "-")

        if search_query in hwid.lower() or search_query in name.lower() or search_query in sec_key.lower():
            found_records = True
            c1, c2, c_sec, c3, c4, c5, c_view, c6, c7 = st.columns([1.6, 1.4, 1.2, 1.3, 1.1, 1.1, 0.7, 0.6, 0.6])
            c1.write(hwid)
            c2.write(name)
            c_sec.write(f"`{sec_key}`")
            
            if data.get("status") == "blocked":
                block_until_str = data.get("blocked_until", "-")
                try:
                    block_date = datetime.strptime(block_until_str, "%Y-%m-%d").date()
                    remaining_days = (block_date - datetime.now().date()).days
                    if remaining_days > 0: c3.error(f"🔴 BLOCKED ({remaining_days} Days)")
                    else: c3.error("🔴 BLOCKED (Expired)")
                except: c3.error("🔴 BLOCKED")
            else: 
                c3.success("🟢 ACTIVE")
                
            c4.write(exp_dt)
            c5.info(f"⏱️ {data.get('offline_limit_days', 30)} d")
            
            if c_view.button("👁️", key=f"view_{hwid}", use_container_width=True):
                show_user_profile(name, hwid, sec_key, u_mobile, u_email, u_address, iss_dt, exp_dt)
            
            if c6.button("✏️", key=f"edit_{hwid}", use_container_width=True):
                st.session_state.sel_hwid = hwid
                st.session_state.sel_name = name
                st.session_state.sel_sec_key = sec_key
                st.session_state.sel_mobile = u_mobile
                st.session_state.sel_email = u_email
                st.session_state.sel_address = u_address
                st.session_state.sel_limit = int(data.get("offline_limit_days", 30))
                st.session_state.sel_block = data.get("blocked_until", "-")
                st.session_state.sel_status = data.get("status", "active")
                try: st.session_state.sel_issue = datetime.strptime(iss_dt, "%Y-%m-%d").date()
                except: st.session_state.sel_issue = datetime.now().date()
                try: st.session_state.sel_expiry = datetime.strptime(exp_dt, "%Y-%m-%d").date()
                except: st.session_state.sel_expiry = datetime.now().date()
                st.toast(f"⚡ MZ, Loaded Data for: {name}")
                st.rerun()
                
            if c7.button("🗑️", key=f"del_{hwid}", use_container_width=True):
                confirm_delete_dialog(hwid, name)
            st.markdown("<hr style='margin: 0px; margin-bottom: 10px; border-top: 1px solid #334155;'>", unsafe_allow_html=True)

    if not found_records: st.info("MZ, No live activated network machines matched your query.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- DEVELOPER FOOTER ---
st.markdown('<div class="dev-footer">Developed by Muhammad Zubair</div>', unsafe_allow_html=True)