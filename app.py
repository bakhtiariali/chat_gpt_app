
#
#  بنفش
# # -*- coding: utf-8 -*-
# import streamlit as st
# import requests
# import json
# import os
# import base64 # To encode the background image

# # --- کلاس ارتباط با API (بدون تغییر در منطق اصلی) ---
# class MetisAI:
#     """
#     A Python client for the MetisAI Chat API, adapted for Streamlit.
#     This class handles creating sessions and generating streamed responses.
#     """
#     BASE_URL = "https://api.metisai.ir/api/v1"

#     def __init__(self, api_key, bot_id):
#         if not api_key or not bot_id:
#             raise ValueError("API key and Bot ID cannot be empty.")
#         self.api_key = api_key
#         self.bot_id = bot_id
#         self.headers = {
#             'Authorization': f'Bearer {self.api_key}',
#             'Content-Type': 'application/json'
#         }

#     def create_session(self):
#         url = f"{self.BASE_URL}/chat/session"
#         payload = {"botId": self.bot_id, "user": None, "initialMessages": []}
#         try:
#             response = requests.post(url, headers=self.headers, json=payload)
#             response.raise_for_status()
#             return response.json().get('id')
#         except requests.exceptions.RequestException as e:
#             st.error(f"خطا در ایجاد جلسه: {e}")
#             return None

#     def send_message_stream_generator(self, session_id, message_content):
#         url = f"{self.BASE_URL}/chat/session/{session_id}/message/stream"
#         payload = {"message": {"content": message_content, "type": "USER"}}
#         try:
#             with requests.post(url, headers=self.headers, json=payload, stream=True) as response:
#                 response.raise_for_status()
#                 response.encoding = 'utf-8'
#                 for line in response.iter_lines(decode_unicode=True):
#                     if line and line.startswith('data:'):
#                         json_str = line[len('data:'):].strip()
#                         if not json_str:
#                             continue
#                         try:
#                             chunk = json.loads(json_str)
#                             content_piece = chunk.get("message", {}).get("content", "")
#                             if content_piece:
#                                 yield content_piece
#                         except json.JSONDecodeError:
#                             pass
#         except requests.exceptions.RequestException as e:
#             st.error(f"خطا در هنگام دریافت پاسخ: {e}")

# # --- سیستم ورود ---
# def check_login():
#     """Returns `True` if the user is logged in, `False` otherwise."""
#     if "logged_in" not in st.session_state or not st.session_state.logged_in:
#         st.set_page_config(page_title="ورود", layout="centered")
#         st.title("ورود به دستیار هوشمند")
        
#         # اطلاعات ورود نمونه - در یک برنامه واقعی از روش امن‌تری استفاده کنید
#         VALID_CREDENTIALS = {"admin": "1234"}

#         username = st.text_input("نام کاربری", key="username_input")
#         password = st.text_input("رمز عبور", type="password", key="password_input")

#         if st.button("ورود"):
#             if username in VALID_CREDENTIALS and password == VALID_CREDENTIALS[username]:
#                 st.session_state.logged_in = True
#                 st.rerun()
#             else:
#                 st.error("نام کاربری یا رمز عبور اشتباه است.")
#         return False
#     return True

# # --- تابع برای تنظیم پس‌زمینه ---
# def set_bg_hack(image_url):
#     '''
#     A function to set a background image from a URL.
#     '''
#     st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url("{image_url}");
#              background-size: cover;
#              background-position: center;
#              background-repeat: no-repeat;
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#      )

# # --- رابط کاربری اصلی برنامه ---
# def main_app():
#     st.set_page_config(page_title="دستیار هوشمند آکادمی خسروی", page_icon="�")
    
#     # آدرس لوگوی خود را در اینجا قرار دهید
#     logo_url = "https://khosraviacademy.ir/"
#     set_bg_hack(logo_url)

#     st.title("🤖 دستیار هوشمند آکادمی خسروی")
#     st.caption("powered by MetisAI & Streamlit")

#     # دریافت کلیدها از متغیرهای محیطی
#     # این روش امن‌تر است و اطلاعات حساس را در کد قرار نمی‌دهد
#     api_key = "tpsg-usFMzwCIzwxQT8tvUCQNoNXSCRdlg0a"
#     bot_id = "41326835-46dd-408a-acc9-465dadd76223"  

