import streamlit as st
import resend

# ==========================================
# PAGE SETUP & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Flex Head | Order Portal", page_icon="🏭", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    div[data-testid="stForm"] { 
        background-color: #ffffff; 
        padding: 30px; 
        border-radius: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); 
        border-top: 5px solid #0b1220; 
    }
    h1 { color: #0b1220; text-align: center; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
    h3 { color: #475569; text-align: center; font-weight: 400; margin-bottom: 30px; }
    .stButton>button { 
        width: 100%; 
        background-color: #28a745; 
        color: white; 
        height: 50px; 
        font-size: 18px; 
        font-weight: bold; 
        border-radius: 8px; 
        border: none; 
    }
    .stButton>button:hover { background-color: #218838; color: white; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏭 FLEX HEAD INDUSTRIES</h1>", unsafe_allow_html=True)
st.markdown("<h3>B2B Online Pipe Ordering Portal</h3>", unsafe_allow_html=True)

# ==========================================
# SECRETS LOAD KAREIN
# ==========================================
try:
    resend.api_key = st.secrets["RESEND_API_KEY"]
    TARGET_EMAIL = st.secrets["EMAIL_RECEIVER"] # Sirf isi email par order jayega
except Exception:
    st.error("⚠️ Secrets missing! Please configure RESEND_API_KEY and EMAIL_RECEIVER in Streamlit Cloud.")
    st.stop()

# ==========================================
# PRODUCTS LIST
# ==========================================
PRODUCTS = [
    "Flex PPRC Pipe - 20mm (Rs. 450/m)",
    "Flex PPRC Pipe - 32mm (Rs. 600/m)",
    "Flex HDPE Pipe - 50mm (Rs. 850/m)",
    "Flex HDPE Pipe - 110mm (Rs. 1500/m)",
    "Flex HDPE Pipe - 160mm (Rs. 2200/m)"
]

# ==========================================
# ORDER FORM
# ==========================================
with st.form("order_form"):
    st.markdown("### 📝 Enter Your Details")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Customer / Company Name *", placeholder="e.g. Ali Builders")
    with col2:
        phone = st.text_input("Phone Number *", placeholder="e.g. 0300 1234567")
    
    st.markdown("### 📦 Select Product")
    col3, col4 = st.columns([2, 1])
    with col3:
        product = st.selectbox("Select Pipe Type *", PRODUCTS)
    with col4:
        quantity = st.number_input("Quantity (Meters) *", min_value=10, step=10, value=10)
    
    submit = st.form_submit_button("🚀 Send Order Request")

# ==========================================
# EMAIL SENDING LOGIC
# ==========================================
if submit:
    if not name.strip() or not phone.strip():
        st.warning("⚠️ Please fill in all required fields.")
    else:
        with st.spinner("Sending your order..."):
            try:
                # Email ka format
                html_content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
                    <div style="background-color: #0b1220; color: white; padding: 20px; text-align: center;">
                        <h2 style="margin: 0;">New Pipe Order Received</h2>
                    </div>
                    <div style="padding: 20px; background-color: #f9f9f9;">
                        <p><strong>Customer Name:</strong> {name}</p>
                        <p><strong>Phone Number:</strong> {phone}</p>
                        <p><strong>Product:</strong> {product}</p>
                        <p><strong>Quantity:</strong> {quantity} Meters</p>
                    </div>
                </div>
                """
                
                # Email Resend ke through bhejein
                params = {
                    "from": "onboarding@resend.dev",
                    "to": [TARGET_EMAIL],  # <--- Yahan sirf aapki email jayegi
                    "subject": f"🚨 New Order: {name} - {quantity}m",
                    "html": html_content
                }
                
                resend.Emails.send(params)
                st.success(f"✅ Thank you {name}! Aapka order kamyabi se bhej diya gaya hai.")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Email bhejne mein masla aaya. Error: {str(e)}")
