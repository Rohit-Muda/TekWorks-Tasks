import pandas as pd
from sklearn.linear_model import LinearRegression

# Load dataset
def load_data():
    df = pd.read_csv("flight_delay_linear_regression_dataset.csv")
    return df


def train_model(df):

    X = df[["distance_km"]]
    y = df["arrival_delay_min"]

    model = LinearRegression()
    model.fit(X, y)

    return model


def predict_delay(model, distance):

    input_df = pd.DataFrame({
        "distance_km": [distance]
    })

    prediction = model.predict(input_df)

    return prediction[0]