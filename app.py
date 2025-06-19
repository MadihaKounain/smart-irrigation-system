import streamlit as st
import pandas as pd
import json
from joblib import load
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="🌿 Smart Irrigation System", layout="wide")

# Custom color scheme
PRIMARY_COLOR = "#2E8B57"  # green
SECONDARY_COLOR = "#5DADE2"  # blue
HIGHLIGHT_COLOR = "#F4D03F"  # yellow

# Header
st.markdown(
    f"<h1 style='color:{PRIMARY_COLOR}; text-align:center;'>🌿 Smart Irrigation System</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:gray;'>Predict irrigation need based on environment, crop, and season</p>",
    unsafe_allow_html=True
)

# Load model and features
model = load("irrigation_model_extended.joblib")
with open("model_features.json", "r") as f:
    model_features = json.load(f)

# Define crop and season types
crop_types = ['Wheat', 'Corn', 'Rice', 'Soybean']
seasons = ['Spring', 'Summer', 'Autumn', 'Winter']

# Input parameters in columns
with st.expander("🧪 Input Parameters", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        temp = st.slider("🌡️ Temperature (°C)", 10.0, 50.0, 25.0)
        humidity = st.slider("💧 Humidity (%)", 10.0, 100.0, 50.0)
        soil = st.slider("🪨 Soil Moisture (%)", 0.0, 100.0, 20.0)
        wind = st.slider("💨 Wind Speed (km/h)", 0.0, 20.0, 5.0)

    with col2:
        rainfall = st.number_input("🌧️ Rainfall Forecast (mm)", min_value=0.0, max_value=500.0, value=0.0)
        crop = st.selectbox("🌾 Crop Type", crop_types)
        season = st.selectbox("🍂 Season", seasons)

# Input summary
st.markdown(f"<h4 style='color:{SECONDARY_COLOR};'>📋 Input Summary</h4>", unsafe_allow_html=True)
input_dict = {
    "Temperature (°C)": temp,
    "Humidity (%)": humidity,
    "Soil Moisture (%)": soil,
    "Wind Speed (km/h)": wind,
    "Rainfall (mm)": rainfall,
    "Crop": crop,
    "Season": season
}
input_summary = pd.DataFrame({k: [v] for k, v in input_dict.items()})

def highlight_low_soil(val):
    return f'background-color: #ffdddd' if val < 30 and isinstance(val, (int, float)) else ''

st.dataframe(input_summary.style.applymap(highlight_low_soil, subset=['Soil Moisture (%)']), height=180)

# Graph
st.markdown(f"<h4 style='color:{SECONDARY_COLOR};'>📊 Sensor Data Visualization</h4>", unsafe_allow_html=True)
plot_data = {
    "Temperature (°C)": temp,
    "Humidity (%)": humidity,
    "Soil Moisture (%)": soil,
    "Wind Speed (km/h)": wind,
    "Rainfall (mm)": rainfall
}
fig = go.Figure(data=go.Bar(
    x=list(plot_data.keys()),
    y=list(plot_data.values()),
    marker=dict(
        color=[PRIMARY_COLOR, "#48C9B0", "#F39C12", "#5D6D7E", "#85C1E9"],
        line=dict(color='black', width=1)
    ),
    text=[f"{v:.1f}" for v in plot_data.values()],
    textposition="auto"
))
fig.update_layout(
    template="plotly_white",
    yaxis_title="Value",
    xaxis_title="Sensor Feature",
    height=400
)
st.plotly_chart(fig, use_container_width=True)

# Predict button in center
st.markdown("<hr style='border: 1px solid #cccccc;'>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns([3, 2, 3])
with btn_col2:
    if st.button("🚰 Predict Irrigation Need", use_container_width=True):
        # Create model input
        pred_dict = {
            "Temp": [temp],
            "Humidity": [humidity],
            "Soil": [soil],
            "Wind": [wind],
            "Rainfall": [rainfall]
        }
        for c in crop_types:
            pred_dict[f"Crop_{c}"] = [1 if crop == c else 0]
        for s in seasons:
            pred_dict[f"Season_{s}"] = [1 if season == s else 0]

        pred_df = pd.DataFrame(pred_dict)
        for col in model_features:
            if col not in pred_df.columns:
                pred_df[col] = 0
        pred_df = pred_df[model_features]

        result = model.predict(pred_df)[0]
        if result == 1:
            st.success("✅ Irrigation is **RECOMMENDED** for current conditions.")
        else:
            st.info("❌ No irrigation required at this time.")

# Footer
st.markdown(
    f"<hr style='border: 1px solid {PRIMARY_COLOR};'><p style='text-align:center; color:gray;'>"
    "Made with ❤️ | Smart Farming Project"
    "</p>",
    unsafe_allow_html=True
)
