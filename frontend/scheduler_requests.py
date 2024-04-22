import requests
import json
import os
import time

import threading

# ORIGINAL CODE ##


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


# For threading
def preprocessing_threaded(url, ticker):
    response_insert = send_request(
        url,
        "/api/data/insert-processed-data",
        ticker=ticker,
        method="post",
        data={"ticker": ticker},
    )
    if response_insert:
        print(f"Processed data for {ticker} inserted into DB successfully.")


def schedule_requests():
    # For assessing elapsed time
    start_time = time.time()

    url = "http://backend:5050"
    # url = "http://127.0.0.1:5050"  # TODO: This is for local
    tickers = ["AAPL", "AMZN", "META", "GOOG", "NFLX"]
    threads = []

    # Create directory if it doesn't exist
    os.makedirs("/frontend/data", exist_ok=True)

    # Crawl stock data
    crawl_response = send_request(url, "/", method="get")
    if crawl_response:
        print("Stock data crawled successfully.")

    for ticker in tickers:
        thread = threading.Thread(target=preprocessing_threaded, args=(url, ticker))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

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

    # For assessing elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")


schedule_requests()

## Multithreading CODE ##

# def process_ticker(url, ticker):
#     # Process and insert data into DB
#     response_insert = send_request(
#         url,
#         "/api/data/insert-processed-data",
#         ticker=ticker,
#         method="post",
#         data={"ticker": ticker},
#     )
#     if response_insert:
#         print(f"Processed data for {ticker} inserted into DB successfully.")

#     # Send prediction requests
#     response_arima = send_request(
#         url,
#         "/api/predict/arima-predict",
#         ticker=ticker,
#         data={"ticker": ticker},
#         method="post",
#     )
#     if response_arima:
#         save_to_json(response_arima, ticker, "arima")

#     response_cnn_lstm = send_request(
#         url,
#         "/api/predict/cnn-lstm-predict",
#         ticker=ticker,
#         data={"ticker": ticker},
#         method="post",
#     )
#     if response_cnn_lstm:
#         save_to_json(response_cnn_lstm, ticker, "cnn_lstm")


# def scheduler_requests():
#     start_time = time.time()

#     url = "http://backend:5050"
#     tickers = ["AAPL", "AMZN", "META", "GOOG", "NFLX"]
#     threads = []

#     # Create directory if it doesn't exist
#     os.makedirs("/frontend/data", exist_ok=True)

#     # Crawl stock data
#     crawl_response = send_request(url, "/", method="get")
#     if crawl_response:
#         print("Stock data crawled successfully.")

#     for ticker in tickers:
#         thread = threading.Thread(target=process_ticker, args=(url, ticker))
#         threads.append(thread)
#         thread.start()

#     for thread in threads:
#         thread.join()

#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"Total execution time of multi-threading: {elapsed_time:.2f} seconds")

# scheduler_requests()


## ASYNC CODE ##
# async def send_request_async(
#     session, url, endpoint, ticker=None, method="post", data=None
# ):
#     headers = {"Content-Type": "application/json"}
#     timeout = aiohttp.ClientTimeout(total=1000)
#     try:
#         if method.lower() == "post":
#             full_url = f"{url}{endpoint}"
#             async with session.post(
#                 full_url, json=data, headers=headers, timeout=timeout
#             ) as response:
#                 print(f"Sending POST to {full_url} with data {data}")
#                 if response.status != 200:
#                     print(f"Failed Response: {await response.text()}")
#                 return await response.json() if response.status == 200 else None
#         else:
#             async with session.get(
#                 url + endpoint, headers=headers, timeout=timeout
#             ) as response:
#                 print(f"Sending GET to {url + endpoint}")
#                 if response.status != 200:
#                     print(f"Failed Response: {await response.text()}")
#                 return await response.json() if response.status == 200 else None
#     except asyncio.TimeoutError:
#         print("Request timed out")
#         return None


# async def save_to_json_async(data, ticker, prediction_type):
#     if not data:
#         print(
#             f"No data received for {ticker} {prediction_type}. Skipping JSON creation."
#         )
#         return

#     try:
#         data_directory = "/frontend/data"
#         os.makedirs(data_directory, exist_ok=True)
#         file_path = f"{data_directory}/{ticker}_{prediction_type}.json"
#         with open(file_path, "w") as json_file:
#             json.dump(data, json_file, indent=4)
#         print(f"Saved {ticker} {prediction_type} data to {file_path}")
#     except Exception as e:
#         print(f"Failed to save data for {ticker} {prediction_type}: {e}")


