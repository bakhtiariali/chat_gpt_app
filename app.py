# -*- coding: utf-8 -*-
import streamlit as st
import requests
import json
import os
import base64 # To encode the background image

# --- کلاس ارتباط با API (بدون تغییر در منطق اصلی) ---
class MetisAI:
    """
    A Python client for the MetisAI Chat API, adapted for Streamlit.
    This class handles creating sessions and generating streamed responses.
    """
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
            st.error(f"خطا در ایجاد جلسه: {e}")
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
            st.error(f"خطا در هنگام دریافت پاسخ: {e}")

# --- سیستم ورود ---
def check_login():
    """Returns `True` if the user is logged in, `False` otherwise."""
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.set_page_config(page_title="ورود", layout="centered")
        st.title("ورود به دستیار هوشمند")
        
        # اطلاعات ورود نمونه - در یک برنامه واقعی از روش امن‌تری استفاده کنید
        VALID_CREDENTIALS = {"admin": "1234"}

        username = st.text_input("نام کاربری", key="username_input")
        password = st.text_input("رمز عبور", type="password", key="password_input")

        if st.button("ورود"):
            if username in VALID_CREDENTIALS and password == VALID_CREDENTIALS[username]:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("نام کاربری یا رمز عبور اشتباه است.")
        return False
    return True

# --- تابع برای تنظیم پس‌زمینه ---
def set_bg_hack(image_url):
    '''
    A function to set a background image from a URL.
    '''
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("{image_url}");
             background-size: cover;
             background-position: center;
             background-repeat: no-repeat;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# --- رابط کاربری اصلی برنامه ---
def main_app():
    st.set_page_config(page_title="دستیار هوشمند آکادمی خسروی", page_icon="�")
    
    # آدرس لوگوی خود را در اینجا قرار دهید
    logo_url = "https://khosraviacademy.ir/"
    set_bg_hack(logo_url)

    st.title("🤖 دستیار هوشمند آکادمی خسروی")
    st.caption("powered by MetisAI & Streamlit")

    # دریافت کلیدها از متغیرهای محیطی
    # این روش امن‌تر است و اطلاعات حساس را در کد قرار نمی‌دهد
    api_key = "tpsg-usFMzwCIzwxQT8tvUCQNoNXSCRdlg0a"
    bot_id = "41326835-46dd-408a-acc9-465dadd76223"  

    if not api_key or not bot_id:
        st.error("کلید API یا شناسه ربات تنظیم نشده است. لطفا با پشتیبانی تماس بگیرید.")
        st.stop()

    with st.sidebar:
        st.header("تنظیمات گفتگو")
        if st.button("شروع گفتگوی جدید"):
            st.session_state.messages = []
            st.session_state.session_id = None
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("سوال خود را اینجا بنویسید..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                client = MetisAI(api_key, bot_id)
                if not st.session_state.session_id:
                    with st.spinner("در حال ایجاد جلسه جدید..."):
                        st.session_state.session_id = client.create_session()
                    if not st.session_state.session_id:
                        st.error("ایجاد جلسه با مشکل مواجه شد. لطفا دوباره تلاش کنید.")
                        st.stop()
                
                response_generator = client.send_message_stream_generator(st.session_state.session_id, prompt)
                full_response = st.write_stream(response_generator)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"خطایی رخ داد: {e}")

# --- اجرای برنامه ---
if check_login():
    main_app()
