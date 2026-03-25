import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from model import load_data, train_model, predict_delay

def predict():
    st.set_page_config(page_title="Flight Delay Predictor")
    st.title("Flight Delay Prediction")
    # Load dataset
    df = load_data()
    
    # Train model
    model = train_model(df)

    # simple input form
    st.subheader("Input Flight Distance")
    distance = st.number_input("Distance (km)", min_value=0.0, value=1000.0)

    if st.button("Predict Delay"):

        # Prediction
        delay = predict_delay(model, distance)

        st.subheader("Predicted Arrival Delay")

        st.success(f"{delay:.2f} minutes")



def Visualization():

    # Load dataset
    df = load_data()
    model = train_model(df)

    st.title("Distance vs Arrival Delay")

    fig, ax = plt.subplots()

    ax.scatter(df["distance_km"], df["arrival_delay_min"], alpha=0.5)

    x_range = np.linspace(df.distance_km.min(), df.distance_km.max(), 100)

    y_range = model.predict(
        x_range.reshape(-1,1)
    )

    ax.plot(x_range, y_range)

    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Arrival Delay (minutes)")

    st.pyplot(fig)

st.sidebar.title("Flight Delay Predictor")
option = st.sidebar.radio("Select an option", ("Predict Delay", "Visualize Data"))
if option == "Predict Delay":
    predict()
elif option == "Visualize Data":
    Visualization()

