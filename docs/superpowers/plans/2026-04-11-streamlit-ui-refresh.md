# Streamlit UI Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the Streamlit app into a balanced medical dashboard while preserving the current heart-disease prediction behavior.

**Architecture:** Keep the app as a single Streamlit entrypoint in `app.py`, but refactor the current top-level script into small helper functions so the styling, layout, and prediction logic are easier to test and maintain. Add lightweight tests around dataframe preparation and prediction-path behavior without changing the trained model artifacts.

**Tech Stack:** Python, Streamlit, pandas, joblib, scikit-learn, pytest

---

## File Structure

- Modify: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/app.py`
  - Keep as the app entrypoint
  - Add page config, CSS, layout helpers, and a `main()` function
  - Extract prediction-prep logic into importable functions
- Create: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/tests/test_app.py`
  - Verify feature alignment and prediction helper behavior
- Modify: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/requirements.txt`
  - Add `pytest` so the planned test commands work consistently

## Task 1: Refactor Prediction Logic Into Testable Helpers

**Files:**
- Modify: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/app.py`
- Create: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/tests/test_app.py`
- Modify: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/requirements.txt`

- [ ] **Step 1: Add `pytest` to project dependencies**

```text
streamlit
pandas
scikit-learn
joblib
numpy
pytest
```

- [ ] **Step 2: Write the failing tests for feature alignment and prediction mapping**

```python
from unittest.mock import Mock

import numpy as np

from app import align_input_frame, build_raw_input, predict_risk_label


def test_build_raw_input_creates_expected_encoded_fields():
    raw = build_raw_input(
        age=45,
        sex="M",
        chest_pain="ATA",
        resting_bp=120,
        cholesterol=220,
        fasting_bs=1,
        resting_ecg="Normal",
        max_hr=160,
        exercise_angina="N",
        oldpeak=1.5,
        st_slope="Up",
    )

    assert raw["Age"] == 45
    assert raw["RestingBP"] == 120
    assert raw["Cholesterol"] == 220
    assert raw["FastingBS"] == 1
    assert raw["MaxHR"] == 160
    assert raw["Oldpeak"] == 1.5
    assert raw["Sex_M"] == 1
    assert raw["ChestPainType_ATA"] == 1
    assert raw["RestingECG_Normal"] == 1
    assert raw["ExerciseAngina_N"] == 1
    assert raw["ST_Slope_Up"] == 1


def test_align_input_frame_adds_missing_columns_and_preserves_order():
    raw = {
        "Age": 50,
        "RestingBP": 130,
        "Sex_F": 1,
    }
    expected_columns = ["Age", "RestingBP", "Cholesterol", "Sex_F", "Sex_M"]

    aligned = align_input_frame(raw, expected_columns)

    assert list(aligned.columns) == expected_columns
    assert aligned.loc[0, "Cholesterol"] == 0
    assert aligned.loc[0, "Sex_M"] == 0
    assert aligned.loc[0, "Sex_F"] == 1


def test_predict_risk_label_maps_model_output_to_low_risk():
    scaler = Mock()
    scaler.transform.return_value = np.array([[0.1, 0.2]])
    model = Mock()
    model.predict.return_value = np.array([0])

    label = predict_risk_label(
        raw_input={"Age": 40},
        expected_columns=["Age"],
        scaler=scaler,
        model=model,
    )

    assert label == "Low Risk"


def test_predict_risk_label_maps_model_output_to_high_risk():
    scaler = Mock()
    scaler.transform.return_value = np.array([[0.4, 0.9]])
    model = Mock()
    model.predict.return_value = np.array([1])

    label = predict_risk_label(
        raw_input={"Age": 62},
        expected_columns=["Age"],
        scaler=scaler,
        model=model,
    )

    assert label == "High Risk"
```

- [ ] **Step 3: Run tests to verify they fail before the refactor**

Run: `cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects && pytest tests/test_app.py -v`
Expected: FAIL with import errors because the helper functions do not exist yet.

- [ ] **Step 4: Refactor `app.py` to expose prediction helpers and isolate app execution**

```python
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
```

- [ ] **Step 5: Add a `main()` wrapper so tests can import the module safely**

```python
def main():
    model, scaler, expected_columns = load_artifacts()
    st.title("Heart Disease Risk Prediction")
    st.write("UI implementation arrives in later tasks.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run tests to verify the refactor passes**

Run: `cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects && pytest tests/test_app.py -v`
Expected: PASS with 4 passed tests.

- [ ] **Step 7: Commit the refactor**

```bash
cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects
git add app.py tests/test_app.py requirements.txt
git commit -m "Refactor prediction helpers for UI refresh"
```

## Task 2: Add Dashboard Styling, Hero Section, and Structured Layout

**Files:**
- Modify: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/app.py`
- Test: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/tests/test_app.py`

- [ ] **Step 1: Write a failing smoke test for the new UI helper output**

```python
from app import build_metric_items


