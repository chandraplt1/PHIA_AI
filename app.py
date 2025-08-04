import streamlit as st
import random
import time

# Set page config
st.set_page_config(
    page_title="PhiaAI - Secondhand Fashion Assistant",
    page_icon="👜",
    layout="wide",
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6F61;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        font-weight: 600;
        color: #333;
        margin-top: 2rem;
    }
    .result-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        border-left: 5px solid #FF6F61;
    }
    .confidence-high {
        color: #28a745;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .confidence-low {
        color: #dc3545;
        font-weight: bold;
    }
    .trend-up {
        color: #28a745;
        font-weight: bold;
    }
    .trend-stable {
        color: #6c757d;
        font-weight: bold;
    }
    .trend-down {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>PhiaAI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Your AI Assistant for Secondhand Fashion</p>", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Authenticity Estimation", "Styling Suggestions", "Resale Value"])

# Mock knowledge base for authenticity checks
authenticity_db = {
    "chanel": {
        "classic flap bag": {
            "key_features": "Quilted pattern, interlocking CC logo, chain strap with leather woven through, burgundy interior",
            "common_fakes": "Misaligned quilting, poor quality hardware, wrong font on serial number, incorrect chain length"
        },
        "boy bag": {
            "key_features": "Boxy shape, bold hardware, chevron or diamond quilting, statement clasp",
            "common_fakes": "Incorrect dimensions, low-quality leather, lightweight hardware, wrong interior stamp"
        }
    },
    "louis vuitton": {
        "neverfull": {
            "key_features": "Monogram canvas, structured base, parallel stitching, date code stamp",
            "common_fakes": "Uneven printing, incorrect hardware color, poor alignment of monogram pattern"
        },
        "speedy": {
            "key_features": "Rounded handles, lock and key, heat-stamped logo, specific date code format",
            "common_fakes": "Incorrect handle patina, poor zipper quality, misaligned patterns, wrong interior material"
        }
    },
    "gucci": {
        "dionysus": {
            "key_features": "Tiger head closure, sliding chain strap, structured rectangular shape, specific interior pattern",
            "common_fakes": "Low-quality hardware, incorrect interior lining, wrong dimensions, poor stitching"
        },
        "marmont": {
            "key_features": "Double G hardware, chevron pattern, antique gold-toned hardware, specific interior stamp",
            "common_fakes": "Incorrect hardware color, wrong leather texture, improper GG alignment, incorrect dimensions"
        },
        "blazer": {
            "key_features": "Distinctive buttons, high-quality wool, perfect alignment of patterns, specific label format",
            "common_fakes": "Poor button quality, synthetic fabric blend, uneven stitching, incorrect label font"
        }
    }
}

# Mock styling suggestions database
styling_suggestions = {
    "chanel flap bag": [
        "Pair with high-waisted jeans, white blouse and kitten heels for a classic brunch look",
        "Layer over a little black dress with statement earrings for elegant evening occasions",
        "Contrast with an oversized blazer, slim turtleneck and straight-leg trousers for office chic"
    ],
    "gucci blazer": [
        "Style with distressed denim, a simple white tee, and statement sneakers for an elevated casual look",
        "Layer over a silk slip dress with heeled ankle boots for a dinner date outfit with edge",
        "Pair with matching wide-leg trousers, a fine knit top, and loafers for an updated power suit vibe"
    ],
    "louis vuitton neverfull": [
        "Perfect for a business casual look with tailored trousers, ballet flats and a silk blouse",
        "Makes a great weekend bag paired with boyfriend jeans, oversized sunglasses and a trench coat",
        "Use as a chic carry-on with a monochromatic travel outfit and comfortable luxe sneakers"
    ]
}

