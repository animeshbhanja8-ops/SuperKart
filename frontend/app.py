# ==============================================================================
# STREAMLIT FRONTEND APPLICATION FOR SUPERKART SALES PREDICTION
# ==============================================================================

# Import Streamlit for building the interactive web UI
import streamlit as st
# Import requests to communicate with the Flask backend API
import requests

# Set up Streamlit page configuration
st.set_page_config(
    page_title="SuperKart Sales Predictor",
    page_icon="🛒",
    layout="centered"
)

# App Title and Description
st.title("🛒 SuperKart Sales Prediction App")
st.markdown("Provide the product and store details below to predict expected sales revenue.")

# Define the API endpoint URL
# Note: When running inside Docker Compose or a Docker network, 'backend' resolves to the backend container.
API_URL = "http://backend:7860/predict"

# Create a form layout for user inputs matching the SuperKart dataset features
with st.form("prediction_form"):
    st.subheader("📋 Product & Store Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_mrp = st.number_input("Product MRP ($)", min_value=0.0, max_value=500.0, value=150.0, step=0.1)
        product_allocated_area = st.number_input("Product Allocated Area", min_value=0.0, max_value=1000.0, value=50.0, step=1.0)
        outlet_establishment_year = st.number_input("Outlet Establishment Year", min_value=1900, max_value=2026, value=2010, step=1)
        
    with col2:
        outlet_size = st.selectbox("Outlet Size", ["Small", "Medium", "High"])
        outlet_location_type = st.selectbox("Outlet Location Type", ["Tier 1", "Tier 2", "Tier 3"])
        outlet_type = st.selectbox("Outlet Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Grocery Store"])

    # Submit button for the form
    submit_button = st.form_submit_button(label="Predict Sales")

# Handle form submission and API call
if submit_button:
    # Construct payload dictionary mapping to training features
    input_data = {
        "Product_MRP": product_mrp,
        "Product_Allocated_Area": product_allocated_area,
        "Outlet_Establishment_Year": outlet_establishment_year,
        "Outlet_Size": outlet_size,
        "Outlet_Location_Type": outlet_location_type,
        "Outlet_Type": outlet_type
    }
    
    try:
        # Send POST request to the Flask backend API
        with st.spinner("Connecting to backend and generating prediction..."):
            response = requests.post(API_URL, json=input_data, timeout=10)
            
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                predicted_sales = result["predictions"][0]
                st.success("🎉 Prediction Successful!")
                st.metric(label="Predicted Sales Revenue", value=f"${predicted_sales:,.2f}")
            else:
                st.error(f"❌ Backend Error: {result.get('error')}")
        else:
            st.error(f"❌ Failed to connect to backend. Status Code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Connection Error: Could not reach the Flask backend. Ensure both containers are running on the same Docker network.")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