#     if not api_key or not bot_id:
#         st.error("کلید API یا شناسه ربات تنظیم نشده است. لطفا با پشتیبانی تماس بگیرید.")
#         st.stop()

#     with st.sidebar:
#         st.header("تنظیمات گفتگو")
#         if st.button("شروع گفتگوی جدید"):
#             st.session_state.messages = []
#             st.session_state.session_id = None
#             st.rerun()

#     if "messages" not in st.session_state:
#         st.session_state.messages = []
#     if "session_id" not in st.session_state:
#         st.session_state.session_id = None

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     if prompt := st.chat_input("سوال خود را اینجا بنویسید..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         with st.chat_message("assistant"):
#             try:
#                 client = MetisAI(api_key, bot_id)
#                 if not st.session_state.session_id:
#                     with st.spinner("در حال ایجاد جلسه جدید..."):
#                         st.session_state.session_id = client.create_session()
#                     if not st.session_state.session_id:
#                         st.error("ایجاد جلسه با مشکل مواجه شد. لطفا دوباره تلاش کنید.")
#                         st.stop()
                
#                 response_generator = client.send_message_stream_generator(st.session_state.session_id, prompt)
#                 full_response = st.write_stream(response_generator)
#                 st.session_state.messages.append({"role": "assistant", "content": full_response})
#             except Exception as e:
#                 st.error(f"خطایی رخ داد: {e}")

# # --- اجرای برنامه ---
# if check_login():
#     main_app()


# بنفش
# -*- coding: utf-8 -*-
# import streamlit as st
# import requests
# import json
# import time
# from datetime import datetime

# # --- تنظیمات صفحه ---
# st.set_page_config(
#     page_title="دستیار هوشمند آکادمی خسروی",
#     page_icon="🎓",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- استایل‌های CSS سفارشی ---
# def load_css():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700&display=swap');
    
#     * {
#         font-family: 'Vazirmatn', sans-serif !important;
#     }
    
#     /* تم اصلی */
#     :root {
#         --primary-color: #6366f1;
#         --secondary-color: #8b5cf6;
#         --accent-color: #ec4899;
#         --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         --chat-bg: rgba(255, 255, 255, 0.95);
#         --message-user: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         --message-bot: #f3f4f6;
#     }
    
#     /* پس‌زمینه اصلی */
#     .stApp {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         background-attachment: fixed;
#     }
    
#     /* هدر سفارشی */
#     .main-header {
#         background: rgba(255, 255, 255, 0.1);
#         backdrop-filter: blur(10px);
#         border-radius: 20px;
#         padding: 2rem;
#         margin-bottom: 2rem;
#         text-align: center;
#         border: 1px solid rgba(255, 255, 255, 0.2);
#         box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
#     }
    
#     .main-header h1 {
#         color: white;
#         font-size: 2.5rem;
#         font-weight: 700;
#         margin-bottom: 0.5rem;
#         text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
#     }
    
#     .main-header p {
#         color: rgba(255, 255, 255, 0.9);
#         font-size: 1.1rem;
#         margin: 0;
#     }
    
#     /* کارت ورود */
#     .login-container {
#         max-width: 450px;
#         margin: 5rem auto;
#         padding: 3rem;
#         background: rgba(255, 255, 255, 0.95);
#         backdrop-filter: blur(10px);
#         border-radius: 25px;
#         box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
#         border: 1px solid rgba(255, 255, 255, 0.3);
#     }
    
#     .login-header {
#         text-align: center;
#         margin-bottom: 2rem;
#     }
    
#     .login-header h1 {
#         color: #667eea;
#         font-size: 2rem;
#         font-weight: 700;
#         margin-bottom: 0.5rem;
#     }
    
#     .login-icon {
#         font-size: 4rem;
#         margin-bottom: 1rem;
#     }
    
#     /* فیلدهای ورودی */
#     .stTextInput > div > div > input {
#         border-radius: 12px;
#         border: 2px solid #e5e7eb;
#         padding: 0.75rem 1rem;
#         font-size: 1rem;
#         transition: all 0.3s ease;
#     }
    
#     .stTextInput > div > div > input:focus {
#         border-color: #667eea;
#         box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
#     }
    
#     /* دکمه‌ها */
#     .stButton > button {
#         width: 100%;
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border: none;
#         border-radius: 12px;
#         padding: 0.75rem 2rem;
#         font-size: 1.1rem;
#         font-weight: 600;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
#     }
    
#     /* پیام‌های چت */
#     .stChatMessage {
#         background: rgba(255, 255, 255, 0.95) !important;
#         border-radius: 15px !important;
#         padding: 1.5rem !important;
#         margin-bottom: 1rem !important;
#         box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
#         border: 1px solid rgba(255, 255, 255, 0.3) !important;
#     }
    
#     .stChatMessage[data-testid="user-message"] {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
#         color: white !important;
#     }
    
#     .stChatMessage[data-testid="user-message"] p {
#         color: white !important;
#     }
    
#     /* ورودی چت */
#     .stChatInputContainer {
#         background: rgba(255, 255, 255, 0.95) !important;
#         backdrop-filter: blur(10px) !important;
#         border-radius: 20px !important;
#         padding: 1rem !important;
#         box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
#         border: 1px solid rgba(255, 255, 255, 0.3) !important;
#     }
    
#     /* سایدبار */
#     .css-1d391kg, [data-testid="stSidebar"] {
#         background: rgba(255, 255, 255, 0.95) !important;
#         backdrop-filter: blur(10px) !important;
#     }
    
#     .sidebar-content {
#         padding: 1rem;
#     }
    
#     .stat-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         padding: 1.5rem;
#         border-radius: 15px;
#         margin-bottom: 1rem;
#         box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
#     }
    
#     .stat-card h3 {
#         margin: 0;
#         font-size: 2rem;
#         font-weight: 700;
#     }
    
#     .stat-card p {
#         margin: 0.5rem 0 0 0;
#         opacity: 0.9;
#     }
    
#     /* انیمیشن‌ها */
#     @keyframes fadeIn {
#         from { opacity: 0; transform: translateY(20px); }
#         to { opacity: 1; transform: translateY(0); }
#     }
    
#     .fade-in {
#         animation: fadeIn 0.5s ease-out;
#     }
    
#     /* پیام خطا */
#     .stAlert {
#         border-radius: 12px;
#         border-left: 4px solid #ef4444;
#     }
    
#     /* لودینگ */
#     .stSpinner > div {
#         border-color: #667eea !important;
#     }
    
#     /* اسکرول‌بار */
#     ::-webkit-scrollbar {
#         width: 8px;
#         height: 8px;
#     }
    
#     ::-webkit-scrollbar-track {
#         background: rgba(255, 255, 255, 0.1);
#         border-radius: 10px;
#     }
    
#     ::-webkit-scrollbar-thumb {
#         background: rgba(102, 126, 234, 0.6);
#         border-radius: 10px;
#     }
    
#     ::-webkit-scrollbar-thumb:hover {
#         background: rgba(102, 126, 234, 0.8);
#     }
    
#     /* تنظیمات RTL */
#     .stMarkdown, .stText {
#         direction: rtl;
#         text-align: right;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # --- کلاس API (بدون تغییر) ---
# class MetisAI:
#     BASE_URL = "https://api.metisai.ir/api/v1"

#     def __init__(self, api_key, bot_id):
#         if not api_key or not bot_id:
#             raise ValueError("API key and Bot ID cannot be empty.")
#         self.api_key = api_key
#         self.bot_id = bot_id
#         self.headers = {
#             'Authorization': f'Bearer {self.api_key}',
#             'Content-Type': 'application/json'
#         }

#     def create_session(self):
#         url = f"{self.BASE_URL}/chat/session"
#         payload = {"botId": self.bot_id, "user": None, "initialMessages": []}
#         try:
#             response = requests.post(url, headers=self.headers, json=payload)
#             response.raise_for_status()
#             return response.json().get('id')
#         except requests.exceptions.RequestException as e:
#             st.error(f"❌ خطا در ایجاد جلسه: {e}")
#             return None

#     def send_message_stream_generator(self, session_id, message_content):
#         url = f"{self.BASE_URL}/chat/session/{session_id}/message/stream"
#         payload = {"message": {"content": message_content, "type": "USER"}}
#         try:
#             with requests.post(url, headers=self.headers, json=payload, stream=True) as response:
#                 response.raise_for_status()
#                 response.encoding = 'utf-8'
#                 for line in response.iter_lines(decode_unicode=True):
#                     if line and line.startswith('data:'):
#                         json_str = line[len('data:'):].strip()
#                         if not json_str:
#                             continue
#                         try:
#                             chunk = json.loads(json_str)
#                             content_piece = chunk.get("message", {}).get("content", "")
#                             if content_piece:
#                                 yield content_piece
#                         except json.JSONDecodeError:
#                             pass
#         except requests.exceptions.RequestException as e:
#             st.error(f"❌ خطا در دریافت پاسخ: {e}")

# # --- سیستم ورود ---
# def login_page():
#     load_css()
    
#     st.markdown("""
#     <div class="login-container fade-in">
#         <div class="login-header">
#             <div class="login-icon">🎓</div>
#             <h1>دستیار هوشمند آکادمی خسروی</h1>
#             <p style="color: #6b7280; margin-top: 0.5rem;">لطفا برای ادامه وارد شوید</p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
    
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         st.markdown("<br>", unsafe_allow_html=True)
#         username = st.text_input("👤 نام کاربری", key="username_input", placeholder="نام کاربری خود را وارد کنید")
#         password = st.text_input("🔒 رمز عبور", type="password", key="password_input", placeholder="رمز عبور خود را وارد کنید")
        
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         if st.button("🚀 ورود به سیستم"):
#             VALID_CREDENTIALS = {"admin": "1234"}
            
#             if username in VALID_CREDENTIALS and password == VALID_CREDENTIALS[username]:
#                 st.session_state.logged_in = True
#                 st.session_state.login_time = datetime.now()
#                 st.success("✅ ورود موفقیت‌آمیز!")
#                 time.sleep(0.5)
#                 st.rerun()
#             else:
#                 st.error("❌ نام کاربری یا رمز عبور اشتباه است")

# # --- صفحه اصلی ---
# def main_app():
#     load_css()
    
#     # هدر
#     st.markdown("""
#     <div class="main-header fade-in">
#         <h1>🎓 دستیار هوشمند آکادمی خسروی</h1>
#         <p>پاسخگویی سریع و دقیق به سوالات شما با قدرت هوش مصنوعی</p>
#     </div>
#     """, unsafe_allow_html=True)

#     # کلیدهای API
#     api_key = "tpsg-usFMzwCIzwxQT8tvUCQNoNXSCRdlg0a"
#     bot_id = "41326835-46dd-408a-acc9-465dadd76223"

#     if not api_key or not bot_id:
#         st.error("❌ کلید API یا شناسه ربات تنظیم نشده است")
#         st.stop()

#     # سایدبار
#     with st.sidebar:
#         st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        
#         # آمار
#         if "messages" in st.session_state:
#             msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
#             st.markdown(f"""
#             <div class="stat-card">
#                 <h3>{msg_count}</h3>
#                 <p>💬 تعداد پیام‌های ارسالی</p>
#             </div>
#             """, unsafe_allow_html=True)
        
#         if "login_time" in st.session_state:
#             duration = datetime.now() - st.session_state.login_time
#             minutes = int(duration.total_seconds() / 60)
#             st.markdown(f"""
#             <div class="stat-card">
#                 <h3>{minutes}</h3>
#                 <p>⏱️ دقیقه در جلسه</p>
#             </div>
#             """, unsafe_allow_html=True)
        
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         # دکمه‌ها
#         if st.button("🔄 شروع گفتگوی جدید", use_container_width=True):
#             st.session_state.messages = []
#             st.session_state.session_id = None
#             st.success("✅ گفتگوی جدید آغاز شد")
#             time.sleep(0.5)
#             st.rerun()
        
#         if st.button("🚪 خروج از حساب", use_container_width=True):
#             st.session_state.clear()
#             st.rerun()
        
#         st.markdown("</div>", unsafe_allow_html=True)
        
#         # فوتر
#         st.markdown("---")
#         st.markdown("""
#         <div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>
#             <p>💡 Powered by MetisAI</p>
#             <p>🚀 Built with Streamlit</p>
#         </div>
#         """, unsafe_allow_html=True)

#     # مدیریت پیام‌ها
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
#     if "session_id" not in st.session_state:
#         st.session_state.session_id = None

#     # نمایش پیام‌ها
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
#             st.markdown(message["content"])

#     # ورودی کاربر
#     if prompt := st.chat_input("💭 سوال خود را اینجا بنویسید..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(prompt)

#         with st.chat_message("assistant", avatar="🤖"):
#             try:
#                 client = MetisAI(api_key, bot_id)
                
#                 if not st.session_state.session_id:
#                     with st.spinner("🔄 در حال ایجاد جلسه جدید..."):
#                         st.session_state.session_id = client.create_session()
                    
#                     if not st.session_state.session_id:
#                         st.error("❌ ایجاد جلسه با مشکل مواجه شد")
#                         st.stop()
                
#                 response_generator = client.send_message_stream_generator(
#                     st.session_state.session_id, 
#                     prompt
#                 )
#                 full_response = st.write_stream(response_generator)
#                 st.session_state.messages.append({"role": "assistant", "content": full_response})
                
#             except Exception as e:
#                 st.error(f"❌ خطایی رخ داد: {e}")

# # --- اجرا ---
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if not st.session_state.logged_in:
#     login_page()
# else:
#     main_app()


# صورتی

# # -*- coding: utf-8 -*-
# import streamlit as st
# import requests
# import json
# from datetime import datetime

# # --- تنظیمات صفحه ---
# st.set_page_config(
#     page_title="دستیار هوشمند خیاطی آکادمی خسروی",
#     page_icon="✂️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- افزودن meta برای charset ---
# st.markdown("<meta charset='utf-8'>", unsafe_allow_html=True)

# # --- استایل‌های CSS ---
# def load_css():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700&display=swap');
#     * { font-family: 'Vazirmatn', sans-serif !important; direction: rtl; text-align: right; }
#     .stApp { background: linear-gradient(135deg, #fce7f3, #fbcfe8, #ec4899); background-attachment: fixed; }
#     </style>
#     """, unsafe_allow_html=True)

# # --- کلاس ارتباط با API ---
# class MetisAI:
#     BASE_URL = "https://api.metisai.ir/api/v1"

#     def __init__(self, api_key, bot_id):
#         if not api_key or not bot_id:
#             raise ValueError("API key or Bot ID missing.")
#         self.api_key = api_key
#         self.bot_id = bot_id
#         self.headers = {
#             'Authorization': f'Bearer {self.api_key}',
#             'Content-Type': 'application/json'
#         }

#     def create_session(self):
#         url = f"{self.BASE_URL}/chat/session"
#         payload = {"botId": self.bot_id, "user": None, "initialMessages": []}
#         try:
#             response = requests.post(url, headers=self.headers, json=payload)
#             response.raise_for_status()
#             return response.json().get('id')
#         except requests.exceptions.RequestException as e:
#             st.error(f"❌ خطا در ایجاد جلسه: {e}")
#             return None

#     def send_message_stream_generator(self, session_id, message_content):
#         url = f"{self.BASE_URL}/chat/session/{session_id}/message/stream"
#         payload = {"message": {"content": message_content, "type": "USER"}}
#         try:
#             with requests.post(url, headers=self.headers, json=payload, stream=True) as response:
#                 response.raise_for_status()
#                 response.encoding = 'utf-8'
#                 for line in response.iter_lines(decode_unicode=True):
#                     if line and line.startswith('data:'):
#                         json_str = line[len('data:'):].strip()
#                         if not json_str:
#                             continue
#                         try:
#                             chunk = json.loads(json_str)
#                             content_piece = chunk.get("message", {}).get("content", "")
#                             if content_piece:
#                                 yield content_piece
#                         except json.JSONDecodeError:
#                             pass
#         except requests.exceptions.RequestException as e:
#             st.error(f"❌ خطا در دریافت پاسخ: {e}")

# # --- صفحه ورود کاربر ---
# def login_page():
#     load_css()
#     st.markdown("""
#     <div style='text-align:center; margin-top:5rem;'>
#         <h1 style='color:#ec4899;'>✂️ دستیار هوشمند خیاطی آکادمی خسروی 🧵</h1>
#         <p style='color:#db2777;'>✨ وارد آتلیه هوشمند شوید ✨</p>
#     </div>
#     """, unsafe_allow_html=True)

#     username = st.text_input("🪡 نام کاربری", key="username_input")
#     password = st.text_input("🔐 رمز عبور", type="password", key="password_input")

#     if st.button("✨ ورود به آتلیه هوشمند"):
#         VALID_CREDENTIALS = {"admin": "1234"}
#         if username in VALID_CREDENTIALS and password == VALID_CREDENTIALS[username]:
#             st.session_state.logged_in = True
#             st.session_state.login_time = datetime.now()
#             st.success("✅ خوش آمدید! آتلیه هوشمند برای شما آماده است 👗")
#             st.stop()
#         else:
#             st.error("❌ نام کاربری یا رمز عبور اشتباه است")

# # --- صفحه اصلی برنامه ---
# def main_app():
#     load_css()

#     st.markdown("""
#     <div style='text-align:center; margin-top:2rem;'>
#         <h1 style='color:white;'>✂️ دستیار هوشمند خیاطی آکادمی خسروی 🧵</h1>
#         <p style='color:#fdf4ff;'>👗 راهنمای شما در دنیای خیاطی، مد و طراحی لباس 📏</p>
#     </div>
#     """, unsafe_allow_html=True)

#     api_key = "tpsg-usFMzwCIzwxQT8tvUCQNoNXSCRdlg0a"
#     bot_id = "41326835-46dd-408a-acc9-465dadd76223"

#     if not api_key or not bot_id:
#         st.error("❌ کلید API یا شناسه ربات تنظیم نشده است")
#         st.stop()

#     with st.sidebar:
#         st.markdown("<h2 style='color:#ec4899;text-align:center;'>🧵 پنل کاربری</h2>", unsafe_allow_html=True)
#         st.markdown("<hr style='border:1px solid #fbcfe8;'>", unsafe_allow_html=True)

#         if "messages" in st.session_state:
#             msg_count = len([m for m in st.session_state.messages if m.get("role") == "user"])
#             st.markdown(f"<p style='color:#fff;'>💬 تعداد سوالات: {msg_count}</p>", unsafe_allow_html=True)

#         if "login_time" in st.session_state:
#             minutes = int((datetime.now() - st.session_state.login_time).total_seconds() / 60)
#             st.markdown(f"<p style='color:#fff;'>⏱️ زمان حضور: {minutes} دقیقه</p>", unsafe_allow_html=True)

#         if st.button("🔄 شروع گفتگوی جدید"):
#             st.session_state.messages = []
#             st.session_state.session_id = None
#             st.success("✅ گفتگو جدید آغاز شد")
#             st.stop()

#         if st.button("🚪 خروج"):
#             st.session_state.clear()
#             st.stop()

#     st.session_state.messages = [m for m in st.session_state.get("messages", []) if m.get("content")]
#     st.session_state.session_id = st.session_state.get("session_id", None)

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "✂️"):
#             st.markdown(message["content"])

