from flask import Flask, request, jsonify
import pandas as pd
import helper
import pymysql

app = Flask(__name__)


if __name__ == "__main__":
    app.run(debug=True)
