import streamlit as st
import requests
import threading
import time
import random
import string
import json
import re
from datetime import datetime
from urllib.parse import unquote

# =========================================================
# Page configuration
# =========================================================
st.set_page_config(
    page_title="MR WALEED OFFLINE",
    page_icon="☠️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# HARDCODED PASSWORD
# =========================================================
PANEL_PASSWORD = "Rishu@12345"

# =========================================================
# PERMANENT GITHUB TXT FILES (HARDCODED - NO CHANGE NEEDED)
# =========================================================
TXT_FILES = {
    # 45K RISHI BRAND GAALI
    "45K RISHI BRAND GAALI.txt": "https://raw.githubusercontent.com/rishikesh199-cmpk/COOKIES-OFFLINE-FAVOURITE-/main/45K%20RISHI%20BRAND%20GAALI.txt",
    
    # RISHI NP 30xl
    "RISHI NP 30xl.txt": "https://raw.githubusercontent.com/rishikesh199-cmpk/COOKIES-OFFLINE-FAVOURITE-/main/RISHI%20NP%2030xl.txt",
    
    # bot response text
    "bot_response_text.txt": "https://raw.githubusercontent.com/rishikesh199-cmpk/COOKIES-OFFLINE-FAVOURITE-/main/bot_response_text.txt",
    
    # EXTRA FILES (PERMANENT)
    "HATE MESSAGES 1.txt": "https://raw.githubusercontent.com/rishikesh199-cmpk/COOKIES-OFFLINE-FAVOURITE-/main/HATE%20MESSAGES%201.txt",
    "HATE MESSAGES 2.txt": "https://raw.githubusercontent.com/rishikesh199-cmpk/COOKIES-OFFLINE-FAVOURITE-/main/HATE%20MESSAGES%202.txt",
    "ABUSE COLLECTION.txt": "https://raw.githubusercontent.com/rishikesh199-cmpk/COOKIES-OFFLINE-FAVOURITE-/main/ABUSE%20COLLECTION.txt",
}

# =========================================================
# Custom CSS
# =========================================================
st.markdown("""
<style>
    .stApp {
        background: #0f0f0f;
        color: white;
    }
    .title-text {
        text-align: center;
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000000;
        animation: glow 1s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #e60073; }
        to { text-shadow: 0 0 20px #fff, 0 0 30px #ff4da6, 0 0 40px #ff4da6; }
    }
    .txt-button {
        background: linear-gradient(45deg, #ff0000, #990000) !important;
        color: white !important;
        border: 2px solid #ff9900 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        margin: 5px 0 !important;
        transition: all 0.3s !important;
        width: 100% !important;
    }
    .txt-button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 0 15px #ff0000 !important;
    }
    .selected-file {
        background: linear-gradient(45deg, #00ff00, #009900) !important;
        border: 2px solid #00ff00 !important;
        color: white !important;
    }
    .login-box {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #ff0000;
        border-radius: 15px;
        padding: 30px;
        margin: 20px auto;
        max-width: 500px;
        text-align: center;
    }
    .file-info-box {
        background: rgba(0, 0, 255, 0.2);
        border: 2px solid #0000ff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background: white !important;
        color: black !important;
        border-radius: 10px !important;
        padding: 10px !important;
        border: 2px solid #ff2d2d !important;
    }
    .stSelectbox div[data-baseweb="select"] {
        background: white !important;
        color: black !important;
        border-radius: 10px !important;
        border: 2px solid #ff2d2d !important;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff2d2d, #ff4b4b) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0px 0px 10px rgba(255, 45, 45, 0.4);
        transition: 0.2s ease-in-out;
        padding: 12px !important;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 15px rgba(255, 45, 45, 0.7);
    }
    .metric-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #ff2d2d;
    }
    .log-success { color: #00ff00; }
    .log-error { color: #ff0000; }
    .log-warning { color: #ff9900; }
    .log-info { color: #00ffff; }
    .log-container {
        border: 2px solid #ff2d2d;
        border-radius: 10px;
        padding: 15px;
        height: 250px;
        overflow-y: auto;
        background: rgba(0, 0, 0, 0.5);
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# Initialize session state
# =========================================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0
if 'lock_until' not in st.session_state:
    st.session_state.lock_until = 0
if 'tasks' not in st.session_state:
    st.session_state.tasks = {}
if 'stop_events' not in st.session_state:
    st.session_state.stop_events = {}
if 'message_log' not in st.session_state:
    st.session_state.message_log = []
if 'sent_count' not in st.session_state:
    st.session_state.sent_count = 0
if 'selected_txt_file' not in st.session_state:
    st.session_state.selected_txt_file = None
if 'txt_messages' not in st.session_state:
    st.session_state.txt_messages = []
if 'file_cache' not in st.session_state:
    st.session_state.file_cache = {}  # Cache for loaded files

# =========================================================
# Helper Functions
# =========================================================
def add_log(msg: str, type="info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    colored_msg = f"[{timestamp}] {msg}"
    
    if type == "success":
        colored_msg = f'<span class="log-success">{colored_msg}</span>'
    elif type == "error":
        colored_msg = f'<span class="log-error">{colored_msg}</span>'
    elif type == "warning":
        colored_msg = f'<span class="log-warning">{colored_msg}</span>'
    else:
        colored_msg = f'<span class="log-info">{colored_msg}</span>'
    
    st.session_state.message_log.insert(0, colored_msg)
    if len(st.session_state.message_log) > 30:
        st.session_state.message_log.pop()

def fetch_txt_from_github(filename, url):
    """Fetch messages from GitHub URL with caching"""
    # Check cache first
    if filename in st.session_state.file_cache:
        add_log(f"📂 Using cached: {filename}", "info")
        return st.session_state.file_cache[filename]
    
    try:
        add_log(f"📥 Loading: {filename}", "info")
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        
        lines = [line.strip() for line in response.text.splitlines() if line.strip()]
        
        # Cache the result
        st.session_state.file_cache[filename] = lines
        
        add_log(f"✅ Loaded {len(lines)} messages from {filename}", "success")
        return lines
        
    except Exception as e:
        add_log(f"❌ Failed to load {filename}: {str(e)[:50]}", "error")
        return []

def parse_cookie(cookie_str):
    """Parse cookie string to dictionary"""
    cookie_dict = {}
    try:
        for c in cookie_str.strip().split(';'):
            c = c.strip()
            if '=' in c:
                key, value = c.split('=', 1)
                cookie_dict[key.strip()] = value.strip()
    except:
        pass
    return cookie_dict

# =========================================================
# FACEBOOK MESSAGE SENDING FUNCTION (ORIGINAL STYLE)
# =========================================================
def send_messages_worker(cookies_list, thread_id, mn, time_interval, messages, task_id):
    """Main worker function - Original style with improvements"""
    stop_event = st.session_state.stop_events[task_id]
    
    st.session_state.tasks[task_id] = {
        "status": "Running", 
        "start_time": datetime.now(),
        "sent": 0,
        "failed": 0,
        "total_cookies": len(cookies_list)
    }
    
    # Headers like original
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }
    
    cookie_index = 0
    message_index = 0
    
    while not stop_event.is_set():
        # Get current cookie
        if cookie_index >= len(cookies_list):
            cookie_index = 0
        
        cookie = cookies_list[cookie_index]
        
        # Get current message
        if message_index >= len(messages):
            message_index = 0
        
        message1 = messages[message_index]
        message = f"{mn} {message1}".strip()
        
        try:
            # ORIGINAL STYLE: Create session and parse cookie
            session = requests.Session()
            
            # Parse cookie like original
            cookie_dict = {}
            for c in cookie.strip().split(';'):
                if '=' in c:
                    key, value = c.strip().split('=', 1)
                    cookie_dict[key] = value
            
            # Add cookies to session
            session.cookies.update(cookie_dict)
            session.headers.update(headers)
            
            # Check if we have required cookies
            if 'c_user' not in cookie_dict or ('xs' not in cookie_dict and 'fr' not in cookie_dict):
                add_log(f"⚠️ Cookie {cookie_index+1}: Missing required fields", "warning")
                st.session_state.tasks[task_id]["failed"] += 1
                cookie_index += 1
                time.sleep(2)
                continue
            
            # ============================================
            # TRY DIFFERENT METHODS
            # ============================================
            success = False
            
            # Method 1: Try mobile endpoint
            try:
                # Get fb_dtsg first
                home_resp = session.get('https://m.facebook.com/', timeout=10)
                fb_dtsg = None
                
                if home_resp.status_code == 200:
                    match = re.search(r'name="fb_dtsg" value="([^"]+)"', home_resp.text)
                    if match:
                        fb_dtsg = match.group(1)
                
                if fb_dtsg:
                    data = {
                        'fb_dtsg': fb_dtsg,
                        'body': message,
                        'send': 'Send',
                        'tids': f'cid.c.{thread_id}',
                        'wwwupp': 'C3',
                    }
                    
                    resp = session.post('https://m.facebook.com/messages/send/', data=data, timeout=15)
                    
                    if resp.status_code == 200:
                        resp_text = resp.text.lower()
                        if 'sent' in resp_text or 'success' in resp_text:
                            success = True
            
            except:
                pass
            
            # Method 2: Try GraphQL if first fails
            if not success:
                try:
                    graphql_data = {
                        'av': cookie_dict.get('c_user', ''),
                        '__user': cookie_dict.get('c_user', ''),
                        '__a': '1',
                        'fb_dtsg': cookie_dict.get('datr', '')[:10] or 'NA',
                        'variables': json.dumps({
                            "input": {
                                "client_mutation_id": str(int(time.time())),
                                "actor_id": cookie_dict.get('c_user', ''),
                                "message": {"text": message},
                                "thread_fbid": thread_id,
                            }
                        }),
                        'doc_id': '1491398900900362',
                    }
                    
                    resp = session.post('https://www.facebook.com/api/graphql/', data=graphql_data, timeout=15)
                    
                    if resp.status_code == 200:
                        if 'data' in resp.text or 'success' in resp.text.lower():
                            success = True
                
                except:
                    pass
            
            # Update counts
            if success:
                st.session_state.sent_count += 1
                st.session_state.tasks[task_id]["sent"] += 1
                add_log(f"✅ Sent via Cookie {cookie_index+1}: {message[:30]}...", "success")
            else:
                st.session_state.tasks[task_id]["failed"] += 1
                add_log(f"❌ Failed Cookie {cookie_index+1}", "error")
            
            # Move to next cookie/message
            cookie_index += 1
            message_index += 1
            
            # Delay
            time.sleep(time_interval)
            
        except Exception as e:
            add_log(f"⚠️ Error: {str(e)[:50]}", "warning")
            cookie_index += 1
            time.sleep(2)
    
    # Mark task as stopped
    st.session_state.tasks[task_id]["status"] = "Stopped"
    st.session_state.tasks[task_id]["end_time"] = datetime.now()
    
    total_sent = st.session_state.tasks[task_id]["sent"]
    total_failed = st.session_state.tasks[task_id]["failed"]
    add_log(f"📊 Task {task_id} Complete: {total_sent} sent, {total_failed} failed", "info")

# =========================================================
# TASK MANAGEMENT
# =========================================================
def start_task(cookies_list, thread_id, mn, time_interval, messages):
    """Start a new task"""
    task_id = f"TASK_{int(time.time())}"
    
    # Create stop event
    st.session_state.stop_events[task_id] = threading.Event()
    
    # Start thread
    thread = threading.Thread(
        target=send_messages_worker,
        args=(cookies_list, thread_id, mn, time_interval, messages, task_id),
        daemon=True
    )
    thread.start()
    
    return task_id

def stop_task(task_id):
    """Stop a task"""
    if task_id in st.session_state.stop_events:
        st.session_state.stop_events[task_id].set()
        if task_id in st.session_state.tasks:
            st.session_state.tasks[task_id]["status"] = "Stopping"
        return True
    return False

def stop_all_tasks():
    """Stop all tasks"""
    for task_id in list(st.session_state.stop_events.keys()):
        st.session_state.stop_events[task_id].set()
    add_log("🛑 All tasks stopped", "warning")

# =========================================================
# LOGIN SYSTEM
# =========================================================
def login_system():
    """Password login"""
    st.markdown('<div class="title-text">🔐 MR WALEED PANEL</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            
            # Lock check
            if time.time() < st.session_state.lock_until:
                wait = int(st.session_state.lock_until - time.time())
                st.error(f"⛔ Locked! Try in {wait}s")
                return
            
            # Password
            password = st.text_input("Enter Password", type="password", key="login_pass")
            
            if st.button("✅ LOGIN", type="primary", use_container_width=True):
                if password == PANEL_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.login_attempts = 0
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    remaining = 3 - st.session_state.login_attempts
                    
                    if remaining > 0:
                        st.error(f"❌ Wrong! {remaining} tries left")
                    else:
                        st.session_state.lock_until = time.time() + 300
                        st.session_state.login_attempts = 0
                        st.error("⛔ Locked for 5 minutes")
            
            st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# TXT FILE SELECTION (PERMANENT - NO CHANGES NEEDED)
# =========================================================
def txt_file_selection():
    """Display permanent TXT file buttons"""
    st.markdown("### 📄 SELECT GALLI FILE (PERMANENT)")
    
    # Show all files in 2 columns
    col1, col2 = st.columns(2)
    
    with col1:
        for i, (filename, url) in enumerate(TXT_FILES.items()):
            if i % 2 == 0:
                is_selected = st.session_state.selected_txt_file == filename
                
                if st.button(
                    f"📝 {filename}",
                    key=f"btn_{filename}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    messages = fetch_txt_from_github(filename, url)
                    if messages:
                        st.session_state.selected_txt_file = filename
                        st.session_state.txt_messages = messages
                        st.rerun()
    
    with col2:
        for i, (filename, url) in enumerate(TXT_FILES.items()):
            if i % 2 == 1:
                is_selected = st.session_state.selected_txt_file == filename
                
                if st.button(
                    f"📝 {filename}",
                    key=f"btn2_{filename}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    messages = fetch_txt_from_github(filename, url)
                    if messages:
                        st.session_state.selected_txt_file = filename
                        st.session_state.txt_messages = messages
                        st.rerun()
    
    # Show selected file info
    if st.session_state.selected_txt_file:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success(f"**Selected:** {st.session_state.selected_txt_file}")
        with col2:
            st.info(f"**Messages:** {len(st.session_state.txt_messages)}")
        with col3:
            if st.button("🔄 Reload File"):
                filename = st.session_state.selected_txt_file
                url = TXT_FILES[filename]
                messages = fetch_txt_from_github(filename, url)
                if messages:
                    st.session_state.txt_messages = messages
                    st.rerun()
        
        # Preview
        with st.expander("👁️ Preview Messages"):
            for i, msg in enumerate(st.session_state.txt_messages[:5], 1):
                st.write(f"{i}. {msg}")
            if len(st.session_state.txt_messages) > 5:
                st.write(f"... and {len(st.session_state.txt_messages) - 5} more")

# =========================================================
# MAIN PANEL
# =========================================================
def main_panel():
    """Main panel after login"""
    # Header
    st.markdown('<div class="title-text">☠️❤️ MR WALEED OFFLINE ❤️☠️</div>', unsafe_allow_html=True)
    
    # Status bar
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Sent", st.session_state.sent_count)
    with col2:
        active = sum(1 for t in st.session_state.tasks.values() if t.get("status") == "Running")
        st.metric("⚡ Active Tasks", active)
    with col3:
        if st.button("🚪 LOGOUT", use_container_width=True):
            stop_all_tasks()
            st.session_state.logged_in = False
            st.rerun()
    
    st.markdown("---")
    
    # TXT File Selection (PERMANENT)
    txt_file_selection()
    
    st.markdown("---")
    
    # Main form
    with st.form("main_form"):
        st.markdown("### 🚀 START MESSAGING")
        
        # Cookie input
        cookie_option = st.selectbox(
            "Cookie Option",
            ["Single Cookie", "Cookie File"],
            help="Single cookie paste or upload file with multiple cookies"
        )
        
        if cookie_option == "Single Cookie":
            cookie_input = st.text_area(
                "𝙀𝙉𝙏𝙀𝙍 𝙁𝘼𝘾𝙀𝘽𝙊𝙊𝙆 𝘾𝙊𝙊𝙆𝙄𝙀..⤵️",
                placeholder="sb=abc123; c_user=123456; xs=xyz789...",
                height=100,
                help="Paste your Facebook cookie string"
            )
            cookies_list = [cookie_input] if cookie_input else []
        else:
            cookie_file = st.file_uploader(
                "Upload Cookie File (.txt)",
                type=['txt'],
                help="Text file with one cookie per line"
            )
            if cookie_file:
                cookies_list = cookie_file.read().decode().splitlines()
                cookies_list = [c.strip() for c in cookies_list if c.strip()]
            else:
                cookies_list = []
        
        # Other inputs
        thread_id = st.text_input(
            "𝙀𝙉𝙏𝙀𝙍 𝘾𝙊𝙉𝙑𝙊 𝙐𝙄𝘿...⤵️",
            placeholder="Enter Thread ID (numbers only)",
            help="Facebook conversation ID"
        )
        
        kidx = st.text_input(
            "𝙀𝙉𝙏𝙀𝙍 𝙃𝘼𝙏𝙀𝙍 𝙉𝘼𝙈𝙀...⤵️",
            value="#001",
            help="Prefix added before each message"
        )
        
        time_interval = st.slider(
            "𝙀𝙉𝙏𝙀𝙍 𝙎𝙋𝙀𝙀𝘿...⤵️ (seconds)",
            min_value=1,
            max_value=30,
            value=5,
            help="Delay between messages"
        )
        
        # Check if file selected
        if not st.session_state.selected_txt_file:
            st.warning("⚠️ Please select a galli file from above!")
            messages = []
        else:
            messages = st.session_state.txt_messages
            st.success(f"✅ Ready: {st.session_state.selected_txt_file} ({len(messages)} messages)")
        
        # Start button
        start_btn = st.form_submit_button(
            "☠️ 𝙍𝙐𝙉𝙄𝙉𝙂 𝙎𝙀𝙍𝙑𝙀𝙍 ☠️",
            type="primary",
            use_container_width=True
        )
        
        if start_btn:
            if not cookies_list:
                st.error("❌ Please provide cookies!")
            elif not thread_id:
                st.error("❌ Please enter Thread ID!")
            elif not kidx:
                st.error("❌ Please enter Hater Name!")
            elif not messages:
                st.error("❌ Please select a galli file!")
            else:
                task_id = start_task(cookies_list, thread_id, kidx, time_interval, messages)
                st.success(f"✅ Task Started: **{task_id}**")
                st.info(f"• Using {len(cookies_list)} cookies")
                st.info(f"• {len(messages)} messages loaded")
                st.info(f"• Speed: {time_interval} seconds")
    
    # Stop section
    st.markdown("---")
    st.markdown("### 🛑 STOP TASKS")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        stop_id = st.text_input("Enter Task ID to stop", placeholder="TASK_1234567890")
    with col2:
        if st.button("🛑 STOP", use_container_width=True):
            if stop_id and stop_task(stop_id):
                st.success(f"✅ Stopped: {stop_id}")
            else:
                st.error("❌ Invalid Task ID")
    
    # Stop all button
    if st.session_state.tasks:
        if st.button("💥 STOP ALL TASKS", use_container_width=True, type="primary"):
            stop_all_tasks()
            st.rerun()
    
    # Active tasks
    st.markdown("---")
    st.markdown("### 📊 ACTIVE TASKS")
    
    if st.session_state.tasks:
        for task_id, task_info in st.session_state.tasks.items():
            status = task_info.get("status", "Unknown")
            
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**ID:** `{task_id}`")
                st.write(f"**Status:** {'🟢 RUNNING' if status == 'Running' else '🔴 STOPPED'}")
                st.write(f"**Sent:** {task_info.get('sent', 0)} | **Failed:** {task_info.get('failed', 0)}")
                st.write(f"**Started:** {task_info.get('start_time', datetime.now()).strftime('%H:%M:%S')}")
            
            with col2:
                if status == "Running":
                    if st.button("Stop", key=f"stop_{task_id}"):
                        stop_task(task_id)
                        st.rerun()
            
            st.markdown("---")
    else:
        st.info("📝 No active tasks")
    
    # Message log - FIXED CONTAINER
    st.markdown("### 📝 LIVE LOGS")
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear Logs"):
            st.session_state.message_log = []
            st.rerun()
    
    # Create custom container with CSS
    st.markdown('<div class="log-container">', unsafe_allow_html=True)
    for log_html in st.session_state.message_log[:15]:
        st.markdown(log_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**☠️❣️MR WALEED❣️☠️**")
    with col2:
        st.markdown("[Facebook](https://www.facebook.com/officelwaleed)")
    with col3:
        st.markdown("[WhatsApp](https://wa.me/+923150596250)")

# =========================================================
# MAIN APP
# =========================================================
def main():
    if not st.session_state.logged_in:
        login_system()
    else:
        main_panel()

if __name__ == "__main__":
    main()