#     if prompt := st.chat_input("✨ سوال خود درباره خیاطی، الگو یا مد را بپرسید..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(prompt)
#         with st.chat_message("assistant", avatar="✂️"):
#             try:
#                 client = MetisAI(api_key, bot_id)
#                 if not st.session_state.session_id:
#                     with st.spinner("🧵 در حال آماده‌سازی آتلیه ..."):
#                         st.session_state.session_id = client.create_session()
#                     if not st.session_state.session_id:
#                         st.error("❌ مشکل در ایجاد جلسه.")
#                         st.stop()

#                 response_generator = client.send_message_stream_generator(st.session_state.session_id, prompt)

#                 # اگر نسخه Streamlit قدیمی باشد write_stream وجود ندارد
#                 if hasattr(st, "write_stream"):
#                     full_response = st.write_stream(response_generator)
#                 else:
#                     full_response = "".join(response_generator)
#                     st.markdown(full_response)

#                 st.session_state.messages.append({"role": "assistant", "content": full_response})
#             except Exception as e:
#                 st.error(f"❌ خطای اجرای گفتگو: {e}")

# # --- اجرای نهایی ---
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if not st.session_state.logged_in:
#     login_page()
# else:
#     main_app()
# -*- coding: utf-8 -*
# 
# -

# import streamlit as st
# import requests
# import json
# from datetime import datetime

