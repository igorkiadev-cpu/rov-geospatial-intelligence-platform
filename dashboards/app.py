import streamlit as st
import pandas as pd
import io
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

st.title("🌊 ROV Mission Intelligence Platform - Enterprise")

uploaded_file = st.file_uploader("Upload ROV CSV", type=["csv"])

# =========================
# 📌 FUNÇÃO DISTÂNCIA
# =========================
def calculate_distance(df):
    lat = df["latitude"].values
    lon = df["longitude"].values

    dist = np.sqrt(np.diff(lat)**2 + np.diff(lon)**2)
    return np.sum(dist)

# =========================
# 🚀 PROCESSAMENTO
# =========================
if uploaded_file is not None:
    with st.spinner("Processando dados da missão..."):
        content = uploaded_file.getvalue().decode("utf-8")
        content = content.replace('"', '')

        df = pd.read_csv(io.StringIO(content), sep=",")
        df.columns = df.columns.str.strip().str.lower()

        required = ['latitude', 'longitude', 'depth']
        missing = [c for c in required if c not in df.columns]

        if missing:
            st.error(f"Missing required columns: {missing}")
        else:
            st.success("Dados carregados!")

            # =========================
            # 🧠 ANOMALIAS (Z-SCORE)
            # =========================
            df["zscore"] = (df["depth"] - df["depth"].mean()) / df["depth"].std()
            df["anomaly"] = df["zscore"].abs() > 2

            # =========================
            # 📊 KPIs
            # =========================
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Profundidade média", f"{df['depth'].mean():.1f}")
            col2.metric("Profundidade máxima", f"{df['depth'].max():.1f}")
            col3.metric("Distância (aprox)", f"{calculate_distance(df):.4f}")
            col4.metric("Anomalias", int(df["anomaly"].sum()))

            st.divider()

            # =========================
            # 🎛️ CONTROLE
            # =========================
            view = st.selectbox(
                "Visualização",
                ["Mapa 2D", "Mapa 3D", "Rota", "Replay", "Anomalias"]
            )

            # =========================
            # 🗺️ MAPA 2D
            # =========================
            if view == "Mapa 2D":
                fig = px.scatter_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    color="depth",
                    zoom=5,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🌐 3D
            # =========================
            elif view == "Mapa 3D":
                fig = px.scatter_3d(
                    df,
                    x="longitude",
                    y="latitude",
                    z="depth",
                    color="depth"
                )
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🧭 ROTA
            # =========================
            elif view == "Rota":
                fig = px.line_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    zoom=5,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🎥 REPLAY MISSÃO
            # =========================
            elif view == "Replay":
                step = st.slider("Tempo da missão", 0, len(df)-1, 10)

                df_slice = df.iloc[:step]

                fig = px.line_mapbox(
                    df_slice,
                    lat="latitude",
                    lon="longitude",
                    zoom=5,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")

                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🔴 ANOMALIAS
            # =========================
            elif view == "Anomalias":
                fig = px.scatter_mapbox(
                    df,
                    lat="latitude",
                    lon="longitude",
                    color="anomaly",
                    zoom=5,
                    height=600
                )
                fig.update_layout(mapbox_style="open-street-map")

                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 📋 DADOS
            # =========================
            with st.expander("Ver dados completos"):
                st.dataframe(df)
