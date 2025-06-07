# intellex/backend/models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# … existing imports …
class Expense(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    amount      = db.Column(db.Float,  nullable=False)
    date        = db.Column(db.Date,   nullable=False)
    description = db.Column(db.String(255))
    category    = db.Column(db.String(64))
    is_anomaly  = db.Column(db.Boolean, default=False)   # ← NEW COLUMN
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
