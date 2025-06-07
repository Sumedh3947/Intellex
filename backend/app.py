from flask import Flask, jsonify, request
from flask_cors import CORS
import joblib, os
# 1️⃣  create the Flask app first
app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(__file__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "categorizer.pkl")
categorizer = joblib.load(MODEL_PATH)

ANOM_PATH = os.path.join(BASE_DIR, "anomaly.pkl")
anomaly_model = joblib.load(ANOM_PATH)      # IsolationForest

# 2️⃣  now import the models and init the DB
from models import db, Expense, init_db
init_db(app)

# ---------- routes ----------
@app.route("/ping")
def ping():
    return jsonify(msg="pong")

from datetime import datetime

@app.route("/api/expenses", methods=["POST"])
def add_expense():
    data = request.get_json(force=True)

    # --- validation & parsing ---
    try:
        amount = float(data["amount"])
        date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        return jsonify(error="amount(float) & date(YYYY-MM-DD) required"), 400

    # --- NEW: auto-categorize if user left it blank ---
    if not data.get("category"):
        category = categorizer.predict([data["description"]])[0]
    else:
        category = data["category"]

    # --- NEW: anomaly score ---
# IsolationForest returns -1 for anomaly, 1 for normal
    is_anomaly = anomaly_model.predict([[amount]])[0] == -1

    exp = Expense(
    amount=amount,
    date=date_obj,
    description=data.get("description", ""),
    category=category,
    is_anomaly=is_anomaly            # ← store flag
    )
    db.session.add(exp)
    db.session.commit()

    return jsonify(status="ok", id=exp.id), 201


@app.route("/api/expenses", methods=["GET"])
def list_expenses():
    rows = Expense.query.order_by(Expense.id.desc()).all()
    return jsonify([
    {
        "id":        e.id,
        "amount":    e.amount,
        "date":      e.date.isoformat(),
        "desc":      e.description,
        "category":  e.category,
        "is_anomaly": e.is_anomaly      # NEW FIELD
    } for e in rows
    ])


# ---------- run ----------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
