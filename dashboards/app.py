import streamlit as st
import sys
import os

# 🔥 ESSA LINHA RESOLVE
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_data
from src.data_processing import clean_data
from src.analytics import detect_anomalies
from src.visualization import map_2d, map_3d, anomalies_map, bathymetry_map
st.set_page_config(page_title="ROV Mission Intelligence", layout="wide")

st.title("🌊 ROV Mission Intelligence Platform")

# -------------------------------
# LOGIN
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

    st.stop()

# -------------------------------
# UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
    df = clean_data(df)
    df = detect_anomalies(df)

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Points", len(df))
    col2.metric("Max Depth", f"{df['depth'].max():.1f}")
    col3.metric("Min Depth", f"{df['depth'].min():.1f}")

    view = st.radio(
        "Mode",
        ["2D Map", "3D View", "Anomalies", "Bathymetry"],
        horizontal=True
    )

    if view == "2D Map":
        fig = map_2d(df)

    elif view == "3D View":
        fig = map_3d(df)

    elif view == "Anomalies":
        fig = anomalies_map(df)

    else:
        fig = bathymetry_map(df)

    st.plotly_chart(fig, use_container_width=True)
