import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# --- 1. การตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="AI Trade Buddy Pro", layout="wide", page_icon="📈")

# ตกแต่ง CSS ให้ช่อง Input และปุ่มดูรวมเป็นกลุ่มเดียวกัน
st.markdown("""
    <style>
    .stTextInput > div > div > input { border-radius: 20px; }
    .stButton > button { border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    div[data-testid="stColumn"] { display: flex; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI Trade Buddy Pro")

# --- 2. การเชื่อมต่อ API (ดึงจาก Secrets เพื่อความปลอดภัย) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("❌ ไม่พบ API KEY ในหน้า Secrets กรุณาตั้งค่าก่อนใช้งาน")

# --- 3. Sidebar และ กราฟ TradingView ---
symbol = st.sidebar.selectbox("🎯 เลือกคู่เทรด:", ["BTCUSD", "ETHUSD", "XAUUSD", "EURUSD"])
ticker = f"BINANCE:{symbol}T" if symbol in ["BTCUSD", "ETHUSD"] else ( "OANDA:XAUUSD" if symbol == "XAUUSD" else f"FX_IDC:{symbol}")

tradingview_html = f'<iframe src="https://s.tradingview.com/widgetembed/?symbol={ticker}&interval=D&theme=dark&locale=th" width="100%" height="450" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen></iframe>'
components.html(tradingview_html, height=460)

st.divider()

# --- 4. ระบบ AI รวมร่าง (Compact Input) ---
st.subheader("💬 ปรึกษาเซียน AI")

# แบ่งคอลัมน์: ช่องพิมพ์ (70%), แนบรูป (15%), ไมค์ (15%)
col_text, col_file, col_mic = st.columns([0.7, 0.15, 0.15])

with col_text:
    user_input = st.text_input("ถามคำถาม:", placeholder="พิมพ์คำถามที่นี่...", label_visibility="collapsed")

with col_file:
    # ช่องแนบรูปแบบไอคอน
    uploaded_file = st.file_uploader("Upload", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

with col_mic:
    # ปุ่มไมค์
    audio_data = mic_recorder(start_prompt="🎤", stop_prompt="🛑", key='recorder')

# ปุ่มส่งแบบเต็มความกว้าง
submit = st.button("🚀 ส่งให้ AI วิเคราะห์ด่วน", use_container_width=True)

# --- 5. ส่วนประมวลผล ---
if submit or audio_data:
    if not user_input and not audio_data and not uploaded_file:
        st.warning("⚠️ โปรดระบุข้อมูลอย่างใดอย่างหนึ่ง (พิมพ์/พูด/ส่งรูป)")
    else:
        with st.spinner('⚡ เซียน AI กำลังวิเคราะห์...'):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                content_list = ["วิเคราะห์ในฐานะเซียนเทรดเดอร์ ตอบเป็นภาษาไทย กระชับ ได้ใจความ: "]
                
                if user_input: content_list[0] += user_input
                if audio_data: content_list.append({"mime_type": "audio/wav", "data": audio_data['bytes']})
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    img.thumbnail((800, 800)) # ลดขนาดภาพให้ประมวลผลเร็วขึ้น
                    content_list.append(img)
                
                response = model.generate_content(content_list)
                st.success("✅ บทวิเคราะห์:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาด: {e}")

st.divider()
st.caption("AI Trade Buddy v7.0 | Compact Interface 2026")
