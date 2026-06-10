import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MZ Central Hub - Terminal", page_icon="🛡️", layout="wide")

# FRESH FIREBASE PROJECT URL
FIREBASE_DB_URL = "https://zubairposbackup-default-rtdb.firebaseio.com/"

# --- ULTRA-PREMIUM ENTERPRISE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    /* Master Background */
    .stApp { 
        background: radial-gradient(circle at center, #1e293b, #020617); 
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Login Screen - Glassmorphism Magic */
    .login-box {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 50px;
        border-radius: 24px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 0 40px rgba(14, 165, 233, 0.2), inset 0 0 20px rgba(255,255,255,0.05);
        text-align: center;
        margin-top: 50px;
    }

    /* Input Fields Styling */
    .stTextInput input {
        background-color: #0f172a !important;
        color: #38bdf8 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-weight: 600;
    }
    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.4) !important;
    }
    
    /* Labels */
    label, div[data-testid="stMarkdownContainer"] p {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        letter-spacing: 0.5px;
    }

    /* Content Cards */
    .section-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }

    .list-header {
        font-weight: 800;
        color: #38bdf8;
        border-bottom: 2px solid #334155;
        padding-bottom: 8px;
        margin-bottom: 15px;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Badges */
    .badge-active { background: rgba(16, 185, 129, 0.15); color: #34d399 !important; padding: 4px 12px; border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: bold; font-size: 12px;}
    .badge-blocked { background: rgba(239, 68, 68, 0.15); color: #f87171 !important; padding: 4px 12px; border-radius: 6px; border: 1px solid rgba(239, 68, 68, 0.3); font-weight: bold; font-size: 12px;}

    /* Top Brand */
    .brand-title { color: #ffffff; font-size: 28px; font-weight: 800; letter-spacing: 1px; text-shadow: 0 0 20px rgba(56,189,248,0.5); margin-bottom: 5px; }
    .brand-sub { color: #94a3b8; font-size: 14px; margin-bottom: 30px; letter-spacing: 2px; }
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
# 🛑 PROFESSIONAL SECURITY ACCESS GATEWAY (LOGIN)
# ==========================================
if st.session_state.auth_status == "unauthenticated":
    # Using columns to center the login box properly like a real web app
    _, col_login, _ = st.columns([1, 1.5, 1])
    
    with col_login:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<div class="brand-title">🛡️ MZ SECURITY HUB</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">ENTERPRISE LICENSE MANAGEMENT</div>', unsafe_allow_html=True)
        
        adm_user = st.text_input("ADMIN USERNAME", placeholder="Enter your identity...")
        adm_pass = st.text_input("SECURITY PIN", type="password", placeholder="Enter master key...")
        
        st.write("")
        if st.button("🔐 AUTHENTICATE & ENTER", type="primary", use_container_width=True):
            if adm_user == "MZAdmin" and adm_pass == "Zubair@786":
                st.session_state.auth_status = "admin"
                st.rerun()
            else:
                st.error("❌ Access Forbidden: Invalid Credentials")
                
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# 🛡️ ADMINISTRATIVE DASHBOARD (LOGGED IN)
# ==========================================
elif st.session_state.auth_status == "admin":
    # --- HEADER & NAVIGATION ---
    head_col1, head_col2 = st.columns([8, 2])
    with head_col1:
        st.markdown('<h2 style="color: #ffffff; font-weight:800; margin-top:0;">🛡️ SAFE-GUARD CENTRAL</h2>', unsafe_allow_html=True)
    with head_col2:
        if st.button("🚪 SYSTEM LOGOUT", use_container_width=True):
            st.session_state.auth_status = "unauthenticated"
            st.rerun()

    unapproved_queue = get_all_registered_keys()
    req_count = len(unapproved_queue)
    req_btn_text = f"📩 PENDING REQUESTS ({req_count})" if req_count > 0 else "📩 PENDING REQUESTS"

    # CUSTOM TAB MENU
    nav_col1, nav_col2, _ = st.columns([3, 3, 4])
    with nav_col1:
        if st.button("🏠 DASHBOARD & ACTIVE NODES", type="primary" if st.session_state.nav_page == "home" else "secondary", use_container_width=True):
            st.session_state.nav_page = "home"
            st.rerun()
    with nav_col2:
        if st.button(req_btn_text, type="primary" if st.session_state.nav_page == "requests" else "secondary", use_container_width=True):
            st.session_state.nav_page = "requests"
            st.rerun()
    st.write("")

    # ==========================================
    # VIEW 1: HOME (REGISTRATION & ACTIVE LIST)
    # ==========================================
    if st.session_state.nav_page == "home":
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#f8fafc; margin-bottom: 20px;">⚙️ Profile Activation & Variables</h4>', unsafe_allow_html=True)

        c_left, c_right = st.columns(2)
        with c_left:
            in_hwid = st.text_input("Target Hardware ID (HWID):", value=st.session_state.sel_hwid)
            in_name = st.text_input("Customer Name:", value=st.session_state.sel_name)
            in_skey = st.text_input("Security Passkey:", value=st.session_state.sel_sec_key)
            edit_mobile = st.text_input("Client Phone:", value=st.session_state.sel_mobile)
            edit_email = st.text_input("Client Email:", value=st.session_state.sel_email)
            edit_address = st.text_input("Physical Address:", value=st.session_state.sel_address)

        with c_right:
            in_days_limit = st.number_input("Offline Guard Threshold (Days):", min_value=1, max_value=365, value=st.session_state.sel_limit)
            
            st.markdown('<div style="background:#020617; padding:15px; border-radius:10px; border:1px solid #1e293b; margin:15px 0;">', unsafe_allow_html=True)
            in_issue = st.date_input("Issuance Date:", value=st.session_state.sel_issue)
            in_expiry = st.date_input("Expiration Date:", value=st.session_state.sel_expiry)
            st.markdown('</div>', unsafe_allow_html=True)
            
            select_block_state = st.radio(
                "Execution Policy:",
                ["🟢 Authorized / Active", "🚫 Master Freeze Lock"],
                index=0 if st.session_state.sel_block == "-" else 1, horizontal=True
            )
            if "Freeze Lock" in select_block_state:
                try: parse_b_date = datetime.strptime(st.session_state.sel_block, "%Y-%m-%d")
                except: parse_b_date = datetime.now()
                assigned_block_val = st.date_input("Maintain Blockade Until:", parse_b_date)
                assigned_status_val = "blocked"
            else:
                assigned_block_val = "-"
                assigned_status_val = "active"

        st.write(" ")
        action_box1, action_box2 = st.columns(2)
        with action_box1:
            if st.button("💾 COMMIT VECTOR TO DATABASE", type="primary", use_container_width=True):
                if in_hwid.strip() and in_skey.strip():
                    with st.spinner("Writing parameters safely..."):
                        committed = push_license_secure(
                            in_hwid.strip(), in_name.strip(), in_skey.strip(), in_issue, in_expiry, 
                            in_days_limit, assigned_block_val, assigned_status_val,
                            edit_mobile.strip(), edit_email.strip(), edit_address.strip()
                        )
                        if committed:
                            if in_skey.strip() in unapproved_queue: remove_pending_request(in_skey.strip())
                            st.success(f"Successfully Updated for: {in_name}")
                            st.session_state.sel_hwid = ""
                            st.session_state.sel_name = ""
                            st.session_state.sel_sec_key = ""
                            st.session_state.sel_mobile = ""
                            st.session_state.sel_email = ""
                            st.session_state.sel_address = ""
                            st.session_state.sel_issue = datetime.now().date()
                            st.session_state.sel_expiry = datetime.now().date() + timedelta(days=365)
                            st.rerun()
                else: st.error("HWID & Security Key are required!")
                
        with action_box2:
            if st.button("🧹 CLEAR FORM", use_container_width=True):
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
        st.markdown('<h4 style="color:#f8fafc; margin-bottom: 20px;">📊 Authorized Production Nodes</h4>', unsafe_allow_html=True)
        
        # HOME SEARCH BAR
        filter_string = st.text_input("🔍 Search Database (Name, Key, HWID, Phone, Address):", "").lower()

        dc1, dc2, dc3, dc4, dc5, dc6, dc7, dc8 = st.columns([1.6, 1.4, 1.2, 1.3, 1.1, 1.2, 0.6, 0.6])
        dc1.markdown('<div class="list-header">HWID</div>', unsafe_allow_html=True)
        dc2.markdown('<div class="list-header">CLIENT NAME</div>', unsafe_allow_html=True)
        dc3.markdown('<div class="list-header">SEC KEY</div>', unsafe_allow_html=True)
        dc4.markdown('<div class="list-header">HEALTH</div>', unsafe_allow_html=True)
        dc5.markdown('<div class="list-header">EXPIRY</div>', unsafe_allow_html=True)
        dc6.markdown('<div class="list-header">PHONE</div>', unsafe_allow_html=True)
        dc7.markdown('<div class="list-header">EDIT</div>', unsafe_allow_html=True)
        dc8.markdown('<div class="list-header">DEL</div>', unsafe_allow_html=True)

        production_licenses = get_all_licenses()
        matched_any = False
        
        for hwid_node, node_data in production_licenses.items():
            n_name = node_data.get("name", "")
            n_skey = node_data.get("security_key", "-")
            n_phone = node_data.get("mobile", "")
            n_address = node_data.get("address", "")
            
            # ADVANCED FILTERING LOGIC
            if (filter_string in hwid_node.lower() or 
                filter_string in n_name.lower() or 
                filter_string in n_skey.lower() or
                filter_string in n_phone.lower() or
                filter_string in n_address.lower()):
                
                matched_any = True
                r1, r2, r3, r4, r5, r6, r7, r8 = st.columns([1.6, 1.4, 1.2, 1.3, 1.1, 1.2, 0.6, 0.6])
                r1.write(f"`{hwid_node[:15]}...`")
                r2.write(n_name)
                r3.write(f"`{n_skey}`")
                
                if node_data.get("status") == "blocked": r4.markdown('<span class="badge-blocked">🚫 FROZEN</span>', unsafe_allow_html=True)
                else: r4.markdown('<span class="badge-active">🟢 ACTIVE</span>', unsafe_allow_html=True)
                    
                r5.write(node_data.get("expiry", "-"))
                r6.write(n_phone if n_phone else "-")
                
                if r7.button("✏️", key=f"edit_{hwid_node}"):
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
                    
                if r8.button("🗑️", key=f"wipe_{hwid_node}"):
                    remove_license_node(hwid_node)
                    st.rerun()
                st.markdown("<hr style='margin: 5px 0; border-top: 1px solid #1e293b;'>", unsafe_allow_html=True)

        if not matched_any: st.info("No active licenses found.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # VIEW 2: PENDING REQUESTS MENU
    # ==========================================
    elif st.session_state.nav_page == "requests":
        st.markdown('<div class="section-card" style="border: 1px solid #f59e0b;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color:#f59e0b; margin-bottom: 20px;">📋 Inbound Device Pipeline</h4>', unsafe_allow_html=True)
        
        if unapproved_queue:
            # REQUESTS SEARCH BAR ADDED HERE
            req_search = st.text_input("🔍 Search Requests (ID, Name, Phone, Address):", "").lower()
            st.write("")

            qh1, qh2, qh3, qh4, qh5, qh6, qh7 = st.columns([1.5, 1.2, 1.2, 1.5, 1.2, 1.0, 1.0])
            qh1.markdown('<div class="list-header">CLIENT NAME</div>', unsafe_allow_html=True)
            qh2.markdown('<div class="list-header">KEY</div>', unsafe_allow_html=True)
            qh3.markdown('<div class="list-header">PHONE</div>', unsafe_allow_html=True)
            qh4.markdown('<div class="list-header">📍 LOCATION/ADDR</div>', unsafe_allow_html=True)
            qh5.markdown('<div class="list-header">HWID</div>', unsafe_allow_html=True)
            qh6.markdown('<div class="list-header">ACTION</div>', unsafe_allow_html=True)
            qh7.markdown('<div class="list-header">REJECT</div>', unsafe_allow_html=True)

            req_matched = False
            for req_key, req_val in unapproved_queue.items():
                q_name = req_val.get("name", "Unknown")
                q_phone = req_val.get("phone", "")
                q_address = req_val.get("address", "N/A") 
                q_hwid = req_val.get("hardware_id", "UNKNOWN")
                q_email = req_val.get("email", "")
                q_issue = req_val.get("issue_date", str(datetime.now().date()))
                q_expiry = req_val.get("expiry_date", str(datetime.now().date() + timedelta(days=365)))

                # REQUESTS FILTERING LOGIC
                if (req_search in q_name.lower() or 
                    req_search in req_key.lower() or 
                    req_search in q_phone.lower() or 
                    req_search in q_address.lower() or 
                    req_search in q_hwid.lower()):
                    
                    req_matched = True
                    qc1, qc2, qc3, qc4, qc5, qc6, qc7 = st.columns([1.5, 1.2, 1.2, 1.5, 1.2, 1.0, 1.0])
                    qc1.write(q_name)
                    qc2.write(f"`{req_key}`")
                    qc3.write(q_phone)
                    qc4.write(f"*{q_address[:20]}*") 
                    qc5.write(f"`{q_hwid[:8]}...`")
                    
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
                    st.markdown("<hr style='margin: 6px 0; border-top: 1px solid #1e293b;'>", unsafe_allow_html=True)
            
            if not req_matched:
                st.info("No matching requests found based on your search.")
        else:
            st.info("Pipeline Status: Clear. No pending requests.")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align: center; color: #475569; font-size: 13px; margin-top: 50px;">🚀 Powered by <span style="color:#38bdf8; font-weight:bold;">Muhammad Zubair</span> | Secure POS Architecture</div>', unsafe_allow_html=True)