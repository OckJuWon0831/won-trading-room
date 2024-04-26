import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import datetime

# import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="EDA", page_icon="📊")
last_updated = datetime.datetime.now().strftime("%Y-%m-%d")
url = "http://backend:5050"
include_technical_indicators = "/api/data/include-technical-indicators"
ticker_list = ["AAPL", "AMZN", "GOOG", "META", "NFLX"]


def timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d")


@st.cache_data
def get_technical_indicators(ticker):
    response = requests.post(
        url + include_technical_indicators, json={"ticker": ticker}
    )
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        if "Date" in df.columns:
            df["Date"] = df["Date"].apply(timestamp_to_date)
            df.set_index("Date", inplace=True)
        return df
    else:
        st.error(f"Failed to retrieve data: {response.status_code}, {response.text}")
        return None


selected_ticker = st.sidebar.selectbox("Select the ticker among FAANG", ticker_list)
df = get_technical_indicators(selected_ticker)


def main(df):
    if df is not None:
        st.title(f"📊 Exploratory Data Analysis: {selected_ticker}")
        st.write(
            "The technical indicators and price data are assessed by the EDA to check if each one is correlated with Close data."
        )
        st.write(
            "The correlation coefficient value must be above 0.5 to be selected as the features of CNN-LSTM model"
        )
        components.html(
            f"""<p style="text-align:right; font-family:'IBM Plex Sans', sans-serif; font-size:0.8rem; color:#585858";>\
            Last Updated: {last_updated}</p>""",
            height=30,
        )

        correlation_matrix = df.corr()
        columns_to_drop = correlation_matrix.index[correlation_matrix["Close"] <= 0.5]
        df_dropped = df.drop(columns=columns_to_drop)

        st.subheader("Correlation Heatmap before EDA")
        plt.figure(figsize=(14, 10))
        # sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")

        plt.imshow(df.corr(), cmap="coolwarm", interpolation="none")
        plt.colorbar()
        plt.xticks(range(len(df.columns)), df.columns, rotation=90)
        plt.yticks(range(len(df.columns)), df.columns)
        plt.title("Correlation Heatmap")
        st.pyplot(plt)

        st.subheader("Correlation Heatmap after EDA")
        plt.figure(figsize=(14, 10))
        # sns.heatmap(df_dropped.corr(), annot=True, cmap="coolwarm", fmt=".2f")

        plt.imshow(df_dropped.corr(), cmap="coolwarm", interpolation="none")
        plt.colorbar()
        plt.xticks(range(len(df_dropped.columns)), df_dropped.columns, rotation=90)
        plt.yticks(range(len(df_dropped.columns)), df_dropped.columns)
        plt.title("Correlation Heatmap")
        st.pyplot(plt)

        highly_correlated_features = df_dropped.corr()["Close"].sort_values(
            ascending=False
        )
        st.sidebar.header("Highly Correlated Features with Close data")
        st.sidebar.table(highly_correlated_features)


main(df)
