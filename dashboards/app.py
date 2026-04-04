import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Corrige import do src no Streamlit Cloud
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.geospatial_analysis import load_data

st.title("ROV Geospatial Intelligence Platform")

uploaded_file = st.file_uploader("Upload ROV CSV", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)

    # 🔥 LIMPA nomes das colunas (evita erro)
    df.columns = df.columns.str.strip().str.lower()

    # 🔍 DEBUG (pode remover depois)
    st.write("Columns detected:", df.columns)

    # ⚠️ Validação das colunas obrigatórias
    required_columns = {"latitude", "longitude", "depth"}
    
    if not required_columns.issubset(df.columns):
        st.error("CSV must contain: latitude, longitude, depth")
    else:
        # 🌍 Mapa
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
