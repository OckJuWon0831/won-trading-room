import numpy as np
import pandas as pd


class Generator:
    def __init__(self):
        pass

    # Simple Moving Average
    def SMA(self, data, windows):
        return data.rolling(window=windows).mean()

    # Exponential Moving Average
    def EMA(self, data, windows):
        return data.ewm(span=windows, adjust=False).mean()

    # Moving Average Convergence Divergence
    def MACD(self, data, long, short, windows):
        ema_fast = data.ewm(span=short, adjust=False).mean()
        ema_slow = data.ewm(span=long, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=windows, adjust=False).mean()
        return macd, signal

    # Relative Strength Index
    def RSI(self, data, windows):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)
        avg_gain = gain.rolling(window=windows).mean()
        avg_loss = loss.rolling(window=windows).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    # Average True Range
    def ATR(self, high, low, close, windows):
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        return true_range.rolling(window=windows).mean()

    # Bollinger Bands
    def BollingerBands(self, data, windows):
        sma = data.rolling(window=windows).mean()
        std = data.rolling(window=windows).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        return upper_band, lower_band

    def CCI(self, high, low, close, windows):
        tp = (high + low + close) / 3
        cci = (tp - tp.rolling(window=windows).mean()) / (
            0.015 * tp.rolling(window=windows).std()
        )
        return cci

    def MOM(self, data, timeperiod):
        return data.diff(periods=timeperiod)

    def ROC(self, data, timeperiod):
        return data.pct_change(periods=timeperiod) * 100

    def WILLR(self, high, low, close, timeperiod):
        highest_high = high.rolling(window=timeperiod).max()
        lowest_low = low.rolling(window=timeperiod).min()
        willr = -100 * ((highest_high - close) / (highest_high - lowest_low))
        return willr

    # Raw Stochastic Value
    def RSV(self, data, windows):
        min_ = data.rolling(window=windows).min()
        max_ = data.rolling(window=windows).max()
        return 100 * (data - min_) / (max_ - min_)

    # Rolling Average Standard Deviation
    def RASD(self, data, windows):
        return data.rolling(window=windows).std().rolling(window=windows).mean()