# # --- تنظیمات صفحه ---
# st.set_page_config(
#     page_title="دستیار هوشمند خیاطی آکادمی خسروی",
#     page_icon="✂️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- افزودن meta برای charset ---
# st.markdown("<meta charset='utf-8'>", unsafe_allow_html=True)

# # --- استایل‌های CSS با رنگ‌های پویا ---
# def load_css(primary="#ec4899", secondary="#d946ef", accent="#f97316"):
#     st.markdown(f"""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700&display=swap');
    
#     :root {{
#         --primary-color: {primary};
#         --secondary-color: {secondary};
#         --accent-color: {accent};
#     }}

#     * {{ font-family: 'Vazirmatn', sans-serif !important; direction: rtl; text-align: right; }}

#     .stApp {{
#         background: linear-gradient(135deg, var(--primary-color)20%, var(--secondary-color)70%);
#         background-attachment: fixed;
#         transition: background 0.6s ease-in-out;
#     }}

#     .stButton>button {{
#         background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
#         color: white; border-radius: 12px; border: none; padding: 0.8rem;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: all 0.3s ease;
#     }}
#     .stButton>button:hover {{
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.3);
#     }}
#     .stChatMessage[data-testid="user-message"] {{
#         background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
#         color: white !important;
#     }}
#     .stChatMessage[data-testid="assistant-message"] {{
#         background: #fff5fa !important; border: 1px solid {primary};
#     }}
#     </style>
#     """, unsafe_allow_html=True)

