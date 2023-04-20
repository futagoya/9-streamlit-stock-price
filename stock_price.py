import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Set up the title and description of the web app
st.write('''
         # Stock Price Data
         
         Enter Stock Ticker Symbol:
         ''')

# Add a text input box for the user to input the stock ticker symbol
tickerSymbol = st.text_input('Stock Ticker Symbol', 'GOOGL')

# Define list of years as labels for the slider
years = list(range(2010, 2024))  # Update to range from 2010 to 2023

# Set default year range from 2010 to 2023
start_year, end_year = st.slider('Year Range', min_value=2010, max_value=2023, value=(2010, 2023), step=1)

# Calculate start date and end date from selected years
start_date = pd.Timestamp(f'{start_year}-01-01')
end_date = pd.Timestamp(f'{end_year}-12-31')

# Fetch stock data for the entered ticker symbol and date range
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date, actions=True)

# Extract dividends data
dividends = tickerDf['Dividends']

# Calculate return percentage
start_price = tickerDf['Close'].iloc[0]
end_price = tickerDf['Close'].iloc[-1]
return_percentage = ((end_price / start_price) - 1) * 100

# Display the return percentage
st.write(f'Return Percentage: {return_percentage:.2f}%')

# Create a candlestick chart for the OHLC data
fig = go.Figure(data=[go.Candlestick(x=tickerDf.index,
                                     open=tickerDf['Open'],
                                     high=tickerDf['High'],
                                     low=tickerDf['Low'],
                                     close=tickerDf['Close'])])

# Set chart title and axis labels for OHLC chart
fig.update_layout(title=f'{tickerSymbol} Stock Price (OHLC)',
                  xaxis_title='Date',
                  yaxis_title='Price')

# Display the candlestick chart
st.write(fig)

# Create a bar chart for dividends data
fig_dividends = go.Figure(data=[go.Bar(x=dividends.index, y=dividends)])

# Set chart title and axis labels for dividends chart
fig_dividends.update_layout(title=f'{tickerSymbol} Dividends (Yearly)',
                            xaxis_title='Year',
                            yaxis_title='Dividends')

# Display the dividends bar chart
st.write(fig_dividends)
