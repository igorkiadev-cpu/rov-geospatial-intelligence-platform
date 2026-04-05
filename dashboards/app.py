import streamlit as st
import pandas as pd
import io
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🌊 ROV Mission Intelligence Platform")

uploaded_file = st.file_uploader("Upload ROV CSV", type=["csv"])

if uploaded_file is not None:
    try:
        content = uploaded_file.getvalue().decode("utf-8")

        # 🔥 remove aspas problemáticas
        content = content.replace('"', '')

        df = pd.read_csv(io.StringIO(content), sep=",")

        df.columns = df.columns.str.strip().str.lower()

        required_columns = ['latitude', 'longitude', 'depth']

        missing = [col for col in required_columns if col not in df.columns]

        if missing:
            st.error(f"Missing required columns: {missing}")
        else:
            st.success("CSV carregado com sucesso!")

            st.subheader("📊 Dados")
            st.dataframe(df)

            # =========================
            # 🎛️ CONTROLE DE VISUALIZAÇÃO
            # =========================
            option = st.selectbox(
                "Escolha a visualização",
                ["Mapa 2D", "Mapa 3D", "Rota", "Depth Chart"]
            )

            # =========================
            # 🗺️ MAPA 2D
            # =========================
            if option == "Mapa 2D":
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
            # 🌐 MAPA 3D
            # =========================
            elif option == "Mapa 3D":
                fig = px.scatter_3d(
                    df,
                    x="longitude",
                    y="latitude",
                    z="depth",
                    color="depth"
                )
                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 🧭 ROTA DO ROV
            # =========================
            elif option == "Rota":
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
            # 📉 GRÁFICO DE PROFUNDIDADE
            # =========================
            elif option == "Depth Chart":
                fig = px.line(
                    df,
                    y="depth",
                    title="Depth ao longo da missão"
                )
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error processing file: {e}")
