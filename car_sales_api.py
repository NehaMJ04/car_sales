from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)
CORS(app)  # Allow requests from Flutter

# Load dataset
car_details = pd.read_csv("car_details_df.csv")
price_cardetails = pd.read_csv("price_cardetails_df.csv")

@app.route('/')
def home():
    return jsonify({"message": "Flask API for Car Analysis is running!"})

# 1️⃣ API: Get Most Common Car Brands
@app.route('/top-brands', methods=['GET'])
def top_brands():
    return jsonify(car_details['Brand'].value_counts().head(5).to_dict())

# 2️⃣ API: Get Car Models for a Brand
@app.route('/brand-models', methods=['GET'])
def brand_models():
    brand = request.args.get('brand', '')
    return jsonify(car_details[car_details['Brand'] == brand]['Model'].unique().tolist())

# 3️⃣ API: Get Popular Brand by Location
@app.route('/popular-brand-location', methods=['GET'])
def popular_brand_location():
    location = request.args.get('location', '')
    return jsonify(car_details[car_details['Location'] == location]['Brand'].value_counts().head(1).to_dict())

# 4️⃣ API: Get Average Mileage per Fuel Type
@app.route('/avg-mileage', methods=['GET'])
def avg_mileage():
    return jsonify(car_details.groupby('Fuel_Type')['Mileage_km'].mean().to_dict())

# 5️⃣ API: Get Transmission Types by Brand
@app.route('/brand-transmission', methods=['GET'])
def brand_transmission():
    brand = request.args.get('brand', '')
    return jsonify(car_details[car_details['Brand'] == brand]['Transmission'].unique().tolist())

# 6️⃣ API: Get Statistical Summary of Price Data
@app.route('/price-summary', methods=['GET'])
def price_summary():
    return jsonify(price_cardetails.describe().to_dict())

# 7️⃣ API: Get Most Common Transmission Type in Recent Years
@app.route('/recent-transmission', methods=['GET'])
def recent_transmission():
    return jsonify(car_details[car_details['Year'] >= 2020]['Transmission'].value_counts().to_dict())

# 8️⃣ API: Get Price Analysis (Min, Max, Average Price by Brand)
@app.route('/price-analysis', methods=['GET'])
def price_analysis():
    return jsonify(price_cardetails.groupby('Brand')['Price'].agg(['min', 'max', 'mean']).to_dict())

# 9️⃣ API: Get Count of Cars by Fuel Type
@app.route('/fuel-count', methods=['GET'])
def fuel_count():
    return jsonify(car_details['Fuel_Type'].value_counts().to_dict())

# 🔟 API: Get Correlation Between Car Age and Price
@app.route('/age-price-correlation', methods=['GET'])
def age_price_correlation():
    car_details['Car_Age'] = 2024 - car_details['Year']
    return jsonify(car_details[['Car_Age', 'Price']].corr().to_dict())

# 11️⃣ API: Get Most Expensive Car Models
@app.route('/expensive-models', methods=['GET'])
def expensive_models():
    return jsonify(price_cardetails.groupby('Model')['Price'].mean().sort_values(ascending=False).head(10).to_dict())

# 12️⃣ API: Get Top Locations with Most Cars Listed
@app.route('/top-locations', methods=['GET'])
def top_locations():
    return jsonify(car_details['Location'].value_counts().head(10).to_dict())

# 13️⃣ API: Get Common Price Range for Each Car Model
@app.route('/common-price-range', methods=['GET'])
def common_price_range():
    return jsonify(price_cardetails.groupby("Model")["Price"].describe().to_dict())

# 14️⃣ API: Get Most Popular Car Colors
@app.route('/popular-colors', methods=['GET'])
def popular_colors():
    return jsonify(car_details['Color'].value_counts().to_dict())

# 15️⃣ API: Get Engine Size vs Average Price
@app.route('/engine-price', methods=['GET'])
def engine_price():
    return jsonify(price_cardetails.groupby("Engine_cc")["Price"].mean().to_dict())

# 16️⃣ API: Get Resale Value by Brand
@app.route('/resale-value', methods=['GET'])
def resale_value():
    return jsonify(price_cardetails.groupby('Brand')['Price'].median().sort_values(ascending=False).to_dict())

# 17️⃣ API: Get Most Popular Car Features
@app.route('/popular-features', methods=['GET'])
def popular_features():
    return jsonify(car_details['Features'].value_counts().to_dict())

# 18️⃣ API: Get Fuel Efficiency by Engine Size
@app.route('/fuel-efficiency', methods=['GET'])
def fuel_efficiency():
    return jsonify(car_details.groupby('Engine_cc')['Mileage_km'].mean().to_dict())

# 19️⃣ API: Get Average Resale Value by Fuel Type
@app.route('/resale-by-fuel', methods=['GET'])
def resale_by_fuel():
    return jsonify(price_cardetails.groupby('Fuel_Type')['Price'].median().to_dict())

# 20️⃣ API: Get Relationship Between Car Age and Mileage
@app.route('/age-mileage', methods=['GET'])
def age_mileage():
    return jsonify(car_details.groupby('Car_Age')['Mileage_km'].mean().to_dict())

# 21️⃣ API: Get Price Distribution Histogram
@app.route('/price-histogram', methods=['GET'])
def price_histogram():
    plt.figure(figsize=(6, 4))
    sns.histplot(price_cardetails['Price'], bins=20, kde=True, color='blue')
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.title("Price Distribution")
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return jsonify({"graph": f"data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}"})

# 22️⃣ API: Get Car Listings by Year
@app.route('/listings-by-year', methods=['GET'])
def listings_by_year():
    return jsonify(car_details['Year'].value_counts().to_dict())

# 23️⃣ API: Get Car Listings by Owner Type
@app.route('/listings-by-owner', methods=['GET'])
def listings_by_owner():
    return jsonify(car_details['Owner_Type'].value_counts().to_dict())

# 24️⃣ API: Get Most Common Car Body Types
@app.route('/common-body-types', methods=['GET'])
def common_body_types():
    return jsonify(car_details['Body_Type'].value_counts().to_dict())

# 25️⃣ API: Get Average Insurance Cost by Brand
@app.route('/insurance-cost', methods=['GET'])
def insurance_cost():
    return jsonify(price_cardetails.groupby('Brand')['Insurance_Cost'].mean().to_dict())

if __name__ == '__main__':
    app.run(debug=True)
