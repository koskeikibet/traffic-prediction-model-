# -*- coding: utf-8 -*-
"""traffic prediction model .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QsnH2ECbG0-7CR_hhuDEUzfWfg6wW_fd
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Generate synthetic traffic data
np.random.seed(42)
date_rng = pd.date_range(start='2023-01-01', end='2023-12-31', freq='H')
data = pd.DataFrame(date_rng, columns=['date'])
data['traffic_volume'] = np.random.poisson(lam=(50 + 10 * np.sin(data['date'].dt.dayofyear * (2 * np.pi / 365))), size=len(data))

# Feature engineering
data['hour'] = data['date'].dt.hour
data['day_of_week'] = data['date'].dt.dayofweek
data['month'] = data['date'].dt.month

# Select features and target variable
X = data[['hour', 'day_of_week', 'month']]
y = data['traffic_volume']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Visualization of true vs predicted traffic volumes
plt.figure(figsize=(10, 6))
plt.scatter(y_test, predictions, alpha=0.6)
plt.xlabel('True Traffic Volume')
plt.ylabel('Predicted Traffic Volume')
plt.title('True vs Predicted Traffic Volume')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')  # diagonal line
plt.show()

# Visualization of feature importance
importances = model.feature_importances_
features = X.columns
indices = np.argsort(importances)

plt.figure(figsize=(10, 6))
plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], align='center')
plt.yticks(range(len(indices)), features[indices])
plt.xlabel('Relative Importance')
plt.show()