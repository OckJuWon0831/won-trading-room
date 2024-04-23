from flask import Flask, request, jsonify, session
import numpy as np
from tool import crawler
from tool import data_preprocessing
from model import cnn_lstm
from model import arima
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from datetime import datetime
import os
import json

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

DB_USER = "root"
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
DB_HOST = "stock_db"
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_CHARSET = "utf8mb4"
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DB_URL)


# Using scheduler, it is only conducted once a day
@app.route("/api/predict/arima-predict", methods=["POST"])
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
@app.route("/api/predict/cnn-lstm-predict", methods=["POST"])
def run_cnn_lstm():
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
@app.route("/api/data/insert-processed-data", methods=["POST"])
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
@app.route("/api/data/include-technical-indicators", methods=["POST"])
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

    response = processed_df.to_json(orient="records", date_format="epoch")
    conn.close()
    return jsonify(json.loads(response))


# @app.route("/api/register", methods=["POST"])
# def register():
#     user_data = request.get_json()
#     user_id = user_data["ID"]
#     user_pw = generate_password_hash(user_data["PASSWORD"])
#     try:
#         conn = engine.connect()
#         trans = conn.begin()

#         check_user_sql = text("SELECT ID FROM USERS WHERE ID = :id")
#         existing_user = conn.execute(check_user_sql, {"id": user_id}).fetchone()

#         if existing_user:
#             trans.rollback()
#             conn.close()
#             return (
#                 jsonify({"status": "error", "message": "User ID already exists"}),
#                 409,
#             )

#         sql = text("INSERT INTO USERS (ID, PASSWORD) VALUES (:id, :password)")
#         conn.execute(sql, {"id": user_id, "password": user_pw})
#         trans.commit()
#         conn.close()
#         return jsonify({"status": "success"}), 200
#     except Exception as e:
#         trans.rollback()
#         conn.close()
#         return jsonify({"status": "error", "message": str(e)}), 500


# @app.route("/api/login", methods=["POST"])
# def login():
#     login_data = request.get_json()
#     user_id = login_data["ID"]
#     user_pw = login_data["PASSWORD"]
#     try:
#         with engine.connect() as conn:
#             sql = text("SELECT PASSWORD FROM USERS WHERE ID = :id")
#             result = conn.execute(sql, {"id": user_id}).fetchone()
#             if result and check_password_hash(result[0], user_pw):
#                 session["login_user"] = user_id
#                 return jsonify({"status": "success"}), 200
#             else:
#                 return (
#                     jsonify({"status": "failed", "message": "Invalid credentials"}),
#                     401,
#                 )
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/", methods=["GET"])
def index():
    crawler.crawl_stock_data()
    return jsonify({"Success": "Stock Data crawled"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
