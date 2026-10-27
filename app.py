import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# PAGE SETUP & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="Flex Head | Order Portal", page_icon="🏭", layout="centered")

st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Form Container Styling */
    div[data-testid="stForm"] {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-top: 5px solid #0b1220;
    }
    
    /* Headings */
    h1 {
        color: #0b1220;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
    }
    h3 {
        color: #475569;
        text-align: center;
        font-weight: 400;
        margin-bottom: 30px;
    }
    
    /* Input Fields */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 10px !important;
    }
    
    /* Submit Button */
    .stButton>button {
        width: 100%;
        background-color: #28a745;
        color: white;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #218838;
        color: white;
        box-shadow: 0 4px 8px rgba(40, 167, 69, 0.3);
    }
    
    /* Success Message */
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-radius: 8px;
        padding: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown("<h1>🏭 FLEX HEAD INDUSTRIES</h1>", unsafe_allow_html=True)
st.markdown("<h3>B2B Online Pipe Ordering Portal</h3>", unsafe_allow_html=True)

# ==========================================
# SECRETS SETUP
# ==========================================
try:
    EMAIL_SENDER = st.secrets["EMAIL_SENDER"]
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
    EMAIL_RECEIVER = st.secrets["EMAIL_RECEIVER"]
except Exception:
    st.error("⚠️ Secrets missing! Please configure secrets.toml (EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER)")
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
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("🚀 Send Order Request")

# ==========================================
# EMAIL SENDING LOGIC
# ==========================================
if submit:
    if not name.strip() or not phone.strip():
        st.warning("⚠️ Please fill in all required fields (Name and Phone).")
    else:
        with st.spinner("Sending your order to our sales team..."):
            try:
                # HTML Email Body
                html_content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
                    <div style="background-color: #0b1220; color: white; padding: 20px; text-align: center;">
                        <h2 style="margin: 0;">New Pipe Order Received</h2>
                    </div>
                    <div style="padding: 20px; background-color: #f9f9f9;">
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Customer Name:</strong></td>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Phone Number:</strong></td>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{phone}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Product:</strong></td>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{product}</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Quantity:</strong></td>
                                <td style="padding: 10px; border-bottom: 1px solid #ddd;">{quantity} Meters</td>
                            </tr>
                        </table>
                    </div>
                    <div style="background-color: #eee; padding: 10px; text-align: center; font-size: 12px; color: #666;">
                        This order was placed via the Flex Head Client Portal.
                    </div>
                </div>
                """

                # MIME Setup
                msg = MIMEMultipart()
                msg['From'] = EMAIL_SENDER
                msg['To'] = EMAIL_RECEIVER
                msg['Subject'] = f"🚨 New Order: {name} - {quantity}m"
                msg.attach(MIMEText(html_content, 'html'))

                # Send via Gmail SMTP
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
                
                st.success(f"✅ Thank you {name}! Aapka order kamyabi se bhej diya gaya hai. Humari team jald aapse rabta karegi.")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Email bhejne mein masla aaya. Please try again later. (Error: {str(e)})")
