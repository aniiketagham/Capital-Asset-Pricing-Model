#importing libraries
import pandas as pd
import pandas_datareader.data as web
import datetime
import streamlit as st
import yfinance as yf
import utils.CAPM_functions as CAPM_functions

st.set_page_config(page_title="CAPM", page_icon=":chart_with_upwards_trend:", layout="wide")

st.title("CAPM Return Analysis")

#getting input from user

col1, col2 = st.columns([1,1])
with col1:
    stocks_list = st.multiselect("Select Stocks for CAPM Analysis",
               options=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "JNJ"],
               default=["AAPL", "MSFT", "GOOGL","AMZN"], key="stocks")
with col2:
    year = int(st.number_input("Number of Years",1,10))

#downloading data for SP500
try:
    
    end=datetime.date.today()
    start = datetime.date(datetime.date.today().year - year, datetime.date.today().month, datetime.date.today().day)
    SP500 = web.DataReader(['sp500'],'fred', start, end)
    #print(SP500.head())

    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        #downloading data for selected stocks
        data = yf.download(stock, period=f"{year}y")
        stocks_df[f'{stock}']= data['Close']

    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns = ['Date', 'sp500']

    stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
    stocks_df['Date'] = stocks_df['Date'].apply(lambda x:str(x)[:10])
    stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### Dataframe Head")
        st.dataframe(stocks_df.head(), use_container_width=True)
    with col2:
        st.markdown("### Dataframe Tail")
        st.dataframe(stocks_df.tail(), use_container_width=True)
        
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("### Price of all the Stocks")
        st.plotly_chart(CAPM_functions.plot_interactive_chart(stocks_df))
    with col2:
        st.markdown("### Normalized Price of all the Stocks")
        st.plotly_chart(CAPM_functions.plot_interactive_chart(CAPM_functions.normalize_prices(stocks_df)))
        
    stocks_daily_returns = CAPM_functions.daily_returns(stocks_df)

    beta = {}
    alpha = {}

    for i in stocks_daily_returns.columns:
        if i != 'Date' and i != 'sp500':
            b,a = CAPM_functions.calculate_betas(stocks_daily_returns, i)
            beta[i] = b
            alpha[i] = a
    print(beta,alpha)

    beta_df = pd.DataFrame(columns=['Stock','Beta Value'])
    beta_df['Stock'] = beta.keys()
    beta_df['Beta Value'] = [str(round(i,2)) for i in beta.values()]

    with col1:
        st.markdown("### Beta Values of Stocks")
        st.dataframe(beta_df, use_container_width=True)

    rf =0
    rm = stocks_daily_returns['sp500'].mean()*252

    return_df = pd.DataFrame()
    return_value = []
    for stock, value in beta.items():
        return_value.append(str(round(rf+(value*(rm-rf)),2)))
    return_df['Stock'] = stocks_list
    return_df['Return Value'] = return_value

    with col2:  
        st.markdown("### Expected Return Values of Stocks")
        st.dataframe(return_df, use_container_width=True)

except:
    st.write("Please select at least one stock to see the CAPM analysis.")