# Mock resale value database with trends
resale_values = {
    "chanel": {
        "classic flap bag": {
            "excellent": {"value": 5500, "trend": "up"},
            "very good": {"value": 4800, "trend": "up"},
            "good": {"value": 4200, "trend": "stable"}
        },
        "boy bag": {
            "excellent": {"value": 4200, "trend": "stable"},
            "very good": {"value": 3800, "trend": "stable"},
            "good": {"value": 3200, "trend": "down"}
        }
    },
    "louis vuitton": {
        "neverfull": {
            "excellent": {"value": 1500, "trend": "stable"},
            "very good": {"value": 1200, "trend": "stable"},
            "good": {"value": 900, "trend": "down"}
        },
        "speedy": {
            "excellent": {"value": 1100, "trend": "down"},
            "very good": {"value": 900, "trend": "down"},
            "good": {"value": 700, "trend": "down"}
        }
    },
    "gucci": {
        "dionysus": {
            "excellent": {"value": 1800, "trend": "up"},
            "very good": {"value": 1500, "trend": "stable"},
            "good": {"value": 1200, "trend": "down"}
        },
        "marmont": {
            "excellent": {"value": 1400, "trend": "down"},
            "very good": {"value": 1100, "trend": "down"},
            "good": {"value": 800, "trend": "down"}
        },
        "blazer": {
            "excellent": {"value": 1200, "trend": "stable"},
            "very good": {"value": 900, "trend": "stable"},
            "good": {"value": 600, "trend": "stable"}
        }
    }
}

# Helper functions
def generate_authenticity_score(brand, item_name, description, condition):
    """Generate a mock authenticity score and reasoning based on the provided details"""
    
    # Normalize inputs for lookup
    brand = brand.lower()
    item_name = item_name.lower()
    
    # Extract key words from the item name to match with our database
    key_words = item_name.split()
    matched_item = None
    
    # Try to find a matching item in our database
    if brand in authenticity_db:
        for db_item in authenticity_db[brand]:
            for word in key_words:
                if word in db_item and len(word) > 2:  # Avoid matching on short words like "of", "a", etc.
                    matched_item = db_item
                    break
            if matched_item:
                break
    
    # If we found a match, analyze based on that item's known features
    if matched_item and brand in authenticity_db:
        key_features = authenticity_db[brand][matched_item]["key_features"]
        common_fakes = authenticity_db[brand][matched_item]["common_fakes"]
        
        # Check description for key features mentioned
        features_found = 0
        for feature in key_features.split(", "):
            if feature.lower() in description.lower():
                features_found += 1
                
        # Calculate a mock confidence score
        total_features = len(key_features.split(", "))
        if total_features == 0:  # Avoid division by zero
            confidence = random.uniform(0.4, 0.6)
        else:
            confidence = min(0.5 + (features_found / total_features * 0.5), 0.95)
            
        # Add some randomness to make it realistic
        confidence = min(max(confidence + random.uniform(-0.1, 0.1), 0.1), 0.99)
        
        # Create response
        if confidence > 0.7:
            confidence_level = "high"
            confidence_text = f"<span class='confidence-high'>{confidence:.0%}</span>"
            reasoning = f"""
            Based on the provided details, I have high confidence this item is likely authentic because:
            - The description matches several key authenticating features of a genuine {brand.title()} {matched_item}
            - The mentioned "{', '.join(key_features.split(', ')[:2])}" align with authentic product specifications
            - No obvious red flags that would indicate a counterfeit
            
            Key authenticating features for this item include: {key_features}
            """
        elif confidence > 0.4:
            confidence_level = "medium"
            confidence_text = f"<span class='confidence-medium'>{confidence:.0%}</span>"
            reasoning = f"""
            Based on the provided details, I have moderate confidence in this item's authenticity:
            - Some key features match authentic {brand.title()} {matched_item}s
            - More detailed photos of {', '.join(key_features.split(', ')[:2])} would help confirm authenticity
            - Would recommend checking {random.choice(key_features.split(', '))} more closely
            
            Common counterfeits often have issues with: {common_fakes}
            """
        else:
            confidence_level = "low"
            confidence_text = f"<span class='confidence-low'>{confidence:.0%}</span>"
            reasoning = f"""
            I have low confidence in this item's authenticity due to:
            - Limited details provided match known authentic features
            - Several key authenticating elements are not mentioned or verifiable
            - Recommend professional authentication before purchasing
            
            Key concerns: Cannot verify {', '.join(key_features.split(', ')[:3])}
            """
    else:
        # If no match found, provide a generic response
        confidence = random.uniform(0.3, 0.5)
        confidence_level = "medium"
        confidence_text = f"<span class='confidence-medium'>{confidence:.0%}</span>"
        reasoning = f"""
        I have limited information about this specific {brand.title()} item in my database.
        
        For a more accurate authentication assessment:
        - Request clear photos of logos, hardware, and any serial numbers
        - Ask for detailed close-ups of stitching and materials
        - Consider professional authentication services for high-value items
        
        General authentication tips for {brand.title()}:
        - Check quality of materials and craftsmanship
        - Verify serial numbers with the brand if possible
        - Examine logo placement and hardware quality
        """
    
    return confidence_text, reasoning, confidence_level

