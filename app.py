import joblib
import pandas as pd
import streamlit as st


def load_artifacts():
    model = joblib.load("knn_heart_model.pkl")
    scaler = joblib.load("heart_scaler.pkl")
    expected_columns = joblib.load("heart_columns.pkl")
    return model, scaler, expected_columns


def build_raw_input(
    age,
    sex,
    chest_pain,
    resting_bp,
    cholesterol,
    fasting_bs,
    resting_ecg,
    max_hr,
    exercise_angina,
    oldpeak,
    st_slope,
):
    return {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,
        f"Sex_{sex}": 1,
        f"ChestPainType_{chest_pain}": 1,
        f"RestingECG_{resting_ecg}": 1,
        f"ExerciseAngina_{exercise_angina}": 1,
        f"ST_Slope_{st_slope}": 1,
    }


def align_input_frame(raw_input, expected_columns):
    input_df = pd.DataFrame([raw_input])
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    return input_df[expected_columns]


def predict_risk_label(raw_input, expected_columns, scaler, model):
    input_df = align_input_frame(raw_input, expected_columns)
    scaled_input = scaler.transform(input_df)
    prediction = model.predict(scaled_input)[0]
    return "High Risk" if prediction == 1 else "Low Risk"


def main():
    model, scaler, expected_columns = load_artifacts()
    st.title("Heart Disease Risk Prediction")
    st.write("UI implementation arrives in later tasks.")


if __name__ == "__main__":
    main()
