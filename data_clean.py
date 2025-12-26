import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


trada = pd.read_csv('tour_logs_train.csv')

missing_values = trada.isnull().sum()
print("Missing values in each column:\n", missing_values[missing_values > 0])


# 1. Use 'hue' to color the points by Venue_ID
# 2. Assign the plot to a variable 'g' to easily adjust limits
g = sns.relplot(
    data=trada, 
    x='Crowd_Size', 
    y='Merch_Sales_Post_Show', 
    kind='scatter', 
    hue='Band_Outfit',      # Differentiate by color
    style='Venue_ID',    # Differentiate by marker shape (optional)
    palette='rocket'    # Optional: Choose a color scheme
)
print(sns.color_palette('rocket'))
# Set the x-axis limits on the FacetGrid object
g.set(xlim=(0, 1000))


plt.title('Crowd Size vs Merch Sales Post Show')










