# async def scheduler_requests_async():
#     start_time = time.time()
#     url = "http://backend:5050"
#     tickers = ["AAPL", "AMZN", "META", "GOOG", "NFLX"]

#     # Create directory if it doesn't exist
#     os.makedirs("/frontend/data", exist_ok=True)

#     async with aiohttp.ClientSession() as session:
#         # Crawl stock data
#         crawl_response = await send_request_async(session, url, "/", method="get")
#         if crawl_response:
#             print("Stock data crawled successfully.")

#             # Insert processed data (synchronous in async context)
#             for ticker in tickers:
#                 response_insert = await send_request_async(
#                     session,
#                     url,
#                     "/api/data/insert-processed-data",
#                     ticker=ticker,
#                     method="post",
#                     data={"ticker": ticker},
#                 )
#                 if response_insert:
#                     print(f"Processed data for {ticker} inserted into DB successfully.")

#             # Once all synchronous tasks are completed, proceed with the predictions
#             await asyncio.gather(
#                 *(
#                     process_ticker_predictions_async(session, url, ticker)
#                     for ticker in tickers
#                 )
#             )

#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"Total execution time of async: {elapsed_time:.2f} seconds")


# async def process_ticker_predictions_async(session, url, ticker):
#     # Only prediction requests are handled here
#     response_arima = await send_request_async(
#         session,
#         url,
#         "/api/predict/arima-predict",
#         ticker=ticker,
#         method="post",
#         data={"ticker": ticker},
#     )
#     if response_arima:
#         await save_to_json_async(response_arima, ticker, "arima")

#     response_cnn_lstm = await send_request_async(
#         session,
#         url,
#         "/api/predict/cnn-lstm-predict",
#         ticker=ticker,
#         method="post",
#         data={"ticker": ticker},
#     )
#     if response_cnn_lstm:
#         await save_to_json_async(response_cnn_lstm, ticker, "cnn_lstm")

# asyncio.run(scheduler_requests_async())


# ## MULTI-processing ##
# def send_request(url, endpoint, ticker=None, method="post", data=None):
#     headers = {"Content-Type": "application/json"}
#     try:
#         full_url = f"{url}{endpoint}"
#         if method.lower() == "post":
#             response = requests.post(full_url, json=data, headers=headers)
#         else:
#             response = requests.get(full_url, headers=headers)

#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(
#                 f"Failed to send {method.upper()} request to {full_url}: {response.text}"
#             )
#             return None
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return None


# def save_to_json(data, ticker, prediction_type):
#     if data is None:
#         print(
#             f"No data received for {ticker} {prediction_type}. Skipping JSON creation."
#         )
#         return

#     try:
#         data_directory = "/frontend/data"
#         os.makedirs(data_directory, exist_ok=True)
#         file_path = f"{data_directory}/{ticker}_{prediction_type}.json"
#         with open(file_path, "w") as json_file:
#             json.dump(data, json_file, indent=4)
#         print(f"Saved {ticker} {prediction_type} data to {file_path}")
#     except Exception as e:
#         print(f"Failed to save data for {ticker} {prediction_type}: {e}")


# def perform_predictions(ticker):
#     url = "http://backend:5050"
#     # Perform ARIMA prediction
#     response_arima = send_request(
#         url,
#         "/api/predict/arima-predict",
#         ticker,
#         method="post",
#         data={"ticker": ticker},
#     )
#     if response_arima:
#         save_to_json(response_arima, ticker, "arima")

#     # Perform CNN-LSTM prediction
#     response_cnn_lstm = send_request(
#         url,
#         "/api/predict/cnn-lstm-predict",
#         ticker,
#         method="post",
#         data={"ticker": ticker},
#     )
#     if response_cnn_lstm:
#         save_to_json(response_cnn_lstm, ticker, "cnn_lstm")


# def scheduler_requests():
#     start_time = time.time()
#     tickers = ["AAPL", "AMZN", "META", "GOOG", "NFLX"]
#     url = "http://backend:5050"

#     # Create directory if it doesn't exist
#     os.makedirs("/frontend/data", exist_ok=True)

#     crawl_response = send_request(url, "/", method="get")
#     if crawl_response:
#         print("Stock data crawled successfully.")

#     # Crawl and preprocess data first
#     for ticker in tickers:
#         send_request(
#             url,
#             "/api/data/insert-processed-data",
#             ticker,
#             method="post",
#             data={"ticker": ticker},
#         )

#     # Set up a pool of processes for predictions
#     with multiprocessing.Pool(processes=5) as pool:
#         pool.map(perform_predictions, tickers)

#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print(f"Total execution time with multiprocessing: {elapsed_time:.2f} seconds")

# scheduler_requests()
