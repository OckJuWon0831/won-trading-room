import streamlit as st
import streamlit.components.v1 as components
import json
import datetime
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Evaluation",
    page_icon="📚",
)
last_updated = datetime.datetime.now().strftime("%Y-%m-%d")
ticker_list = ["AAPL", "AMZN", "GOOG", "META", "NFLX"]
model_list = ["ARIMA", "CNN_LSTM"]

stock = st.sidebar.selectbox("Select the ticker among FAANG", ticker_list)
model_type = st.sidebar.selectbox("Select the model", model_list)
file_path = f"./data/{stock.upper()}_{model_type.lower()}.json"


def load_and_process_data(file_path, model_type):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        index = None
        if model_type != "cnn_lstm":
            index = pd.to_datetime(
                [int(x) / 1000 for x in data["Actual_Price"].keys()], unit="s"
            )

        df = pd.DataFrame(
            {
                "Actual Cumulative Return": list(
                    data["Actual_Cumulative_Return"].values()
                ),
                "Predicted Cumulative Return": list(
                    data["Predicted_Cumulative_Return"].values()
                ),
                "Actual Return": list(data["Actual_Return"].values()),
                "Predicted Return": list(data["Predicted_Return"].values()),
            },
            index=index,
        )
        return df
    except Exception as e:
        st.error(f"Error loading and processing data: {e}")
        return None


def calculate_performance_metrics(df):
    predicted_final_return = df["Predicted Cumulative Return"].iloc[-1]
    actual_final_return = df["Actual Cumulative Return"].iloc[-1]
    sharpe_ratio = (
        np.mean(df["Predicted Return"]) / np.std(df["Predicted Return"]) * np.sqrt(252)
    )
    return predicted_final_return, actual_final_return, sharpe_ratio


def main():
    st.title("🔎 Evaluation")
    st.write("📈 Buy & Hold strategy has been adopted for each stock.")
    components.html(
        f"""<p style="text-align:right; font-family:'IBM Plex Sans', sans-serif; font-size:0.8rem; color:#585858";>\
            Last Updated: {last_updated}</p>""",
        height=30,
    )
    df = load_and_process_data(file_path, model_type.lower())
    if df is not None:
        try:
            st.subheader("1️⃣ Actual & Predicted Return")
            st.line_chart(
                df[["Actual Return", "Predicted Return"]],
                color=["#ff0000", "#0067a3"],
            )
            st.subheader("2️⃣ Actual & Predicted Cumulative Return")
            st.line_chart(
                df[["Actual Cumulative Return", "Predicted Cumulative Return"]],
                color=["#ff0000", "#0067a3"],
            )

            predicted_final_return, actual_final_return, sharpe_ratio = (
                calculate_performance_metrics(df)
            )
            st.sidebar.header("Rate of Return Metrics")
            st.sidebar.metric("Predicted Final Return", f"{predicted_final_return:.2%}")
            st.sidebar.metric("Actual Final Return", f"{actual_final_return:.2%}")
            st.sidebar.metric("Sharpe Ratio", f"{sharpe_ratio:.2f}")
        except Exception as e:
            st.error(f"Data visualization error: {e}")


main()