def generate_styling_suggestions(item_name, context=""):
    """Generate styling suggestions based on the item and optional context"""
    
    # Normalize input
    item_name = item_name.lower()
    
    # Try to find matching item in our suggestions database
    matched_item = None
    for db_item in styling_suggestions:
        if any(word in item_name for word in db_item.split() if len(word) > 2):
            matched_item = db_item
            break
    
    # If we found a match, return those suggestions
    if matched_item:
        suggestions = styling_suggestions[matched_item].copy()
        
        # If context is provided, try to tailor the suggestions
        if context:
            context = context.lower()
            
            # Check for season mentions
            if any(season in context for season in ["spring", "summer"]):
                suggestions.append(f"For warm weather, pair your {matched_item} with linen shorts, a lightweight blouse and strappy sandals")
            elif any(season in context for season in ["fall", "autumn", "winter"]):
                suggestions.append(f"For colder days, style your {matched_item} with a chunky knit sweater, wool coat and knee-high boots")
            
            # Check for occasion mentions
            if any(occasion in context for occasion in ["work", "office", "business"]):
                suggestions.append(f"For a professional setting, your {matched_item} works beautifully with a tailored pencil skirt, silk blouse and pointed toe pumps")
            elif any(occasion in context for occasion in ["date", "dinner", "evening"]):
                suggestions.append(f"For your {context}, pair the {matched_item} with a sleek midi dress, statement earrings and strappy heels for an elegant look")
            elif any(occasion in context for occasion in ["casual", "weekend", "brunch"]):
                suggestions.append(f"For a relaxed {context} vibe, style your {matched_item} with premium denim, a cashmere tee and designer sneakers")
            
        # Return 3 suggestions (either from original set or with context-specific ones included)
        return random.sample(suggestions, min(3, len(suggestions)))
    
    # If no exact match, generate generic suggestions based on item type
    item_type = ""
    for word in item_name.split():
        if word in ["bag", "purse", "handbag", "tote", "clutch", "backpack", "satchel"]:
            item_type = "bag"
            break
        elif word in ["jacket", "blazer", "coat", "cardigan"]:
            item_type = "outerwear"
            break
        elif word in ["dress", "gown", "frock"]:
            item_type = "dress"
            break
        elif word in ["shoe", "shoes", "heel", "heels", "boot", "boots", "sneaker", "sneakers"]:
            item_type = "shoes"
            break
    
    # Default generic suggestions based on item type
    generic_suggestions = {
        "bag": [
            f"Style your {item_name} with a monochromatic outfit to let the bag be the focal point",
            f"For casual outings, pair your {item_name} with premium denim, a crisp white tee, and minimal jewelry",
            f"Create an elegant evening look by carrying your {item_name} with a little black dress and statement heels"
        ],
        "outerwear": [
            f"Layer your {item_name} over a silk slip dress with ankle boots for an elegant day-to-night transition",
            f"For a casual look, pair your {item_name} with a white tee, straight-leg jeans, and loafers",
            f"Create contrast by styling your structured {item_name} with relaxed wide-leg pants and a fitted top"
        ],
        "dress": [
            f"Elevate your {item_name} with architectural heels and a structured designer handbag",
            f"For cooler weather, layer your {item_name} with a tailored blazer and knee-high boots",
            f"Keep it minimal with your {item_name} by adding just delicate jewelry and simple sandals"
        ],
        "shoes": [
            f"Build an outfit around your {item_name} with neutral tones that highlight the footwear",
            f"Balance the look by pairing statement {item_name} with minimalist clothing pieces",
            f"For an unexpected twist, style your {item_name} with contrasting patterns in complementary colors"
        ],
        "": [
            f"Create a monochromatic outfit incorporating your {item_name} for a sophisticated look",
            f"Balance your {item_name} with pieces of contrasting structure or texture",
            f"Use your {item_name} as a statement piece with minimal accessories for maximum impact"
        ]
    }
    
    return generic_suggestions.get(item_type, generic_suggestions[""])

