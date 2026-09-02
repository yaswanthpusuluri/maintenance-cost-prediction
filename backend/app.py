from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import HTTPException
import pandas as pd
import joblib

# Load Model and Preprocessor
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(BASE_DIR / "model" / "LinearRegression.joblib")
preprocessor = joblib.load(BASE_DIR / "model" / "preprocessor.pkl")

# Create App
app = FastAPI(
    title="Maintenance Cost Prediction API",
    version="1.0"
)

# Input Schema
class MachineInput(BaseModel):
    machine_type: str
    temperature_motor: float
    rpm: float
    operating_mode: str
    hours_since_maintenance: float
    rul_hours: float
    failure_type: str


@app.get("/")
def home():

    return {
        "Project": "Maintenance Cost Prediction",
        "Model": "Linear Regression",
        "Status": "Running"
    }

@app.post("/predict")
def predict(data: MachineInput):

    try:

        df = pd.DataFrame([data.model_dump()])

        df["maintenance_ratio"] = (
            df["hours_since_maintenance"] /
            (df["rul_hours"] + 1)
        )

        X = preprocessor.transform(df)

        prediction = model.predict(X)

        return {
            "Estimated Repair Cost": round(float(prediction[0]), 2)
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )