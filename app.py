import streamlit as st
import resend
import os

# ==========================================
# PAGE SETUP & STYLING
# ==========================================
st.set_page_config(page_title="Flex Pipe | Order", layout="centered")

st.markdown("""
    <style>
    /* Page Background */
    .stApp {
        background-color: #f4f7f6;
    }
    
    /* Form Container */
    div[data-testid="stForm"] {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        border-top: 4px solid #0056b3; /* Flex Pipe Blue */
    }
    
    /* Headings */
    h3 {
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }
    
    /* Input Fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 6px !important;
        border: 1px solid #d1d5db !important;
    }
    
    /* Submit Button */
    .stButton>button {
        width: 100%;
        background-color: #0056b3;
        color: white;
        height: 48px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        transition: background-color 0.3s ease;
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
if os.path.exists("logo.png"):
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image("logo.png", use_container_width=True)

st.markdown("<h3 style='text-align: center;'>Client Order Form</h3>", unsafe_allow_html=True)

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
# PRODUCTS LIST
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
# ORDER FORM WITH SEARCH BAR
# ==========================================
with st.form("order_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name")
    with col2:
        phone = st.text_input("Phone")
    
    # Search Bar and Selectbox
    st.markdown("**Search & Select Product**")
    search_query = st.text_input("Type to search (e.g., 110MM, PN 16)", placeholder="Search product here...")
    
    # Filter products based on search query
    if search_query:
        filtered_products = [p for p in PRODUCTS if search_query.upper() in p.upper()]
        if not filtered_products:
            st.warning("No products found for this search.")
            filtered_products = PRODUCTS # Fallback to show all if nothing matches
    else:
        filtered_products = PRODUCTS

    # Product Selectbox
    product = st.selectbox("Select Product", filtered_products)
    
    col3, col4 = st.columns(2)
    with col3:
        quantity = st.number_input("Quantity (RFT)", min_value=1, step=1)
    with col4:
        location = st.text_input("Location")
    
    submit = st.form_submit_button("Submit Order")

# ==========================================
# EMAIL SENDING LOGIC
# ==========================================
if submit:
    if not name.strip() or not phone.strip() or not location.strip():
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Processing..."):
            try:
                html_content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px; border-top: 4px solid #0056b3;">
                    <h3 style="color: #0056b3;">New Order Received</h3>
                    <hr>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Phone:</strong> {phone}</p>
                    <p><strong>Product:</strong> {product}</p>
                    <p><strong>Quantity:</strong> {quantity} RFT</p>
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
