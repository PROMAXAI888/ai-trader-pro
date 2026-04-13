import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# --- 1. การตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="AI Trade Buddy Pro", layout="wide", page_icon="📈")

# --- 2. ปรับแต่ง UI ให้เหมือน Gemini (CSS) ---
st.markdown("""
    <style>
    /* ปรับแต่งช่อง Input ให้มนและดูคลีน */
    .stTextInput > div > div > input {
        border-radius: 25px;
        padding-left: 20px;
        background-color: #262730;
        border: 1px solid #444;
    }
    /* ซ่อน Label ของ File Uploader */
    .stFileUploader label { display: none; }
    
    /* ปรับแต่งปุ่มส่งให้ดูพรีเมียม */
    .stButton > button {
        border-radius: 20px;
        background-color: #4A90E2;
        color: white;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #357ABD;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI Trade Buddy Pro")

# --- 3. การเชื่อมต่อ API (ดึงจาก Secrets) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("❌ กรุณาตั้งค่า GOOGLE_API_KEY ในหน้า Secrets ของ Streamlit")

# --- 4. Sidebar และ กราฟ TradingView ---
with st.sidebar:
    st.header("📈 ตลาด")
    symbol = st.selectbox("เลือกคู่เทรด:", ["BTCUSD", "ETHUSD", "XAUUSD", "EURUSD"])
    st.divider()
    st.info("ใช้ระบบ Gemini 2.5 Flash วิเคราะห์ข้อมูลแบบ Real-time")

# จัดการ Ticker
if symbol in ["BTCUSD", "ETHUSD"]:
    ticker = f"BINANCE:{symbol}T"
elif symbol == "XAUUSD":
    ticker = "OANDA:XAUUSD"
else:
    ticker = f"FX_IDC:{symbol}"

# แสดงกราฟ
tv_html = f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={ticker}&interval=D&theme=dark&locale=th" width="100%" height="450" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen></iframe>'
components.html(tv_html, height=460)

st
