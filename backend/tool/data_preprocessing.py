from tool import technical_generator
import numpy as np
import pandas as pd


def data_preprocessing(df):
    df["pct_change"] = (df["Close"] - df["Close"].shift(1)) / df["Close"].shift(1)
    df["log_change"] = np.log(df["Close"] / df["Close"].shift(1))

    Generator = technical_generator.Generator()

    # Moving Average
    df["7ema"] = Generator.EMA(df["Close"], 7)
    df["14ema"] = Generator.EMA(df["Close"], 14)
    df["21ema"] = Generator.EMA(df["Close"], 21)
    df["5sma"] = Generator.SMA(df["Close"], 5)
    df["10sma"] = Generator.SMA(df["Close"], 10)

    # RASD - Rolling Average Standard Deviation
    df["5rasd"] = Generator.RASD(df["Close"], 5)
    df["10rasd"] = Generator.RASD(df["Close"], 10)

    # MACD calculations
    df["7macd"] = Generator.MACD(df["Close"], 3, 11, 7)[0]  # Only taking the MACD value
    df["14macd"] = Generator.MACD(df["Close"], 7, 21, 14)[0]

    # RSI calculations
    df["7rsi"] = Generator.RSI(df["Close"], 7)
    df["14rsi"] = Generator.RSI(df["Close"], 14)
    df["21rsi"] = Generator.RSI(df["Close"], 21)

    # ATR calculations
    df["7atr"] = Generator.ATR(df["High"], df["Low"], df["Close"], 7)
    df["14atr"] = Generator.ATR(df["High"], df["Low"], df["Close"], 14)
    df["21atr"] = Generator.ATR(df["High"], df["Low"], df["Close"], 21)

    # Bollinger Bands calculations
    df["7upper"], df["7lower"] = Generator.BollingerBands(df["Close"], 7)
    df["14upper"], df["14lower"] = Generator.BollingerBands(df["Close"], 14)
    df["21upper"], df["21lower"] = Generator.BollingerBands(df["Close"], 21)

    # Momentum (MTM) calculations
    df["1mtm"] = Generator.MOM(df["Close"], 1)
    df["3mtm"] = Generator.MOM(df["Close"], 3)

    # Rate of Change (ROC) calculation
    df["60roc"] = Generator.ROC(df["Close"], 60)

    # Raw Stochastic Value (RSV)
    df["7rsv"] = Generator.RSV(df["Close"], 7)
    df["14rsv"] = Generator.RSV(df["Close"], 14)
    df["21rsv"] = Generator.RSV(df["Close"], 21)

    # 9.WPR : william percent range (Williams' %R)
    df["15wpr"] = Generator.WILLR(df["High"], df["Low"], df["Close"], 14)

    # Commodity Channel Index (CCI)
    df["14cci"] = Generator.CCI(df["High"], df["Low"], df["Close"], 14)

    # Next return
    df["next_rtn"] = df["Close"] / df["Open"] - 1
    df = df.dropna()

    # Fourier transform
    close_fft = np.fft.fft(np.asarray(df["Close"].tolist()))
    fft_df = pd.DataFrame({"fft": close_fft})
    fft_df["absolute"] = fft_df["fft"].apply(lambda x: np.abs(x))
    fft_df["angle"] = fft_df["fft"].apply(lambda x: np.angle(x))

    fft_list = np.asarray(fft_df["fft"].tolist())
    for num_ in [3, 6, 9, 27, 81, 100]:
        fft_list_m10 = np.copy(fft_list)
        fft_list_m10[num_:-num_] = 0
        df[f"FT_{num_}components"] = np.fft.ifft(fft_list_m10)

    df["FT_3components"] = df["FT_3components"].astype("float")
    df["FT_6components"] = df["FT_6components"].astype("float")
    df["FT_9components"] = df["FT_9components"].astype("float")
    df["FT_27components"] = df["FT_27components"].astype("float")
    df["FT_81components"] = df["FT_81components"].astype("float")
    df["FT_100components"] = df["FT_100components"].astype("float")

    return df
