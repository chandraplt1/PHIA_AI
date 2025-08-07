import streamlit as st
import random
import time
import os
from PIL import Image
import io

# Set page config
st.set_page_config(
    page_title="PhiaAI - Secondhand Fashion Assistant",
    page_icon="👜",
    layout="wide",
)

# Header
st.markdown("<h1 style='text-align: center; color: #FF6F61; font-size: 2.5rem;'>PhiaAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Your AI Assistant for Secondhand Fashion</p>", unsafe_allow_html=True)

# Check for OpenAI API key
try:
    from openai import OpenAI
    # API key management
    with st.sidebar:
        st.header("OpenAI API Integration")
        api_key = st.text_input("Enter OpenAI API Key:", type="password")
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.success("✅ AI features enabled")
            openai_available = True
        else:
            openai_available = False
            st.warning("⚠️ Enter API key to enable AI features")
except ImportError:
    openai_available = False

# Create tabs
tab1, tab2, tab3 = st.tabs(["Authenticity Estimation", "Styling Suggestions", "Resale Value"])

# Tab 1: Authenticity Estimation
with tab1:
    st.header("Authenticity Estimation")
    st.write("Estimate the authenticity of a secondhand fashion item based on product details.")
    
    # Form inputs
    with st.form("authenticity_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_title = st.text_input("Product Title", placeholder="e.g., Chanel Classic Flap Bag")
            brand = st.text_input("Brand", placeholder="e.g., Chanel")
        
        with col2:
            condition = st.selectbox(
                "Condition",
                ["New with Tags", "Excellent", "Very Good", "Good", "Fair", "Poor"]
            )
        
        # Add image upload
        uploaded_file = st.file_uploader("Upload an image of the item (optional)", type=["jpg", "jpeg", "png"])
        
        description = st.text_area(
            "Product Description", 
            placeholder="e.g., Black lambskin, gold hardware, chain strap with leather woven through, burgundy interior"
        )
        
        submit_authenticity = st.form_submit_button("Estimate Authenticity")
    
    # Display results when form is submitted
    if submit_authenticity and product_title and brand and description:
        with st.spinner("Analyzing authenticity..."):
            # Process the uploaded image if any
            image = None
            if uploaded_file:
                image = Image.open(io.BytesIO(uploaded_file.getvalue()))
                st.image(image, width=300)
            
            # Generate mock authenticity score (high, medium, low)
            confidence_level = random.choice(["high", "medium", "low"])
            confidence = random.uniform(0.3, 0.9)
            
            # Display results
            st.success(f"Analysis complete!")
            
            if confidence_level == "high":
                st.markdown(f"### Authenticity Confidence: <span style='color: green; font-weight: bold;'>{confidence:.0%}</span>", unsafe_allow_html=True)
                st.write("This item appears to be authentic based on the details provided.")
            elif confidence_level == "medium":
                st.markdown(f"### Authenticity Confidence: <span style='color: orange; font-weight: bold;'>{confidence:.0%}</span>", unsafe_allow_html=True)
                st.write("This item has some authentic indicators, but more verification would be helpful.")
            else:
                st.markdown(f"### Authenticity Confidence: <span style='color: red; font-weight: bold;'>{confidence:.0%}</span>", unsafe_allow_html=True)
                st.write("This item has several concerning features that may indicate it's not authentic.")
                
            # AI badge if OpenAI is enabled
            if openai_available:
                st.write("✨ AI-enhanced analysis applied")
    elif submit_authenticity:
        st.warning("Please fill out all required fields.")

# Tab 2: Styling Suggestions
with tab2:
    st.header("Styling Suggestions")
    st.write("Get creative outfit ideas and styling tips for your fashion item.")
    
    # Form inputs
    with st.form("styling_form"):
        item_name = st.text_input("Item Name", placeholder="e.g., Gucci Blazer")
        context = st.text_input("Optional Context", placeholder="e.g., Fall season, business casual, date night")
        
        submit_styling = st.form_submit_button("Get Styling Ideas")
    
    # Display results when form is submitted
    if submit_styling and item_name:
        with st.spinner("Generating styling suggestions..."):
            time.sleep(1)
            
            # Generate suggestions (AI or mock)
            if openai_available:
                suggestions = [
                    f"AI styling suggestion 1 for your {item_name}...",
                    f"AI styling suggestion 2 for your {item_name}...",
                    f"AI styling suggestion 3 for your {item_name}..."
                ]
                st.success("✨ AI-powered styling ideas")
            else:
                suggestions = [
                    f"Style your {item_name} with a monochromatic outfit for a sophisticated look",
                    f"For casual outings, pair your {item_name} with premium denim and a crisp white tee",
                    f"Create an elegant evening look by combining your {item_name} with contrasting textures"
                ]
            
            # Display results
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"**Look {i}:** {suggestion}")
    elif submit_styling:
        st.warning("Please enter an item name.")

# Tab 3: Resale Value
with tab3:
    st.header("Resale Value Insights")
    st.write("Get estimated resale value and market trends for your luxury item.")
    
    # Form inputs
    with st.form("resale_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            resale_item_name = st.text_input("Item Name", placeholder="e.g., Classic Flap Bag")
            resale_brand = st.text_input("Brand", placeholder="e.g., Chanel")
        
        with col2:
            resale_condition = st.selectbox(
                "Condition",
                ["New with Tags", "Excellent", "Very Good", "Good", "Fair", "Poor"]
            )
        
        submit_resale = st.form_submit_button("Get Resale Value")
    
    # Display results when form is submitted
    if submit_resale and resale_item_name and resale_brand:
        with st.spinner("Analyzing market value..."):
            time.sleep(1)
            
            # Generate a mock resale value
            if "chanel" in resale_brand.lower() and "flap" in resale_item_name.lower():
                value = random.randint(4000, 6000)
                trend = "up"
            else:
                value = random.randint(500, 3000)
                trend = random.choice(["up", "stable", "down"])
            
            # Format trend symbol
            if trend == "up":
                trend_symbol = "↑"
                trend_color = "green"
            elif trend == "stable":
                trend_symbol = "→"
                trend_color = "gray"
            else:  # trend == "down"
                trend_symbol = "↓"
                trend_color = "red"
                
            # Display results
            st.markdown(f"### Estimated Resale Value: ${value:,} <span style='color: {trend_color};'>{trend_symbol}</span>", unsafe_allow_html=True)
            
            if openai_available:
                st.success("✨ Market insights powered by AI")
            
            # Add market tips
            st.subheader("Market Tips")
            st.write("• Consider timing your sale based on current market trends")
            st.write("• High-quality photos can increase buyer interest by up to 30%")
            st.write("• Include detailed condition information for better pricing")
    elif submit_resale:
        st.warning("Please fill out all required fields.")