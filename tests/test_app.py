from unittest.mock import Mock

import numpy as np

from app import align_input_frame, build_raw_input, predict_risk_label, build_metric_items


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
    transformed_input = np.array([[0.1, 0.2]])
    scaler.transform.return_value = transformed_input
    model = Mock()
    model.predict.return_value = np.array([0])
    raw_input = {"Age": 40, "RestingBP": 120}
    expected_columns = ["Age", "RestingBP"]

    label = predict_risk_label(
        raw_input=raw_input,
        expected_columns=expected_columns,
        scaler=scaler,
        model=model,
    )

    scaler.transform.assert_called_once()
    aligned_df = scaler.transform.call_args.args[0]
    assert list(aligned_df.columns) == expected_columns
    assert aligned_df.loc[0, "Age"] == 40
    assert aligned_df.loc[0, "RestingBP"] == 120
    model.predict.assert_called_once_with(transformed_input)
    assert label == "Low Risk"


def test_predict_risk_label_maps_model_output_to_high_risk():
    scaler = Mock()
    transformed_input = np.array([[0.4, 0.9]])
    scaler.transform.return_value = transformed_input
    model = Mock()
    model.predict.return_value = np.array([1])
    raw_input = {"Age": 62, "RestingBP": 150}
    expected_columns = ["Age", "RestingBP"]

    label = predict_risk_label(
        raw_input=raw_input,
        expected_columns=expected_columns,
        scaler=scaler,
        model=model,
    )

    scaler.transform.assert_called_once()
    aligned_df = scaler.transform.call_args.args[0]
    assert list(aligned_df.columns) == expected_columns
    assert aligned_df.loc[0, "Age"] == 62
    assert aligned_df.loc[0, "RestingBP"] == 150
    model.predict.assert_called_once_with(transformed_input)
    assert label == "High Risk"


def test_build_metric_items_returns_three_dashboard_badges():
    items = build_metric_items()

    assert len(items) == 3
    assert items[0]["label"] == "Model"
    assert items[0]["value"] == "KNN Classifier"
    assert items[1]["label"] == "Interface"
    assert items[1]["value"] == "Streamlit Dashboard"
    assert items[2]["label"] == "Result"
    assert items[2]["value"] == "High / Low Risk"