def generate_resale_value(brand, item_name, condition):
    """Generate a mock resale value and trend based on the provided details"""
    
    # Normalize inputs
    brand = brand.lower()
    item_name = item_name.lower()
    condition = condition.lower()
    
    # Map user-input condition to our condition categories
    if "excellent" in condition or "mint" in condition or "new" in condition:
        condition_category = "excellent"
    elif "very good" in condition or "great" in condition:
        condition_category = "very good"
    else:
        condition_category = "good"
        
    # Try to find matching item in our resale database
    if brand in resale_values:
        matched_item = None
        for db_item in resale_values[brand]:
            if any(word in item_name for word in db_item.split() if len(word) > 2):
                matched_item = db_item
                break
                
        if matched_item:
            value_data = resale_values[brand][matched_item][condition_category]
            value = value_data["value"]
            trend = value_data["trend"]
            
            # Add some randomness to the value
            value = int(value * random.uniform(0.9, 1.1))
            
            # Create explanations based on trend
            if trend == "up":
                trend_symbol = "↑"
                trend_class = "trend-up"
                explanation = f"The resale market for {brand.title()} {matched_item} is currently trending upward. Limited availability and sustained demand from collectors are driving prices higher than retail in some cases."
            elif trend == "stable":
                trend_symbol = "→"
                trend_class = "trend-stable"
                explanation = f"The {brand.title()} {matched_item} holds its value well in the resale market. These pieces tend to remain stable investments over time with minimal depreciation."
            else:  # trend == "down"
                trend_symbol = "↓"
                trend_class = "trend-down"
                explanation = f"The market for {brand.title()} {matched_item} is currently experiencing a downward trend. This may be due to changing trends or increased availability of similar styles."
                
            # Format value with commas
            formatted_value = f"${value:,}"
            trend_display = f"<span class='{trend_class}'>{trend_symbol}</span>"
            
            return formatted_value, trend_display, explanation, trend_class
    
    # If no match found, generate a generic estimate
    # Base values by brand tier
    luxury_tiers = {
        "hermes": {"base": 5000, "range": 15000},
        "chanel": {"base": 2500, "range": 5000},
        "louis vuitton": {"base": 1000, "range": 2000},
        "dior": {"base": 1500, "range": 3000},
        "gucci": {"base": 800, "range": 1500},
        "prada": {"base": 700, "range": 1300}
    }
    
    # Default for brands not in our list
    default_tier = {"base": 300, "range": 700}
    
    # Get base values for this brand
    brand_values = luxury_tiers.get(brand, default_tier)
    base_value = brand_values["base"]
    value_range = brand_values["range"]
    
    # Adjust for condition
    if condition_category == "excellent":
        condition_multiplier = 1.0
    elif condition_category == "very good":
        condition_multiplier = 0.8
    else:
        condition_multiplier = 0.6
        
    # Calculate value
    value = int((base_value + random.uniform(0, value_range)) * condition_multiplier)
    
    # Randomly select trend for generic items
    trend_options = ["up", "stable", "down"]
    trend_weights = [0.3, 0.5, 0.2]  # More likely to be stable
    trend = random.choices(trend_options, weights=trend_weights, k=1)[0]
    
    # Format response
    if trend == "up":
        trend_symbol = "↑"
        trend_class = "trend-up"
        explanation = f"Based on similar {brand.title()} items, this piece appears to be appreciating in value. Limited availability and growing interest in vintage {brand.title()} are contributing factors."
    elif trend == "stable":
        trend_symbol = "→"
        trend_class = "trend-stable"
        explanation = f"This {brand.title()} item seems to maintain consistent value in the secondhand market. The classic design and brand reputation help preserve its worth."
    else:  # trend == "down"
        trend_symbol = "↓"
        trend_class = "trend-down"
        explanation = f"Similar {brand.title()} items have been declining slightly in resale value. This may be due to changing fashion trends or increased market availability."
        
    # Format value with commas
    formatted_value = f"${value:,}"
    trend_display = f"<span class='{trend_class}'>{trend_symbol}</span>"
    
    return formatted_value, trend_display, explanation, trend_class

