import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MZ Central Hub - Terminal", page_icon="🛡️", layout="wide")

# FRESH FIREBASE PROJECT URL
FIREBASE_DB_URL = "https://zubairposbackup-default-rtdb.firebaseio.com/"

# --- ULTRA-PREMIUM ENTERPRISE DESIGN CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    /* Master Background & Typography Reset */
    .stApp { 
        background: radial-gradient(circle at 50% 0%, #0f172a, #020617); 
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Smooth Global Animations */
    * {
        transition: background-color 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }

    /* Premium Glassmorphic Container Blocks */
    .login-box {
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        padding: 45px;
        border-radius: 24px;
        border: 1px solid rgba(56, 189, 248, 0.15);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.05);
        text-align: center;
        margin-top: 60px;
    }

    .section-card {
        background: rgba(15, 23, 42, 0.35);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 28px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
    }

    /* Native Widget Interface Overrides */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        background-color: rgba(2, 6, 23, 0.6) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(51, 65, 85, 0.7) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 500 !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus, .stDateInput input:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 15px rgba(14, 165, 233, 0.25) !important;
    }
    
    /* Native Buttons - High End Interactive Micro-Physics */
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        border: none !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 14px rgba(14, 165, 233, 0.4) !important;
    }
    button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.6) !important;
    }
    button[data-testid="baseButton-primary"]:active {
        transform: translateY(0);
    }

    button[data-testid="baseButton-secondary"] {
        background: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
    }
    button[data-testid="baseButton-secondary"]:hover {
        background: rgba(51, 65, 85, 0.7) !important;
        color: #38bdf8 !important;
        border-color: rgba(56, 189, 248, 0.3) !important;
    }

    /* Form Field Labels Custom Typo */
    label, div[data-testid="stMarkdownContainer"] p {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        letter-spacing: 0.3px;
    }

    /* Clean Enterprise Data Rows & Grid Headers */
    .list-header {
        font-weight: 700;
        color: #0ea5e9;
        border-bottom: 1px solid rgba(56, 189, 248, 0.2);
        padding-bottom: 10px;
        margin-bottom: 15px;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .data-row-container {
        padding: 8px 0;
        align-items: center;
    }

    /* Status Badges */
    .badge-active { 
        background: rgba(16, 185, 129, 0.1); 
        color: #10b981 !important; 
        padding: 5px 14px; 
        border-radius: 20px; 
        border: 1px solid rgba(16, 185, 129, 0.25); 
        font-weight: 700; 
        font-size: 11px;
        letter-spacing: 0.5px;
    }
    .badge-blocked { 
        background: rgba(239, 68, 68, 0.1); 
        color: #ef4444 !important; 
        padding: 5px 14px; 
        border-radius: 20px; 
        border: 1px solid rgba(239, 68, 68, 0.25); 
        font-weight: 700; 
        font-size: 11px;
        letter-spacing: 0.5px;
    }

    /* Typography Branding Elements */
    .brand-title { 
        color: #ffffff; 
        font-size: 32px; 
        font-weight: 800; 
        letter-spacing: 1.5px; 
        background: linear-gradient(to right, #ffffff, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px; 
    }
    .brand-sub { 
        color: #64748b; 
        font-size: 11px; 
        margin-bottom: 35px; 
        letter-spacing: 3px; 
        font-weight: 700;
    }
    
    /* Custom Inline Code Styling for Monospace Data */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        color: #38bdf8 !important;
        background: rgba(56, 189, 248, 0.08) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        padding: 3px 6px !important;
        border-radius: 6px !important;
        font-size: 12.5px !important;
    }

    /* Persistent Top Horizontal Rule Spacer */
    hr {
        border-color: rgba(255, 255, 255, 0.05) !important;
        margin: 20px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FIREBASE FUNCTIONS ---
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
            "name": name, "security_key": sec_key, "mobile": mobile, "email": email, "address": address, 
            "issuance_date": str(issuance), "expiry": str(expiry), "status": status,
            "blocked_until": str(block_date), "offline_limit_days": int(limit)
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

# --- STATE ENGINE MANAGEMENT ---
if "auth_status" not in st.session_state: st.session_state.auth_status = "unauthenticated"
if "nav_page" not in st.session_state: st.session_state.nav_page = "home" 
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
# 🛑 SECURITY ACCESS GATEWAY (LOGIN)
# ==========================================
if st.session_state.auth_status == "unauthenticated":
    _, col_login, _ = st.columns([1, 1.3, 1])
    
    with col_login:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<div class="brand-title">🛡️ MZ SECURITY HUB</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">ENTERPRISE LICENSE ARCHITECTURE</div>', unsafe_allow_html=True)
        
        adm_user = st.text_input("ADMIN USERNAME", placeholder="Enter authorization ID...")
        adm_pass = st.text_input("SECURITY PIN", type="password", placeholder="Enter master access signature...")
        
        st.write("")
        if st.button("🔐 AUTHENTICATE SYSTEM", type="primary", use_container_width=True):
            if adm_user == "MZAdmin" and adm_pass == "Zubair@786":
                st.session_state.auth_status = "admin"
                st.rerun()
            else:
                st.error("❌ Access Forbidden: Invalid Signature Credentials")
                
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# 🛡️ ADMINISTRATIVE DASHBOARD (LOGGED IN)
# ==========================================
elif st.session_state.auth_status == "admin":
    # --- PERSISTENT TOP NAVIGATION CONTROLLER ---
    unapproved_queue = get_all_registered_keys()
    req_count = len(unapproved_queue)
    req_btn_text = f"📩 PENDING INBOUND PIPELINE ({req_count})" if req_count > 0 else "📩 PENDING INBOUND PIPELINE"

    # Sleek Sticky Nav Structure
    nav_col1, nav_col2, nav_logout = st.columns([4, 4, 2])
    
    with nav_col1:
        if st.button("🏠 DASHBOARD & ACTIVE PRODUCTION NODES", type="primary" if st.session_state.nav_page == "home" else "secondary", use_container_width=True):
            st.session_state.nav_page = "home"
            st.rerun()
    with nav_col2:
        if st.button(req_btn_text, type="primary" if st.session_state.nav_page == "requests" else "secondary", use_container_width=True):
            st.session_state.nav_page = "requests"
            st.rerun()
    with nav_logout:
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.auth_status = "unauthenticated"
            st.rerun()

    st.markdown("<hr style='margin: 10px 0 25px 0 !important;'>", unsafe_allow_html=True)

    # ==========================================
    # VIEW 1: HOME (REGISTRATION & ACTIVE LIST)
    # ==========================================
    if st.session_state.nav_page == "home":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#ffffff; font-weight:700; margin-bottom: 25px; font-size:16px; letter-spacing:0.5px;">⚙️ PROFILE CONFIGURATION MATRIX</h4>', unsafe_allow_html=True)

        c_left, c_right = st.columns(2)
        with c_left:
            in_hwid = st.text_input("Target Hardware ID (HWID):", value=st.session_state.sel_hwid)
            in_name = st.text_input("Customer Name:", value=st.session_state.sel_name)
            in_skey = st.text_input("Security Passkey:", value=st.session_state.sel_sec_key)
            edit_mobile = st.text_input("Client Phone Configuration:", value=st.session_state.sel_mobile)
            edit_email = st.text_input("Client Email Address:", value=st.session_state.sel_email)
            edit_address = st.text_input("Physical Node Location:", value=st.session_state.sel_address)

        with c_right:
            in_days_limit = st.number_input("Offline Guard Threshold Limit (Days):", min_value=1, max_value=365, value=st.session_state.sel_limit)
            
            st.markdown('<div style="background: rgba(2, 6, 23, 0.4); padding:20px; border-radius:14px; border:1px solid rgba(255,255,255,0.04); margin:18px 0;">', unsafe_allow_html=True)
            in_issue = st.date_input("Vector Issuance Date:", value=st.session_state.sel_issue)
            in_expiry = st.date_input("Vector Expiration Date:", value=st.session_state.sel_expiry)
            st.markdown('</div>', unsafe_allow_html=True)
            
            select_block_state = st.radio(
                "Execution Protocol Policy:",
                ["🟢 Authorized / Active Run", "🚫 Master Freeze Lockout"],
                index=0 if st.session_state.sel_block == "-" else 1, horizontal=True
            )
            if "Freeze Lockout" in select_block_state:
                try: parse_b_date = datetime.strptime(st.session_state.sel_block, "%Y-%m-%d")
                except: parse_b_date = datetime.now()
                assigned_block_val = st.date_input("Maintain Policy Blockade Until:", parse_b_date)
                assigned_status_val = "blocked"
            else:
                assigned_block_val = "-"
                assigned_status_val = "active"

        st.write(" ")
        action_box1, action_box2 = st.columns(2)
        with action_box1:
            if st.button("💾 COMMIT VECTOR TO LIVE ENGINES", type="primary", use_container_width=True):
                if in_hwid.strip() and in_skey.strip():
                    with st.spinner("Synchronizing parameters safely with secure nodes..."):
                        committed = push_license_secure(
                            in_hwid.strip(), in_name.strip(), in_skey.strip(), in_issue, in_expiry, 
                            in_days_limit, assigned_block_val, assigned_status_val,
                            edit_mobile.strip(), edit_email.strip(), edit_address.strip()
                        )
                        if committed:
                            if in_skey.strip() in unapproved_queue: remove_pending_request(in_skey.strip())
                            st.success(f"Execution Parameters Comitted for Node: {in_name}")
                            st.session_state.sel_hwid = ""
                            st.session_state.sel_name = ""
                            st.session_state.sel_sec_key = ""
                            st.session_state.sel_mobile = ""
                            st.session_state.sel_email = ""
                            st.session_state.sel_address = ""
                            st.session_state.sel_issue = datetime.now().date()
                            st.session_state.sel_expiry = datetime.now().date() + timedelta(days=365)
                            st.rerun()
                else: st.error("Validation Halt: HWID & Security Passkey variables are strictly required!")
                
        with action_box2:
            if st.button("🧹 PURGE BUFFER / CLEAR FORM", use_container_width=True):
                st.session_state.sel_hwid = ""
                st.session_state.sel_name = ""
                st.session_state.sel_sec_key = ""
                st.session_state.sel_mobile = ""
                st.session_state.sel_email = ""
                st.session_state.sel_address = ""
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # PANEL: ACTIVE LIVE SYSTEMS
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#ffffff; font-weight:700; margin-bottom: 25px; font-size:16px; letter-spacing:0.5px;">📊 AUTHORIZED PRODUCTION DATA MATRIX</h4>', unsafe_allow_html=True)
        
        # INSTANT GLOBAL FILTER
        filter_string = st.text_input("🔍 Real-time Filter Interface (Name, Key, HWID, Phone, Address):", "").lower()
        st.write(" ")

        # Column Layout Optimised to display complete 16-character HWID string flawlessly
        dc1, dc2, dc3, dc4, dc5, dc6, dc7, dc8 = st.columns([2.3, 1.4, 1.2, 1.3, 1.1, 1.1, 0.4, 0.4])
        dc1.markdown('<div class="list-header">Target HWID</div>', unsafe_allow_html=True)
        dc2.markdown('<div class="list-header">Client Identity</div>', unsafe_allow_html=True)
        dc3.markdown('<div class="list-header">Passkey</div>', unsafe_allow_html=True)
        dc4.markdown('<div class="list-header">Node Health</div>', unsafe_allow_html=True)
        dc5.markdown('<div class="list-header">Expiration</div>', unsafe_allow_html=True)
        dc6.markdown('<div class="list-header">Comms Contact</div>', unsafe_allow_html=True)
        dc7.markdown('<div class="list-header">Edit</div>', unsafe_allow_html=True)
        dc8.markdown('<div class="list-header">Wipe</div>', unsafe_allow_html=True)

        production_licenses = get_all_licenses()
        matched_any = False
        
        for hwid_node, node_data in production_licenses.items():
            n_name = node_data.get("name", "")
            n_skey = node_data.get("security_key", "-")
            n_phone = node_data.get("mobile", "")
            n_address = node_data.get("address", "")
            
            if (filter_string in hwid_node.lower() or 
                filter_string in n_name.lower() or 
                filter_string in n_skey.lower() or
                filter_string in n_phone.lower() or
                filter_string in n_address.lower()):
                
                matched_any = True
                r1, r2, r3, r4, r5, r6, r7, r8 = st.columns([2.3, 1.4, 1.2, 1.3, 1.1, 1.1, 0.4, 0.4])
                
                with r1: st.markdown(f"`{hwid_node}`", unsafe_allow_html=True) # Full 16-Char HWID No Truncation
                with r2: st.markdown(f"<span style='font-weight:600; color:#e2e8f0;'>{n_name}</span>", unsafe_allow_html=True)
                with r3: st.markdown(f"`{n_skey}`", unsafe_allow_html=True)
                
                with r4:
                    if node_data.get("status") == "blocked": 
                        st.markdown('<span class="badge-blocked">🚫 FROZEN RESTRAIN</span>', unsafe_allow_html=True)
                    else: 
                        st.markdown('<span class="badge-active">🟢 OPERATIONAL</span>', unsafe_allow_html=True)
                    
                with r5: st.markdown(f"<span style='color:#94a3b8; font-family:\"JetBrains Mono\"; font-size:13px;'>{node_data.get('expiry', '-')}</span>", unsafe_allow_html=True)
                with r6: st.markdown(f"<span style='color:#cbd5e1; font-size:13px;'>{n_phone if n_phone else '-'}</span>", unsafe_allow_html=True)
                
                if r7.button("✏️", key=f"edit_{hwid_node}", use_container_width=True):
                    st.session_state.sel_hwid = hwid_node
                    st.session_state.sel_name = n_name
                    st.session_state.sel_sec_key = n_skey
                    st.session_state.sel_mobile = n_phone
                    st.session_state.sel_email = node_data.get("email", "")
                    st.session_state.sel_address = n_address
                    st.session_state.sel_limit = int(node_data.get("offline_limit_days", 30))
                    st.session_state.sel_block = node_data.get("blocked_until", "-")
                    st.session_state.sel_status = node_data.get("status", "active")
                    try: st.session_state.sel_issue = datetime.strptime(node_data.get("issuance_date", ""), "%Y-%m-%d").date()
                    except: pass
                    try: st.session_state.sel_expiry = datetime.strptime(node_data.get("expiry", ""), "%Y-%m-%d").date()
                    except: pass
                    st.rerun()
                    
                if r8.button("🗑️", key=f"wipe_{hwid_node}", use_container_width=True):
                    remove_license_node(hwid_node)
                    st.rerun()
                    
                st.markdown("<hr style='margin: 4px 0 !important; opacity:0.3;'>", unsafe_allow_html=True)

        if not matched_any: 
            st.info("System Notification: Search parameter matched zero active production records.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # VIEW 2: PENDING REQUESTS MENU
    # ==========================================
    elif st.session_state.nav_page == "requests":
        st.markdown('<div class="section-card" style="border: 1px solid rgba(245, 158, 11, 0.25);">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#f59e0b; font-weight:700; margin-bottom: 25px; font-size:16px; letter-spacing:0.5px;">📋 INBOUND DEVICE PIPELINE INFRASTRUCTURE</h4>', unsafe_allow_html=True)
        
        if unapproved_queue:
            req_search = st.text_input("🔍 Real-time Filter Request Vault (ID, Name, Phone, Address):", "").lower()
            st.write(" ")

            # Column weights optimized to fit the complete 16-character request HWID
            qh1, qh2, qh3, qh4, qh5, qh6, qh7 = st.columns([1.3, 1.0, 1.1, 1.3, 2.3, 0.9, 0.9])
            qh1.markdown('<div class="list-header">Client Identity</div>', unsafe_allow_html=True)
            qh2.markdown('<div class="list-header">Assigned Key</div>', unsafe_allow_html=True)
            qh3.markdown('<div class="list-header">Contact Comms</div>', unsafe_allow_html=True)
            qh4.markdown('<div class="list-header">📍 Node Location</div>', unsafe_allow_html=True)
            qh5.markdown('<div class="list-header">Request HWID</div>', unsafe_allow_html=True)
            qh6.markdown('<div class="list-header">Stage Load</div>', unsafe_allow_html=True)
            qh7.markdown('<div class="list-header">Drop Request</div>', unsafe_allow_html=True)

            req_matched = False
            for req_key, req_val in unapproved_queue.items():
                q_name = req_val.get("name", "Unknown")
                q_phone = req_val.get("phone", "")
                q_address = req_val.get("address", "N/A") 
                q_hwid = req_val.get("hardware_id", "UNKNOWN")
                q_email = req_val.get("email", "")
                q_issue = req_val.get("issue_date", str(datetime.now().date()))
                q_expiry = req_val.get("expiry_date", str(datetime.now().date() + timedelta(days=365)))

                if (req_search in q_name.lower() or 
                    req_search in req_key.lower() or 
                    req_search in q_phone.lower() or 
                    req_search in q_address.lower() or 
                    req_search in q_hwid.lower()):
                    
                    req_matched = True
                    qc1, qc2, qc3, qc4, qc5, qc6, qc7 = st.columns([1.3, 1.0, 1.1, 1.3, 2.3, 0.9, 0.9])
                    
                    with qc1: st.markdown(f"<span style='font-weight:600; color:#e2e8f0;'>{q_name}</span>", unsafe_allow_html=True)
                    with qc2: st.markdown(f"`{req_key}`", unsafe_allow_html=True)
                    with qc3: st.markdown(f"<span style='color:#cbd5e1; font-size:13px;'>{q_phone}</span>", unsafe_allow_html=True)
                    with qc4: st.markdown(f"<span style='color:#94a3b8; font-style:italic; font-size:13px;'>{q_address[:24]}</span>", unsafe_allow_html=True) 
                    with qc5: st.markdown(f"`{q_hwid}`", unsafe_allow_html=True) # Full HWID displays perfectly now
                    
                    if qc6.button("Load 👍", key=f"load_{req_key}", use_container_width=True):
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
                        
                        st.session_state.nav_page = "home"
                        st.rerun()

                    if qc7.button("Drop ❌", key=f"drop_{req_key}", use_container_width=True):
                        remove_pending_request(req_key)
                        st.rerun()
                        
                    st.markdown("<hr style='margin: 4px 0 !important; opacity:0.3;'>", unsafe_allow_html=True)
            
            if not req_matched:
                st.info("System Notification: Search filter matched zero records inside the pending inbound queue.")
        else:
            st.info("Pipeline Status Check: Clear. Zero inbound device requests waiting validation.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- PREMIUM FOOTER ARCHITECTURE ---
st.markdown("""
    <div style="text-align: center; color: #475569; font-size: 12px; margin-top: 80px; font-weight: 600; letter-spacing: 1px;">
        ENGINEERED BY <span style="color:#0ea5e9; font-weight:800;">MUHAMMAD ZUBAIR</span> | SECURE POS DISTRIBUTED DATA SYSTEMS ARCHITECTURE v2.0
    </div>
""", unsafe_allow_html=True)