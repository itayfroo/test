import streamlit as st
import requests
import yfinance as yf
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf

# List of API keys
api_keys = ['MNI5T6CU7KLSFJA8', 'QJFF49AEUN6NX884', '9ZZWS60Q2CZ6JYUK']
current_api_key_index = 0

def rotate_api_key():
    global current_api_key_index
    current_api_key_index = (current_api_key_index + 1) % len(api_keys)
    return api_keys[current_api_key_index]

def get_stock_symbol(company_name):
    for _ in range(len(api_keys)):
        api_key = rotate_api_key()
        base_url = "https://www.alphavantage.co/query"
        function = "SYMBOL_SEARCH"

        params = {
            "function": function,
            "keywords": company_name,
            "apikey": api_key,
        }

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            if "bestMatches" in data and data["bestMatches"]:
                # Convert the symbol to uppercase before returning
                stock_symbol = data["bestMatches"][0]["1. symbol"].upper()
                return stock_symbol
        except Exception as e:
            st.error(f"Error: {e}")

    return None

def get_stock_data(symbol):
    try:
        stock_data = yf.download(symbol, start="2022-01-01", end="2023-01-01")
        return stock_data
    except Exception as e:
        st.error(f"Error retrieving data: {e}")
        return None

def plot_stock_data(stock_data):
    fig = px.line(stock_data, x=stock_data.index, y='Close', title='Stock Prices Over the Last Year')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Stock Price (USD)')
    st.plotly_chart(fig)

def predict_tomorrows_stock_value_linear_regression(stock_data):
    X = pd.DataFrame({'Days': range(1, len(stock_data) + 1)})
    y = stock_data['Close']

    model = LinearRegression()
    model.fit(X, y)

    tomorrow = X.iloc[[-1]]['Days'].values[0] + 1
    predicted_value = model.predict([[tomorrow]])[0]

    return predicted_value

def predict_tomorrows_stock_value_lstm(stock_data):
    scaler = MinMaxScaler()
    data_normalized = scaler.fit_transform(stock_data['Close'].values.reshape(-1, 1))

    seq_length = 10
    sequences, labels = [], []
    for i in range(len(data_normalized) - seq_length):
        seq = data_normalized[i:i + seq_length]
        label = data_normalized[i + seq_length]
        sequences.append(seq)
        labels.append(label)

    X_train, y_train = np.array(sequences), np.array(labels)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))

    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, activation='relu', input_shape=(seq_length, 1)),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    model.fit(X_train, y_train, epochs=50, batch_size=32)

    last_sequence = data_normalized[-seq_length:]
    last_sequence = last_sequence.reshape((1, seq_length, 1))

    predicted_value = model.predict(last_sequence)
    predicted_value = scaler.inverse_transform(predicted_value.reshape(1, -1))[0, 0]

    return predicted_value

# Function to display information about LSTM
def display_lstm_info():
    st.markdown("""
        Long Short-Term Memory (LSTM) is a type of recurrent neural network (RNN) architecture that is designed to overcome the limitations of traditional RNNs in capturing long-term dependencies in sequential data. RNNs, in theory, can learn from past information to make predictions on future data points, but in practice, they often struggle to learn and remember information from distant past time steps due to the vanishing gradient problem.

LSTM was introduced to address the vanishing gradient problem by incorporating memory cells and gating mechanisms. The key components of an LSTM cell include:

1. **Cell State (Ct):** This is the memory of the cell. It can retain information over long sequences, allowing the model to capture long-term dependencies.

2. **Hidden State (ht):** This is the output of the cell and is used for making predictions. It can selectively expose parts of the cell state.

3. **Three Gates:**
   - **Forget Gate (ft):** Decides what information to throw away from the cell state.
   - **Input Gate (it):** Updates the cell state with new information.
   - **Output Gate (ot):** Controls what parts of the cell state should be output.

LSTM's ability to selectively learn, forget, and store information makes it particularly effective for tasks involving sequences, such as time series forecasting, natural language processing, and speech recognition.

In the context of time series prediction, like predicting stock prices, LSTM models are well-suited to capture patterns and dependencies in historical data and make predictions for future values based on that learned context.
    """)

def linear_Regression(stock_data):
    st.markdown("""
Linear regression is a statistical method used for modeling the relationship between a dependent variable and one or more independent variables by fitting a linear equation to the observed data. The most common form is simple linear regression, which deals with the relationship between two variables, while multiple linear regression deals with two or more predictors.

The linear regression equation has the form:

Y =  β(0)+ β(1)X(1) + β(2)X(2) + ... + β(n)x(n) +  ε

Here:
- Y  is the dependent variable.
- X(1), X(2), ..., X(n) are independent variables.
- β(0) is the intercept.
- β(1), β(2)...,β(N) are the coefficients representing the relationship between the independent variables and the dependent variable.
- ε is the error term, representing the unobserved factors that affect the dependent variable.

The goal of linear regression is to find the values of the coefficients that minimize the sum of the squared differences between the observed and predicted values. Once the model is trained, it can be used to make predictions for new data.

Linear regression is widely used in various fields for tasks such as predicting stock prices, housing prices, sales forecasting, and many other applications where understanding the relationship between variables is crucial.  
                """)
    X = pd.DataFrame({'Days': range(1, len(stock_data) + 1)})
    y = stock_data['Close']

    model = LinearRegression()
    model.fit(X, y)

    # Predictions for the entire range
    predictions = model.predict(X)

    # Plot the actual and predicted values
    fig_lr = px.line(X, x='Days', y=y, title='Actual vs Predicted (Linear Regression)')
    fig_lr.add_scatter(x=X['Days'], y=predictions, mode='lines', name='Predicted')
    fig_lr.update_xaxes(title_text='Days')
    fig_lr.update_yaxes(title_text='Stock Price (USD)')

    st.plotly_chart(fig_lr)

st.set_page_config(
    page_title="Stocks analyzer",
    page_icon=r"icons8-stock-48.png",
    layout="wide",
)
st.markdown(
    r"""
    <style>
    .reportview-container {
        background: url("C:\Users\user\Documents\test\background.jpg");
    }
   </style>
    """,
    unsafe_allow_html=True
)
st.title("Stock Analyzer")

company_name = st.text_input("Enter company name or item:")

if st.button("Get Stock Symbol"):
    stock_symbol = get_stock_symbol(company_name)

    if stock_symbol:
        st.title("Stock Price Visualization App")
        st.write(f"Displaying stock data for {stock_symbol}")

        stock_data = get_stock_data(stock_symbol)
        if stock_data is not None:
            plot_stock_data(stock_data)
            try:
                predicted_value_lr = predict_tomorrows_stock_value_linear_regression(stock_data)
                predicted_value_lstm = predict_tomorrows_stock_value_lstm(stock_data)

                st.write(f"Approximate tomorrow's stock value (Linear Regression): ${predicted_value_lr:.2f}")
                st.write(f"Approximate tomorrow's stock value (LSTM): ${predicted_value_lstm:.2f}")

                # Expander for LSTM information
                with st.expander("💡 What is LSTM?"):
                    display_lstm_info()

                # Expander for Linear Regression information and graph
                with st.expander("💡 What is Linear Regression?"):
                    st.write("Linear Regression Simulation:")
                    linear_Regression(stock_data)
            except:
                st.warning("Not enough info for an AI aproximation")
    else:
        st.warning("Stock dosent exit.")
