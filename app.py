from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

##################################################
# READ DATA FROM AI FILE
##################################################

def read_data():
    try:
        with open("data.txt", "r") as f:
            temp, violations, risk = f.read().split(",")

            return {
                "temp": int(temp),
                "violations": int(violations),
                "risk": risk,
                "alerts": int(violations)
            }

    except:
        return {
            "temp": 0,
            "violations": 0,
            "risk": "LOW",
            "alerts": 0
        }

##################################################
# HOME ROUTE
##################################################

@app.route("/")
def home():
    return "SafeSense API Running 🚀"

##################################################
# DASHBOARD API
##################################################

@app.route("/api/data")
def data():
    return jsonify(read_data())

##################################################
# PRODUCTS API (4 PRODUCTS)
##################################################

@app.route("/api/products")
def products():
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
# RUN SERVER
##################################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)