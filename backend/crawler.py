import pymysql
from sqlalchemy import create_engine
import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# Load MySQL connection details from environment variables
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = "localhost"
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_CHARSET = "utf8mb4"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
)
conn = pymysql.connect(
    user=DB_USER, passwd=DB_PASSWORD, host=DB_HOST, db=DB_NAME, charset=DB_CHARSET
)

# Define the tickers and the start date for data retrieval
tickers_for_companies = ["AAPL", "GOOG", "META", "NFLX", "AMZN"]
start_date = "2009-12-31"
end_date = datetime.now().date()

for ticker in tickers_for_companies:
    df = yf.download(ticker, start=start_date, end=end_date)

    # Generate SQL query
    with conn.cursor() as cursor:
        for index, row in df.iterrows():
            sql = f"""
                INSERT INTO {ticker} (Date, Open, High, Low, Close, `Adj Close`, Volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    Open=VALUES(Open),
                    High=VALUES(High),
                    Low=VALUES(Low),
                    Close=VALUES(Close),
                    `Adj Close`=VALUES(`Adj Close`),
                    Volume=VALUES(Volume)
            """
            cursor.execute(
                sql,
                (
                    index.strftime("%Y-%m-%d"),
                    row["Open"],
                    row["High"],
                    row["Low"],
                    row["Close"],
                    row["Adj Close"],
                    row["Volume"],
                ),
            )

    # Commit the transaction
    conn.commit()

# Close the MySQL connection
conn.close()
