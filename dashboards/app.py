import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# adiciona a pasta raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.geospatial_analysis import load_data

st.title("ROV Geospatial Intelligence Platform")

uploaded_file = st.file_uploader("Upload ROV CSV", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="depth",
        zoom=5,
        height=500
    )

    fig.update_layout(mapbox_style="open-street-map")

    st.plotly_chart(fig)
