from flask import Flask, jsonify, request
from flask_cors import CORS

# 1️⃣  create the Flask app first
app = Flask(__name__)
CORS(app)

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
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify(error="Invalid JSON"), 400

    # --- basic validation & parsing ---
    try:
        amount = float(data["amount"])
        # convert "YYYY-MM-DD" -> datetime.date
        date_obj = datetime.strptime(data["date"], "%Y-%m-%d").date()
    except (KeyError, ValueError):
        return jsonify(error="Fields: amount(float), date(YYYY-MM-DD) required"), 400

    exp = Expense(
        amount=amount,
        date=date_obj,
        description=data.get("description", ""),
        category=data.get("category")  # ML will fill later
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
            "category":  e.category
        } for e in rows
    ])


# ---------- run ----------
if __name__ == "__main__":
    app.run(debug=True, port=5001)
