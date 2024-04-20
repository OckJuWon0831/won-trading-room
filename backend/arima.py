import numpy as np
import pandas as pd
import pmdarima as pm
from pmdarima.arima import ndiffs
from statsmodels.tsa.arima_model import ARIMA


def get_n_diffs(data):
    n_diffs = ndiffs(data, alpha=0.05, test="adf", max_d=6)
    print(f"Estimated d = {n_diffs}")
    return n_diffs


def arima(train_data, n_diffs):
    model_fit = pm.auto_arima(
        y=train_data,
        d=n_diffs,
        start_p=0,
        max_p=2,
        start_q=0,
        max_q=2,
        m=1,
        seasonal=False,
        stepwise=True,
        trace=True,
    )
    return model_fit


# forecast
def forecast_n_step(model, n=1):
    fc, conf_int = model.predict(n_periods=n, return_conf_int=True)
    return (fc.tolist()[0:n], np.asarray(conf_int).tolist()[0:n])


def forecast(len, model, index, data=None):
    y_pred = []
    pred_upper = []
    pred_lower = []

    if data is not None:
        for new_ob in data:
            fc, conf = forecast_n_step(model)
            y_pred.append(fc[0])
            pred_upper.append(conf[0][1])
            pred_lower.append(conf[0][0])
            model.update(new_ob)
    else:
        for i in range(len):
            fc, conf = forecast_n_step(model)
            y_pred.append(fc[0])
            pred_upper.append(conf[0][1])
            pred_lower.append(conf[0][0])
            model.update(fc[0])
    return pd.Series(y_pred, index=index), pred_upper, pred_lower


# Return as JSON file for front-end
def compare_return_and_sharpe(fc, test_data):
    results_df = pd.DataFrame(
        {
            "Predicted_Price": fc,
            "Actual_Price": test_data,
        }
    )

    results_df["Predicted_Return"] = results_df["Predicted_Price"].pct_change()
    results_df["Actual_Return"] = results_df["Actual_Price"].pct_change()

    results_df["Predicted_Cumulative_Return"] = (
        1 + results_df["Predicted_Return"]
    ).cumprod()
    results_df["Actual_Cumulative_Return"] = (1 + results_df["Actual_Return"]).cumprod()

    return results_df