# # --- کلاس ارتباط با API ---
# class MetisAI:
#     BASE_URL = "https://api.metisai.ir/api/v1"

#     def __init__(self, api_key, bot_id):
#         if not api_key or not bot_id:
#             raise ValueError("API key or Bot ID missing.")
#         self.api_key = api_key
#         self.bot_id = bot_id
#         self.headers = {
#             'Authorization': f'Bearer {self.api_key}',
#             'Content-Type': 'application/json'
#         }

#     def create_session(self):
#         url = f"{self.BASE_URL}/chat/session"
#         payload = {"botId": self.bot_id, "user": None, "initialMessages": []}
#         try:
#             response = requests.post(url, headers=self.headers, json=payload)
#             response.raise_for_status()
#             return response.json().get('id')
#         except requests.exceptions.RequestException as e:
#             st.error(f"❌ خطا در ایجاد جلسه: {e}")
#             return None

#     def send_message_stream_generator(self, session_id, message_content):
#         url = f"{self.BASE_URL}/chat/session/{session_id}/message/stream"
#         payload = {"message": {"content": message_content, "type": "USER"}}
#         try:
#             with requests.post(url, headers=self.headers, json=payload, stream=True) as response:
#                 response.raise_for_status()
#                 response.encoding = 'utf-8'
#                 for line in response.iter_lines(decode_unicode=True):
#                     if line and line.startswith('data:'):
#                         json_str = line[len('data:'):].strip()
#                         if not json_str:
#                             continue
#                         try:
#                             chunk = json.loads(json_str)
#                             content_piece = chunk.get("message", {}).get("content", "")
#                             if content_piece:
#                                 yield content_piece
#                         except json.JSONDecodeError:
#                             pass
#         except requests.exceptions.RequestException as e:
#             st.error(f"❌ خطا در دریافت پاسخ: {e}")

