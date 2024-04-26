import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import datetime
from indicator_descriptions import IndicatorDescriptions
import matplotlib.pyplot as plt

last_updated = datetime.datetime.now().strftime("%Y-%m-%d")

plt.style.use("ggplot")

url = "http://backend:5050"
include_technical_indicators = "/api/data/include-technical-indicators"
ticker_list = ["AAPL", "AMZN", "GOOG", "META", "NFLX"]

st.set_page_config(page_title="Technical Indicators", page_icon="🔢")


def timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp) / 1000).strftime("%Y-%m-%d")


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


selected_ticker = st.sidebar.selectbox("Select the ticker among FAANG", ticker_list)
df = get_technical_indicators(selected_ticker)


def main(df):

    descriptions = IndicatorDescriptions().descriptions

    st.title(f"🚀 Technical indicators of {selected_ticker}")
    st.write("These technical indicators were considered as features.")

    components.html(
        f"""<p style="text-align:right; font-family:'IBM Plex Sans', sans-serif; font-size:0.8rem; color:#585858";>\
            Last Updated: {last_updated}</p>""",
        height=30,
    )
    feature_choices = ["-"] + list(df.columns)
    st.sidebar.header("Technical indicators before EDA")
    feature_choice = st.sidebar.selectbox(
        "Select the feature to see", feature_choices, index=0
    )

    if feature_choice != "-":
        description = descriptions.get(feature_choice, feature_choice)
        st.subheader(description)
        st.line_chart(df[feature_choice])
    else:
        for column in df.columns:
            description = descriptions.get(column, column)
            st.subheader(description)
            st.line_chart(df[column])
    if feature_choice in ["Close", "-"]:
        plot_features(df, feature_choice)


def plot_features(df, feature_choice):
    if feature_choice == "Close" or feature_choice == "-":
        df["Daily Return"] = df["Close"].pct_change()
        st.subheader("Daily Return")
        st.line_chart(df["Daily Return"].dropna())

        fig, ax = plt.subplots()
        ax.set_title("Distribution of Daily Returns", fontsize=20)
        ax.hist(df["Daily Return"].dropna(), bins=80, color="blue")
        ax.set_title("Distribution of Daily Returns")
        ax.set_xlabel("Daily Return")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)


main(df)
