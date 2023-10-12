import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the economic data
economic_data = pd.read_csv('economic_data.csv')

# Display the first few rows of the economic data
print("\nFirst few rows of economic data:")
print(economic_data.head())

# Perform analysis on economic data
try:
    # Analysis 1: Descriptive Statistics
    economic_stats = economic_data.describe()
    print("\nDescriptive Statistics of Economic Data:")
    print(economic_stats)

    # Analysis 2: Correlation between Economic Factors
    correlation_matrix = economic_data.corr()
    print("\nCorrelation Matrix:")
    print(correlation_matrix)

    # Analysis 3: Identify Key Economic Indicators
    key_indicators = economic_stats.loc[['mean', 'std']].transpose()
    key_indicators['CV'] = key_indicators['std'] / key_indicators['mean']
    key_indicators = key_indicators.sort_values(by='CV', ascending=False)
    print("\nKey Economic Indicators:")
    print(key_indicators)

    # Analysis 4: Identify Trends or Patterns
    # Assuming 'Year' is a column in the economic_data DataFrame
    economic_data['Year'] = pd.to_datetime(economic_data['Year'])
    economic_data.set_index('Year', inplace=True)

    # Decompose time series data
    result = seasonal_decompose(economic_data['GDP'], model='multiplicative', period=12)

    # Visualize decomposition
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 8), sharex=True)
    result.observed.plot(ax=ax1)
    ax1.set_ylabel('Observed')
    result.trend.plot(ax=ax2)
    ax2.set_ylabel('Trend')
    result.seasonal.plot(ax=ax3)
    ax3.set_ylabel('Seasonal')
    result.resid.plot(ax=ax4)
    ax4.set_ylabel('Residual')
    plt.tight_layout()
    plt.show()

except Exception as e:
    print(f"Error during trend identification: {e}")

# Analysis 5: Build Predictive Models (e.g., regression models)
try:
    # Assuming 'GDP' is the target variable and other columns are features
    X = economic_data.drop(columns=['GDP'])
    y = economic_data['GDP']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    print(f"\nMean Squared Error: {mse}")

except Exception as e:
    print(f"Error during predictive modeling: {e}")

# Analysis 6: Economic Scenario Simulation
# Simulate economic scenarios based on historical data to test crisis response strategies.

# Analysis 7: Generate Recommendations
# Based on the simulated scenarios, generate recommendations for crisis response strategies.
