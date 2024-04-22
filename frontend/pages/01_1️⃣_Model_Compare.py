import streamlit as st
import streamlit.components.v1 as components
from collections import OrderedDict
import os
import pickle
import json
import datetime
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

last_updated = datetime.datetime.now().strftime("%Y-%m-%d")
st.set_page_config(
    page_title="Model Comparison",
    page_icon="🤺",
)


def timestamp_to_date_updated(timestamp):
    return datetime.datetime.fromtimestamp(
        int(timestamp) / 1000, tz=datetime.timezone.utc
    ).strftime("%Y-%m-%d")


@st.cache_data
def load_and_process_data(file_path, model_type):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        if data and isinstance(data, dict) and "Actual_Price" in data:
            df = pd.DataFrame(
                list(data["Actual_Price"].items()),
                columns=["timestamp", "value"],
            )
            df["timestamp"] = df["timestamp"].apply(
                lambda x: pd.to_datetime(timestamp_to_date_updated(x))
            )
        else:
            df = pd.DataFrame()

        if model_type == "arima" and not df.empty:
            df.set_index("timestamp", inplace=True)
        elif model_type == "cnn_lstm" and not df.empty:
            df.reset_index(drop=True, inplace=True)
    except Exception as e:
        st.error(f"Error: {e}")
        df = pd.DataFrame()

    return df


def main():
    st.title("CNN-LSTM 🆚 ARIMA")

    components.html(
        f"""<p style="text-align:right; font-family:'IBM Plex Sans', sans-serif; font-size:0.8rem; color:#585858";>\
            Last Updated: {last_updated}</p>""",
        height=30,
    )

    stock = st.selectbox(
        "Select the ticker among FAANG", ["AAPL", "AMZN", "GOOG", "META", "NFLX"]
    )
    model_type = st.selectbox("Select the model", ["ARIMA", "CNN_LSTM"])

    file_path = f"./data/{stock.upper()}_{model_type.lower()}.json"

    data = load_and_process_data(file_path, model_type.lower())

    if not data.empty and "value" in data.columns:
        st.line_chart(data["value"])
    else:
        st.error("'Actual_Price' field is empty of data")


main()
