from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://winhackverify-default-rtdb.firebaseio.com"  # Replace with your Firebase database URL
})

# Reference to the Firebase Realtime Database
firebase_ref = db.reference("mobile_numbers")

# Endpoint to store a mobile number
@app.route("/store_number", methods=["POST"])
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
@app.route("/check_number/<mobile_number>", methods=["GET"])
def check_number(mobile_number):
    try:
        if not mobile_number.isdigit() or len(mobile_number) != 10:
            return jsonify({"error": "Invalid mobile number"}), 400

        # Check if the mobile number exists in Firebase
        exists = firebase_ref.child(mobile_number).get()

        if exists:
            return jsonify({"exists": 1}), 200
        else:
            return jsonify({"exists": 0}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
