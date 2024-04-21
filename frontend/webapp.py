import streamlit as st
import streamlit.components.v1 as components
from collections import OrderedDict
import os
import pickle
import json
import datetime
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 모델 API endpoint
url = "http://api:5050"  # TODO: Docker 배포 시 설정
# url = 'http://127.0.0.1:5000'
predict_endpoint = "/model/predict/"
shap_endpoint = "/model/calculate-shap-values/"
st.write("HI! Ock Ju Won")
