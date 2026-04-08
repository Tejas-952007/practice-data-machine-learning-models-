import pandas as pd
import numpy as np
import datetime

def generate_energy_data(start_date='2018-01-01', end_date='2023-12-31'):
    date_rng = pd.date_range(start=start_date, end=end_date, freq='H')
    df = pd.DataFrame(date_rng, columns=['datetime'])
    
    # Base consumption
    base = 15000 
    
    # Time factors
    df['hour'] = df['datetime'].dt.hour
    df['dayofweek'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['dayofyear'] = df['datetime'].dt.dayofyear
    df['year'] = df['datetime'].dt.year
    
    # Yearly trend (slight increase)
    trend = (df['year'] - df['year'].min()) * 500
    
    # Seasonal effect (Sinusoidal with peaks in Summer and Winter)
    # Using 2 periods for Summer (July) and Winter (January) peaks
    seasonal = 3000 * np.sin(2 * np.pi * (df['dayofyear'] + 15) / 365) + \
               1000 * np.cos(4 * np.pi * (df['dayofyear'] + 15) / 365) # Adding complexity
    
    # Weekly effect (Lower on weekends)
    weekly = df['dayofweek'].map({0: 0, 1: 100, 2: 200, 3: 150, 4: 100, 5: -800, 6: -1000})
    
    # Diurnal effect (Two peaks: morning and evening)
    diurnal = 2000 * np.sin(2 * np.pi * (df['hour'] - 6) / 24) + \
              1500 * np.sin(4 * np.pi * (df['hour'] - 12) / 24)
    
    # Add noise
    noise = np.random.normal(0, 500, size=len(df))
    
    # Combine
    df['consumption'] = base + trend + seasonal + weekly + diurnal + noise
    
    # Clean up and save
    df = df[['datetime', 'consumption']]
    return df

if __name__ == "__main__":
    energy_df = generate_energy_data()
    energy_df.to_csv('energy_data.csv', index=False)
    print(f"Generated {len(energy_df)} rows of data and saved to energy_data.csv")
