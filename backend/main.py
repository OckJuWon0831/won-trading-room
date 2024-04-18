from flask import Flask, request, jsonify
import numpy as np
from tool import crawler
from tool import data_preprocessing

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
    return 0


# Using scheduler, it is only conducted once a day
@app.route("/predict/cnn-lstm-predict", methods=["POST"])
def run_cnn_lstm():
    return 0


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


@app.route("/", methods=["POST"])
def index():
    crawler.crawl_stock_data()
    return jsonify({"Success": "Stock Data crawled"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
