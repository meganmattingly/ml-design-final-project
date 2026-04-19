from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import mlflow
import mlflow.sklearn

app = FastAPI(title="Spotify Churn Prediction API")

mlflow.set_tracking_uri("http://127.0.0.1:5000")

#MODEL_URI = "models:/spotify_churn_logreg_clean/2"
#model = mlflow.sklearn.load_model(MODEL_URI)

#Automatically get the latest version of the model, regardless of the number 
client = mlflow.tracking.MlflowClient()
latest_version = client.get_latest_versions("spotify_churn_logreg_clean")[0].version
MODEL_URI = f"models:/spotify_churn_logreg_clean/{latest_version}"
model = mlflow.sklearn.load_model(MODEL_URI)



class ChurnInput(BaseModel):
    country: str
    music_suggestion_rating_1_to_5: int
    avg_listening_hours_per_week: float
    most_liked_feature: str
    desired_future_feature: str
    primary_device: str
    playlists_created: int
    likes_personalization: bool
    dislikes_suggestions: bool
    heavy_listener: bool
    new_user: bool


@app.get("/")
def home():
    return {"message": "Spotify Churn API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: ChurnInput):
    input_df = pd.DataFrame([data.model_dump()])

    prediction = int(model.predict(input_df)[0])

    result = {
        "prediction": prediction,
        "label": "churn" if prediction == 1 else "not churn"
    }

    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(input_df)[:, 1][0])
        result["churn_probability"] = round(probability, 4)

    return result
