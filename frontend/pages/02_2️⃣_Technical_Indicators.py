import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import datetime
from indicator_descriptions import IndicatorDescriptions
import matplotlib.pyplot as plt

plt.style.use("ggplot")

url = "http://backend:5050"
include_technical_indicators = "/api/data/include-technical-indicators"
ticker_list = ["AAPL", "AMZN", "GOOG", "META", "NFLX"]

st.set_page_config(page_title="Technical Indicators", page_icon="🔢")


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
            df.drop("Volume", axis=1, inplace=True)
        return df
    else:
        st.error("Failed to retrieve data.")
        return None


selected_ticker = st.sidebar.selectbox("Select a ticker:", ticker_list)
df = get_technical_indicators(selected_ticker)


def plot_feature(df):

    descriptions = IndicatorDescriptions().descriptions

    st.title(f"🚀 Technical indicators of {selected_ticker}")
    feature_choices = ["-"] + list(df.columns)
    st.header("Technical indicators before EDA")
    feature_choice = st.selectbox(
        "Select the feature to see:", feature_choices, index=0
    )

    if feature_choice != "-":
        description = descriptions.get(feature_choice, feature_choice)
        fig, ax = plt.subplots(figsize=(10, 5))
        df[feature_choice].plot(ax=ax, title=description)
        st.pyplot(fig)
    else:
        fig, axes = plt.subplots(
            nrows=len(df.columns), ncols=1, figsize=(10, 5 * len(df.columns))
        )
        with st.spinner("Wait for it..."):
            for ax, column in zip(axes, df.columns):
                description = descriptions.get(column, column)
                df[column].plot(ax=ax, title=description)
            plt.tight_layout()
            st.pyplot(fig)
        st.balloons()
    plot_selected_features(df, feature_choice)


def plot_selected_features(df, feature_choice):
    if feature_choice == "Close" or feature_choice == "-":
        df["Daily Return"] = df["Close"].pct_change()
        fig, ax = plt.subplots(figsize=(10, 5))
        df["Daily Return"].plot(ax=ax, legend=True, linestyle=":", marker="o")
        ax.set_title("Daily Return")
        st.pyplot(fig)

        fig, ax = plt.subplots()
        ax.hist(df["Daily Return"].dropna(), bins=100, color="red")
        ax.set_title("Distribution of Daily Returns")
        ax.set_xlabel("Daily Return")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)


plot_feature(df)
