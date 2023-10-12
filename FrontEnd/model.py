import argparse
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import json
import numpy as np

def process_csv(csv_file):
    response = {}
    try:
        # Read the CSV file
        economic_data = pd.read_csv(csv_file)

        # Calculate statistics, correlation, and key indicators
        economic_stats = economic_data.describe()
        correlation_matrix = economic_data.corr()
        key_indicators = economic_stats.loc[['mean', 'std']].transpose()
        key_indicators['CV'] = key_indicators['std'] / key_indicators['mean']

        # Perform seasonal decomposition
        economic_data['Year'] = pd.to_datetime(economic_data['Year'])
        economic_data.set_index('Year', inplace=True)
        result = seasonal_decompose(economic_data['GDP'], model='multiplicative', period=12)

        # Train a Linear Regression model
        X = economic_data.drop(columns=['GDP'])
        y = economic_data['GDP']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)

        # Replace NaN values with None in the result before serialization
        result_dict = {
            'observed': result.observed.tolist(),
            'trend': result.trend.tolist(),
            'seasonal': result.seasonal.tolist(),
            'residual': result.resid.tolist(),
        }
        for key in result_dict:
            result_dict[key] = [None if np.isnan(value) else value for value in result_dict[key]]

        # Prepare the response data
        output_data = {
            'data': economic_data.to_dict(orient='records'),
            'stats': economic_stats.to_dict(),
            'correlation': correlation_matrix.to_dict(),
            'key_indicators': key_indicators.to_dict(),
            'trends': result_dict,
            'prediction_mse': mse,
        }

        response['success'] = True
        response['data'] = output_data

    except Exception as e:
        response['success'] = False
        response['error'] = str(e)

    return json.dumps(response)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process economic data from a CSV file')
    parser.add_argument('csv_file', type=str, help='Path to the input CSV file')

    args = parser.parse_args()
    output = process_csv(args.csv_file)
    print(output)
