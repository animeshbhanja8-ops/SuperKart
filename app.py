# ==============================================================================
# FLASK BACKEND APPLICATION FOR SUPERKART SALES PREDICTION
# ==============================================================================

# Import Flask web framework modules for handling requests and JSON responses
from flask import Flask, request, jsonify
# Import joblib to load the serialized machine learning model pipeline
import joblib
# Import pandas to process incoming JSON payloads into a DataFrame format
import pandas as pd
# Import os to check for model file existence
import os

# Initialize the Flask application instance
# We alias 'app' and 'house_price_api' to match standard Gunicorn configuration expectations
app = Flask(__name__)
house_price_api = app

# Define the file path for the serialized machine learning model inside backend_files
model_path = "superkart_model.joblib"

# Load the trained model pipeline into memory when the server starts
if os.path.exists(model_path):
    model = joblib.load(model_path)
    print("✅ SuperKart model loaded successfully into Flask backend.")
else:
    model = None
    print("❌ Warning: Model file not found at the specified path!")

# Define root health-check endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "SuperKart Sales Prediction Backend API is running successfully!"
    })

# Define prediction endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Extract JSON data from the incoming HTTP request
        json_data = request.get_json(force=True)
        
        # Convert JSON object or list of objects into a pandas DataFrame
        input_df = pd.DataFrame([json_data] if isinstance(json_data, dict) else json_data)
        
        # Generate sales predictions using the loaded pipeline (preprocessing + model)
        predictions = model.predict(input_df)
        
        # Return predictions as a formatted JSON response
        return jsonify({
            "success": True,
            "predictions": predictions.tolist()
        })
        
    except Exception as e:
        # Return error message if prediction fails
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# Run the Flask app locally if executed directly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)
