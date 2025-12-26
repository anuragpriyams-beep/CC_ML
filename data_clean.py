import pandas as pd
import numpy as np
import re

def wrangle(df):
    # 1. DROP DATA LEAKAGE: Post-show data cannot be used for prediction

    # 2. STANDARDIZE CURRENCY: £1 = $1.27, €1 = $1.09
    def convert_price(val):
        if pd.isna(val) or str(val).lower() == 'free':
            return 0.0
        
        val_str = str(val)
        # Use regex to find the first numeric price (handles cases like "$56.79 (VIP: $85)")
        match = re.search(r"(\d+\.?\d*)", val_str)
        if not match:
            return np.nan
        
        price = float(match.group(1))
        
        # Apply exchange rates
        if '£' in val_str:
            return round(price * 1.27, 2)
        elif '€' in val_str:
            return round(price * 1.09, 2)
        else:
            return round(price, 2)

    df['Ticket_Price'] = df['Ticket_Price'].apply(convert_price)

    # 3. FIX DATE INCONSISTENCIES
    # Map text descriptions to approximate times
    time_map = {
        'Morning': '08:00:00',
        'Afternoon': '14:00:00',
        'Evening': '19:00:00',
        'Late Night': '23:00:00'
    }
    month_map = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    # Replace text times before parsing
    for text, time_val in time_map.items():
        df['Show_DateTime'] = df['Show_DateTime'].str.replace(text, time_val, regex=False)

    df['Show_DateTime'] = pd.to_datetime(df['Show_DateTime'], errors='coerce')
    
    # Fill Day_of_Week based on the cleaned date
    df['Day_of_Week'] = df['Show_DateTime'].dt.dayofweek.fillna(df['Day_of_Week'])

    # 4. FIX SENSOR GLITCHES & OUTLIERS
    # Volume Level range is 1-11
    df.loc[df['Volume_Level'] > 11, 'Volume_Level'] = np.nan
    df.loc[df['Volume_Level'] <= 0, 'Volume_Level'] = np.nan
    
    # Crowd Energy range is 0-100
    if 'Crowd_Energy' in df.columns:
        df.loc[df['Crowd_Energy'] > 100, 'Crowd_Energy'] = np.nan
        df.loc[df['Crowd_Energy'] < 0, 'Crowd_Energy'] = np.nan
    
    # Venue Capacity is ~1000
    df.loc[df['Crowd_Size'] > 1000, 'Crowd_Size'] = np.nan

    # 5. IMPUTATION: Fill remaining NaNs with Median (less sensitive to outliers)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    return df

# Usage
train_df = pd.read_csv('tour_logs_train.csv')
test_df = pd.read_csv('tour_logs_test_input.csv')

train_cleaned = clean_tour_data(train_df)
test_cleaned = clean_tour_data(test_df)

print("Data Cleaning Complete.")
print(train_cleaned.head())