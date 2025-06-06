import pandas as pd, joblib, os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv("mini_expenses.csv")
X_train, X_test, y_train, y_test = train_test_split(
    df["description"], df["category"], test_size=0.2, random_state=42
)

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf",  LogisticRegression(max_iter=1000))
]).fit(X_train, y_train)

print("💡 accuracy:", (model.predict(X_test) == y_test).mean())
out = os.path.join("..", "backend", "categorizer.pkl")
joblib.dump(model, out)
print("✅ saved to", out)