# # --- صفحه ورود ---
# def login_page():
#     load_css()
#     st.markdown("""
#     <div style='text-align:center; margin-top:5rem;'>
#         <h1 style='color:var(--primary-color);'>✂️ دستیار هوشمند خیاطی آکادمی خسروی 🧵</h1>
#         <p style='color:var(--secondary-color);'>✨ وارد آتلیه هوشمند شوید ✨</p>
#     </div>
#     """, unsafe_allow_html=True)
#     username = st.text_input("🪡 نام کاربری", key="username_input")
#     password = st.text_input("🔐 رمز عبور", type="password", key="password_input")
#     if st.button("✨ ورود"):
#         VALID_CREDENTIALS = {"admin": "1234"}
#         if username in VALID_CREDENTIALS and password == VALID_CREDENTIALS[username]:
#             st.session_state.logged_in = True
#             st.session_state.login_time = datetime.now()
#             st.stop()
#         else:
#             st.error("❌ نام کاربری یا رمز عبور اشتباه است")

# # --- صفحه اصلی ---
# def main_app():
#     theme_colors = st.session_state.get("theme_colors", {"primary": "#ec4899", "secondary": "#d946ef", "accent": "#f97316"})
#     load_css(theme_colors["primary"], theme_colors["secondary"], theme_colors["accent"])

