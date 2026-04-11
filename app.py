import joblib
import pandas as pd
import streamlit as st
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent


def load_artifacts():
    model = joblib.load(APP_DIR / "knn_heart_model.pkl")
    scaler = joblib.load(APP_DIR / "heart_scaler.pkl")
    expected_columns = joblib.load(APP_DIR / "heart_columns.pkl")
    return model, scaler, expected_columns


def build_metric_items():
    return [
        {"label": "Model", "value": "KNN Classifier"},
        {"label": "Interface", "value": "Streamlit Dashboard"},
        {"label": "Result", "value": "High / Low Risk"},
    ]


def inject_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(60, 160, 180, 0.18), transparent 30%),
                linear-gradient(180deg, #f4fbfc 0%, #eef6f7 100%);
        }
        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .hero-card, .panel-card, .result-card {
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid rgba(15, 76, 92, 0.10);
            border-radius: 24px;
            box-shadow: 0 18px 50px rgba(10, 42, 51, 0.08);
            padding: 1.4rem;
        }
        .hero-title {
            color: #103946;
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }
        .hero-text {
            color: #47606a;
            font-size: 1rem;
            line-height: 1.65;
        }
        .metric-row {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }
        .metric-pill {
            background: #f1fbfc;
            border: 1px solid #cfe7eb;
            border-radius: 999px;
            padding: 0.65rem 0.95rem;
        }
        .metric-label {
            color: #5f7a84;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .metric-value {
            color: #103946;
            font-size: 0.95rem;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    pills = "".join(
        f"""
        <div class="metric-pill">
            <div class="metric-label">{item['label']}</div>
            <div class="metric-value">{item['value']}</div>
        </div>
        """
        for item in build_metric_items()
    )
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">Heart Disease Risk Dashboard</div>
            <div class="hero-text">
                Enter clinical details to generate a simple heart disease risk prediction
                using the trained machine learning model behind this project.
            </div>
            <div class="metric-row">{pills}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_form():
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown("### Patient Details")
    st.caption("Fill in the clinical information below to generate a heart disease risk prediction.")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        age = st.slider("Age", 18, 100, 40)
        sex = st.selectbox("Sex", ["M", "F"])
        chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])
        resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200, 120)
        cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1])

    with col2:
        resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
        max_hr = st.slider("Max Heart Rate", 60, 220, 150)
        exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"])
        oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0)
        st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

    submitted = st.button("Predict Risk", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    return submitted, {
        "age": age,
        "sex": sex,
        "chest_pain": chest_pain,
        "resting_bp": resting_bp,
        "cholesterol": cholesterol,
        "fasting_bs": fasting_bs,
        "resting_ecg": resting_ecg,
        "max_hr": max_hr,
        "exercise_angina": exercise_angina,
        "oldpeak": oldpeak,
        "st_slope": st_slope,
    }


def render_info_panel():
    st.markdown(
        """
        <div class="panel-card">
            <h3 style="margin-top:0;color:#103946;">About This App</h3>
            <p style="color:#4e6771;line-height:1.7;">
                This dashboard uses a trained K-Nearest Neighbors model to evaluate
                heart disease risk from common clinical inputs.
            </p>
            <ul style="color:#4e6771;line-height:1.8;padding-left:1.2rem;">
                <li>Interactive Streamlit interface</li>
                <li>Encoded feature alignment before prediction</li>
                <li>Standard scaling with saved training artifacts</li>
                <li>Simple result output for quick demos and portfolio review</li>
            </ul>
            <p style="color:#7a4b00;background:#fff7e6;border-radius:16px;padding:0.9rem 1rem;margin:0;">
                Educational ML project only. This app does not replace professional medical advice.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
    st.set_page_config(page_title="Heart Disease Risk Dashboard", layout="wide")
    model, scaler, expected_columns = load_artifacts()
    inject_styles()
    render_hero()

    form_col, info_col = st.columns([1.55, 1], gap="large")

    with form_col:
        submitted, form_values = render_prediction_form()

    with info_col:
        render_info_panel()

    if submitted:
        raw_input = build_raw_input(
            age=form_values["age"],
            sex=form_values["sex"],
            chest_pain=form_values["chest_pain"],
            resting_bp=form_values["resting_bp"],
            cholesterol=form_values["cholesterol"],
            fasting_bs=form_values["fasting_bs"],
            resting_ecg=form_values["resting_ecg"],
            max_hr=form_values["max_hr"],
            exercise_angina=form_values["exercise_angina"],
            oldpeak=form_values["oldpeak"],
            st_slope=form_values["st_slope"],
        )
        risk_label = predict_risk_label(raw_input, expected_columns, scaler, model)

        if risk_label == "High Risk":
            st.error("⚠️ High Risk of Heart Disease")
        else:
            st.success("✅ Low Risk of Heart Disease")


if __name__ == "__main__":
    main()
