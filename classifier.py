import joblib

model = joblib.load(
    "models/complaint_model.pkl"
)


def classify_complaint(text):

    prediction = model.predict([text])

    category = prediction[0]

    return category