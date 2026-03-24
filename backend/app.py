from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STUDENT = {
    "name":            "Niketh B Nath",
    "roll_number":     "2023BCD0056",
    "register_number": "N/A",
    "department":      "BCD"
}

@app.route("/student-details", methods=["GET"])
def student_details():
    return jsonify(STUDENT)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