def test_build_metric_items_returns_three_dashboard_badges():
    items = build_metric_items()

    assert len(items) == 3
    assert items[0]["label"] == "Model"
    assert items[1]["label"] == "Interface"
    assert items[2]["label"] == "Result"
```

- [ ] **Step 2: Run the new test to verify it fails**

Run: `cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects && pytest tests/test_app.py::test_build_metric_items_returns_three_dashboard_badges -v`
Expected: FAIL with import error because `build_metric_items` does not exist yet.

- [ ] **Step 3: Add page config, CSS, and dashboard metadata helper**

```python
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
```

- [ ] **Step 4: Render the hero section and two-column shell in `main()`**

```python
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


def main():
    st.set_page_config(page_title="Heart Disease Risk Dashboard", layout="wide")
    model, scaler, expected_columns = load_artifacts()
    inject_styles()
    render_hero()
    form_col, info_col = st.columns([1.55, 1], gap="large")
```

- [ ] **Step 5: Run tests to verify the helper-based UI changes pass**

Run: `cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects && pytest tests/test_app.py -v`
Expected: PASS with 5 passed tests.

- [ ] **Step 6: Commit the layout foundation**

```bash
cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects
git add app.py tests/test_app.py
git commit -m "Add dashboard layout foundation"
```

## Task 3: Replace the Plain Form With a Structured Medical Dashboard Form

**Files:**
- Modify: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/app.py`

- [ ] **Step 1: Add a helper that collects form values in grouped columns**

```python
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
```

- [ ] **Step 2: Add a sidebar-style info panel beside the form**

```python
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
```

- [ ] **Step 3: Wire the form and info panel into `main()`**

```python
with form_col:
    submitted, form_values = render_prediction_form()

with info_col:
    render_info_panel()
```

- [ ] **Step 4: Run the app locally as a smoke test**

Run: `cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects && streamlit run app.py`
Expected: The app opens with a hero header, a two-column patient form, and a right-hand guidance panel.

- [ ] **Step 5: Commit the form redesign**

```bash
cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects
git add app.py
git commit -m "Redesign prediction form layout"
```

## Task 4: Add the Styled Result Card and Final Copy Cleanup

**Files:**
- Modify: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/app.py`
- Test: `/Users/sumitjadhav/Heart-Disease-Prediction-Projects/tests/test_app.py`

- [ ] **Step 1: Add a failing test for result-card metadata**

```python
from app import build_result_theme


def test_build_result_theme_for_high_risk():
    theme = build_result_theme("High Risk")

    assert theme["accent"] == "#b42318"
    assert "High Risk of Heart Disease" in theme["title"]


def test_build_result_theme_for_low_risk():
    theme = build_result_theme("Low Risk")

    assert theme["accent"] == "#027a48"
    assert "Low Risk of Heart Disease" in theme["title"]
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects && pytest tests/test_app.py::test_build_result_theme_for_high_risk tests/test_app.py::test_build_result_theme_for_low_risk -v`
Expected: FAIL with import error because `build_result_theme` does not exist yet.

- [ ] **Step 3: Add the result theme helper and result-card renderer**

```python
def build_result_theme(risk_label):
    if risk_label == "High Risk":
        return {
            "accent": "#b42318",
            "background": "#fff1f1",
            "title": "High Risk of Heart Disease",
        }
    return {
        "accent": "#027a48",
        "background": "#ecfdf3",
        "title": "Low Risk of Heart Disease",
    }


def render_result_card(risk_label):
    theme = build_result_theme(risk_label)
    st.markdown(
        f"""
        <div class="result-card" style="border-left:8px solid {theme['accent']};background:{theme['background']};margin-top:1rem;">
            <div style="font-size:0.8rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:{theme['accent']};">
                Prediction Result
            </div>
            <div style="font-size:1.6rem;font-weight:800;color:#12333d;margin-top:0.3rem;">
                {theme['title']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
```

- [ ] **Step 4: Connect the form submission to the styled result card**

```python
with form_col:
    submitted, form_values = render_prediction_form()

    if submitted:
        raw_input = build_raw_input(**form_values)
        risk_label = predict_risk_label(
            raw_input=raw_input,
            expected_columns=expected_columns,
            scaler=scaler,
            model=model,
        )
        render_result_card(risk_label)
```

- [ ] **Step 5: Run the full test suite**

Run: `cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects && pytest tests/test_app.py -v`
Expected: PASS with 7 passed tests.

- [ ] **Step 6: Run the app for final verification**

Run: `cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects && streamlit run app.py`
Expected: The app shows the balanced dashboard layout, produces styled high-risk and low-risk result cards, and preserves the original prediction behavior.

- [ ] **Step 7: Commit the finished UI refresh**

```bash
cd /Users/sumitjadhav/Heart-Disease-Prediction-Projects
git add app.py tests/test_app.py
git commit -m "Refresh Streamlit dashboard UI"
```