#     st.markdown(f"<h1 style='color:white;text-align:center;'>✂️ آتلیه هوشمند خیاطی</h1>", unsafe_allow_html=True)

#     api_key = "tpsg-usFMzwCIzwxQT8tvUCQNoNXSCRdlg0a"
#     bot_id = "41326835-46dd-408a-acc9-465dadd76223"

#     # --- سایدبار ---
#     with st.sidebar:
#         st.markdown("<h2 style='text-align:center;color:var(--primary-color);'>🎨 تنظیم رنگ تم</h2>", unsafe_allow_html=True)
#         primary_color = st.color_picker("رنگ اصلی", theme_colors["primary"])
#         secondary_color = st.color_picker("رنگ ثانویه", theme_colors["secondary"])
#         accent_color = st.color_picker("رنگ تأکیدی", theme_colors["accent"])
#         if st.button("اعمال تم جدید"):
#             st.session_state.theme_colors = {"primary": primary_color, "secondary": secondary_color, "accent": accent_color}
#             st.success("✅ رنگ‌های جدید اعمال شدند")
#             st.rerun()

#         st.markdown("<hr>", unsafe_allow_html=True)
#         st.markdown("<h2 style='text-align:center;color:var(--primary-color);'>پنل کاربری</h2>", unsafe_allow_html=True)
#         if st.button("🔄 شروع گفتگوی جدید"):
#             st.session_state.messages = []
#             st.session_state.session_id = None
#             st.success("✅ گفتگو جدید آغاز شد")
#             st.stop()
#         if st.button("🚪 خروج"):
#             st.session_state.clear()
#             st.stop()

