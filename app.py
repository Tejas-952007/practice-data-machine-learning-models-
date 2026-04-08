from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
from datetime import datetime, timedelta

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

def create_features(dt_obj):
    return pd.DataFrame([{
        'hour': dt_obj.hour,
        'dayofweek': dt_obj.weekday(),
        'quarter': (dt_obj.month - 1) // 3 + 1,
        'month': dt_obj.month,
        'year': dt_obj.year,
        'dayofyear': dt_obj.timetuple().tm_yday,
        'dayofmonth': dt_obj.day,
        'weekofyear': dt_obj.isocalendar()[1]
    }])

@app.get("/predict")
async def predict(timestamp: str = None):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        if timestamp:
            dt = datetime.fromisoformat(timestamp)
        else:
            dt = datetime.now()
        
        features = create_features(dt)
        prediction = model.predict(features)[0]
        
        return {
            "timestamp": dt.isoformat(),
            "prediction": float(prediction),
            "unit": "MW"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/forecast")
async def forecast(days: int = 7):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    predictions = []
    start_dt = datetime.now()
    
    for i in range(days * 24):
        dt = start_dt + timedelta(hours=i)
        features = create_features(dt)
        pred = model.predict(features)[0]
        predictions.append({
            "timestamp": dt.isoformat(),
            "val": float(pred)
        })
    
    return predictions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
