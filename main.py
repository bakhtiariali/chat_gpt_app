# -*- coding: utf-8 -*-
import streamlit as st
import requests
import json
import time
from datetime import datetime

# --- تنظیمات صفحه ---
st.set_page_config(
    page_title="دستیار هوشمند خیاطی",
    page_icon="✂️",  # تغییر آیکون به قیچی
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Vazirmatn', sans-serif !important;
    }
    
    /* تم اصلی مشکی و طلایی */
    :root {
        --primary-color: #d4af37;
        --secondary-color: #e0e0e0;
        --background-dark: #121212;
        --background-light: #1c1c1c;
        --card-bg: rgba(30, 30, 30, 0.8);
        --gold-gradient: linear-gradient(135deg, #f0c75a 0%, #d4af37 100%);
        # --message-user: linear-gradient(135deg, #f0c75a 0%, #c89b3f 100%);
        --message-user: linear-gradient(135deg, #2a2a2a 0%, #333333 100%);

        /* --- ❇️ تغییر اصلی اینجا اعمال شد ❇️ --- */
        /* رنگ پس‌زمینه ربات را کمی روشن‌تر کردم تا از پس‌زمینه اصلی متمایز شود */
        --message-bot-bg: var(--background-dark);
    }
    
    /* --- همه استایل‌‌های اصلی همان نسخه‌ی تو هستند --- */

    .stApp {
        background: linear-gradient(135deg, var(--background-light) 0%, var(--background-dark) 100%);
        background-attachment: fixed;
    }

    /* ... (تمام استایل‌های قبلی شما برای هدر، لاگین، سایدبار و غیره اینجا قرار می‌گیرند) ... */
    
    .main-header {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid rgba(212, 175, 55, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    .main-header h1 {
        color: var(--primary-color);
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        color: var(--secondary-color);
        font-size: 1.2rem;
        margin: 0;
    }
    
    .login-container {
        max-width: 450px;
        margin: 4rem auto;
        padding: 3rem;
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(212, 175, 55, 0.3);
        direction: rtl;
        text-align: right;
    }

    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .login-header h1 {
        color: var(--primary-color);
        font-size: 2rem;
        font-weight: 700;
    }

    .login-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        color: var(--primary-color);
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
    }

    /* ✅ تغییرات فقط در این بخش */

    /* راست‌چین و انتقال آیکون‌ها به سمت راست */
    .stTextInput {
        direction: rtl !important;
        text-align: right !important;
    }

    .stTextInput label {
        display: flex;
        flex-direction: row-reverse; /* آیکون سمت راست */
        justify-content: flex-end;
        align-items: center;
        gap: 6px;
        color: var(--secondary-color);
        font-weight: 600;
    }

    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #444;
        background-color: #2a2a2a;
        color: var(--secondary-color);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        text-align: right;
    }

    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
    }

    /* ✅ راست‌چین کردن دکمه (Login) */
    .stButton {
        direction: rtl !important;
        text-align: right !important;
    }

    .stButton > button {
        background: var(--gold-gradient);
        color: #1a1a1a;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(212, 175, 55, 0.5);
        filter: brightness(1.1);
    }
    /* سایدبار */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: var(--card-bg) !important;
        backdrop-filter: blur(10px) !important;
        border-right: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    .sidebar-content { padding: 1rem; }
    
    .stat-card {
        background: var(--gold-gradient);
        color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2);
    }
    
    .stat-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    
    .stat-card p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-weight: 600;
    }
    
    /* انیمیشن‌ها */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeIn 0.5s ease-out; }
    
    /* پیام خطا */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid #ef4444;
        background-color: rgba(239, 68, 68, 0.1);
        color: white;
    }
    
    /* لودینگ */
    .stSpinner > div { border-color: var(--primary-color) !important; }
    
    /* اسکرول‌بار */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.2); }
    ::-webkit-scrollbar-thumb { background: rgba(212, 175, 55, 0.5); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(212, 175, 55, 0.8); }

    /* --- ❇️ شروع بخش استایل‌دهی به چت‌بات ❇️ --- */

    /* (۱) محفظه اصلی هر پیام (شامل آیکون و حباب متن) */
    [data-testid="chat-message-container"] {
        direction: rtl; /* این خط آیکون را به سمت راست منتقل می‌کند */
        margin-bottom: 1rem; /* فاصله بین پیام‌ها */
    }

    /* (۲) استایل پایه برای خود حباب پیام */
    .stChatMessage {
        border-radius: 12px; /* گوشه‌های گرد */
        padding: 1rem 1.25rem; /* پدینگ داخلی */
        /* متن داخل حباب هم باید راست‌چین باشد */
        direction: rtl; 
        text-align: right;
    }




    /* (۴) استایل اختصاصی حباب پیام «ربات» (پاسخ) */
    /* از سلکتور has: برای پیدا کردن پیامی که آواتار "assistant" دارد استفاده می‌کنیم */
    [data-testid="chat-message-container"]:has([data-testid="chat-avatar-assistant"]) .stChatMessage {
        background: var(--message-bot-bg); /* پس‌زمینه تیره هماهنگ با تم */
        color: var(--secondary-color); /* رنگ متن روشن (تغییری نکرده و درست است) */
        border: 1px solid rgba(212, 175, 55, 0.2); /* حاشیه طلایی محو */
    }

    /* (۵) تنظیم فاصله آیکون (آواتار) از حباب متن */
    [data-testid="chat-avatar"] {
        margin-left: 0.75rem; /* فاصله آیکون (راست) از حباب (چپ) */
        margin-right: 0;
    }

    /* --- ❇️ پایان بخش استایل‌دهی به چت‌بات ❇️ --- */

    /* تنظیمات RTL */
    .stMarkdown, .stText, .stButton > button, .stTextInput > div > div > input {
        direction: rtl;
        text-align: right;
    }
    .stTextInput > div > div > input { text-align: right; }
    .stChatInputContainer textarea { text-align: right; direction: rtl; }
                

    /* حذف کامل پس‌زمینه و حاشیه باکس چت */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)



