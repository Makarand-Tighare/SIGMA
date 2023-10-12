import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Load your recession dataset
df = pd.read_csv('recessionPT.csv')

# Extract the 'Recession' column
df1 = df['Recession']

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
df1 = scaler.fit_transform(np.array(df1).reshape(-1, 1))

# Define the time step
time_step = 100

# Create a function to create input and output sequences
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

# Split the data into training and test sets
training_size = int(len(df1) * 0.65)
test_size = len(df1) - training_size
train_data, test_data = df1[0:training_size], df1[training_size:len(df1)]

# Create sequences for training and test data
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

# Reshape the data for the LSTM model
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# Create and compile the LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(50, return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# Train the model
model.fit(X_train, y_train, epochs=100, batch_size=64, verbose=0)

# Make predictions for the next 30 days
n_steps = 100
last_points = test_data[-n_steps:]
x_input = last_points.reshape(1, -1)

prediction_days = 30
predictions = []

for i in range(prediction_days):
    x_input = x_input.reshape((1, n_steps, 1))
    yhat = model.predict(x_input, verbose=0)
    predictions.append(yhat[0])
    x_input = np.append(x_input[:, 1:, :], [yhat], axis=1)

predictions = scaler.inverse_transform(predictions)

# Set your threshold
threshold = 0.5

# Convert predictions to "yes" or "no" based on the threshold
recession_predictions = ["yes" if value >= threshold else "no" for value in predictions]

print(recession_predictions)
