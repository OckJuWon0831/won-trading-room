import requests
import json
import os


def send_request(url, endpoint, ticker=None, method="post", data=None):
    headers = {"Content-Type": "application/json"}
    if method == "post":
        full_url = f"{url}{endpoint}"
        response = requests.post(full_url, data=json.dumps(data), headers=headers)
        print(f"Sending POST to {full_url} with data {data}")
    else:
        response = requests.get(url + endpoint, headers=headers)

    print(f"Response Status Code: {response.status_code}")
    if response.status_code != 200:
        print(f"Failed Response: {response.text}")

    return response.json() if response.status_code == 200 else None


def save_to_json(data, ticker, prediction_type):
    if not data:
        print(
            f"No data received for {ticker} {prediction_type}. Skipping JSON creation."
        )
        return

    try:
        data_directory = "/frontend/data"
        os.makedirs(data_directory, exist_ok=True)
        file_path = f"{data_directory}/{ticker}_{prediction_type}.json"
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Saved {ticker} {prediction_type} data to {file_path}")
    except Exception as e:
        print(f"Failed to save data for {ticker} {prediction_type}: {e}")


def schedule_requests():
    url = "http://backend:5050"
    # url = "http://127.0.0.1:5050"  # TODO: This is for local
    tickers = ["AAPL", "AMZN", "META", "GOOG", "NFLX"]

    # Create directory if it doesn't exist
    os.makedirs("/frontend/data", exist_ok=True)

    # Crawl stock data
    crawl_response = send_request(url, "/", method="get")
    if crawl_response:
        print("Stock data crawled successfully.")

    # Process and insert data into DB
    for ticker in tickers:
        response_insert = send_request(
            url,
            "/api/data/insert-processed-data",
            ticker=ticker,
            method="post",
            data={"ticker": ticker},
        )
        if response_insert:
            print(f"Processed data for {ticker} inserted into DB successfully.")

    # Send prediction requests
    for ticker in tickers:
        response_arima = send_request(
            url,
            "/api/predict/arima-predict",
            ticker=ticker,
            data={"ticker": ticker},
            method="post",
        )
        if response_arima:
            save_to_json(response_arima, ticker, "arima")

        response_cnn_lstm = send_request(
            url,
            "/api/predict/cnn-lstm-predict",
            ticker=ticker,
            data={"ticker": ticker},
            method="post",
        )
        if response_cnn_lstm:
            save_to_json(response_cnn_lstm, ticker, "cnn_lstm")


schedule_requests()