# --- کلاس API (بدون تغییر) ---
class MetisAI:
    BASE_URL = "https://api.metisai.ir/api/v1"

    def __init__(self, api_key, bot_id):
        if not api_key or not bot_id:
            raise ValueError("API key and Bot ID cannot be empty.")
        self.api_key = api_key
        self.bot_id = bot_id
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def create_session(self):
        url = f"{self.BASE_URL}/chat/session"
        payload = {"botId": self.bot_id, "user": None, "initialMessages": []}
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json().get('id')
        except requests.exceptions.RequestException as e:
            st.error(f"❌ خطا در ایجاد جلسه: {e}")
            return None

    def send_message_stream_generator(self, session_id, message_content):
        url = f"{self.BASE_URL}/chat/session/{session_id}/message/stream"
        payload = {"message": {"content": message_content, "type": "USER"}}
        try:
            with requests.post(url, headers=self.headers, json=payload, stream=True) as response:
                response.raise_for_status()
                response.encoding = 'utf-8'
                for line in response.iter_lines(decode_unicode=True):
                    if line and line.startswith('data:'):
                        json_str = line[len('data:'):].strip()
                        if not json_str:
                            continue
                        try:
                            chunk = json.loads(json_str)
                            content_piece = chunk.get("message", {}).get("content", "")
                            if content_piece:
                                yield content_piece
                        except json.JSONDecodeError:
                            pass
        except requests.exceptions.RequestException as e:
            st.error(f"❌ خطا در دریافت پاسخ: {e}")

