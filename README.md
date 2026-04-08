# Energy Consumption Prediction (Regression & Time Factors)

A high-performance machine learning project designed to predict hourly energy consumption using temporal features. This project features a robust XGBoost-based pipeline and a premium React dashboard for visualization.

## 🚀 Key Features
- **Synthetic Data Engine**: Generates 5 years of hourly energy data with realistic diurnal, weekly, and seasonal patterns.
- **XGBoost Regressor**: Optimized model with an **R² Score of 0.90**, achieving high precision in energy forecasting.
- **Time Factor Engineering**: Automated extraction of hour, day, week, month, and year features.
- **Premium Dashboard**: A sleek, dark-mode UI built with React, featuring:
    - Glassmorphism effects.
    - Real-time 72-hour forecast charts.
    - Key performance indicators (KPIs) for current demand and accuracy.
    - Dynamic responsiveness.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React (Vite), Chart.js, Lucide Icons, Vanilla CSS
- **ML Engine**: XGBoost, Scikit-learn, Pandas, NumPy
- **Styling**: Premium Custom CSS (Glassmorphism)

## 📂 Project Structure
- `data_generation.py`: Script to generate the synthetic dataset.
- `train_model.py`: ML pipeline for feature engineering, training, and evaluation.
- `app.py`: FastAPI backend that serves model predictions.
- `dashboard/`: React application for the user interface.
- `energy_data.csv`: The generated dataset (43,000+ rows).
- `model.pkl`: The trained XGBoost model.
- `feature_importance.png`: Visual analysis of factors driving energy consumption.

## 🏃 How to Run Locally

1. **Backend**:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:8000`.

2. **Frontend**:
   ```bash
   cd dashboard
   npm install
   npm run dev
   ```
   The dashboard will be available at `http://localhost:5173`.

---
**
