import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


# Load dataset
data = pd.read_csv("data/complaints.csv")

X = data["complaint"]
y = data["category"]


# Create AI pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# Train model
model.fit(X, y)


# Save trained model
joblib.dump(
    model,
    "models/complaint_model.pkl"
)

print("AI model trained successfully!")
print("Model saved to models/complaint_model.pkl")