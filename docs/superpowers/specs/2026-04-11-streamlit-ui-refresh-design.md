# Streamlit UI Refresh Design

## Goal

Refresh the Streamlit app so it feels as polished as the README while staying professional and appropriate for a medical prediction interface.

The redesigned app should:

- feel trustworthy and modern
- improve visual hierarchy and spacing
- present inputs in a more organized way
- keep the prediction output simple: `High Risk` or `Low Risk`
- remain easy to run locally with the current model files and dependencies

## Chosen Direction

Use a **Balanced Dashboard** style:

- professional medical tone
- modern polish without flashy or distracting effects
- portfolio-ready presentation
- stronger layout and styling without changing the prediction behavior

## Current State

The existing app works functionally, but the interface is very plain:

- a single ungrouped vertical form
- minimal structure and weak visual hierarchy
- no strong landing area or explanation section
- result output is correct but visually basic
- title text currently says "Heart Stroke Prediction" even though the project and model are about heart disease risk

## Design Overview

The new UI should be organized into four visible sections:

1. **Hero Header**
   - A stronger page title focused on heart disease prediction
   - A short supporting sentence explaining what the app does
   - Small stat or info badges that highlight the model, app type, and prediction output

2. **Main Form Card**
   - Inputs grouped into two columns for easier scanning on desktop
   - Labels rewritten or tightened where needed for clarity
   - The existing input fields preserved so the model interface does not change
   - A single prominent action button labeled clearly

3. **Prediction Result Card**
   - Result shown in a dedicated styled card after prediction
   - Use a strong visual difference between low-risk and high-risk states
   - Keep the result message simple and short
   - Do not add probability or expanded interpretation text

4. **About / Guidance Panel**
   - Short explanation of what the model uses
   - Quick notes about the clinical inputs
   - A reminder that the app is an ML project and not a medical diagnosis

## Layout

### Desktop

- Wide page container
- Hero section across the top
- Main content split into two columns:
  - left: prediction form
  - right: app info / guidance
- Prediction result displayed below the form or directly under the button in a styled card

### Mobile

- Single-column stack
- Hero first
- Form next
- Result card after submission
- Guidance content moved below the form

## Visual Style

Use a restrained medical-dashboard aesthetic:

- soft background gradient or tinted background section
- white or near-white cards with subtle borders/shadows
- strong heading typography and cleaner spacing
- teal/blue health-tech accent colors
- red for high-risk result state
- green for low-risk result state

Avoid:

- overly dark themes
- aggressive animations
- excessive glow effects
- playful or game-like visuals

## Interaction Behavior

Prediction behavior should remain logically identical to the current version:

- collect the same user inputs
- build the input dataframe the same way
- align to expected encoded columns
- scale with the saved scaler
- predict with the saved KNN model

UI behavior changes:

- the button should feel more prominent
- the result should appear in a dedicated visual container
- input sections should be easier to scan and complete

## Content Changes

Update wording for consistency and trust:

- change the title from "Heart Stroke Prediction by Sumit" to a heart-disease-specific title
- refine helper text so the app sounds clearer and more professional
- add a short disclaimer that it is an educational ML tool, not clinical advice

## Technical Plan

The implementation should stay inside the existing `app.py` file unless a clearly reusable helper is helpful.

Expected implementation pieces:

- page config for title and layout
- custom CSS injected through Streamlit markdown
- helper layout containers using `st.container()`, `st.columns()`, and styled markdown blocks
- small helper function for rendering a result card if it improves clarity
- same prediction logic as current app

## Testing Strategy

Verify:

- app still runs with `streamlit run app.py`
- both result paths still render correctly
- layout remains readable on narrow screens
- no model-loading or column-alignment behavior changes
- text accurately reflects heart disease prediction

## Out of Scope

The redesign will not:

- retrain or replace the model
- add charts, confidence scores, or advanced analytics
- add authentication or data persistence
- change project dependencies unless required for existing functionality
- turn the app into a medical decision support product
