"""
train_anomaly.py
────────────────
Trains a 1-dimensional Isolation Forest on historical expense AMOUNTS
and saves the model as  backend/anomaly.pkl
"""

from pathlib import Path
import sqlite3, joblib, pandas as pd
from sklearn.ensemble import IsolationForest

# ── 1) Resolve file paths ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent            # …/intellex/ml
DB_PATH  = BASE_DIR.parent / "backend" / "instance" / "expenses.sqlite3"
OUT_PATH = BASE_DIR.parent / "backend" / "anomaly.pkl"
OUT_PATH.parent.mkdir(exist_ok=True)                  # backend/ (safety)

# ── 2) Load existing expense amounts from SQLite ───────────────────────
with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query("SELECT amount FROM expense", conn)

# Fallback sample if the DB is still empty
if df.empty:
    df = pd.DataFrame({"amount": [50, 12, 400, 35, 60, 45, 500, 20]})

# ── 3) Fit Isolation Forest ────────────────────────────────────────────
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,       # ≈ 5 % assumed anomalies
    random_state=42
).fit(df[["amount"]])

# ── 4) Persist the model next to backend/app.py ────────────────────────
joblib.dump(model, OUT_PATH)
print("✅  Trained IsolationForest and saved to", OUT_PATH)
