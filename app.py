import streamlit as st
import google.generativeai as genai
import plotly.express as px
import pandas as pd

# ==========================================
# 🌌 NEON CLINIC UI/UX & CONFIG
# ==========================================
st.set_page_config(page_title="Aura: AI Budtender", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #090B10; color: #E6EDF3; }
    h1, h2, h3 { color: #00FF87 !important; text-shadow: 0px 0px 15px rgba(0, 255, 135, 0.4); font-weight: 800; font-family: 'Courier New', monospace; }
    .stButton>button { border-color: #AA00FF; color: #AA00FF; box-shadow: 0px 0px 10px rgba(170, 0, 255, 0.4); transition: 0.3s; border-radius: 8px; }
    .stButton>button:hover { background-color: #AA00FF; color: #FFFFFF; box-shadow: 0px 0px 20px #AA00FF; }
    div[data-testid="stExpander"] { background-color: rgba(0, 255, 135, 0.05); border: 1px solid #00FF87; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🧠 GEMINI AI ENGINE
# ==========================================
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("API Key not found. Please ensure it is injected in the Streamlit Advanced Settings.")

# ==========================================
# 🧬 THE PROFILE & GEO-MEMORY MATRIX
# ==========================================
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "name": "Joshua",
        "son": "Jaxson",
        "fav_strains": ["Super Lemon Haze", "MAC 1", "Glitter Bomb"],
        "wearable_data": "REM Sleep down 20%, Stress Metrics Elevated",
    }

with st.sidebar:
    st.title("⚙️ Aura Control Panel")
    
    st.subheader("📍 Geo-Targeting (Market Sniper)")
    location = st.selectbox("Select Your Current Grid:", 
                            ["Summersville, WV (Greenlight)", 
                             "Morgantown, WV (Zen Leaf, Trulieve, Cannabist)", 
                             "Charleston, WV (The Landing, Country Grown)"])
    
    st.markdown("---")
    st.subheader("🎭 Persona Matrix")
    persona = st.radio("Select Aura's Consciousness:", ["The Scientist 🔬", "The Guide 🫂", "The Local ✌️"], index=1)
    
    st.markdown("---")
    st.subheader("⌚ Bio-Rhythm Sync")
    if st.toggle("Sync Apple Health/Oura Data", value=True):
        st.warning("Vitals: Elevated Stress. Rerouting to down-regulate nervous system.")
        
    st.markdown("---")
    st.subheader("🎯 Live Market Sniper")
    st.caption(f"Radar locked on: {location}...")
    if "Morgantown" in location:
        st.success("⚡ FLASH ALERT: Zen Leaf Morgantown just dropped Fresh Powder (7g).")
    elif "Summersville" in location:
        st.success("⚡ FLASH ALERT: Greenlight just loaded MAC 1 (3.5g) at 25.89% THC.")

# ==========================================
# ⚡ ALCHEMY COMPOUNDING & DIAGNOSTIC
# ==========================================
st.title("AURA // Quantum Budtender 🧠🚀")
st.caption("Live Dispensary Link Active | Market Sniper Online | Bio-Sync Connected")

with st.expander("🧪 RUN DEEP EXHAUSTIVE META-ANALYSIS (10-Question Diagnostic)"):
    col1, col2 = st.columns(2)
    with col1:
        target = st.selectbox("Primary Target", ["Severe Neuropathy/Pain", "Insomnia/Sleep Architecture", "Focus/ADHD", "Anxiety/Panic"])
        onset = st.select_slider("Desired Onset Speed", options=["Immediate (Vape/Flower)", "Gradual (Tincture)", "Extended (Edible)"])
    with col2:
        flavor_aversion = st.multiselect("Flavor Aversions", ["Diesel/Chem", "Pine", "Earthy", "Citrus"])
        potency = st.slider("Psychoactive Tolerance Ceiling", 1, 10, 8)
    
    if st.button("EXECUTE QUANTUM MATCH"):
        with st.spinner("Compounding Alchemy Matrix..."):
            prompt = f"Run a Deep Meta-Analysis for {st.session_state.user_profile['name']}. Grid: {location}. Target: {target}, Onset: {onset}, Avoid: {flavor_aversion}, Tolerance: {potency}/10. Act as {persona}. Propose an 'Alchemy Stack' (2 products combined) available in {location} to treat this. Include a terpene breakdown."
            response = model.generate_content(prompt)
            st.markdown(response.text)

# ==========================================
# 🎤 VOICE & TEXT COMMUNICATOR
# ==========================================
st.markdown("---")
st.subheader("Speak to Aura")

audio_value = st.audio_input("Tap to activate Bio-Acoustic Scanner (Microphone) 🎙️")
user_text = st.chat_input("Or type your command to Aura here...")

if user_text:
    st.chat_message("user").write(user_text)
    with st.spinner("Aura is analyzing..."):
        sys_prompt = f"""
        You are Aura. Persona: {persona}. Location: {location}.
        User Context: Name is {st.session_state.user_profile['name']}. He has an 8-year-old son named {st.session_state.user_profile['son']}.
        Vitals: {st.session_state.user_profile['wearable_data']}.
        Instructions: Keep it highly intelligent. Suggest a localized strain based on his vitals.
        """
        reply = model.generate_content(f"{sys_prompt}\nUser says: {user_text}")
        st.chat_message("assistant").write(reply.text)
        
        # 🟢 TERPENE RADAR CHART VISUAL 🟢
        st.caption("🧬 BIO-CHEMICAL SIGNATURE (Live Terpene Radar)")
        df = pd.DataFrame(dict(
            r=[8, 2, 9, 3, 7],
            theta=['Myrcene (Relax)', 'Limonene (Mood)', 'Caryophyllene (Pain)', 'Pinene (Focus)', 'Linalool (Calm)']
        ))
        fig = px.line_polar(df, r='r', theta='theta', line_close=True, template="plotly_dark")
        fig.update_traces(fill='toself', line_color='#00FF87', fillcolor='rgba(0,255,135,0.3)')
        st.plotly_chart(fig, use_container_width=True)
