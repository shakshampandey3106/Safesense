from flask import Flask, render_template, request, jsonify
import razorpay

app = Flask(__name__)

# 🔑 REPLACE THESE
KEY_ID = "rzp_test_SiRwbhD3I2yE7U"
KEY_SECRET = "5GwE1xe42FGNY6ZTxRewL1zH"

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


# ROUTES
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        return render_template("contact.html", success=True)
    return render_template("contact.html", success=False)


# DATA API
@app.route("/data")
def data():
    return jsonify({
        "temp": 60,
        "violations": 2,
        "risk": "MEDIUM"
    })


# PAYMENT
@app.route("/create_order", methods=["POST"])
def create_order():
    data = request.get_json()
    amount = int(data["amount"]) * 100

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify(order)


@app.route("/verify_payment", methods=["POST"])
def verify_payment():
    data = request.get_json()

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })
        return jsonify({"status":"success"})
    except:
        return jsonify({"status":"failed"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    