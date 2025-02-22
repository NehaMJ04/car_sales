from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os

# Use non-GUI backend for Matplotlib (important for Render)
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
CORS(app)  # Allow requests from Flutter

# Load dataset with error handling
try:
    car_details = pd.read_csv("car_details_df.csv")
    price_cardetails = pd.read_csv("price_cardetails_df.csv")
except Exception as e:
    print(f"Error loading datasets: {e}")
    car_details = pd.DataFrame()  # Empty DataFrame if loading fails
    price_cardetails = pd.DataFrame()

@app.route('/')
def home():
    return jsonify({"message": "Flask API for Car Analysis is running!"})

# 1️⃣ API: Get Most Common Car Brands
@app.route('/top-brands', methods=['GET'])
def top_brands():
    if 'Brand' in car_details:
        return jsonify(car_details['Brand'].value_counts().head(5).to_dict())
    return jsonify({"error": "Brand column missing"}), 500

# 2️⃣ API: Get Car Models for a Brand
@app.route('/brand-models', methods=['GET'])
def brand_models():
    brand = request.args.get('brand', '')
    if 'Brand' in car_details and 'Model' in car_details:
        return jsonify(car_details[car_details['Brand'] == brand]['Model'].unique().tolist())
    return jsonify({"error": "Brand or Model column missing"}), 500

# 3️⃣ API: Get Popular Brand by Location
@app.route('/popular-brand-location', methods=['GET'])
def popular_brand_location():
    location = request.args.get('location', '')
    if 'Location' in car_details and 'Brand' in car_details:
        return jsonify(car_details[car_details['Location'] == location]['Brand'].value_counts().head(1).to_dict())
    return jsonify({"error": "Location or Brand column missing"}), 500

# 4️⃣ API: Get Average Mileage per Fuel Type
@app.route('/avg-mileage', methods=['GET'])
def avg_mileage():
    if 'Fuel_Type' in car_details and 'Mileage_km' in car_details:
        return jsonify(car_details.groupby('Fuel_Type')['Mileage_km'].mean().to_dict())
    return jsonify({"error": "Fuel_Type or Mileage_km column missing"}), 500

# ✅ FIXED GRAPH API
@app.route('/price-histogram', methods=['GET'])
def price_histogram():
    try:
        # Ensure 'Price' column exists and is not empty
        if 'Price' not in price_cardetails or price_cardetails['Price'].isnull().all():
            return jsonify({"error": "Price data is missing or invalid"}), 500

        plt.figure(figsize=(6, 4))
        sns.histplot(price_cardetails['Price'].dropna(), bins=20, kde=True, color='blue')  # Drop NaN values
        plt.xlabel("Price")
        plt.ylabel("Frequency")
        plt.title("Price Distribution")
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return jsonify({"graph": f"data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Send error message

# ✅ FIXED: Handle Missing Insurance Cost Column
@app.route('/insurance-cost', methods=['GET'])
def insurance_cost():
    if 'Insurance_Cost' not in price_cardetails:
        return jsonify({"error": "Insurance_Cost column missing"}), 500  # Return error message

    return jsonify(price_cardetails.groupby('Brand')['Insurance_Cost'].mean().to_dict())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render assigns a dynamic port
    app.run(host="0.0.0.0", port=port, debug=False)
