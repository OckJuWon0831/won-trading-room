from dataclasses import dataclass, field
import typing as t


@dataclass
class IndicatorDescriptions:
    descriptions: t.Dict[str, str] = field(
        default_factory=lambda: {
            "10rasd": "Rolling Average Standard Deviation for 10 days",
            "10sma": "Simple Moving Average for 10 days",
            "14atr": "Average True Range for 14 days",
            "14cci": "Commodity Channel Index for 14 days",
            "14ema": "Exponential Moving Average for 14 days",
            "14lower": "Lower Band of the 14-day Bollinger Bands",
            "14macd": "Moving Average Convergence Divergence for 14 days",
            "14rsi": "Relative Strength Index for 14 days",
            "14rsv": "Raw Stochastic Value for 14 days",
            "14upper": "Upper Band of the 14-day Bollinger Bands",
            "15wpr": "Williams %R for 15 days",
            "1mtm": "One Month Momentum",
            "21atr": "Average True Range for 21 days",
            "21ema": "Exponential Moving Average for 21 days",
            "21lower": "Lower Band of the 21-day Bollinger Bands",
            "21rsi": "Relative Strength Index for 21 days",
            "21rsv": "Raw Stochastic Value for 21 days",
            "21upper": "Upper Band of the 21-day Bollinger Bands",
            "3mtm": "Three Month Momentum",
            "5rasd": "Rolling Average Standard Deviation for 5 days",
            "5sma": "Simple Moving Average for 5 days",
            "60roc": "Rate of Change over 60 days",
            "7atr": "Average True Range for 7 days",
            "7ema": "Exponential Moving Average for 7 days",
            "7lower": "Lower Band of the 7-day Bollinger Bands",
            "7macd": "Moving Average Convergence Divergence for 7 days",
            "7rsi": "Relative Strength Index for 7 days",
            "7rsv": "Raw Stochastic Value for 7 days",
            "7upper": "Upper Band of the 7-day Bollinger Bands",
            "Adj Close": "Adjusted Close Price",
            "Close": "Closing Price",
            "FT_100components": "Fourier Transform components over 100 days",
            "FT_27components": "Fourier Transform components over 27 days",
            "FT_3components": "Fourier Transform components over 3 days",
            "FT_6components": "Fourier Transform components over 6 days",
            "FT_81components": "Fourier Transform components over 81 days",
            "FT_9components": "Fourier Transform components over 9 days",
            "High": "High Price of the day",
            "Low": "Low Price of the day",
            "Open": "Opening Price",
            "log_change": "Logarithmic Daily Price Change",
            "next_rtn": "Next Day Return",
            "pct_change": "Percentage Change",
            "Volume": "Trading Volume",
        }
    )
