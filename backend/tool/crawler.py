import pymysql
from datetime import datetime
import os
import yfinance as yf

DB_USER = "root"
DB_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
DB_HOST = "stock_db"
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_CHARSET = "utf8mb4"

tickers_for_companies = ["AAPL", "GOOG", "META", "NFLX", "AMZN"]
start_date = "2009-12-31"
end_date = datetime.now().date()


def crawl_stock_data():
    conn = pymysql.connect(
        user=DB_USER,
        passwd=DB_PASSWORD,
        host=DB_HOST,
        db=DB_NAME,
        charset=DB_CHARSET,
    )

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