#     st.session_state.messages = [m for m in st.session_state.get("messages", []) if m.get("content")]
#     st.session_state.session_id = st.session_state.get("session_id", None)

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "✂️"):
#             st.markdown(message["content"])

#     if prompt := st.chat_input("✨ سوال خود درباره خیاطی، الگو یا مد را بپرسید..."):
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user", avatar="👤"):
#             st.markdown(prompt)
#         with st.chat_message("assistant", avatar="✂️"):
#             try:
#                 client = MetisAI(api_key, bot_id)
#                 if not st.session_state.session_id:
#                     with st.spinner("🧵 آماده‌سازی آتلیه..."):
#                         st.session_state.session_id = client.create_session()
#                     if not st.session_state.session_id:
#                         st.error("❌ مشکل در ایجاد جلسه.")
#                         st.stop()

#                 response_generator = client.send_message_stream_generator(st.session_state.session_id, prompt)
#                 if hasattr(st, "write_stream"):
#                     full_response = st.write_stream(response_generator)
#                 else:
#                     full_response = "".join(response_generator)
#                     st.markdown(full_response)
#                 st.session_state.messages.append({"role": "assistant", "content": full_response})
#             except Exception as e:
#                 st.error(f"❌ خطای اجرای گفتگو: {e}")

# # --- اجرای نهایی ---
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# if not st.session_state.logged_in:
#     login_page()
# else:
#     main_app()
