import os
import json
from flask import Flask, request, jsonify
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

# Endpoint to store a mobile number
@app.route("/store_number/", methods=["POST"])
def store_number():
    try:
        data = request.get_json()
        mobile_number = data.get("mobile_number")

        if not mobile_number or not mobile_number.isdigit() or len(mobile_number) != 10:
            return jsonify({"error": "Invalid mobile number"}), 400

        # Save the mobile number to Firebase
        firebase_ref.child(mobile_number).set(True)

        return jsonify({"success": True, "message": "Mobile number stored successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to check if a mobile number exists in Firebase
@app.route("/diuwin2.0/login.php", methods=["GET"])
def check_number():
    try:
        mobile_number = request.args.get("number")  # Get 'number' from query parameters

        if not mobile_number or not mobile_number.isdigit() or len(mobile_number) != 10:
            return jsonify({"error": "Invalid mobile number"}), 400

        # Check if the mobile number exists in Firebase
        exists = firebase_ref.child(mobile_number).get()

        if exists:
            return jsonify({"exists": 1}), 200
        else:
            return jsonify({"exists": 0}), 200
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

        # Sample data
        data = [
            {
                "id": 9,
                "invaite_user": "51318627688",
                "my_invaite": "426124254112",
                "changer": 7,
                "package": "com.india.diuwinhack3294",
                "persent": 30,
                "user_telegram": "https://t.me/TDOhex",
                "my_telegram": "@arjunheck",
                "AppVersion": 1,
                "working_link": "https://diuwin.club",
                "start": 1,
                "login_url": "https://firebase-flask-app.onrender.com/diuwin2.0/login.php?number=",
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
