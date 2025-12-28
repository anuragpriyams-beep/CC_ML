import pandas as pd
import numpy as np
import re

df = pd.read_csv('tour_logs_train.csv')
format = df['Show_DateTime'].str.contains(r'\d+-\d+-\d{4}\s+\d{2}:\d{2}')
df_temp = df.loc[format].copy()
print(df_temp.shape)
