import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MZ Central Hub - Terminal", page_icon="🛡️", layout="wide")

# FRESH FIREBASE PROJECT URL
FIREBASE_DB_URL = "https://zubairposbackup-default-rtdb.firebaseio.com/"

# --- ULTRA-PROFESSIONAL PREMIUM DARK CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at top right, #0a0f1d, #030712); 
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }
    
    /* Form Labels High Contrast */
    label, div[data-testid="stMarkdownContainer"] p {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 12px !important;
        letter-spacing: 0.7px;
    }
    
    /* Login Screen Container */
    .login-box {
        background: rgba(17, 24, 39, 0.7);
        backdrop-filter: blur(15px);
        padding: 45px;
        border-radius: 20px;
        border: 1px solid rgba(245, 158, 11, 0.2);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        text-align: center;
        margin-top: 60px;
    }

    /* Professional Content Cards */
    .section-card {
        background: #111827;
        padding: 30px;
        border-radius: 16px;
        border: 1px solid #1f2937;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 35px;
    }
    
    .section-heading {
        color: #f9fafb !important;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 1px solid #374151;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .list-header {
        font-weight: 700;
        color: #38bdf8;
        border-bottom: 2px solid #1f2937;
        padding-bottom: 6px;
        margin-bottom: 15px;
        font-size: 12px;
        text-transform: uppercase;
    }

    /* Badges */
    .badge-active {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981 !important;
        padding: 3px 12px;
        border-radius: 6px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        font-weight: bold;
    }
    .badge-blocked {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444 !important;
        padding: 3px 12px;
        border-radius: 6px;
        border: 1px solid rgba(239, 68, 68, 0.2);
        font-weight: bold;
    }

    /* Core Branding Footer */
    .dev-footer {
        text-align: center;
        color: #4b5563;
        font-size: 13px;
        font-weight: 600;
        margin-top: 80px;
        padding: 20px 0;
        border-top: 1px solid #1f2937;
    }
    .dev-footer span {
        color: #f59e0b;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION ENGINE ---
if "auth_status" not in st.session_state:
    st.session_state.auth_status = "unauthenticated"

# ==========================================
# 🛑 PROFESSIONAL SECURITY ACCESS GATEWAY
# ==========================================
if st.session_state.auth_status == "unauthenticated":
    _, center_col, _ = st.columns([1.3, 1.4, 1.3])
    with center_col:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #ffffff; font-weight:800; margin-bottom:5px;">🛡️ MZ SECURITY TERMINAL</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #6b7280; font-size:13px; margin-bottom:35px;">AUTHENTICATED SYSTEM ADMIN ACCESS ONLY</p>', unsafe_allow_html=True)
        
        adm_user = st.text_input("ADMIN USERNAME:")
        adm_pass = st.text_input("ADMIN PASSWORD:", type="password")
        
        st.write("")
        if st.button("🔐 ACCESS HUB CORE", type="primary", use_container_width=True):
            if adm_user == "MZAdmin" and adm_pass == "Zubair@786":
                st.session_state.auth_status = "admin"
                st.toast("Authorization Granted.")
                st.rerun()
            else:
                st.error("Access Forbidden: Invalid Control Signatures")
                
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# 🛡️ ADMINISTRATIVE DASHBOARD WORKING AREA
# ==========================================
elif st.session_state.auth_status == "admin":
    title_area, logout_area = st.columns([8.5, 1.5])
    with title_area:
        st.markdown('<h3 style="color: #ffffff; font-weight:800; margin-top:5px;">🛡️ CENTRAL LICENSE ECOSYSTEM</h3>', unsafe_allow_html=True)
    with logout_area:
        if st.button("🚪 CLOSE TERMINAL", use_container_width=True):
            st.session_state.auth_status = "unauthenticated"
            st.rerun()

    st.write("")

    # --- FIREBASE REST CLIENT FUNCTIONS ---
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

    def push_license_secure(hwid, name, sec_key, issuance, expiry, limit, block_date, status, mobile, email, address):
        try:
            payload = {
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
            requests.put(f"{FIREBASE_DB_URL}/security_licenses/{hwid}.json", json=payload)
            return True
        except: return False

    def remove_license_node(hwid):
        try:
            requests.delete(f"{FIREBASE_DB_URL}/security_licenses/{hwid}.json")
            return True
        except: return False

    def remove_pending_request(sec_key):
        try:
            requests.delete(f"{FIREBASE_DB_URL}/registered_keys/{sec_key}.json")
            return True
        except: return False

    # --- POPUP DIALOG WINDOWS ---
    @st.dialog("⚠️ Absolute Core Deletion Request")
    def trigger_deletion_popup(hwid, name):
        st.markdown(f"#### Completely clear node authorization for client: **{name}**?")
        st.write("Warning: The targeted desktop installation will be locked instantly.")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("💥 Wipe Node", use_container_width=True):
                remove_license_node(hwid)
                st.success("Target data purged.")
                st.rerun()
        with b2:
            if st.button("Cancel", use_container_width=True): st.rerun()

    # --- STATE ENGINE MANAGEMENT ---
    if "sel_hwid" not in st.session_state: st.session_state.sel_hwid = ""
    if "sel_name" not in st.session_state: st.session_state.sel_name = ""
    if "sel_sec_key" not in st.session_state: st.session_state.sel_sec_key = ""
    if "sel_limit" not in st.session_state: st.session_state.sel_limit = 30
    if "sel_issue" not in st.session_state: st.session_state.sel_issue = datetime.now().date()
    if "sel_expiry" not in st.session_state: st.session_state.sel_expiry = datetime.now().date() + timedelta(days=365)
    if "sel_block" not in st.session_state: st.session_state.sel_block = "-"
    if "sel_status" not in st.session_state: st.session_state.sel_status = "active"
    if "sel_mobile" not in st.session_state: st.session_state.sel_mobile = ""
    if "sel_email" not in st.session_state: st.session_state.sel_email = ""
    if "sel_address" not in st.session_state: st.session_state.sel_address = ""

    # ==========================================
    # PANEL 1: MASTER CONTROLLER FIELD ENTRY (TOP PANEL)
    # ==========================================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🛠️ Profiles Activation & Variable Calibration</div>', unsafe_allow_html=True)

    c_left, c_right = st.columns(2)
    with c_left:
        in_hwid = st.text_input("Target Hardware ID (HWID):", value=st.session_state.sel_hwid)
        in_name = st.text_input("Customer Name Reference:", value=st.session_state.sel_name)
        in_skey = st.text_input("Configured Security Passkey (Fully Editable):", value=st.session_state.sel_sec_key)
        
        edit_mobile = st.text_input("Client Phone Contact:", value=st.session_state.sel_mobile)
        edit_email = st.text_input("Client Account Email:", value=st.session_state.sel_email)
        edit_address = st.text_input("Physical Premises Address:", value=st.session_state.sel_address)

    with c_right:
        in_days_limit = st.number_input("Allowed Offline Guard Threshold (Days):", min_value=1, max_value=365, value=st.session_state.sel_limit)
        
        st.markdown('<div style="background:#0b0f19; padding:20px; border-radius:12px; border:1px solid #1f2937; margin-top:15px; margin-bottom:15px;">', unsafe_allow_html=True)
        st.markdown('<span style="color:#38bdf8; font-weight:700; font-size:13px;">📅 TIMELINE INTEGRITY OVERRIDE</span>', unsafe_allow_html=True)
        in_issue = st.date_input("Issuance Authentication Date:", value=st.session_state.sel_issue)
        in_expiry = st.date_input("Expiration Enforcement Date:", value=st.session_state.sel_expiry)
        st.markdown('</div>', unsafe_allow_html=True)
        
        select_block_state = st.radio(
            "System Master Execution Policy:",
            ["🟢 Node Authorized / Active Operations", "🚫 Deploy Master Freeze Lock Restriction"],
            index=0 if st.session_state.sel_block == "-" else 1, horizontal=True
        )
        if "Deploy Master Freeze" in select_block_state:
            try: parse_b_date = datetime.strptime(st.session_state.sel_block, "%Y-%m-%d")
            except: parse_b_date = datetime.now()
            picked_block_date = st.date_input("Maintain Blockade Until Date:", parse_b_date)
            assigned_block_val = picked_block_date
            assigned_status_val = "blocked"
        else:
            assigned_block_val = "-"
            assigned_status_val = "active"

    st.write(" ")
    action_box1, action_box2 = st.columns(2)
    with action_box1:
        if st.button("💾 COMMIT VECTOR TO LIVE DATABASE", type="primary", use_container_width=True):
            if in_hwid.strip() and in_skey.strip():
                with st.spinner("Writing parameters safely to nodes..."):
                    committed = push_license_secure(
                        hwid=in_hwid.strip(), 
                        name=in_name.strip(), 
                        sec_key=in_skey.strip(), 
                        issuance=in_issue,
                        expiry=in_expiry, 
                        limit=in_days_limit, 
                        block_date=assigned_block_val, 
                        status=assigned_status_val,
                        mobile=edit_mobile.strip(),
                        email=edit_email.strip(),
                        address=edit_address.strip()
                    )
                    if committed:
                        # Clear request block if it was accepted from queue
                        live_queue = get_all_registered_keys()
                        if in_skey.strip() in live_queue:
                            remove_pending_request(in_skey.strip())
                        
                        st.success(f"System Matrix Successfully Updated for: {in_name}")
                        
                        # Flush active memory buffer
                        st.session_state.sel_hwid = ""
                        st.session_state.sel_name = ""
                        st.session_state.sel_sec_key = ""
                        st.session_state.sel_mobile = ""
                        st.session_state.sel_email = ""
                        st.session_state.sel_address = ""
                        st.session_state.sel_issue = datetime.now().date()
                        st.session_state.sel_expiry = datetime.now().date() + timedelta(days=365)
                        st.session_state.sel_block = "-"
                        st.session_state.sel_status = "active"
                        st.rerun()
            else: st.error("Operation Aborted: HWID & Security Key vectors cannot be evaluated empty.")
            
    with action_box2:
        if st.button("🧹 PURGE ENTRY SLOTS", use_container_width=True):
            st.session_state.sel_hwid = ""
            st.session_state.sel_name = ""
            st.session_state.sel_sec_key = ""
            st.session_state.sel_mobile = ""
            st.session_state.sel_email = ""
            st.session_state.sel_address = ""
            st.session_state.sel_limit = 30
            st.session_state.sel_issue = datetime.now().date()
            st.session_state.sel_expiry = datetime.now().date() + timedelta(days=365)
            st.session_state.sel_block = "-"
            st.session_state.sel_status = "active"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # PANEL 2: LIVE OPERATIONAL SYSTEMS RUNNING (MIDDLE PANEL)
    # ==========================================
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📊 Authorized Production Node Registry</div>', unsafe_allow_html=True)
    filter_string = st.text_input("🔍 Filter Memory Indexes (HWID / Name / Key):", "").lower()

    dc1, dc2, dc3, dc4, dc5, dc6, dc7, dc8 = st.columns([1.6, 1.4, 1.2, 1.3, 1.1, 1.2, 0.6, 0.6])
    dc1.markdown('<div class="list-header">💻 HARDWARE ID</div>', unsafe_allow_html=True)
    dc2.markdown('<div class="list-header">👤 CLIENT NAME</div>', unsafe_allow_html=True)
    dc3.markdown('<div class="list-header">🔑 KEY DEPLOYED</div>', unsafe_allow_html=True)
    dc4.markdown('<div class="list-header">🛡️ HEALTH LIFE</div>', unsafe_allow_html=True)
    dc5.markdown('<div class="list-header">⏳ DEADLINE</div>', unsafe_allow_html=True)
    dc6.markdown('<div class="list-header">📞 PHONE</div>', unsafe_allow_html=True)
    dc7.markdown('<div class="list-header">EDIT</div>', unsafe_allow_html=True)
    dc8.markdown('<div class="list-header">WIPE</div>', unsafe_allow_html=True)

    production_licenses = get_all_licenses()
    matched_any_live = False
    
    for hwid_node, node_data in production_licenses.items():
        n_name = node_data.get("name", "")
        n_skey = node_data.get("security_key", "-")
        n_phone = node_data.get("mobile", "")
        n_mail = node_data.get("email", "")
        n_addr = node_data.get("address", "")
        n_iss = node_data.get("issuance_date", "-")
        n_exp = node_data.get("expiry", "-")

        if filter_string in hwid_node.lower() or filter_string in n_name.lower() or filter_string in n_skey.lower():
            matched_any_live = True
            r1, r2, r3, r4, r5, r6, r7, r8 = st.columns([1.6, 1.4, 1.2, 1.3, 1.1, 1.2, 0.6, 0.6])
            r1.write(f"`{hwid_node}`")
            r2.write(n_name)
            r3.write(f"`{n_skey}`")
            
            if node_data.get("status") == "blocked":
                bl_str = node_data.get("blocked_until", "-")
                try:
                    p_date = datetime.strptime(bl_str, "%Y-%m-%d").date()
                    rem_days = (p_date - datetime.now().date()).days
                    r4.markdown(f'<span class="badge-blocked">🚫 FROZEN ({rem_days} d)</span>', unsafe_allow_html=True)
                except: 
                    r4.markdown('<span class="badge-blocked">🚫 MASTER LOCK</span>', unsafe_allow_html=True)
            else: 
                r4.markdown('<span class="badge-active">🟢 AUTHORIZED</span>', unsafe_allow_html=True)
                
            r5.write(n_exp)
            r6.write(n_phone if n_phone else "No Data")
            
            # EDIT ACTION FUNCTION: Pulls absolutely all data fields to the master configuration box at top!
            if r7.button("✏️", key=f"edit_node_{hwid_node}", use_container_width=True):
                st.session_state.sel_hwid = hwid_node
                st.session_state.sel_name = n_name
                st.session_state.sel_sec_key = n_skey  # Properly map key to enable field overrides
                st.session_state.sel_mobile = n_phone
                st.session_state.sel_email = n_mail
                st.session_state.sel_address = n_addr
                st.session_state.sel_limit = int(node_data.get("offline_limit_days", 30))
                st.session_state.sel_block = node_data.get("blocked_until", "-")
                st.session_state.sel_status = node_data.get("status", "active")
                try: st.session_state.sel_issue = datetime.strptime(n_iss, "%Y-%m-%d").date()
                except: st.session_state.sel_issue = datetime.now().date()
                try: st.session_state.sel_expiry = datetime.strptime(n_exp, "%Y-%m-%d").date()
                except: st.session_state.sel_expiry = datetime.now().date()
                st.toast(f"Data Vectors loaded for client: {n_name}")
                st.rerun()
                
            if r8.button("🗑️", key=f"wipe_node_{hwid_node}", use_container_width=True):
                trigger_deletion_popup(hwid_node, n_name)
            st.markdown("<hr style='margin: 6px 0; border-top: 1px solid #1f2937;'>", unsafe_allow_html=True)

    if not matched_any_live: 
        st.info("Ecosystem Status: No active deployed production hardware matches current filter index.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # PANEL 3: PENDING INBOUND CONNECTION REQUESTS (SABSY NICHY - BOTTOM PANEL)
    # ==========================================
    st.markdown('<div class="section-card" style="border-top: 4px solid #f59e0b;">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading" style="color: #f59e0b !important;">📋 Inbound Device Pipeline Connections (Awaiting Verification)</div>', unsafe_allow_html=True)
    
    unapproved_queue = get_all_registered_keys()
    if unapproved_queue:
        qh1, qh2, qh3, qh4, qh5, qh6 = st.columns([1.5, 1.3, 1.2, 1.8, 1.0, 1.0])
        qh1.markdown('<div class="list-header">👤 PROSPECT CLIENT</div>', unsafe_allow_html=True)
        qh2.markdown('<div class="list-header">🔑 KEY DEPLOYED BY USER</div>', unsafe_allow_html=True)
        qh3.markdown('<div class="list-header">📱 PHONE NUMBER</div>', unsafe_allow_html=True)
        qh4.markdown('<div class="list-header">💻 REQUESTING HARDWARE SOURCE</div>', unsafe_allow_html=True)
        qh5.markdown('<div class="list-header">EVALUATE PIPELINE</div>', unsafe_allow_html=True)
        qh6.markdown('<div class="list-header">DISCARD</div>', unsafe_allow_html=True)

        for req_key, req_val in unapproved_queue.items():
            q_name = req_val.get("name", "Unknown Client")
            q_phone = req_val.get("phone", "")
            q_hwid = req_val.get("hardware_id", "UNKNOWN_SOURCE_ID")
            q_email = req_val.get("email", "")
            q_address = req_val.get("address", "")
            q_issue = req_val.get("issue_date", str(datetime.now().date()))
            q_expiry = req_val.get("expiry_date", str(datetime.now().date() + timedelta(days=365)))

            qc1, qc2, qc3, qc4, qc5, qc6 = st.columns([1.5, 1.3, 1.2, 1.8, 1.0, 1.0])
            qc1.write(q_name)
            qc2.write(f"`{req_key}`")
            qc3.write(q_phone if q_phone else "Not Given")
            qc4.write(f"`{q_hwid}`")
            
            # VALIDATE PIPELINE ACTION: Safely sends data fields to top input parameters for adjustments
            if qc5.button("Verify & Load 👍", key=f"load_req_{req_key}", use_container_width=True):
                st.session_state.sel_hwid = q_hwid
                st.session_state.sel_name = q_name
                st.session_state.sel_sec_key = req_key
                st.session_state.sel_mobile = q_phone
                st.session_state.sel_email = q_email
                st.session_state.sel_address = q_address
                try: st.session_state.sel_issue = datetime.strptime(q_issue, "%Y-%m-%d").date()
                except: st.session_state.sel_issue = datetime.now().date()
                try: st.session_state.sel_expiry = datetime.strptime(q_expiry, "%Y-%m-%d").date()
                except: st.session_state.sel_expiry = datetime.now().date()
                st.toast(f"Pipeline Request loaded for {q_name}. Map parameters above to register live link.")
                st.rerun()

            if qc6.button("Reject Request ❌", key=f"drop_req_{req_key}", use_container_width=True):
                remove_pending_request(req_key)
                st.toast(f"Connection string request from {q_name} drop successfully.")
                st.rerun()
            st.markdown("<hr style='margin: 6px 0; border-top: 1px solid #1f2937;'>", unsafe_allow_html=True)
    else:
        st.info("Pipeline Sync Status: Clear. No inbound remote registration requests are floating on the server network.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- HIGH-END BRANDED FOOTER ---
st.markdown('<div class="dev-footer">🚀 Powered by <span>Muhammad Zubair</span> | Safe-Guard POS Licensing Server Engine</div>', unsafe_allow_html=True)