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

last_updated = datetime.datetime.now().strftime("%Y-%m-%d")

st.set_page_config(
    page_title="Won Trading Room",
    page_icon="📈",
)


def streamlit_main():

    st.markdown(
        """
        # 📉 Won Trading Room 📈
        ## COMP3071 Project

        20197749

        Ock Ju Won

        """
    )


if __name__ == "__main__":
    streamlit_main()
