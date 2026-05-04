from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # IMPORTANT for Flutter web/mobile

##################################################
# HOME ROUTE (for browser)
##################################################

@app.route("/")
def home():
    return "SafeSense API is running 🚀"

##################################################
# DASHBOARD API
##################################################

@app.route("/api/data")
def get_data():
    return jsonify({
        "temp": 55,
        "risk": "LOW",
        "alerts": 12
    })

##################################################
# PRODUCTS API
##################################################

@app.route("/api/products")
def get_products():
    return jsonify([
        {
            "name": "Temperature Sensor",
            "price": 500,
            "image": "https://via.placeholder.com/150"
        },
        {
            "name": "Electrical Monitoring Kit",
            "price": 1200,
            "image": "https://via.placeholder.com/150"
        },
        {
            "name": "AI Monitoring Software",
            "price": 2000,
            "image": "https://via.placeholder.com/150"
        },
        {
            "name": "Alert System",
            "price": 1500,
            "image": "https://via.placeholder.com/150"
        }
    ])

##################################################
# RUN APP
##################################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)