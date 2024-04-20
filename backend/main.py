from flask import Flask, request, jsonify
import numpy as np
from tool import crawler
from tool import data_preprocessing
import cnn_lstm
import arima

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime
import os
import json


app = Flask(__name__)

DB_USER = "root"
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
DB_HOST = "stock_db"
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_CHARSET = "utf8mb4"
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DB_URL)


# Using scheduler, it is only conducted once a day
@app.route("/predict/arima-predict", methods=["POST"])
def run_arima():
    try:
        data = request.get_json()
        ticker = data.get("ticker").upper()

        if ticker not in ["AAPL", "AMZN", "META", "GOOG", "NFLX"]:
            return jsonify({"Error": "Invalid ticker"}), 400

        with engine.begin() as conn:
            sql = f"SELECT * FROM `{ticker}_processed`"
            df = pd.read_sql(sql, conn)
            df["Date"] = pd.to_datetime(df["Date"])
            df.set_index("Date", inplace=True)

        df = df["Close"]
        df_dropped = df.dropna()
        n_diffs = arima.get_n_diffs(df_dropped)

        train_data, test_data = (
            df_dropped[: int(len(df_dropped) * 0.8)],
            df_dropped[int(len(df_dropped) * 0.8) :],
        )
        arima_model = arima.arima(train_data, n_diffs)
        fc, upper, lower = arima.forecast(
            len(test_data), arima_model, test_data.index, data=test_data
        )
        # lower_series = pd.Series(lower, index=test_data.index)
        # upper_series = pd.Series(upper, index=test_data.index)

        RESULT_DF = arima.compare_return_and_sharpe(fc, test_data)
        response = RESULT_DF.to_json(orient="columns")
        return jsonify(json.loads(response))

    except SQLAlchemyError as e:
        return jsonify({"Error": str(e)}), 500
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


# Using scheduler, it is only conducted once a day
@app.route("/predict/cnn-lstm-predict", methods=["GET"])
def run_cnn_lstm():
    try:
        data = request.get_json()
        ticker = data.get("ticker").upper()

        if ticker not in ["AAPL", "AMZN", "META", "GOOG", "NFLX"]:
            return jsonify({"Error": "Invalid ticker"}), 400

        with engine.begin() as conn:
            sql = f"SELECT * FROM `{ticker}_processed`"
            df = pd.read_sql(sql, conn)
            df["Date"] = pd.to_datetime(df["Date"])  # Date 칼럼을 datetime으로 변환
            df.set_index("Date", inplace=True)  # Date 칼럼을 인덱스로 설정

        df_dropped = cnn_lstm.correlation_matrix_eval(df)
        train_X, train_Y, test_X, test_Y = cnn_lstm.data_of_train_test_split(df_dropped)
        model = cnn_lstm.cnn_lstm()
        model.fit(
            train_X,
            train_Y,
            validation_data=(test_X, test_Y),
            epochs=40,
            batch_size=40,
            verbose=1,
            shuffle=False,
        )

        #
        #   RESULT_DF is already a processed dataframe
        #
        predicted, test_label = cnn_lstm.return_stock_price_prediction(
            model, train_X, test_X, test_Y, df_dropped
        )
        RESULT_DF = cnn_lstm.compare_return_and_sharpe(predicted, test_label)
        response = RESULT_DF.to_json(orient="columns")
        return jsonify(json.loads(response))

    except SQLAlchemyError as e:
        return jsonify({"Error": str(e)}), 500
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


# Insert processed data in DB server
@app.route("/data/insert-processed-data", methods=["POST"])
def insert_data():
    try:
        data = request.get_json()
        ticker = data.get("ticker").upper()

        if ticker not in ["AAPL", "AMZN", "META", "GOOG", "NFLX"]:
            return jsonify({"Error": "Invalid ticker"}), 400

        with engine.begin() as conn:
            sql = f"SELECT * FROM `{ticker}`"
            df = pd.read_sql(sql, conn)

            processed_df = data_preprocessing.data_preprocessing(df)

            processed_df.to_sql(
                name=f"{ticker}_processed", con=conn, if_exists="replace", index=False
            )

            if processed_df.empty:
                return jsonify({"Error": "Processed data is empty"}), 400
            else:
                return jsonify({"Success!": "Processed data inserted"}), 200

    except SQLAlchemyError as e:
        return jsonify({"Error": str(e)}), 500
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


# Get the raw processed data for each company
@app.route("/data/include-technical-indicators", methods=["POST"])
def get_data():
    data = request.get_json()
    ticker = data.get("ticker").upper()

    if ticker not in ["AAPL", "AMZN", "META", "GOOG", "NFLX"]:
        return jsonify({"Error": "Invalid ticker"}), 400

    conn = pymysql.connect(
        user=DB_USER, passwd=DB_PASSWORD, host=DB_HOST, db=DB_NAME, charset=DB_CHARSET
    )

    sql = f"SELECT * FROM `{ticker}`"
    df = pd.read_sql(sql, conn)

    processed_df = data_preprocessing.data_preprocessing(df)

    response = processed_df.to_json(orient="records", date_format="iso")
    conn.close()
    return jsonify(json.loads(response))


@app.route("/", methods=["GET"])
def index():
    crawler.crawl_stock_data()
    return jsonify({"Success": "Stock Data crawled"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
