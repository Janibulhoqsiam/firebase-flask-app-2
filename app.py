import os
import json
from flask import Flask, request,Response, jsonify
import firebase_admin
from firebase_admin import credentials, db
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

CORS(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("/etc/secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://winhackverify-default-rtdb.firebaseio.com"  # Replace with your Firebase database URL
})

# Reference to the Firebase Realtime Database
firebase_ref = db.reference("mobile_numbers")

firebase_ref_dp = db.reference("deposit_amount")



@app.route("/diuwin2.0/register.php", methods=["POST"])
def store_number():
    try:
        # Extract the 'number' query parameter from the URL
        query_number = request.args.get("number")

        # Extract the JSON body data
        data = request.get_json()
        mobile_number = data.get("mobile_number") if data else None

        # Validate both query parameter and JSON body number
        if query_number and (not query_number.isdigit() or len(query_number) != 10):
            return jsonify({"error": "Invalid mobile number in query parameter"}), 400
        if mobile_number and (not mobile_number.isdigit() or len(mobile_number) != 10):
            return jsonify({"error": "Invalid mobile number in JSON body"}), 400

        # Use query parameter number if provided, otherwise fallback to JSON body
        final_number = query_number if query_number else mobile_number

        if not final_number:
            return jsonify({"error": "No valid mobile number provided"}), 400

        # Save the mobile number to Firebase
        firebase_ref.child(final_number).set(True)

        return jsonify({"success": True, "message": "Mobile number stored successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to check if a mobile number exists in Firebase
@app.route("/diuwin2.0/login.php", methods=["GET"])
def check_number():
    try:
        mobile_number = request.args.get("number")
        if not mobile_number or not mobile_number.isdigit() or len(mobile_number) != 10: return "Invalid mobile number", 400 
        exists = firebase_ref.child(mobile_number).get() 
        return "1" if exists else "0", 200 
    except Exception as e: 
        return str(e), 500 



@app.route("/diuwin2.0/deposit.php", methods=["POST"])
def store_deposit():
    try:
        # Extract the deposit amount from the query parameters
        deposit_amount = request.args.get("amount")

        # Validate the deposit amount
        if not deposit_amount or not deposit_amount.isdigit() :
            return jsonify({"error": "Invalid deposit amount"}), 400

        # Store the deposit amount in Firebase under a fixed key
        firebase_ref_dp.child("deposit_amount").set(int(deposit_amount))

        return jsonify({"success": True, "message": "Deposit amount stored successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# New Endpoint to return the exact JSON data

@app.route("/diuwin2.0/splash.php", methods=["GET"])
def api_data():
    try:
        # Get the 'package' query parameter
        package_name = request.args.get("package")

        if not package_name:
            return jsonify({"error": "Package parameter is required"}), 400


        # Fetch the deposit amount from Firebase
        deposit_amount = firebase_ref_dp.child("deposit_amount").get()
        if not deposit_amount:
            deposit_amount = 0  # Default value if no deposit amount is stored


        # Sample data
        data = [
            {
                "id": 9,
                "invaite_user": "421214841570",
                "my_invaite": "421214841570",
                "changer": deposit_amount,
                "package": "com.india.okwin2891", 
                "persent": 30,
                "user_telegram": "https://t.me/+2f4sEUeysVU1MjY1",
                "my_telegram": "@flash_earns",
                "AppVersion": 1,
                "working_link": "https://www.okwin.ws",
                "start": 1,
                "login_url": "https://firebase-flask-app-2.onrender.com/diuwin2.0/login.php?number=",
                "register_url": "https://pesagyan.com/diuwin2.0/register.php?number=",
                "appName": "Diuwin Manish"
            }
        ]

        # Serialize data with escaped slashes
        response = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        
        return Response(response, content_type="application/json")

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/', methods=['GET'])
def working():
    return "Working", 200        

if __name__ == "__main__":
    # Use the PORT environment variable set by Render
    port = int(os.getenv("PORT", 5000))  # Defaults to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