# --- سیستم ورود ---
def login_page():
    load_css()
    
    st.markdown("""
    <div class="login-container fade-in">
        <div class="login-header">
            <div class="login-icon">✂️</div>
            <h1>دستیار هوشمند خیاطی</h1>
            <p style="color: #a0a0a0; margin-top: 0.5rem;">برای شروع، وارد حساب کاربری خود شوید</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("👤 نام کاربری", key="username_input", placeholder="نام کاربری خود را وارد کنید")
        password = st.text_input("🔒 رمز عبور", type="password", key="password_input", placeholder="رمز عبور خود را وارد کنید")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("⚜️ ورود به آتلیه هوشمند"):
            VALID_CREDENTIALS = {"admin": "1234"} # اطلاعات ورود را اینجا تغییر دهید
            
            if username in VALID_CREDENTIALS and password == VALID_CREDENTIALS[username]:
                st.session_state.logged_in = True
                st.session_state.login_time = datetime.now()
                st.success("✅ ورود موفقیت‌آمیز! خوش آمدید.")
                time.sleep(0.7)
                st.rerun()
            else:
                st.error("❌ نام کاربری یا رمز عبور اشتباه است")

# --- صفحه اصلی ---
def main_app():
    load_css()
    
    # هدر
    st.markdown("""
    <div class="main-header fade-in">
        <h1>✂️ دستیار هوشمند خیاطی ✂️</h1>
        <p>الگوهای ذهنی خود را با هوش مصنوعی به واقعیت تبدیل کنید</p>
    </div>
    """, unsafe_allow_html=True)

    # کلیدهای API
    api_key = "tpsg-usFMzwCIzwxQT8tvUCQNoNXSCRdlg0a"
    bot_id = "41326835-46dd-408a-acc9-465dadd76223"

    if not api_key or not bot_id:
        st.error("❌ کلید API یا شناسه ربات تنظیم نشده است")
        st.stop()

    # سایدبار
    with st.sidebar:
        st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        
        # آمار
        if "messages" in st.session_state:
            msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.markdown(f"""
            <div class="stat-card">
                <h3>{msg_count}</h3>
                <p>🪡 تعداد سوالات پرسیده شده</p>
            </div>
            """, unsafe_allow_html=True)
        
        if "login_time" in st.session_state:
            duration = datetime.now() - st.session_state.login_time
            minutes = int(duration.total_seconds() / 60)
            st.markdown(f"""
            <div class="stat-card">
                <h3>{minutes}</h3>
                <p>⏱️ دقیقه در جلسه</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # دکمه‌ها
        if st.button("✨ شروع گفتگوی جدید", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = None
            st.success("✅ میز کار شما برای یک پروژه جدید آماده است!")
            time.sleep(0.7)
            st.rerun()
        
        if st.button("🚪 خروج از حساب", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # فوتر
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #888; font-size: 0.9rem;'>
            <p>💡 Powered by MetisAI</p>
            <p>🎨 Design by Gemini</p>
        </div>
        """, unsafe_allow_html=True)

    # مدیریت پیام‌ها
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    # نمایش پیام‌ها
    for message in st.session_state.messages:
        avatar_icon = "🪡" if message["role"] == "user" else "🧵"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

    # ورودی کاربر
    if prompt := st.chat_input("💭 سوال خیاطی خود را بپرسید..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🪡"):
            st.markdown(f"<p style='color:#fff; font-weight:500;'>{prompt}</p>", unsafe_allow_html=True)
        with st.chat_message("assistant", avatar="🧵"):
            try:
                client = MetisAI(api_key, bot_id)

                if not st.session_state.session_id:
                    with st.spinner("🧵 در حال آماده‌سازی چرخ خیاطی هوشمند..."):
                        st.session_state.session_id = client.create_session()

                response_generator = client.send_message_stream_generator(
                    st.session_state.session_id,
                    prompt
                )

                # ✅ نمایش استریم به‌صورت روان و درست
                full_response = ""
                response_placeholder = st.empty()

                for chunk in response_generator:
                    full_response += chunk
                    response_placeholder.markdown(f"""
                    <div style="direction: rtl; text-align: right; font-family: 'Vazirmatn', sans-serif;
                                line-height: 1.9; font-size: 1.05rem; color: #f8d26b;">
                        {full_response}
                    </div>
                    """, unsafe_allow_html=True)

                # ذخیره پاسخ کامل در state
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"❌ خطایی در ارتباط با دستیار رخ داد: {e}")

# --- اجرا ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
else:
    main_app()