# Tab 1: Authenticity Estimation
with tab1:
    st.markdown("<h2 class='subheader'>Authenticity Estimation</h2>", unsafe_allow_html=True)
    st.markdown("Estimate the authenticity of a secondhand fashion item based on product details.")
    
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
        
        description = st.text_area(
            "Product Description", 
            placeholder="e.g., Black lambskin, gold hardware, chain strap with leather woven through, burgundy interior"
        )
        
        submit_authenticity = st.form_submit_button("Estimate Authenticity")
    
    # Display results when form is submitted
    if submit_authenticity and product_title and brand and description:
        with st.spinner("Analyzing authenticity..."):
            # Simulate processing time
            time.sleep(1.5)
            
            # Generate authenticity assessment
            confidence_text, reasoning, confidence_level = generate_authenticity_score(
                brand, product_title, description, condition
            )
            
            # Display results
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.markdown(f"### Authenticity Confidence: {confidence_text}", unsafe_allow_html=True)
            st.markdown(reasoning)
            st.markdown("</div>", unsafe_allow_html=True)
    elif submit_authenticity:
        st.warning("Please fill out all required fields.")

# Tab 2: Styling Suggestions
with tab2:
    st.markdown("<h2 class='subheader'>Styling Suggestions</h2>", unsafe_allow_html=True)
    st.markdown("Get creative outfit ideas and styling tips for your fashion item.")
    
    # Form inputs
    with st.form("styling_form"):
        item_name = st.text_input("Item Name", placeholder="e.g., Gucci Blazer")
        context = st.text_input("Optional Context", placeholder="e.g., Fall season, business casual, date night")
        
        submit_styling = st.form_submit_button("Get Styling Ideas")
    
    # Display results when form is submitted
    if submit_styling and item_name:
        with st.spinner("Generating styling suggestions..."):
            # Simulate processing time
            time.sleep(1.5)
            
            # Generate styling suggestions
            suggestions = generate_styling_suggestions(item_name, context)
            
            # Display results
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.markdown(f"### Styling Ideas for your {item_name}")
            
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"**Look {i}:** {suggestion}")
                
            st.markdown("</div>", unsafe_allow_html=True)
    elif submit_styling:
        st.warning("Please enter an item name.")

# Tab 3: Resale Value
with tab3:
    st.markdown("<h2 class='subheader'>Resale Value Insights</h2>", unsafe_allow_html=True)
    st.markdown("Get estimated resale value and market trends for your luxury item.")
    
    # Form inputs
    with st.form("resale_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            resale_item_name = st.text_input("Item Name", placeholder="e.g., Classic Flap Bag", key="resale_item")
            resale_brand = st.text_input("Brand", placeholder="e.g., Chanel", key="resale_brand")
        
        with col2:
            resale_condition = st.selectbox(
                "Condition",
                ["New with Tags", "Excellent", "Very Good", "Good", "Fair", "Poor"],
                key="resale_condition"
            )
        
        submit_resale = st.form_submit_button("Get Resale Value")
    
    # Display results when form is submitted
    if submit_resale and resale_item_name and resale_brand:
        with st.spinner("Analyzing market value..."):
            # Simulate processing time
            time.sleep(1.5)
            
            # Generate resale value estimate
            value, trend_symbol, explanation, trend_class = generate_resale_value(
                resale_brand, resale_item_name, resale_condition
            )
            
            # Display results
            st.markdown("<div class='result-box'>", unsafe_allow_html=True)
            st.markdown(f"### Estimated Resale Value: {value} {trend_symbol}", unsafe_allow_html=True)
            st.markdown(explanation)
            
            # Add market tips based on trend
            st.markdown("#### Market Tips")
            
            if trend_class == "trend-up":
                st.markdown("- Consider holding this item if you're not in a rush to sell, as its value may continue to increase")
                st.markdown("- Research current listings to set a competitive but premium price point")
                st.markdown("- Highlight the investment potential in your listing description")
            elif trend_class == "trend-stable":
                st.markdown("- This item has consistent demand and holds its value well")
                st.markdown("- Focus on highlighting condition and authenticity in your listing")
                st.markdown("- Standard pricing strategies apply; research comparable recent sales")
            else:  # trend_class == "trend-down"
                st.markdown("- Consider selling sooner rather than later if you plan to part with this item")
                st.markdown("- Focus marketing on the item's versatility and timeless qualities rather than investment potential")
                st.markdown("- Competitive pricing is key; research recent comparable sales carefully")
            
            st.markdown("</div>", unsafe_allow_html=True)
    elif submit_resale:
        st.warning("Please fill out all required fields.")