import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder

# --- 1. การตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="AI Trade Buddy Pro", layout="wide", page_icon="📈")

# ตกแต่ง CSS ให้ปุ่มไมค์ดูเรียบเนียนขึ้น
st.markdown("""
    <style>
    .stButton > button { width: 100%; border-radius: 20px; }
    .stTextInput > div > div > input { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI Trade Buddy Pro")
st.caption("เวอร์ชัน 2026: รองรับการสั่งงานด้วยเสียง วิเคราะห์ภาพ และกราฟเทรดดิ้ง")

# --- 2. การเชื่อมต่อ API ---
API_KEY = "AIzaSyACJPtk0ApHJPbF9VWqu8Z9pdYE3LDI-y4"
genai.configure(api_key=API_KEY)

# --- 3. Sidebar เมนูตั้งค่า ---
st.sidebar.header("⚙️ ตั้งค่าสินทรัพย์")
symbol = st.sidebar.selectbox(
    "เลือกคู่เทรด:", 
    ["BTCUSD", "ETHUSD", "XAUUSD", "EURUSD", "GBPUSD"]
)
st.sidebar.divider()
st.sidebar.write("🟢 สถานะ: เชื่อมต่อ Gemini 2.5 Flash")

# --- 4. แสดงกราฟ TradingView ---
st.subheader(f"📊 กราฟราคาปัจจุบัน: {symbol}")

if symbol in ["BTCUSD", "ETHUSD"]:
    ticker = f"BINANCE:{symbol}T"
elif symbol == "XAUUSD":
    ticker = "OANDA:XAUUSD"
else:
    ticker = f"FX_IDC:{symbol}"

tradingview_html = f"""
<iframe 
    src="https://s.tradingview.com/widgetembed/?symbol={ticker}&interval=D&theme=dark&locale=th" 
    width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen>
</iframe>
"""
components.html(tradingview_html, height=510)

st.divider()

# --- 5. ระบบ AI (Voice behind Text input) ---
st.subheader("💬 ปรึกษาเซียน AI")

# สร้าง Layout ให้ปุ่มไมค์อยู่หลังช่องพิมพ์
col_text, col_mic = st.columns([0.85, 0.15])

with col_text:
    user_input = st.text_input(
        "ถามคำถาม:", 
        placeholder="พิมพ์คำถามที่นี่ หรือกดไมค์ด้านข้างเพื่อพูด...",
        label_visibility="collapsed"
    )

with col_mic:
    # ปุ่มไมค์แบบกระชับอยู่ท้ายช่องพิมพ์
    audio_data = mic_recorder(
        start_prompt="🎤 พูด",
        stop_prompt="🛑 หยุด",
        key='recorder'
    )

# ส่วนอัปโหลดรูปภาพ
uploaded_file = st.file_uploader("📸 แนบรูปกราฟเพื่อวิเคราะห์ภาพ:", type=["jpg", "jpeg", "png"])

# ปุ่มส่งคำถามหลัก
submit_all = st.button("🚀 ส่งให้ AI วิเคราะห์")

# --- 6. ส่วนประมวลผล Logic ---
if submit_all or audio_data:
    if not user_input and not audio_data and not uploaded_file:
        st.warning("⚠️ โปรดระบุข้อมูล (พิมพ์, พูด หรือ แนบรูป) อย่างใดอย่างหนึ่ง")
    else:
        with st.spinner('🔍 เซียน AI กำลังประมวลผล...'):
            try:
                # ใช้รุ่นที่รองรับ Audio & Vision พร้อมกัน (รุ่น 2.5 ขึ้นไป)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                content_list = ["คุณคือเซียนเทรดเดอร์ ตอบเป็นภาษาไทยและวิเคราะห์อย่างมืออาชีพ: "]
                
                # เพิ่มเสียง (ถ้ามี)
                if audio_data:
                    content_list.append({"mime_type": "audio/wav", "data": audio_data['bytes']})
                
                # เพิ่มข้อความ (ถ้ามี)
                if user_input:
                    content_list[0] += user_input
                
                # เพิ่มรูปภาพ (ถ้ามี)
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    content_list.append(img)
                
                # สั่งงาน AI
                response = model.generate_content(content_list)
                
                st.success("✅ ผลการวิเคราะห์:")
                st.markdown(f"> {response.text}")
                
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาด: {e}")
                st.info("💡 คำแนะนำ: หากติดปัญหา 404 ให้เช็คชื่อ Model ในเครื่องอีกครั้ง")

st.divider()
st.markdown("<center><small>AI Trade Buddy Pro v6.5 | 2026 Stable</small></center>", unsafe_allow_html=True)