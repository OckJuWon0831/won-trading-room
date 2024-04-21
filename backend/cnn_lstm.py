import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.layers import (  # type: ignore
    Conv1D,
    LSTM,
    Dense,
    Dropout,
    Bidirectional,
    TimeDistributed,
    MaxPooling1D,
    Flatten,
)


def correlation_matrix_eval(data):
    correlation_matrix = data.corr()

    # Drop the columns unrelated to "Close" data
    columns_to_drop = correlation_matrix.index[correlation_matrix["Close"] <= 0.5]
    df_dropped = data.drop(columns=columns_to_drop)

    return df_dropped


# Return data for model training
def data_of_train_test_split(df):
    X = []
    Y = []
    window_size = 100
    for i in range(1, len(df) - window_size - 1, 1):
        first = df.iloc[i, 2]
        temp = []
        temp2 = []
        for j in range(window_size):
            temp.append((df.iloc[i + j, 2] - first) / first)
        temp2.append((df.iloc[i + window_size, 2] - first) / first)
        X.append(np.array(temp).reshape(100, 1))
        Y.append(np.array(temp2).reshape(1, 1))

    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, shuffle=True
    )

    train_X = np.array(x_train)
    test_X = np.array(x_test)
    train_Y = np.array(y_train)
    test_Y = np.array(y_test)

    train_X = train_X.reshape(train_X.shape[0], 1, 100, 1)
    test_X = test_X.reshape(test_X.shape[0], 1, 100, 1)

    return train_X, train_Y, test_X, test_Y


def cnn_lstm():
    model = tf.keras.Sequential()

    # Creating the Neural Network model here...
    # CNN layers
    model.add(
        TimeDistributed(
            Conv1D(64, kernel_size=3, activation="relu", input_shape=(None, 100, 1))
        )
    )
    model.add(TimeDistributed(MaxPooling1D(2)))
    model.add(TimeDistributed(Conv1D(128, kernel_size=3, activation="relu")))
    model.add(TimeDistributed(MaxPooling1D(2)))
    model.add(TimeDistributed(Conv1D(64, kernel_size=3, activation="relu")))
    model.add(TimeDistributed(MaxPooling1D(2)))
    model.add(TimeDistributed(Flatten()))

    # LSTM layers
    model.add(Bidirectional(LSTM(100, return_sequences=True)))
    model.add(Dropout(0.5))
    model.add(Bidirectional(LSTM(100, return_sequences=False)))
    model.add(Dropout(0.5))

    # Final layers
    model.add(Dense(1, activation="linear"))
    model.compile(optimizer="adam", loss="mse", metrics=["mse", "mae"])

    return model


# Return original testing price values and predicted price values for compare_return_and_sharpe
def return_stock_price_prediction(model, train_X, test_X, test_Y, df_dropped):
    predicted = model.predict(test_X)
    test_label = test_Y.reshape(-1, 1)
    predicted = np.array(predicted[:, 0]).reshape(-1, 1)
    len_t = len(train_X)

    for j in range(len_t, len_t + len(test_X)):
        temp = df_dropped.iloc[j, 3]
        test_label[j - len_t] = test_label[j - len_t] * temp + temp
        predicted[j - len_t] = predicted[j - len_t] * temp + temp

    return predicted, test_label


# Return as JSON file for front-end
def compare_return_and_sharpe(predicted, test_label):
    results_df = pd.DataFrame(
        {"Predicted_Price": predicted.flatten(), "Actual_Price": test_label.flatten()}
    )

    results_df["Predicted_Return"] = results_df["Predicted_Price"].pct_change()
    results_df["Actual_Return"] = results_df["Actual_Price"].pct_change()

    results_df["Predicted_Cumulative_Return"] = (
        1 + results_df["Predicted_Return"]
    ).cumprod()
    results_df["Actual_Cumulative_Return"] = (1 + results_df["Actual_Return"]).cumprod()

    #   PREDICTED, ACTUAL_FIN_RTN & SHARPE_RATIO are simple float numbers

    # predicted_final_return = results_df["Predicted_Cumulative_Return"].iloc[-1]
    # actual_final_return = results_df["Actual_Cumulative_Return"].iloc[-1]
    # sharpe_ratio = (
    #     np.mean(results_df["Predicted_Return"])
    #     / np.std(results_df["Predicted_Return"])
    #     * np.sqrt(252.0)
    # )

    # return results_df, predicted_final_return, actual_final_return, sharpe_ratio

    return results_df
