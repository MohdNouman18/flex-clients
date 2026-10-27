import streamlit as st
import resend
import os

# ==========================================
# PAGE SETUP & MINIMAL CSS
# ==========================================
st.set_page_config(page_title="Flex Pipe | Order", layout="centered")

st.markdown("""
    <style>
    /* Simple and clean background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Form container */
    div[data-testid="stForm"] {
        padding: 20px;
        border: 1px solid #ddd;
        border-radius: 8px;
    }
    
    /* Button style */
    .stButton>button {
        width: 100%;
        background-color: #0056b3;
        color: white;
        height: 45px;
        font-size: 16px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #004494;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER & LOGO
# ==========================================
# Agar logo.png file folder mein hai toh show hoga
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", use_container_width=True)

st.markdown("<h3 style='text-align: center; color: #333;'>Order Form</h3>", unsafe_allow_html=True)

# ==========================================
# SECRETS SETUP
# ==========================================
try:
    resend.api_key = st.secrets["RESEND_API_KEY"]
    TARGET_EMAIL = st.secrets["EMAIL_RECEIVER"]
except Exception:
    st.error("Secrets missing. Please configure RESEND_API_KEY and EMAIL_RECEIVER.")
    st.stop()

# ==========================================
# PRODUCTS LIST (From your CSV)
# ==========================================
PRODUCTS = [
    "HDPE (PE-100) 20MM PN 16 BLACK", "HDPE (PE-100) 25MM PN 16 BLACK", "HDPE (PE-100) 32MM PN 16 BLACK",
    "HDPE (PE-100) 40MM PN 16 BLACK", "HDPE (PE-100) 50MM PN 16 BLACK", "HDPE (PE-100) 63MM PN 16 BLACK",
    "HDPE (PE-100) 75MM PN 16 BLACK", "HDPE (PE-100) 90MM PN 16 BLACK", "HDPE (PE-100) 110MM PN 16 BLACK",
    "HDPE (PE-100) 125MM PN 16 BLACK", "HDPE (PE-100) 140MM PN 16 BLACK", "HDPE (PE-100) 160MM PN 16 BLACK",
    "HDPE (PE-100) 180MM PN 16 BLACK", "HDPE (PE-100) 200MM PN 16 BLACK", "HDPE (PE-100) 225MM PN 16 BLACK",
    "HDPE (PE-100) 250MM PN 16 BLACK", "HDPE (PE-100) 280MM PN 16 BLACK", "HDPE (PE-100) 315MM PN 16 BLACK",
    "HDPE (PE-100) 355MM PN 16 BLACK", "HDPE (PE-100) 400MM PN 16 BLACK", "HDPE (PE-100) 450MM PN 16 BLACK",
    "HDPE (PE-100) 500MM PN 16 BLACK", "HDPE (PE-100) 560MM PN 16 BLACK", "HDPE (PE-100) 630MM PN 16 BLACK",
    "HDPE (PE-100) 20MM PN 12.5 BLACK", "HDPE (PE-100) 25MM PN 12.5 BLACK", "HDPE (PE-100) 32MM PN 12.5 BLACK",
    "HDPE (PE-100) 40MM PN 12.5 BLACK", "HDPE (PE-100) 50MM PN 12.5 BLACK", "HDPE (PE-100) 63MM PN 12.5 BLACK",
    "HDPE (PE-100) 75MM PN 12.5 BLACK", "HDPE (PE-100) 90MM PN 12.5 BLACK", "HDPE (PE-100) 110MM PN 12.5 BLACK",
    "HDPE (PE-100) 125MM PN 12.5 BLACK", "HDPE (PE-100) 140MM PN 12.5 BLACK", "HDPE (PE-100) 160MM PN 12.5 BLACK",
    "HDPE (PE-100) 180MM PN 12.5 BLACK", "HDPE (PE-100) 200MM PN 12.5 BLACK", "HDPE (PE-100) 225MM PN 12.5 BLACK",
    "HDPE (PE-100) 250MM PN 12.5 BLACK", "HDPE (PE-100) 280MM PN 12.5 BLACK", "HDPE (PE-100) 315MM PN 12.5 BLACK",
    "HDPE (PE-100) 355MM PN 12.5 BLACK", "HDPE (PE-100) 400MM PN 12.5 BLACK", "HDPE (PE-100) 450MM PN 12.5 BLACK",
    "HDPE (PE-100) 560MM PN 12.5 BLACK", "HDPE (PE-100) 630MM PN 12.5 BLACK",
    "HDPE (PE-100) 20MM PN 10 BLACK", "HDPE (PE-100) 25MM PN 10 BLACK", "HDPE (PE-100) 32MM PN 10 BLACK",
    "HDPE (PE-100) 40MM PN 10 BLACK", "HDPE (PE-100) 50MM PN 10 BLACK", "HDPE (PE-100) 63MM PN 10 BLACK",
    "HDPE (PE-100) 75MM PN 10 BLACK", "HDPE (PE-100) 90MM PN 10 BLACK", "HDPE (PE-100) 110MM PN 10 BLACK",
    "HDPE (PE-100) 125MM PN 10 BLACK", "HDPE (PE-100) 140MM PN 10 BLACK", "HDPE (PE-100) 160MM PN 10 BLACK",
    "HDPE (PE-100) 180MM PN 10 BLACK", "HDPE (PE-100) 200MM PN 10 BLACK", "HDPE (PE-100) 225MM PN 10 BLACK",
    "HDPE (PE-100) 250MM PN 10 BLACK", "HDPE (PE-100) 280MM PN 10 BLACK", "HDPE (PE-100) 315MM PN 10 BLACK",
    "HDPE (PE-100) 355MM PN 10 BLACK", "HDPE (PE-100) 400MM PN 10 BLACK", "HDPE (PE-100) 450MM PN 10 BLACK",
    "HDPE (PE-100) 500MM PN 10 BLACK", "HDPE (PE-100) 560MM PN 10 BLACK", "HDPE (PE-100) 630MM PN 10 BLACK",
    "HDPE (PE-100) 20MM PN 8 BLACK", "HDPE (PE-100) 25MM PN 8 BLACK", "HDPE (PE-100) 32MM PN 8 BLACK",
    "HDPE (PE-100) 40MM PN 8 BLACK", "HDPE (PE-100) 50MM PN 8 BLACK", "HDPE (PE-100) 63MM PN 8 BLACK",
    "HDPE (PE-100) 75MM PN 8 BLACK", "HDPE (PE-100) 90MM PN 8 BLACK", "HDPE (PE-100) 90MM PN 8 BLACK (65%+35%)",
    "HDPE (PE-100) 110MM PN 8 BLACK", "HDPE (PE-100) 125MM PN 8 BLACK", "HDPE (PE-100) 140MM PN 8 BLACK",
    "HDPE (PE-100) 160MM PN 8 BLACK", "HDPE (PE-100) 180MM PN 8 BLACK", "HDPE (PE-100) 200MM PN 8 BLACK",
    "HDPE (PE-100) 225MM PN 8 BLACK", "HDPE (PE-100) 250MM PN 8 BLACK", "HDPE (PE-100) 280MM PN 8 BLACK",
    "HDPE (PE-100) 315MM PN 8 BLACK", "HDPE (PE-100) 355MM PN 8 BLACK", "HDPE (PE-100) 400MM PN 8 BLACK",
    "HDPE (PE-100) 450MM PN 8 BLACK", "HDPE (PE-100) 500MM PN 8 BLACK", "HDPE (PE-100) 560MM PN 8 BLACK",
    "HDPE (PE-100) 630MM PN 8 BLACK", "HDPE (PE-100) 20MM PN 6 BLACK", "HDPE (PE-100) 25MM PN 6 BLACK",
    "HDPE (PE-100) 32MM PN 6 BLACK", "HDPE (PE-100) 40MM PN 6 BLACK", "HDPE (PE-100) 50MM PN 6 BLACK",
    "HDPE (PE-100) 63MM PN 6 BLACK", "HDPE (PE-100) 75MM PN 6 BLACK", "HDPE (PE-100) 90MM PN 6 BLACK",
    "HDPE (PE-100) 110MM PN 6 BLACK", "HDPE (PE-100) 125MM PN 6 BLACK", "HDPE (PE-100) 140MM PN 6 BLACK",
    "HDPE (PE-100) 160MM PN 6 BLACK", "HDPE (PE-100) 180MM PN 6 BLACK", "HDPE (PE-100) 200MM PN 6 BLACK",
    "HDPE (PE-100) 225MM PN 6 BLACK", "HDPE (PE-100) 250MM PN 6 BLACK", "HDPE (PE-100) 280MM PN 6 BLACK",
    "HDPE (PE-100) 315MM PN 6 BLACK", "HDPE (PE-100) 355MM PN 6 BLACK", "HDPE (PE-100) 400MM PN 6 BLACK",
    "HDPE (PE-100) 450MM PN 6 BLACK", "HDPE (PE-100) 500MM PN 6 BLACK", "HDPE (PE-100) 560MM PN 6 BLACK",
    "HDPE (PE-100) 630MM PN 6 BLACK", "HDPE (PE-100) 110MM PN 8 BLACK (65%+35%)", "HDPE (PE-100) 125MM PN 8 BLACK (65%+35%)",
    "HDPE (PE-100) 110MM PN 8 BLACK (65%+35%)", "HDPE (PE-100) 200MM PN 8 BLACK (65%+35%)", "HDPE (PE-100) 225MM PN 8 BLACK (65%+35%)",
    "HDPE (PE-100) 250MM PN 8 BLACK (65%+35%)", "HDPE (PE-100) 315MM PN 8 BLACK (65%+35%) W/O PRINT", "HDPE (PE-100) 355M PN 8 BLACK (W/ PN-10 PRINT)",
    "HDPE (PE-100) 400MM PN 8 BLACK (65%+35%)", "HDPE (PE-100) 450MM PN 8 BLACK (65%+35%)", "HDPE (PE-100) 630MM PN 8 BLACK (60%+40%)",
    "HDPE (PE-100) 90MM PN 10 BLACK (65%+35%)", "HDPE (PE-100) 110MM PN 10 BLACK (R65%+L35%)", "HDPE (PE-100) 160MM PN 10 BLACK (R65%+L35%)",
    "HDPE (PE-100) 200MM PN 10 BLACK (65%+35%)", "HDPE (PE-100) 250MM PN 10 BLACK (65%+35%)", "HDPE (PE-100) 315MM PN 10 BLACK (65%+35%)",
    "HDPE (PE-100) 500MM PN 10 BLACK (60%+40%)", "HDPE (PE-100) 500MM PN 10 (60%+40%) INSIDE ROUGH"
]

# ==========================================
# ORDER FORM (Name, Phone, Product, Qty, Location)
# ==========================================
with st.form("order_form"):
    
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    product = st.selectbox("Product", PRODUCTS)
    quantity = st.number_input("Quantity (Meters)", min_value=1, step=1)
    location = st.text_input("Location")
    
    submit = st.form_submit_button("Submit Order")

# ==========================================
# EMAIL SENDING LOGIC
# ==========================================
if submit:
    if not name.strip() or not phone.strip() or not location.strip():
        st.warning("Please fill all fields.")
    else:
        with st.spinner("Processing..."):
            try:
                html_content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px;">
                    <h3 style="color: #0056b3;">New Order Received</h3>
                    <hr>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Phone:</strong> {phone}</p>
                    <p><strong>Product:</strong> {product}</p>
                    <p><strong>Quantity:</strong> {quantity} Meters</p>
                    <p><strong>Location:</strong> {location}</p>
                </div>
                """
                
                params = {
                    "from": "onboarding@resend.dev",
                    "to": [TARGET_EMAIL],
                    "subject": f"Order: {name} - {quantity}m",
                    "html": html_content
                }
                
                resend.Emails.send(params)
                st.success("Order submitted successfully.")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
