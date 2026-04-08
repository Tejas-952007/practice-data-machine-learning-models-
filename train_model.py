import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import matplotlib.pyplot as plt

def create_features(df):
    """
    Create time series features based on time series index.
    """
    df = df.copy()
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['dayofweek'] = df['datetime'].dt.dayofweek
    df['quarter'] = df['datetime'].dt.quarter
    df['month'] = df['datetime'].dt.month
    df['year'] = df['datetime'].dt.year
    df['dayofyear'] = df['datetime'].dt.dayofyear
    df['dayofmonth'] = df['datetime'].dt.day
    df['weekofyear'] = df['datetime'].dt.isocalendar().week.astype(int)
    return df

def train_model():
    # Load data
    df = pd.read_csv('energy_data.csv')
    df = create_features(df)
    
    # Split features and target
    X = df[['hour', 'dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'dayofmonth', 'weekofyear']]
    y = df['consumption']
    
    # Split into train and test
    # Since it's time series, we should split by date, but for this demo a simple split is fine 
    # or we can do a time-based split.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Create model
    reg = xgb.XGBRegressor(
        base_score=0.5, 
        booster='gbtree',    
        n_estimators=1000,
        early_stopping_rounds=50,
        objective='reg:squarederror',
        max_depth=3,
        learning_rate=0.01
    )
    
    # Train
    reg.fit(X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=100)
    
    # Forecast on test set
    y_pred = reg.predict(X_test)
    
    # Evaluation
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"Root Mean Squared Error: {rmse:.2f}")
    print(f"R2 Score: {r2:.4f}")
    
    # Save model
    with open('model.pkl', 'wb') as f:
        pickle.dump(reg, f)
    
    print("Model saved as model.pkl")
    
    # Plot importance
    plt.figure(figsize=(10,6))
    xgb.plot_importance(reg)
    plt.savefig('feature_importance.png')
    print("Feature importance plot saved as feature_importance.png")

if __name__ == "__main__":
    train_model()
