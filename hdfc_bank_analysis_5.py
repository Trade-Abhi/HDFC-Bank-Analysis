# -*- coding: utf-8 -*-
"""HDFC Bank Analysis 5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vMt-JgCAIpXIDv_hU_oAGT0OIYvYp9mp
"""

# Import The Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score

# Load HDFC Bank stock data from an Excel file
data = pd.read_excel('HDFCData.xlsx')

# Calculate RSI (Relative Strength Index)
def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = delta.mask(delta < 0, 0)
    loss = -delta.mask(delta > 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

data['RSI'] = calculate_rsi(data)

# Calculate 14-day average volume
data['Volume_Avg_14'] = data['Volume'].rolling(14).mean()

# Calculate 14-day average price
data['Price_Avg_14'] = data['Close'].rolling(14).mean()

# Create label column
data['Label'] = np.where(data['Close'] > data['Open'], 'Green', 'Red')

# Drop rows with missing values
data = data.dropna()

# Extract features and label
features = data[['Open', 'Low', 'Close', 'High', 'RSI', 'Volume_Avg_14', 'Price_Avg_14']]
label = data['Label']

# Impute missing values
imputer = SimpleImputer(strategy='mean')
features = pd.DataFrame(imputer.fit_transform(features), columns=features.columns)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=42)

# Train a HistGradientBoostingClassifier on the training set
model = HistGradientBoostingClassifier()
model.fit(X_train, y_train)

# Predict labels for the training set
y_pred_train = model.predict(X_train)

# Calculate the accuracy of the predictions on the training set
accuracy_train = accuracy_score(y_train, y_pred_train)

# Print the accuracy on the training set
print("Accuracy on the training set:", accuracy_train)

# Predict labels for the testing set
y_pred_test = model.predict(X_test)

# Calculate the accuracy of the predictions on the testing set
accuracy_test = accuracy_score(y_test, y_pred_test)

# Print the accuracy on the testing set
print("Accuracy on the testing set:", accuracy_test)

# Use the entire dataset to predict the probabilities for the next day's candle color
# Predict probabilities for the next day's candle color
next_day_features = features.tail(1)  # Get the last row of features as next day's data
next_day_probabilities = model.predict_proba(next_day_features)

# Extract the probabilities for green and red
green_probability = next_day_probabilities[0][0]
red_probability = next_day_probabilities[0][1]

# Print the probabilities
print("Next Day's (23/06/2023) Green Candle Probability:", green_probability)
print("Next Day's (23/06/2023) Red Candle Probability:", red_probability)