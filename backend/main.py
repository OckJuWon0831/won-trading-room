from flask import Flask, request, jsonify
import numpy as np
from tool import crawler
from tool import data_preprocessing

import pandas as pd
import pymysql
from datetime import datetime
import os
import json


app = Flask(__name__)

DB_USER = "root"
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
DB_HOST = "stock_db"
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_CHARSET = "utf8mb4"


@app.route("/data/arima-predict", methods=["POST"])
def get_arima():
    return 0


@app.route("/data/cnn-lstm-predict", methods=["POST"])
def get_cnn_lstm():
    return 0


@app.route("/data/include-technical-indicators", methods=["POST"])
def get_data():
    data = request.get_json()
    ticker = data.get("ticker").upper()

    if ticker not in ["AAPL", "AMZN", "META", "GOOG", "NFLX"]:
        return jsonify({"error": "Invalid ticker"}), 400

    conn = pymysql.connect(
        user=DB_USER, passwd=DB_PASSWORD, host=DB_HOST, db=DB_NAME, charset=DB_CHARSET
    )

    sql = f"SELECT * FROM `{ticker}`"
    df = pd.read_sql(sql, conn)

    processed_df = data_preprocessing.data_preprocessing(df)

    response = processed_df.to_json(orient="records")
    conn.close()
    return jsonify(json.loads(response))


@app.route("/", methods=["POST"])
def index():
    crawler.crawl_stock_data()
    return jsonify({"Success!": "Stock Data crawled"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
