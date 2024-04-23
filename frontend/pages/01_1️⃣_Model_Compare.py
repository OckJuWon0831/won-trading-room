import streamlit as st
import streamlit.components.v1 as components
import json
import datetime
import pandas as pd

# Set the page configuration
st.set_page_config(page_title="Model Comparison", page_icon="🤺")
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

        if model_type == "cnn_lstm":
            actual_df = pd.DataFrame(
                list(data["Actual_Price"].values()),
                columns=["Actual Price"],
            )
            predicted_df = pd.DataFrame(
                list(data["Predicted_Price"].values()),
                columns=["Predicted Price"],
            )
        else:
            actual_df = pd.DataFrame(
                list(data["Actual_Price"].values()),
                index=pd.to_datetime(
                    [int(x) / 1000 for x in data["Actual_Price"].keys()], unit="s"
                ),
                columns=["Actual Price"],
            )
            predicted_df = pd.DataFrame(
                list(data["Predicted_Price"].values()),
                index=pd.to_datetime(
                    [int(x) / 1000 for x in data["Predicted_Price"].keys()], unit="s"
                ),
                columns=["Predicted Price"],
            )

        df = pd.merge(actual_df, predicted_df, left_index=True, right_index=True)
        return df
    except Exception as e:
        st.error(f"Error loading and processing data: {e}")


def main():
    st.title("CNN-LSTM 🆚 ARIMA")
    st.write("Customized Machine Learning Model & Statistical Analysis Model")
    components.html(
        f"""<p style="text-align:right; font-family:'IBM Plex Sans', sans-serif; font-size:0.8rem; color:#585858";>\
            Last Updated: {last_updated}</p>""",
        height=30,
    )
    df = load_and_process_data(file_path, model_type.lower())
    st.subheader("Price($) comparisons 💰")

    try:
        st.line_chart(
            df[["Actual Price", "Predicted Price"]],
            color=["#ff0000", "#0067a3"],
        )
    except Exception as e:
        st.error(f"Data visualization error: {e}")


main()
