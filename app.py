import streamlit as st
import requests
import json
import google.generativeai as genai

# ==========================================
# 1. APP CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="Aura | AI Budtender", page_icon="🌿", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; }
    h1 { color: #00FF87; font-family: 'Helvetica Neue', sans-serif; }
    .stTextArea textarea { background-color: #1E2329; color: white; border: 1px solid #00FF87; }
    .stButton>button { background-color: #00FF87; color: black; font-weight: bold; border-radius: 8px; width: 100%; }
    .stButton>button:hover { background-color: #00CC6A; color: white; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. THE ENGINE: FETCHING LIVE DATA
# ==========================================
@st.cache_data(ttl=300) 
def fetch_greenlight_inventory():
    url = "https://dutchie.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    payload = {
        "operationName": "FilteredProducts",
        "variables": {
            "dispensaryId": "greenlight-summersville", 
            "pricingType": "med",
            "productsFilter": {"categories": ["Flower", "Vaporizers"], "useCache": False},
            "page": 0,
            "limit": 30
        },
        "query": "query FilteredProducts($dispensaryId: String!, $productsFilter: ProductsFilterInput, $page: Int, $limit: Int) { filteredProducts(dispensaryId: $dispensaryId, filter: $productsFilter, page: $page, limit: $limit) { products { name brandName { name } prices { price salePrice } thcPotency { formatted } } } }"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        products = response.json().get("data", {}).get("filteredProducts", {}).get("products", [])
        
        clean_inventory = []
        for p in products:
            price = p.get("prices", {}).get("salePrice") or p.get("prices", {}).get("price")
            clean_inventory.append({
                "Brand": p.get("brandName", {}).get("name"),
                "Strain": p.get("name"),
                "Price": f"${price}",
                "THC": p.get("thcPotency", {}).get("formatted", "N/A")
            })
        return clean_inventory
    except Exception as e:
        return []

# ==========================================
# 3. THE AI BRAIN: GEMINI INTEGRATION
# ==========================================
def ask_clinical_botanist(user_symptoms, live_menu):
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) 
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    system_prompt = f"""
    You are Aura, a Clinical Neuro-Botanist AI. 
    A medical marijuana patient has asked for help. 
    Here is the LIVE inventory right now at Greenlight Summersville: {json.dumps(live_menu)}
    
    Match their symptoms/desires to the best 2 products on this specific list. 
    Format your response beautifully with bold text, bullet points, and the current price. 
    Explain exactly WHY these strains match chemically (mention terpenes).
    """
    
    response = model.generate_content(system_prompt + "\nUser Request: " + user_symptoms)
    return response.text

# ==========================================
# 4. THE CUSTOMER FRONT-END (UI)
# ==========================================
st.title("🌿 Aura")
st.subheader("Precision Medicine & Live Inventory Snipe")
st.markdown("Currently connected to: **Greenlight Dispensary (Summersville, WV)**")

user_request = st.text_area(
    "What are you looking for today?", 
    placeholder="e.g., I have severe shoulder pain and need something fruity that will help me sleep."
)

if st.button("Consult AI Budtender"):
    if user_request:
        with st.spinner("📡 Intercepting live dispensary data..."):
            menu_data = fetch_greenlight_inventory()
            
        if not menu_data:
            st.error("Failed to connect to dispensary. They may have updated their security.")
        else:
            with st.spinner("🧬 Aura is analyzing terpene profiles and matching symptoms..."):
                recommendation = ask_clinical_botanist(user_request, menu_data)
                
            st.success("Analysis Complete.")
            st.markdown("---")
            st.markdown(recommendation)
    else:
        st.warning("Please tell Aura what effects you are looking for first.")
